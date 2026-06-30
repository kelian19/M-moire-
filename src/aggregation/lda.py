"""
aggregation/lda.py
--------------------
Pipeline LDA Monte Carlo COMPLET à 4 briques, agrégées par copule de Gumbel
(ou modèle à facteur commun en robustesse).

LES 4 BRIQUES — décision de sourcing (trancher la question laissée ouverte)
=============================================================================
Chaque brique réutilise une donnée DÉJÀ SOURCÉE dans le mémoire, plutôt que
d'inventer une calibration indépendante (ce qu'aucune base disponible ne
permettrait — cf. chapitre Limites et cadre épistémique) :

  1. AGGRAVATION   : la sévérité de base de l'incident, GPD déjà calibrée
                      (PRC ou OpRisk, cf. chapitres sévérité). C'est la
                      brique dominante, seule à reposer sur une calibration
                      statistique directe.

  2. PRESTATAIRE    : surcharge MULTIPLICATIVE sur la sévérité de base,
                      déclenchée lorsque l'incident relève du vecteur
                      "supply_chain_tiers" (15.8% des incidents, Hackmageddon).
                      Magnitude : surcoût mesuré IBM/Ponemon (+11.8% brèche
                      partenaire, +8.3% brèche logicielle) — tirage uniforme
                      dans [8.3%, 11.8%].

  3. REMÉDIATION    : surcharge MULTIPLICATIVE liée à la qualité du dispositif
                      de réponse à incident. Magnitude ancrée sur IBM/Ponemon :
                      un plan de réponse testé permet une économie de 58% —
                      en son absence (scénario non conforme), surcharge
                      tirée dans [20%, 58%] (fraction de l'effet mesuré,
                      tempérée comme les autres multiplicateurs du mémoire).

  4. SANCTION       : composante ADDITIVE, indépendante par construction de
                      la sévérité de l'incident. Probabilité d'occurrence =
                      PCD de la variable latente de conformité (lien direct
                      avec compliance/latent.py — ce n'est PAS un paramètre
                      arbitraire, c'est la probabilité de défaut déjà
                      calculée). Magnitude bornée par l'Article 50 DORA :
                      amendes jusqu'à 2% du CA, plafonds nationaux observés
                      entre 2M€ et 20M€ — on retient un tirage uniforme dans
                      [2, 20] M€ comme proxy de cette fourchette réglementaire.

AGRÉGATION : copule de Gumbel (θ=1.8) sur les 4 marginales, capturant la
dépendance de queue — un incident qui dégénère entraîne typiquement
remédiation lourde, recours prestataire ET risque de sanction simultanément.
"""

import numpy as np
from scipy.stats import genpareto, nbinom
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.aggregation.copule import gumbel_copula_uniforms, common_factor_uniforms
from src.frequency.negbin import HACKMAGEDDON_PROPORTIONS
from src.compliance.latent import pcd_conditional, ANCHORED_PARAMS, PROFILS_TYPES
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA


# ---------------------------------------------------------------------------
# 1. PARAMÈTRES DES BRIQUES (sourcés, cf. docstring du module)
# ---------------------------------------------------------------------------

BRIQUE_PARAMS = {
    "prestataire": {"trigger_prop": HACKMAGEDDON_PROPORTIONS["supply_chain_tiers"],
                     "loading_range": (0.083, 0.118),
                     "source": "IBM/Ponemon 2023-2025 — surcoût brèches tierces"},
    "remediation": {"loading_range": (0.20, 0.58),
                     "source": "IBM/Ponemon — économie de 58% avec plan IR testé"},
    "sanction": {"montant_range_eur_m": (2.0, 20.0),
                 "source": "DORA Art. 50 — plafonds nationaux observés 2-20M€"},
    # Chargement systémique sur l'AGGRAVATION elle-même — PAS sourcé sur une
    # donnée externe (aucune littérature ne mesure directement cet effet) :
    # hypothèse de modélisation explicite, représentant la dégradation de la
    # capacité de réponse en cas de stress systémique (incidents concurrents,
    # ressources de remédiation saturées). Borne haute volontairement modeste
    # (15%) pour ne pas double-compter la queue déjà lourde de la GPD.
    "aggravation_stress": {"loading_range": (0.0, 0.15),
                           "source": "HYPOTHÈSE DE MODÉLISATION — non sourcée, "
                                     "à justifier/discuter dans le mémoire"},
}


