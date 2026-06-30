"""
scenarios/delta_dora.py
-----------------------
Calcul du Δ_DORA — différentiel de capital entre un état conforme
et un état de non-conformité DORA — via approche contrefactuelle (C).

Architecture :
  1. Simulation LDA sous S0 (conforme) → SCR_S0
  2. Simulation LDA sous S1/S2 (non conforme) → SCR_S1 / SCR_S2
  3. Δ_DORA = SCR_Sx - SCR_S0
  4. Bootstrap deux niveaux → Distribution de Δ_DORA

Références :
  Approche C (contrefactuelle) : Kher, Lopez & Rapior (2023)
  Bootstrap deux niveaux : Farkas, Lopez & Thomas (2021)
"""

import numpy as np
import pandas as pd
from scipy.stats import genpareto, nbinom
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# 1. SIMULATION LDA — UN SCÉNARIO
# ---------------------------------------------------------------------------

def simulate_lda(lambda_scenario: float,
                 gpd_params: dict,
                 n_sim: int = 1_000_000,
                 seed: int = 42) -> np.ndarray:
    """
    Simulation LDA (Loss Distribution Approach) pour un scénario.
    Modèle simplifié : fréquence NegBin × sévérité GPD, une seule brique.

    Parameters
    ----------
    lambda_scenario : fréquence annuelle sous le scénario
    gpd_params      : dict {xi, sigma, u, p_u} issu de fit_gpd()
    n_sim           : nombre de simulations
    seed            : graine

    Returns
    -------
    array de n_sim pertes agrégées annuelles
    """
    np.random.seed(seed)
    xi = gpd_params["xi"]
    sigma = gpd_params["sigma"]
    u = gpd_params["u"]
    p_u = gpd_params["p_u"]

    # Paramètres NegBin : r à calibrer, p déduit de lambda
    # Utiliser dispersion_factor de la calibration PRC
    dispersion = gpd_params.get("dispersion_factor", 9.2)
    mu = lambda_scenario
    r = mu / (dispersion - 1) if dispersion > 1 else mu
    p = r / (r + mu)

    pertes_agregees = np.zeros(n_sim)

    for i in range(n_sim):
        # Fréquence
        n_events = nbinom.rvs(r, p)
        if n_events == 0:
            continue
        # Sévérité : mélange corps (< u) + queue GPD
        # Simplification : on modélise uniquement les pertes > u (queue)
        # Le corps est approximé par une exponentielle tronquée
        n_gpdloss = np.random.binomial(n_events, p_u)
        if n_gpdloss > 0:
            u_vals = np.random.uniform(0, 1, n_gpdloss)
            # Quantile GPD
            gpd_losses = u + genpareto.ppf(u_vals, c=xi, scale=sigma)
            pertes_agregees[i] = gpd_losses.sum()

    return pertes_agregees


