"""
aggregation/lda.py
--------------------
Pipeline LDA Monte Carlo COMPLET aligné sur le document méthodologique du 16 juin 2026.
Agrégation par copule de Gumbel (ou modèle à facteur commun en robustesse).

LES 4 BRIQUES (strictement définies selon le PDF) :
=============================================================================
  1. REMÉDIATION   : La vraie brique statistique (fréquence x sévérité).
                     Repose sur la GPD calibrée sur PRC ou OpRisk.
                     
  2. PRESTATAIRE   : Défaillance d'un tiers critique. Scénario d'expert.
                     Tirage Lognormal indépendant, déclenché uniquement sur 
                     les incidents "supply_chain_tiers" (15.8% des cas).

  3. SANCTION      : Composante additive réglementaire. 
                     Probabilité d'occurrence = PCD de la variable latente.
                     Montant = Loi Bêta mise à l'échelle sur les plafonds [2M€, 20M€].

  4. AGGRAVATION   : Le surcoût du non-respect (le contrefactuel).
                     N'est PAS une brique additive dans la boucle Monte-Carlo, 
                     mais la différence de VaR (Delta_DORA) entre un run 
                     non-conforme et un run conforme, à profil de risque constant 
                     (neutralisation du biais de sélection via graine figée).
"""

import numpy as np
from scipy.stats import genpareto, lognorm, beta
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.aggregation.copule import gumbel_copula_uniforms, common_factor_uniforms
from src.frequency.negbin import HACKMAGEDDON_PROPORTIONS
from src.compliance.latent import pcd_conditional, ANCHORED_PARAMS, PROFILS_TYPES
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA

# ---------------------------------------------------------------------------
# 1. PARAMÈTRES DES BRIQUES (sourcés sur le PDF et avis d'expert)
# ---------------------------------------------------------------------------

BRIQUE_PARAMS = {
    "prestataire": {
        "trigger_prop": HACKMAGEDDON_PROPORTIONS["supply_chain_tiers"],
        # Calibration 3 quantiles (Expert/ORSA) traduite en Lognormale
        # exp(1.6) ≈ 4.95 M€ (médiane), queue épaisse (sigma=1.2)
        "mu_lognorm": 1.6, 
        "sigma_lognorm": 1.2,
        "source": "Scénarios d'experts — calibration Lognormale sur 3 quantiles"
    },
    "sanction": {
        "montant_range_eur_m": (2.0, 20.0),
        # Loi Bêta asymétrique (biais vers la gauche, les amendes max sont rares)
        "beta_a": 1.5, 
        "beta_b": 5.0,
        "source": "DORA Art. 50-52 — Loi Bêta x Plafonds nationaux"
    },
    # Facteur d'intensification systémique via la copule
    "stress_systemique": {"max_loading": 0.15} 
}

# ---------------------------------------------------------------------------
# 2. SIMULATION DE LA SÉVÉRITÉ DE BASE (Brique Remédiation)
# ---------------------------------------------------------------------------

def simulate_remediation_severity(n_events: int, xi: float, sigma: float, u: float,
                                  p_u: float, severity_cap: float, rng) -> np.ndarray:
    """Sévérité de la remédiation par incident (Théorie des Valeurs Extrêmes - GPD)."""
    is_tail = rng.random(n_events) < p_u
    severities = np.zeros(n_events)
    n_tail = int(is_tail.sum())
    
    if n_tail > 0:
        u_vals = rng.uniform(0, 1, n_tail)
        sev = u + genpareto.ppf(u_vals, c=xi, scale=sigma)
        if severity_cap is not None:
            sev = np.minimum(sev, severity_cap)
        severities[is_tail] = sev
    return severities

# ---------------------------------------------------------------------------
# 3. SIMULATION ANNUELLE DES 3 BRIQUES PHYSIQUES
# ---------------------------------------------------------------------------