# ---------------------------------------------------------------------------
# 2. SIMULATION DE LA BRIQUE 1 — AGGRAVATION (sévérité de base, par incident)
# ---------------------------------------------------------------------------

def simulate_aggravation(n_events: int, xi: float, sigma: float, u: float,
                          p_u: float, severity_cap: float, rng) -> np.ndarray:
    """Sévérité de base par incident — réutilise la logique GPD + p_u déjà
    validée (cf. scenarios/bootstrap_delta_dora.py)."""
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
# 3. SIMULATION ANNUELLE À 4 BRIQUES, AGRÉGÉES PAR COPULE
# ---------------------------------------------------------------------------

def simulate_year_4_briques(lambda_annual: float, severity_params: dict,
                             pcd_sanction: float, n_sim: int,
                             dependence: str = "gumbel", theta: float = 1.8,
                             p_sys: float = None, seed: int = 42) -> dict:
    """
    Simule n_sim années de pertes agrégées sur les 4 briques.

    Parameters
    ----------
    lambda_annual   : fréquence annuelle d'incidents (déjà ajustée scénario)
    severity_params : dict avec xi, sigma, u, p_u, dispersion, cap (sévérité
                      de la brique aggravation)
    pcd_sanction    : probabilité de défaut de conformité (déclenche sanction)
    n_sim           : nombre de simulations Monte Carlo
    dependence      : 'gumbel' (copule) ou 'common_factor' (robustesse)
    theta           : paramètre de la copule de Gumbel
    p_sys           : probabilité de choc systémique (modèle facteur commun) ;
                      si None, utilise pcd_sanction comme proxy de p_sys
    seed            : graine

    Returns
    -------
    dict : pertes agrégées totales + décomposition par brique (médianes)
    """
    rng = np.random.default_rng(seed)
    xi, sigma, u, p_u = (severity_params["xi"], severity_params["sigma"],
                         severity_params["u"], severity_params["p_u"])
    dispersion = severity_params.get("dispersion_factor", 9.2)
    cap = severity_params.get("severity_cap", None)

    # --- Fréquence annuelle (NegBin) ---
    r = lambda_annual / (dispersion - 1) if dispersion > 1 else lambda_annual
    p = r / (r + lambda_annual)
    freqs = rng.negative_binomial(r, p, size=n_sim)
    total_events = int(freqs.sum())

    # --- Brique 1 : Aggravation (par incident) ---
    aggravation = simulate_aggravation(total_events, xi, sigma, u, p_u, cap, rng)

    # --- Vecteur d'attaque de chaque incident (pour déclencher "prestataire") ---
    vecteurs = rng.choice(list(HACKMAGEDDON_PROPORTIONS.keys()), size=total_events,
                          p=list(HACKMAGEDDON_PROPORTIONS.values()))
    is_tiers = vecteurs == "supply_chain_tiers"

    # --- Copule reliant les 4 briques (au niveau ANNUEL, pas par incident :
    #     la dépendance modélisée est celle de l'ANNÉE qui dégénère, pas du
    #     micro-incident) ---
    if dependence == "gumbel":
        U = gumbel_copula_uniforms(n_sim, theta, dim=4, seed=seed + 1)
    elif dependence == "common_factor":
        p_sys = p_sys if p_sys is not None else pcd_sanction
        U = common_factor_uniforms(n_sim, p_sys, dim=4, seed=seed + 1)
    else:
        raise ValueError("dependence doit être 'gumbel' ou 'common_factor'")

    # U[:,0] -> chargement systémique sur l'AGGRAVATION (cf. correction :
    #            sans ce couplage, la brique dominante échappait entièrement
    #            à la copule, rendant p_sys/theta quasi sans effet sur le SCR)
    # U[:,1] -> facteur d'intensité prestataire de l'année
    # U[:,2] -> facteur d'intensité remédiation de l'année
    # U[:,3] -> facteur déclenchant la sanction de l'année

    # --- Agrégation par simulation (découpage des incidents par année) ---
    splits = np.cumsum(freqs)[:-1]
    aggravation_par_an = np.array([s.sum() for s in np.split(aggravation, splits)])
    tiers_par_an = np.array([s.sum() for s in np.split(is_tiers.astype(float), splits)])

    # --- Couplage de l'aggravation au facteur de dépendance (la correction) ---
    low_a, high_a = BRIQUE_PARAMS["aggravation_stress"]["loading_range"]
    stress_loading = low_a + U[:, 0] * (high_a - low_a)
    aggravation_par_an = aggravation_par_an * (1.0 + stress_loading)

    # --- Brique 2 : Prestataire (loading sur la part tiers de l'aggravation) ---
    low_p, high_p = BRIQUE_PARAMS["prestataire"]["loading_range"]
    loading_prestataire = low_p + U[:, 1] * (high_p - low_p)
    # Approxime la part de sévérité imputable aux incidents "tiers" de l'année
    part_tiers_severite = aggravation_par_an * (tiers_par_an / np.maximum(freqs, 1))
    brique_prestataire = part_tiers_severite * loading_prestataire

    # --- Brique 3 : Remédiation (loading sur la sévérité totale) ---
    low_r, high_r = BRIQUE_PARAMS["remediation"]["loading_range"]
    loading_remediation = low_r + U[:, 2] * (high_r - low_r)
    brique_remediation = aggravation_par_an * loading_remediation

    # --- Brique 4 : Sanction (additive, indépendante, probabilité = PCD) ---
    low_s, high_s = BRIQUE_PARAMS["sanction"]["montant_range_eur_m"]
    sanction_survient = U[:, 3] < pcd_sanction
    montant_sanction = low_s + rng.uniform(0, 1, n_sim) * (high_s - low_s)
    brique_sanction = np.where(sanction_survient, montant_sanction, 0.0)

    # --- Perte totale agrégée ---
    total = aggravation_par_an + brique_prestataire + brique_remediation + brique_sanction

    return {
        "total": total,
        "aggravation": aggravation_par_an,
        "prestataire": brique_prestataire,
        "remediation": brique_remediation,
        "sanction": brique_sanction,
        "dependence": dependence,
    }


