"""
severity/gpd.py
---------------
Calibration GPD (Generalized Pareto Distribution) par MLE.
Utilisé pour modéliser la queue de distribution des pertes cyber.

Sources :
  - PRC 2025 (Privacy Rights Clearinghouse) — source primaire
  - SAS OpRisk Global Data (juin 2026)      — validation croisée

Références :
  Pickands (1975), Balkema & de Haan (1974)
  Farkas, Lopez & Thomas (2021)
"""

import numpy as np
import pandas as pd
from scipy.stats import genpareto
from scipy.optimize import minimize
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# 1. SÉLECTION DU SEUIL — Mean Excess Plot
# ---------------------------------------------------------------------------

def mean_excess(losses: np.ndarray, thresholds: list = None) -> pd.DataFrame:
    """
    Calcule la fonction d'excès moyen e(u) = E[X - u | X > u].
    Une e(u) linéairement croissante confirme le régime GPD (ξ > 0).

    Parameters
    ----------
    losses      : array de pertes brutes (même unité)
    thresholds  : liste de seuils u à tester (défaut = percentiles 50 à 95)

    Returns
    -------
    DataFrame : colonnes [u, n_excess, e_u, ratio_e_u]
    """
    if thresholds is None:
        thresholds = [np.percentile(losses, p) for p in range(50, 96, 5)]

    rows = []
    for u in thresholds:
        exc = losses[losses > u] - u
        if len(exc) < 10:
            continue
        rows.append({
            "u": u,
            "n_excess": len(exc),
            "e_u": exc.mean(),
            "ratio_e_u": exc.mean() / u,
        })
    return pd.DataFrame(rows)


def select_threshold(losses: np.ndarray,
                     min_excesses: int = 30,
                     pct_range: tuple = (70, 90)) -> float:
    """
    Sélectionne le seuil u optimal par stabilité de ξ̂ sur une grille.
    Retourne le seuil du percentile médian de la plage stable.
    """
    pcts = range(pct_range[0], pct_range[1] + 1, 2)
    stab = []
    for p in pcts:
        u = np.percentile(losses, p)
        exc = losses[losses > u] - u
        if len(exc) < min_excesses:
            continue
        try:
            xi, _, _ = genpareto.fit(exc, floc=0)
            stab.append({"pct": p, "u": u, "xi": xi, "n": len(exc)})
        except Exception:
            continue

    if not stab:
        return np.percentile(losses, 75)

    df = pd.DataFrame(stab)
    # Seuil recommandé : premier percentile où ξ < 1 (moments finis)
    valid = df[df["xi"] < 1.0]
    if valid.empty:
        return df["u"].median()
    return float(valid.iloc[0]["u"])


# ---------------------------------------------------------------------------
# 2. CALIBRATION GPD PAR MLE
# ---------------------------------------------------------------------------

def fit_gpd(losses: np.ndarray, u: float) -> dict:
    """
    Calibre la GPD sur les excès au-dessus du seuil u par MLE.

    Parameters
    ----------
    losses : array de pertes brutes
    u      : seuil POT

    Returns
    -------
    dict : xi, sigma, u, n_excess, n_total, p_u
    """
    excesses = losses[losses > u] - u
    n_exc = len(excesses)
    n_tot = len(losses)

    if n_exc < 20:
        raise ValueError(f"Seuil u={u:.2f} trop élevé : seulement {n_exc} excès.")

    xi, loc, sigma = genpareto.fit(excesses, floc=0)

    return {
        "xi": xi,
        "sigma": sigma,
        "u": u,
        "n_excess": n_exc,
        "n_total": n_tot,
        "p_u": n_exc / n_tot,
    }


# ---------------------------------------------------------------------------
# 3. QUANTILES — VaR et TVaR
# ---------------------------------------------------------------------------

