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
                     Fréquence ANNUELLE INDÉPENDANTE (pas dérivée du pool
                     d'incidents remédiation), calibrée sur un ordre de
                     grandeur de quelques événements/an pour une entité.
                     Tirage Lognormal sur occurrence.

  3. SANCTION      : Composante additive réglementaire.
                     Probabilité d'occurrence = PCD de la variable latente.
                     Montant = Loi Bêta mise à l'échelle sur les plafonds [2M€, 20M€].

  4. AGGRAVATION   : Le surcoût du non-respect (le contrefactuel).
                     N'est PAS une brique additive dans la boucle Monte-Carlo,
                     mais la différence de VaR (Delta_DORA) entre un run
                     non-conforme et un run conforme, à profil de risque constant
                     (neutralisation du biais de sélection via graine figée).

CORRECTIF (01/07/2026) :
  - Bug identifié : la brique Prestataire réutilisait le pool d'événements
    "total_events" dérivé de lambda_global (remédiation), qui inclut déjà
    le scénario S2_non_conforme. Résultat : jusqu'à 134 incidents "tiers
    critiques" simulés par an pour une seule entité, ce qui est irréaliste
    (cf. mémoire, cadre du marché cyber réel).
  - Correction : fréquence prestataire indépendante, calibrée séparément,
    avec son propre multiplicateur de conformité (plus modéré que celui
    de la remédiation, car il reflète la maîtrise de la gouvernance
    tiers ICT - Chapitre V DORA - et non l'ensemble des vecteurs d'attaque).
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
        # Calibration 3 quantiles (Expert/ORSA) traduite en Lognormale
        # exp(1.6) ≈ 4.95 M€ (médiane), queue épaisse (sigma=1.2)
        "mu_lognorm": 1.6,
        "sigma_lognorm": 1.2,
        # NOUVEAU : fréquence annuelle INDÉPENDANTE du pool remédiation.
        # Ordre de grandeur : quelques défaillances de tiers critiques par an
        # pour une entité (et non 15.8% d'un pool de 341-848 incidents/an).
        "lambda_annuel_conforme": 0.8,
        "lambda_annuel_non_conforme": 2.5,
        "source": "Scénarios d'experts — calibration Lognormale sur 3 quantiles ; "
                  "fréquence propre indépendante du pool remédiation (corrigé 01/07/2026)"
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
                            is_conforme: bool = False,
                            pcd_prestataire: float = None,
                            dependence: str = "gumbel", theta: float = 1.8,
                            p_sys: float = None, seed: int = 42) -> dict:
    """
    Simule n_sim années de pertes agrégées sur les 3 briques "physiques"
    (Remédiation, Prestataire, Sanction).
    L'Aggravation (4ème brique) est un contrefactuel calculé en aval.

    Parameters
    ----------
    lambda_annual : fréquence annuelle globale de la brique REMÉDIATION uniquement
                     (calculée en amont via compute_lambda_scenario, tous vecteurs
                     confondus). Ne pilote plus la brique Prestataire.
    is_conforme   : bool, sélectionne le régime de fréquence du Prestataire
                     (lambda_annuel_conforme vs lambda_annuel_non_conforme).
    """
    rng = np.random.default_rng(seed)

    # Paramètres GPD Remédiation
    xi, sigma, u, p_u = (severity_params["xi"], severity_params["sigma"],
                         severity_params["u"], severity_params["p_u"])
    dispersion = severity_params.get("dispersion_factor", 9.2)
    cap = severity_params.get("severity_cap", None)

    # --- Fréquence annuelle REMÉDIATION (Loi Binomiale Négative) ---
    r = lambda_annual / (dispersion - 1) if dispersion > 1 else lambda_annual
    p = r / (r + lambda_annual)
    freqs = rng.negative_binomial(r, p, size=n_sim)
    total_events = int(freqs.sum())

    # --- BRIQUE 1 : Remédiation (Base GPD) ---
    remediation_events = simulate_remediation_severity(total_events, xi, sigma, u, p_u, cap, rng)

    splits = np.cumsum(freqs)[:-1]
    brique_remediation = np.array([s.sum() for s in np.split(remediation_events, splits)])

    # --- BRIQUE 2 : Prestataire (fréquence INDÉPENDANTE, scénario d'expert) ---
    # CORRECTIF : on ne réutilise plus total_events (pool remédiation).
    # La fréquence prestataire suit son propre régime, distinct du pool
    # d'incidents opérationnels, conformément à la logique "événement importé,
    # rare, potentiellement corrélé entre acteurs du marché" du mémoire.
    lam_conf = BRIQUE_PARAMS["prestataire"]["lambda_annuel_conforme"]
    lam_non_conf = BRIQUE_PARAMS["prestataire"]["lambda_annuel_non_conforme"]

    if pcd_prestataire is not None:
        lam_presta = (1 - pcd_prestataire) * lam_conf + pcd_prestataire * lam_non_conf
    else:
        lam_presta = lam_non_conf if is_conforme is False else lam_conf


    freqs_presta = rng.poisson(lam_presta, size=n_sim)
    total_events_presta = int(freqs_presta.sum())

    mu_p = BRIQUE_PARAMS["prestataire"]["mu_lognorm"]
    sig_p = BRIQUE_PARAMS["prestataire"]["sigma_lognorm"]
    prestataire_severities = rng.lognormal(mean=mu_p, sigma=sig_p, size=total_events_presta)

    splits_presta = np.cumsum(freqs_presta)[:-1]
    brique_prestataire = np.array([s.sum() for s in np.split(prestataire_severities, splits_presta)])

    # --- COPULE (Dépendance de queue annuelle) ---
    if dependence == "gumbel":
        U = gumbel_copula_uniforms(n_sim, theta, dim=3, seed=seed + 1)
    elif dependence == "common_factor":
        p_sys = p_sys if p_sys is not None else pcd_sanction
        U = common_factor_uniforms(n_sim, p_sys, dim=3, seed=seed + 1)
    else:
        raise ValueError("dependence doit être 'gumbel' ou 'common_factor'")

    # Couplage : U[:, 0] génère un stress systémique (surcoût) sur la remédiation
    max_stress = BRIQUE_PARAMS["stress_systemique"]["max_loading"]
    stress_loading = U[:, 0] * max_stress
    brique_remediation = brique_remediation * (1.0 + stress_loading)

    # Couplage : U[:, 1] génère un stress sur le coût prestataire
    brique_prestataire = brique_prestataire * (1.0 + U[:, 1] * max_stress)

    # --- BRIQUE 3 : Sanction (Pilotée par la PCD et U[:, 2]) ---
    sanction_survient = U[:, 2] < pcd_sanction
    low_s, high_s = BRIQUE_PARAMS["sanction"]["montant_range_eur_m"]

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
        "severity_cap": SCR_DORA.get("cap_eur", 40.0),  # appliqué systématiquement, PRC et OpRisk
    }   

    # --- ÉTAT 1 : Entité NON-CONFORME (Réalité) ---
    sc_nc = compute_lambda_scenario(lambda_ref, "S2_non_conforme", mode="center")
    lam_nc = sc_nc["lambda_global"]
    pcd_nc = pcd_conditional(PROFILS_TYPES["median"], 0.0, ANCHORED_PARAMS)

    res_nc = simulate_year_3_briques(lam_nc, severity_params, pcd_nc, n_sim,
                                     is_conforme=False,
                                     dependence=dependence, theta=1.8, seed=42)
    scr_nc = np.quantile(res_nc["total"], alpha)

    # --- ÉTAT 2 : Entité CONFORME (Contrefactuel) ---
    sc_c = compute_lambda_scenario(lambda_ref, "S0_conforme", mode="center")
    lam_c = sc_c["lambda_global"]
    pcd_c = pcd_conditional(PROFILS_TYPES["leader"], 0.0, ANCHORED_PARAMS)

    res_c = simulate_year_3_briques(lam_c, severity_params, pcd_c, n_sim,
                                    is_conforme=True,
                                    dependence=dependence, theta=1.2, seed=42)
    scr_c = np.quantile(res_c["total"], alpha)

    # --- BRIQUE 4 : Aggravation ---
    aggravation_scr = scr_nc - scr_c

    # --- AFFICHAGE ---
    print(f"\\n{'='*70}")
    print(f"  SCR DORA (Modèle complet PDF, corrigé) — {source} / {dependence.upper()}")
    print(f"{'='*70}")
    print(f"  État NON-CONFORME : λ_rem = {lam_nc:.1f} | λ_presta = "
          f"{BRIQUE_PARAMS['prestataire']['lambda_annuel_non_conforme']:.1f} | "
          f"PCD = {pcd_nc:.1%} | θ = 1.8")
    print(f"  État CONFORME     : λ_rem = {lam_c:.1f} | λ_presta = "
          f"{BRIQUE_PARAMS['prestataire']['lambda_annuel_conforme']:.1f} | "
          f"PCD = {pcd_c:.1%} | θ = 1.2")
    print(f"  n_sim = {n_sim:,} | Graine figée (Neutralisation biais de sélection)")

    print(f"\\n  VaR {alpha*100:.1f}% (SCR_DORA Non-Conforme) = {scr_nc:>8.1f} M€")
    print(f"  VaR {alpha*100:.1f}% (SCR_DORA Conforme)     = {scr_c:>8.1f} M€")

    print(f"\\n  Décomposition du risque (Moyenne du run Non-Conforme) :")
    total_mean = res_nc["total"].mean()
    for brique in ["remediation", "prestataire", "sanction"]:
        m = res_nc[brique].mean()
        pct = 100*m/total_mean if total_mean > 0 else 0.0
        print(f"    {brique.capitalize():14s} : {m:>8.1f} M€  ({pct:>5.1f}%)")

    print(f"\\n  >> Brique AGGRAVATION (Contrefactuel Δ_DORA) : {aggravation_scr:>8.1f} M€")
    print(f"     (Surcoût en capital imputable strictement au non-respect)")
    print(f"{'='*70}")

    res_nc["scr_total"] = scr_nc
    res_nc["scr_aggravation"] = aggravation_scr
    return res_nc


if __name__ == "__main__":
    scr_4_briques_report(source="PRC", n_sim=100_000, dependence="gumbel")
    scr_4_briques_report(source="OPRISK", n_sim=100_000, dependence="gumbel")