def simulate_lda_vectorized(lambda_scenario: float,
                             gpd_params: dict,
                             n_sim: int = 1_000_000,
                             seed: int = 42,
                             severity_cap: float = None) -> np.ndarray:
    """
    Version vectorisée (plus rapide) de simulate_lda.
    Hypothèse : toutes les pertes suivent GPD (pas de corps).
    Utilisable si le seuil u est bas.

    Parameters
    ----------
    severity_cap : plafond de sévérité par incident (même unité que gpd_params).
                   OBLIGATOIRE en pratique si ξ >= 1 (espérance infinie) :
                   sans plafond, la somme Monte Carlo explose numériquement
                   et ne représente plus une charge de capital interprétable.
                   Référence : plafond 40-50 M€ ancré sur la capacité de
                   réassurance cyber (cf. notes de calibration du mémoire).
    """
    np.random.seed(seed)
    xi = gpd_params["xi"]
    sigma = gpd_params["sigma"]
    u = gpd_params["u"]

    if xi >= 1.0 and severity_cap is None:
        import warnings
        warnings.warn(
            f"ξ={xi:.3f} >= 1 : espérance de sévérité infinie. "
            "Sans severity_cap, la VaR simulée est numériquement instable "
            "et économiquement non interprétable. Un plafond est fortement recommandé.",
            UserWarning
        )

    dispersion = gpd_params.get("dispersion_factor", 9.2)
    mu = lambda_scenario
    r = mu / (dispersion - 1) if dispersion > 1 else mu
    p = r / (r + mu)

    # Fréquences simulées
    freqs = nbinom.rvs(r, p, size=n_sim, random_state=seed)
    total_events = freqs.sum()

    # Application correcte de p_u : seule une fraction p_u des événements
    # dépasse le seuil u et relève de la GPD. Les autres (1-p_u) sont des
    # pertes "corps" (sous le seuil) — approximées ici à 0 (simplification
    # explicite : sans modèle de corps calibré, leur contribution à un
    # quantile de queue élevé comme la VaR 99.5% est marginale).
    p_u = gpd_params.get("p_u", 1.0)
    rng = np.random.default_rng(seed)
    is_tail = rng.random(total_events) < p_u
    severities = np.zeros(total_events)
    n_tail = int(is_tail.sum())
    if n_tail > 0:
        u_vals = rng.uniform(0, 1, n_tail)
        severities[is_tail] = u + genpareto.ppf(u_vals, c=xi, scale=sigma)

    # Application du plafond de sévérité (troncature par incident)
    if severity_cap is not None:
        severities = np.minimum(severities, severity_cap)

    # Agrégation par simulation
    splits = np.cumsum(freqs)[:-1]
    pertes = np.array([s.sum() for s in np.split(severities, splits)])

    return pertes


# ---------------------------------------------------------------------------
# 2. VaR ET TVaR EMPIRIQUES
# ---------------------------------------------------------------------------

def empirical_var(losses: np.ndarray, alpha: float = 0.995) -> float:
    """VaR empirique au niveau alpha."""
    return float(np.quantile(losses, alpha))


def empirical_tvar(losses: np.ndarray, alpha: float = 0.99) -> float:
    """TVaR empirique = moyenne des pertes au-delà de la VaR."""
    var = empirical_var(losses, alpha)
    tail = losses[losses >= var]
    return float(tail.mean()) if len(tail) > 0 else float(var)


# ---------------------------------------------------------------------------
# 3. DELTA_DORA — APPROCHE CONTREFACTUELLE C
# ---------------------------------------------------------------------------

def compute_delta_dora(gpd_params: dict,
                        lambda_s0: float,
                        lambda_sx: float,
                        n_sim: int = 1_000_000,
                        alpha: float = 0.995,
                        seed: int = 42) -> dict:
    """
    Calcule Δ_DORA = VaR_Sx(α) - VaR_S0(α).

    Approche C (contrefactuelle) :
      - S0 : scénario conforme (référence)
      - Sx : scénario non conforme (partiel ou total)

    Parameters
    ----------
    gpd_params   : paramètres GPD calibrés
    lambda_s0    : fréquence annuelle sous S0
    lambda_sx    : fréquence annuelle sous Sx
    n_sim        : simulations Monte Carlo
    alpha        : niveau VaR (défaut 99.5% Solvabilité 2)
    seed         : graine

    Returns
    -------
    dict : scr_s0, scr_sx, delta_dora, ratio
    """
    print(f"Simulation S0 (λ={lambda_s0:.1f})...")
    losses_s0 = simulate_lda_vectorized(lambda_s0, gpd_params, n_sim, seed)
    scr_s0 = empirical_var(losses_s0, alpha)

    print(f"Simulation Sx (λ={lambda_sx:.1f})...")
    losses_sx = simulate_lda_vectorized(lambda_sx, gpd_params, n_sim, seed + 1)
    scr_sx = empirical_var(losses_sx, alpha)

    delta = scr_sx - scr_s0

    result = {
        "scr_s0": scr_s0,
        "scr_sx": scr_sx,
        "delta_dora": delta,
        "ratio": scr_sx / scr_s0 if scr_s0 > 0 else None,
        "lambda_s0": lambda_s0,
        "lambda_sx": lambda_sx,
        "mult_effectif": lambda_sx / lambda_s0,
        "alpha": alpha,
        "n_sim": n_sim,
    }

    print(f"\n=== Δ_DORA ===")
    print(f"  SCR S0 (conforme)      = {scr_s0:.2f} M€")
    print(f"  SCR Sx (non conforme)  = {scr_sx:.2f} M€")
    print(f"  Δ_DORA                 = {delta:.2f} M€")
    print(f"  Ratio SCR_Sx / SCR_S0  = {result['ratio']:.3f}")

    return result