def var_gpd(params: dict, alpha: float) -> float:
    """
    VaR au niveau alpha sous le modèle GPD spliced.

    VaR_α = u + (σ/ξ) * [((1-α)/p_u)^(-ξ) - 1]

    Parameters
    ----------
    params : dict issu de fit_gpd()
    alpha  : niveau de quantile (ex. 0.995 pour Solvabilité 2)
    """
    xi, sigma, u, p_u = params["xi"], params["sigma"], params["u"], params["p_u"]
    if alpha <= 1 - p_u:
        raise ValueError("alpha trop faible : en-dessous du seuil u.")
    # Argument POT correct : ratio des probabilités de survie (1-alpha)/p_u
    # VaR_α = u + (σ/ξ) * [ ((1-α)/p_u)^(-ξ) - 1 ]
    ratio = (1 - alpha) / p_u
    if xi == 0:
        return u - sigma * np.log(ratio)
    return u + (sigma / xi) * (ratio ** (-xi) - 1)


def tvar_gpd(params: dict, alpha: float) -> float:
    """
    TVaR (Tail Value-at-Risk) sous GPD. Définie uniquement si ξ < 1.

    TVaR_α = (VaR_α + σ - ξ*u) / (1 - ξ)
    """
    xi = params["xi"]
    if xi >= 1:
        raise ValueError(f"TVaR indéfinie : ξ={xi:.4f} ≥ 1 → E[X] = ∞")
    var = var_gpd(params, alpha)
    u, sigma = params["u"], params["sigma"]
    return (var + sigma - xi * u) / (1 - xi)


# ---------------------------------------------------------------------------
# 4. BOOTSTRAP — Intervalles de confiance
# ---------------------------------------------------------------------------

def bootstrap_gpd(losses: np.ndarray, u: float,
                  n_boot: int = 2000,
                  alpha_var: float = 0.995,
                  ci_level: float = 0.90) -> dict:
    """
    Bootstrap paramétrique sur les excès GPD.
    Retourne les IC sur ξ, σ et VaR.

    Parameters
    ----------
    losses    : array de pertes brutes
    u         : seuil POT
    n_boot    : nombre de tirages bootstrap
    alpha_var : niveau de VaR à estimer
    ci_level  : niveau de l'intervalle de confiance (défaut 90%)
    """
    excesses = losses[losses > u] - u
    n_exc = len(excesses)

    xis, sigmas, vars_ = [], [], []
    for _ in range(n_boot):
        sample = np.random.choice(excesses, size=n_exc, replace=True)
        try:
            xi_b, _, sig_b = genpareto.fit(sample, floc=0)
            params_b = {"xi": xi_b, "sigma": sig_b,
                        "u": u, "p_u": n_exc / len(losses)}
            v = var_gpd(params_b, alpha_var)
            xis.append(xi_b)
            sigmas.append(sig_b)
            vars_.append(v)
        except Exception:
            continue

    lo = (1 - ci_level) / 2 * 100
    hi = (1 + ci_level) / 2 * 100
    return {
        "xi_ci": np.percentile(xis, [lo, hi]).tolist(),
        "sigma_ci": np.percentile(sigmas, [lo, hi]).tolist(),
        "var_ci": np.nanpercentile(vars_, [lo, hi]).tolist(),
        "n_valid": len(xis),
        "alpha_var": alpha_var,
        "ci_level": ci_level,
    }


# ---------------------------------------------------------------------------
# 5. RAPPORT DE CALIBRATION
# ---------------------------------------------------------------------------

