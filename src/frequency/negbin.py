"""
frequency/negbin.py
--------------------
Modèle de fréquence NegBin (Negative Binomial) calibré sur la PRC 2025.
Scénarios de fréquence conditionnels au niveau de conformité DORA.

Justification NegBin : surdispersion observée (Var/Mean >> 1) dans les
données cyber — le processus de Poisson simple est rejeté.

Références :
  Farkas, Lopez & Thomas (2021)
  Kher, Lopez & Rapior (2023)
"""

import numpy as np
import pandas as pd
from scipy.stats import nbinom
from scipy.optimize import minimize
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# 1. CALIBRATION NEGBIN PAR MLE
# ---------------------------------------------------------------------------

def fit_negbin(counts: np.ndarray) -> dict:
    """
    Calibre la loi NegBin(r, p) sur une série de comptages mensuels.
    Paramétrage : E[X] = r(1-p)/p, Var[X] = r(1-p)/p²

    Parameters
    ----------
    counts : array d'entiers (nombre d'incidents par période)

    Returns
    -------
    dict : r, p, mu (moyenne), sigma2 (variance), dispersion_factor
    """
    mu_hat = np.mean(counts)
    var_hat = np.var(counts, ddof=1)

    if var_hat <= mu_hat:
        raise ValueError(
            f"Pas de surdispersion détectée (Var={var_hat:.2f} ≤ Mu={mu_hat:.2f}). "
            "Vérifier les données ou utiliser Poisson."
        )

    # Méthode des moments pour initialisation
    r_init = mu_hat ** 2 / (var_hat - mu_hat)
    p_init = mu_hat / var_hat

    # MLE
    def neg_loglik(params):
        r, p = params
        if r <= 0 or p <= 0 or p >= 1:
            return 1e10
        return -np.sum(nbinom.logpmf(counts.astype(int), r, p))

    result = minimize(neg_loglik, x0=[r_init, p_init],
                      method="Nelder-Mead",
                      options={"xatol": 1e-8, "fatol": 1e-8, "maxiter": 10000})

    r, p = result.x
    mu = r * (1 - p) / p
    sigma2 = r * (1 - p) / p ** 2
    dispersion = sigma2 / mu  # facteur de surdispersion (= 1 pour Poisson)

    params = {
        "r": r, "p": p,
        "mu": mu, "sigma2": sigma2,
        "dispersion_factor": dispersion,
        "n_periods": len(counts),
        "log_lik": -result.fun,
    }

    print(f"\n=== CALIBRATION NegBin ===")
    print(f"  r  = {r:.4f}")
    print(f"  p  = {p:.4f}")
    print(f"  μ  = {mu:.2f} incidents/période")
    print(f"  σ² = {sigma2:.2f}")
    print(f"  Facteur de surdispersion = {dispersion:.2f}  (Poisson = 1)")
    print(f"  Périodes calibrées       = {len(counts)}\n")

    return params


# ---------------------------------------------------------------------------
# 2. MAPPING VECTEURS D'ATTAQUE → MULTIPLICATEURS DORA
# ---------------------------------------------------------------------------

# Proportions par vecteur (source : Hackmageddon S1 2026, 1 041 incidents)
HACKMAGEDDON_PROPORTIONS = {
    "phishing_social_eng": 0.388,       # Art. 13 — Formation
    "exploit_vuln":        0.338,       # Art. 26 — TLPT
    "supply_chain_tiers":  0.158,       # Art. 28-44 — Tiers ICT
    "identifiants":        0.063,       # Art. 9 — Accès/MFA
    "autres":              0.053,       # Transverse
}

# Articles DORA par vecteur
DORA_MAPPING = {
    "phishing_social_eng": "Art. 13 — Sensibilisation & formation",
    "exploit_vuln":        "Art. 26 — Tests TLPT ; Art. 8-10",
    "supply_chain_tiers":  "Art. 28-44 — Gestion risque tiers ICT",
    "identifiants":        "Art. 9 — Contrôle d'accès & MFA",
    "autres":              "Transverse",
}