# ---------------------------------------------------------------------------
# 4. BOOTSTRAP DEUX NIVEAUX — DISTRIBUTION DE DELTA_DORA
# ---------------------------------------------------------------------------

def bootstrap_delta_dora(gpd_params_list: list,
                          lambda_s0_list: list,
                          lambda_sx_list: list,
                          n_boot: int = 500,
                          n_sim: int = 500_000,
                          alpha: float = 0.995) -> dict:
    """
    Bootstrap deux niveaux sur Δ_DORA :
      Niveau 1 : incertitude sur les paramètres GPD (ξ, σ)
      Niveau 2 : incertitude Monte Carlo

    Parameters
    ----------
    gpd_params_list  : liste de dicts GPD (tirages bootstrap niveau 1)
    lambda_s0_list   : liste de λ_S0 (tirages bootstrap niveau 1)
    lambda_sx_list   : liste de λ_Sx (tirages bootstrap niveau 1)
    n_boot           : nombre de tirages bootstrap
    n_sim            : simulations par tirage
    alpha            : niveau VaR

    Returns
    -------
    dict : distribution de Δ_DORA, IC, décomposition de variance
    """
    deltas = []
    scr_s0_list, scr_sx_list = [], []

    n_iter = min(n_boot, len(gpd_params_list))
    print(f"Bootstrap Δ_DORA : {n_iter} itérations × {n_sim:,} simulations...")

    for i in range(n_iter):
        seed = 100 + i
        try:
            params_i = gpd_params_list[i]
            l0_i = lambda_s0_list[i]
            lx_i = lambda_sx_list[i]

            losses_s0 = simulate_lda_vectorized(l0_i, params_i, n_sim, seed)
            losses_sx = simulate_lda_vectorized(lx_i, params_i, n_sim, seed + 1)

            s0 = empirical_var(losses_s0, alpha)
            sx = empirical_var(losses_sx, alpha)

            scr_s0_list.append(s0)
            scr_sx_list.append(sx)
            deltas.append(sx - s0)
        except Exception:
            continue

    deltas = np.array(deltas)
    ci90 = np.percentile(deltas, [5, 95])
    ci95 = np.percentile(deltas, [2.5, 97.5])

    result = {
        "delta_median": float(np.median(deltas)),
        "delta_mean": float(np.mean(deltas)),
        "delta_std": float(np.std(deltas)),
        "ic90": ci90.tolist(),
        "ic95": ci95.tolist(),
        "n_valid": len(deltas),
        "distribution": deltas,
    }

    print(f"\n=== DISTRIBUTION Δ_DORA (bootstrap {len(deltas)} itérations) ===")
    print(f"  Médiane  = {result['delta_median']:.2f} M€")
    print(f"  Moyenne  = {result['delta_mean']:.2f} M€")
    print(f"  Std      = {result['delta_std']:.2f} M€")
    print(f"  IC 90%   = [{ci90[0]:.2f}, {ci90[1]:.2f}] M€")
    print(f"  IC 95%   = [{ci95[0]:.2f}, {ci95[1]:.2f}] M€")
    print(f"\n  → 'Le SCR cyber n'est pas un nombre, c'est une distribution large.'")

    return result


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Module delta_dora.py chargé.")
    print()
    print("Exemple :")
    print("  from src.scenarios.delta_dora import compute_delta_dora")
    print("  from src.frequency.negbin import compute_lambda_scenario")
    print()
    print("  gpd_params = {'xi': 1.30, 'sigma': 0.257, 'u': 0.128,")
    print("                'p_u': 0.15, 'dispersion_factor': 9.2}")
    print("  lambda_s0 = 341  # incidents/an (PRC calibration)")
    print("  sc = compute_lambda_scenario(lambda_s0, 'S2_non_conforme')")
    print("  result = compute_delta_dora(gpd_params, lambda_s0, sc['lambda_global'])")