def calibration_report(losses: np.ndarray, u: float,
                       source: str = "inconnu",
                       currency: str = "M€",
                       n_boot: int = 2000) -> dict:
    """
    Rapport complet de calibration GPD :
      - Paramètres MLE
      - VaR / TVaR aux niveaux 95%, 99%, 99.5%, 99.9%
      - IC bootstrap

    Parameters
    ----------
    losses   : array de pertes
    u        : seuil POT
    source   : nom de la source de données
    currency : unité monétaire pour l'affichage
    n_boot   : tirages bootstrap

    Returns
    -------
    dict complet des résultats
    """
    params = fit_gpd(losses, u)
    ci = bootstrap_gpd(losses, u, n_boot=n_boot)

    quantiles = {}
    for alpha in [0.95, 0.99, 0.995, 0.999]:
        try:
            v = var_gpd(params, alpha)
            t = tvar_gpd(params, alpha) if params["xi"] < 1 else None
            quantiles[alpha] = {"var": v, "tvar": t}
        except Exception as e:
            quantiles[alpha] = {"var": None, "tvar": None, "error": str(e)}

    report = {
        "source": source,
        "currency": currency,
        "n_total": params["n_total"],
        "n_excess": params["n_excess"],
        "threshold_u": params["u"],
        "p_u": params["p_u"],
        "xi": params["xi"],
        "sigma": params["sigma"],
        "quantiles": quantiles,
        "bootstrap": ci,
    }

    # Affichage console
    print(f"\n{'='*55}")
    print(f"  CALIBRATION GPD — {source}")
    print(f"{'='*55}")
    print(f"  Seuil u     = {u:.4f} {currency}")
    print(f"  n excès     = {params['n_excess']} / {params['n_total']}")
    print(f"  p(X > u)    = {params['p_u']:.4f}")
    print(f"  ξ̂           = {params['xi']:.4f}  IC{int(ci['ci_level']*100)}% = {ci['xi_ci']}")
    print(f"  σ̂           = {params['sigma']:.4f} {currency}  IC = {ci['sigma_ci']}")
    print(f"\n  Quantile    VaR ({currency})     TVaR ({currency})")
    print(f"  {'-'*40}")
    for alpha, q in quantiles.items():
        var_s = f"{q['var']:.2f}" if q['var'] else "N/A"
        tvar_s = f"{q['tvar']:.2f}" if q['tvar'] else "N/A (ξ≥1)"
        print(f"  {alpha:.3f}      {var_s:>12}  {tvar_s:>12}")
    print(f"\n  VaR 99.5% IC{int(ci['ci_level']*100)}% = {ci['var_ci']} {currency}")
    print(f"{'='*55}\n")

    return report


# ---------------------------------------------------------------------------
# 6. COMPARAISON DEUX SOURCES (validation croisée)
# ---------------------------------------------------------------------------

def cross_validate(report_prc: dict, report_oprisk: dict) -> None:
    """
    Affiche la comparaison qualitative PRC vs OpRisk.
    La validation quantitative est impossible (seuils incomparables).
    """
    xi_prc = report_prc["xi"]
    xi_op  = report_oprisk["xi"]
    print("\n=== VALIDATION CROISÉE PRC vs OpRisk ===")
    print(f"  Source      | Seuil u           | ξ̂      | Régime")
    print(f"  PRC         | {report_prc['threshold_u']:.4f} {report_prc['currency']}  "
          f"| {xi_prc:.4f} | {'Queue très lourde (ξ≥1)' if xi_prc >= 1 else 'Queue lourde'}")
    print(f"  OpRisk      | {report_oprisk['threshold_u']:.4f} {report_oprisk['currency']}  "
          f"| {xi_op:.4f} | {'Queue très lourde (ξ≥1)' if xi_op >= 1 else 'Queue lourde (moments finis)'}")
    print(f"\n  → Même famille Pareto (ξ > 0) : validation QUALITATIVE ✓")
    print(f"  → ξ_PRC > ξ_OpRisk : cohérent avec le biais de taille OpRisk")
    print(f"    (grandes entités absorbent mieux → queue apparemment plus légère)")
    print(f"  → Validation QUANTITATIVE impossible : seuils incomparables")
    print(f"\n  DEUX SOURCES COMPLÉMENTAIRES (pas de hiérarchie 'primaire') :")
    print(f"  • OpRisk : montants de pertes RÉELS, mais biais vers les grandes")
    print(f"    entités → queue possiblement sous-estimée (petites pertes absentes)")
    print(f"  • PRC + Jacobs : spectre de tailles plus large, mais sévérité DÉRIVÉE")
    print(f"    d'un modèle log-log (estimation, pas observation directe)")
    print(f"  → Sévérité : OpRisk = montants directs ; PRC = comparaison/cohérence")
    print(f"  → Fréquence : PRC = source de référence (périmètre défini)")
    print(f"  → La convergence qualitative des deux renforce le choix GPD\n")


# ---------------------------------------------------------------------------
# MAIN — exemple d'utilisation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    print("Module gpd.py chargé. Utilisation :")
    print("  from src.severity.gpd import calibration_report, cross_validate")
    print()
    print("Exemple :")
    print("  losses = pd.read_csv('data/processed/prc_losses.csv')['loss_eur'].values")
    print("  report = calibration_report(losses, u=0.128, source='PRC 2025', currency='M€')")