# ---------------------------------------------------------------------------
# 4. RAPPORT — SCR À 4 BRIQUES
# ---------------------------------------------------------------------------

def scr_4_briques_report(source: str = "OPRISK", scenario: str = "S2_non_conforme",
                          alpha: float = 0.995, n_sim: int = 100_000,
                          dependence: str = "gumbel"):
    """
    Calcule et affiche le SCR sous le modèle complet à 4 briques, avec
    décomposition par brique (contribution moyenne à la perte totale).
    """
    from src.frequency.negbin import compute_lambda_scenario

    source_map = {"PRC": PRC, "OPRISK": OPRISK}
    src = source_map[source]
    lambda_ref = FREQUENCY["lambda_ref"] if source == "PRC" else OPRISK["n_incidents"] / 27
    sc = compute_lambda_scenario(lambda_ref, scenario, mode="center")
    lam = sc["lambda_global"]

    severity_params = {
        "xi": src["xi"], "sigma": src["sigma_eur"], "u": src["seuil_u_eur"],
        "p_u": src["p_u"], "dispersion_factor": FREQUENCY["dispersion_factor"],
        "severity_cap": SCR_DORA.get("cap_eur", 40.0) if source == "PRC" else None,
    }

    # PCD de référence (entité médiane, environnement normal) pour piloter la sanction
    pcd = pcd_conditional(PROFILS_TYPES["median"], 0.0, ANCHORED_PARAMS)

    res = simulate_year_4_briques(lam, severity_params, pcd, n_sim,
                                   dependence=dependence)

    scr_total = np.quantile(res["total"], alpha)
    print(f"\n{'='*66}")
    print(f"  SCR À 4 BRIQUES — {source} / {scenario} / {dependence}")
    print(f"{'='*66}")
    print(f"  λ = {lam:.1f}  |  PCD (sanction) = {pcd:.1%}  |  n_sim = {n_sim:,}")
    print(f"\n  SCR total (VaR {alpha*100:.1f}%) = {scr_total:,.1f} M€")
    print(f"\n  Décomposition (moyenne par brique, % du total) :")
    total_mean = res["total"].mean()
    for brique in ["aggravation", "prestataire", "remediation", "sanction"]:
        m = res[brique].mean()
        print(f"    {brique:14s} : {m:>10.1f} M€  ({100*m/total_mean:>5.1f}%)")
    print(f"{'='*66}")
    return res, scr_total


if __name__ == "__main__":
    scr_4_briques_report(source="OPRISK", scenario="S2_non_conforme",
                         n_sim=100_000, dependence="gumbel")
    scr_4_briques_report(source="OPRISK", scenario="S2_non_conforme",
                         n_sim=100_000, dependence="common_factor")