def simulate_year_3_briques(lambda_annual: float, severity_params: dict,
                            pcd_sanction: float, n_sim: int,
                            dependence: str = "gumbel", theta: float = 1.8,
                            p_sys: float = None, seed: int = 42) -> dict:
    """
    Simule n_sim années de pertes agrégées sur les 3 briques "physiques" 
    (Remédiation, Prestataire, Sanction).
    L'Aggravation (4ème brique) est un contrefactuel calculé en aval.
    """
    rng = np.random.default_rng(seed)
    
    # Paramètres GPD Remédiation
    xi, sigma, u, p_u = (severity_params["xi"], severity_params["sigma"],
                         severity_params["u"], severity_params["p_u"])
    dispersion = severity_params.get("dispersion_factor", 9.2)
    cap = severity_params.get("severity_cap", None)

    # --- Fréquence annuelle (Loi Binomiale Négative) ---
    r = lambda_annual / (dispersion - 1) if dispersion > 1 else lambda_annual
    p = r / (r + lambda_annual)
    freqs = rng.negative_binomial(r, p, size=n_sim)
    total_events = int(freqs.sum())

    # --- BRIQUE 1 : Remédiation (Base GPD) ---
    remediation_events = simulate_remediation_severity(total_events, xi, sigma, u, p_u, cap, rng)

    # --- BRIQUE 2 : Prestataire (Scénario d'expert sur incidents tiers) ---
    vecteurs = rng.choice(list(HACKMAGEDDON_PROPORTIONS.keys()), size=total_events,
                          p=list(HACKMAGEDDON_PROPORTIONS.values()))
    is_tiers = vecteurs == "supply_chain_tiers"
    n_tiers = int(is_tiers.sum())
    
    # Tirage Lognormal pour les incidents impliquant un tiers
    mu_p = BRIQUE_PARAMS["prestataire"]["mu_lognorm"]
    sig_p = BRIQUE_PARAMS["prestataire"]["sigma_lognorm"]
    prestataire_events = np.zeros(total_events)
    prestataire_events[is_tiers] = rng.lognormal(mean=mu_p, sigma=sig_p, size=n_tiers)

    # --- COPULE (Dépendance de queue annuelle) ---
    if dependence == "gumbel":
        U = gumbel_copula_uniforms(n_sim, theta, dim=3, seed=seed + 1)
    elif dependence == "common_factor":
        p_sys = p_sys if p_sys is not None else pcd_sanction
        U = common_factor_uniforms(n_sim, p_sys, dim=3, seed=seed + 1)
    else:
        raise ValueError("dependence doit être 'gumbel' ou 'common_factor'")

    # --- Agrégation par année ---
    splits = np.cumsum(freqs)[:-1]
    brique_remediation = np.array([s.sum() for s in np.split(remediation_events, splits)])
    brique_prestataire = np.array([s.sum() for s in np.split(prestataire_events, splits)])

    # Couplage : U[:, 0] génère un stress systémique (surcoût) sur la remédiation
    max_stress = BRIQUE_PARAMS["stress_systemique"]["max_loading"]
    stress_loading = U[:, 0] * max_stress
    brique_remediation = brique_remediation * (1.0 + stress_loading)

    # Couplage : U[:, 1] génère un stress sur le coût prestataire
    brique_prestataire = brique_prestataire * (1.0 + U[:, 1] * max_stress)

    # --- BRIQUE 3 : Sanction (Pilotée par la PCD et U[:, 2]) ---
    sanction_survient = U[:, 2] < pcd_sanction
    low_s, high_s = BRIQUE_PARAMS["sanction"]["montant_range_eur_m"]
    
    # Tirage Bêta mis à l'échelle des plafonds réglementaires
    amendes_beta = rng.beta(a=BRIQUE_PARAMS["sanction"]["beta_a"], 
                            b=BRIQUE_PARAMS["sanction"]["beta_b"], size=n_sim)
    montant_sanction = low_s + amendes_beta * (high_s - low_s)
    brique_sanction = np.where(sanction_survient, montant_sanction, 0.0)

    # --- Perte totale agrégée LDORA ---
    total = brique_remediation + brique_prestataire + brique_sanction

    return {
        "total": total,
        "remediation": brique_remediation,
        "prestataire": brique_prestataire,
        "sanction": brique_sanction,
        "dependence": dependence,
    }


# ---------------------------------------------------------------------------
# 4. RAPPORT & CONTREFACTUEL — SCR À 4 BRIQUES (Section 3.4 du PDF)
# ---------------------------------------------------------------------------