# Multiplicateurs de fréquence par vecteur et par niveau de conformité
# Calibrés sur la littérature ENISA / Ponemon sur l'efficacité des contrôles
# [référence : ENISA Threat Landscape 2024, Ponemon Cost of Data Breach 2024]
MULTIPLICATEURS_DORA = {
    "S0_conforme": {
        vecteur: 1.0 for vecteur in HACKMAGEDDON_PROPORTIONS
    },
    "S1_partiel": {
        "phishing_social_eng": 1.3,   # Art. 13 non appliqué → +30%
        "exploit_vuln":        1.5,   # Pas de TLPT → +50%
        "supply_chain_tiers":  1.8,   # Tiers non supervisés → +80%
        "identifiants":        1.4,   # Pas de MFA → +40%
        "autres":              1.2,
    },
    "S2_non_conforme": {
        "phishing_social_eng": 1.7,
        "exploit_vuln":        2.5,
        "supply_chain_tiers":  3.0,   # Exposition maximale tiers
        "identifiants":        2.0,
        "autres":              1.5,
    },
}


def compute_lambda_scenario(lambda_ref: float, scenario: str) -> dict:
    """
    Calcule le λ effectif pour chaque vecteur sous un scénario DORA.
    Le λ global est la somme pondérée des λ par vecteur.

    Parameters
    ----------
    lambda_ref : fréquence de référence (scénario S0 conforme)
    scenario   : 'S0_conforme', 'S1_partiel', 'S2_non_conforme'

    Returns
    -------
    dict : lambda_par_vecteur, lambda_global, multiplicateur_global
    """
    if scenario not in MULTIPLICATEURS_DORA:
        raise ValueError(f"Scénario inconnu : {scenario}. "
                         f"Choisir parmi {list(MULTIPLICATEURS_DORA.keys())}")

    mults = MULTIPLICATEURS_DORA[scenario]
    props = HACKMAGEDDON_PROPORTIONS

    lambda_vecteur = {}
    lambda_global = 0.0

    for v, prop in props.items():
        lv = lambda_ref * prop * mults[v]
        lambda_vecteur[v] = lv
        lambda_global += lv

    mult_global = lambda_global / lambda_ref

    return {
        "scenario": scenario,
        "lambda_ref": lambda_ref,
        "lambda_global": lambda_global,
        "multiplicateur_global": mult_global,
        "lambda_par_vecteur": lambda_vecteur,
    }


def scenario_comparison(lambda_ref: float) -> pd.DataFrame:
    """
    Compare les trois scénarios de conformité DORA.

    Returns
    -------
    DataFrame : un scénario par ligne
    """
    rows = []
    for sc in ["S0_conforme", "S1_partiel", "S2_non_conforme"]:
        res = compute_lambda_scenario(lambda_ref, sc)
        rows.append({
            "Scénario": sc,
            "λ_global": res["lambda_global"],
            "Multiplicateur": res["multiplicateur_global"],
            "Δλ vs S0": res["lambda_global"] - lambda_ref,
        })

    df = pd.DataFrame(rows)
    print("\n=== SCÉNARIOS DE CONFORMITÉ DORA ===")
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\nSource multiplicateurs : Hackmageddon S1 2026 (1 041 incidents)")
    print(f"Borne calibration : ENISA Threat Landscape 2024 / Ponemon 2024\n")
    return df


# ---------------------------------------------------------------------------
# 3. SIMULATION NEGBIN SOUS SCÉNARIO DORA
# ---------------------------------------------------------------------------

def simulate_frequency(params: dict, scenario: str,
                        lambda_ref: float,
                        n_sim: int = 1_000_000,
                        seed: int = 42) -> np.ndarray:
    """
    Simule n_sim réalisations de la fréquence annuelle sous un scénario DORA.

    Parameters
    ----------
    params     : dict issu de fit_negbin()
    scenario   : scénario DORA
    lambda_ref : fréquence de référence annuelle
    n_sim      : nombre de simulations
    seed       : graine aléatoire

    Returns
    -------
    array de n_sim entiers (nombre d'incidents simulés)
    """
    np.random.seed(seed)
    sc_res = compute_lambda_scenario(lambda_ref, scenario)
    mult = sc_res["multiplicateur_global"]

    # Ajuster r et p pour le multiplicateur de fréquence
    # Si X ~ NegBin(r, p) avec E[X] = mu,
    # alors k*X ~ NegBin(r, p') avec E = k*mu
    # Approche : on recale mu et on refite p à r fixé
    r = params["r"]
    mu_new = params["mu"] * mult
    p_new = r / (r + mu_new)

    counts = nbinom.rvs(r, p_new, size=n_sim, random_state=seed)
    return counts


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Module negbin.py chargé.")
    print()
    print("Exemple :")
    print("  from src.frequency.negbin import fit_negbin, scenario_comparison")
    print("  counts = np.array([120, 145, 130, ...])  # incidents mensuels")
    print("  params = fit_negbin(counts)")
    print("  df = scenario_comparison(lambda_ref=params['mu'] * 12)")