def scr_4_briques_report(source: str = "OPRISK", alpha: float = 0.995, 
                         n_sim: int = 100_000, dependence: str = "gumbel"):
    """
    Calcule le SCR DORA en intégrant la 4ème brique (Aggravation) par la méthode
    du contrefactuel neutralisé (Section 3.5 du PDF).
    """
    from src.frequency.negbin import compute_lambda_scenario

    source_map = {"PRC": PRC, "OPRISK": OPRISK}
    src = source_map[source]
    lambda_ref = FREQUENCY["lambda_ref"] if source == "PRC" else OPRISK["n_incidents"] / OPRISK["n_years"]
    
    severity_params = {
        "xi": src["xi"], "sigma": src["sigma_eur"], "u": src["seuil_u_eur"],
        "p_u": src["p_u"], "dispersion_factor": FREQUENCY["dispersion_factor"],
        "severity_cap": SCR_DORA.get("cap_eur", 40.0) if source == "PRC" else None,
    }

    # --- ÉTAT 1 : Entité NON-CONFORME (Réalité) ---
    sc_nc = compute_lambda_scenario(lambda_ref, "S2_non_conforme", mode="center")
    lam_nc = sc_nc["lambda_global"]
    pcd_nc = pcd_conditional(PROFILS_TYPES["median"], 0.0, ANCHORED_PARAMS)
    
    # Graine figée pour bloquer le biais de sélection !
    res_nc = simulate_year_3_briques(lam_nc, severity_params, pcd_nc, n_sim, 
                                     dependence=dependence, theta=1.8, seed=42)
    scr_nc = np.quantile(res_nc["total"], alpha)

    # --- ÉTAT 2 : Entité CONFORME (Contrefactuel) ---
    sc_c = compute_lambda_scenario(lambda_ref, "S0_conforme", mode="center")
    lam_c = sc_c["lambda_global"]
    pcd_c = pcd_conditional(PROFILS_TYPES["leader"], 0.0, ANCHORED_PARAMS)
    
    # Même graine (seed=42), seuls les paramètres métiers baissent
    res_c = simulate_year_3_briques(lam_c, severity_params, pcd_c, n_sim, 
                                    dependence=dependence, theta=1.2, seed=42)
    scr_c = np.quantile(res_c["total"], alpha)

    # --- BRIQUE 4 : Aggravation ---
    # Delta DORA : Le surcoût strict imputable au défaut de conformité
    aggravation_scr = scr_nc - scr_c

    # --- AFFICHAGE ---
    print(f"\n{'='*70}")
    print(f"  SCR DORA (Modèle complet PDF) — {source} / {dependence.upper()}")
    print(f"{'='*70}")
    print(f"  État NON-CONFORME : λ = {lam_nc:.1f} | PCD = {pcd_nc:.1%} | θ = 1.8")
    print(f"  État CONFORME     : λ = {lam_c:.1f} | PCD = {pcd_c:.1%} | θ = 1.2")
    print(f"  n_sim = {n_sim:,} | Graine figée (Neutralisation biais de sélection)")
    
    print(f"\n  VaR {alpha*100:.1f}% (SCR_DORA Non-Conforme) = {scr_nc:>8.1f} M€")
    print(f"  VaR {alpha*100:.1f}% (SCR_DORA Conforme)     = {scr_c:>8.1f} M€")
    
    print(f"\n  Décomposition du risque (Moyenne du run Non-Conforme) :")
    total_mean = res_nc["total"].mean()
    for brique in ["remediation", "prestataire", "sanction"]:
        m = res_nc[brique].mean()
        print(f"    {brique.capitalize():14s} : {m:>8.1f} M€  ({100*m/total_mean:>5.1f}%)")
    
    print(f"\n  >> Brique AGGRAVATION (Contrefactuel Δ_DORA) : {aggravation_scr:>8.1f} M€")
    print(f"     (Surcoût en capital imputable strictement au non-respect)")
    print(f"{'='*70}")
    
    # On ajoute la valeur scalaire de l'aggravation au dictionnaire de sortie
    # pour tes notebooks aval s'ils en ont besoin.
    res_nc["scr_total"] = scr_nc
    res_nc["scr_aggravation"] = aggravation_scr 
    return res_nc


if __name__ == "__main__":
    scr_4_briques_report(source="PRC", n_sim=100_000, dependence="gumbel")
    scr_4_briques_report(source="OPRISK", n_sim=100_000, dependence="gumbel")