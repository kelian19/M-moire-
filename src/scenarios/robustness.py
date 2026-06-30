"""
scenarios/robustness.py
------------------------
Exécute le LDA en PARALLÈLE sur les deux sources de sévérité disponibles
(PRC + Jacobs, et SAS OpRisk Global) pour exposer la sensibilité du
SCR_DORA au choix de source — une dimension d'incertitude à part entière.

Logique :
  - La FRÉQUENCE est toujours PRC (+ multiplicateurs Hackmageddon si scénario DORA)
  - La SÉVÉRITÉ tourne deux fois : une fois avec les params PRC/Jacobs,
    une fois avec les params OpRisk
  - Comparaison des deux SCR obtenus → fourchette de robustesse "source"

Cette approche répond directement à la consigne de Caroline Hillairet :
ne jamais présenter un SCR ponctuel comme s'il était connu avec certitude.
Ici, l'écart entre les deux sources EST une partie du message.
"""

import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.scenarios.delta_dora import compute_delta_dora, simulate_lda_vectorized, empirical_var
from src.frequency.negbin import compute_lambda_scenario
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA


def _to_gpd_params(source_dict: dict, dispersion: float = None) -> dict:
    """Convertit un dict config (PRC ou OPRISK) au format attendu par le LDA."""
    return {
        "xi": source_dict["xi"],
        "sigma": source_dict["sigma_eur"],
        "u": source_dict["seuil_u_eur"],
        "p_u": source_dict["p_u"],
        "dispersion_factor": dispersion or FREQUENCY.get("dispersion_factor", 9.2),
    }


def _severity_cap_for(source_name: str) -> float:
    """
    Retourne le plafond de sévérité applicable selon la source.
    OBLIGATOIRE pour PRC (ξ=1.30 >= 1, espérance infinie sans plafond).
    Référence : SCR_DORA['cap_eur'] = 40 M€, ancré sur la capacité de
    réassurance cyber (cf. config.py).
    """
    if source_name == "PRC":
        return SCR_DORA.get("cap_eur", 40.0)
    return None  # OpRisk : ξ=0.60 < 1, espérance finie, pas de cap nécessaire


# ---------------------------------------------------------------------------
# 1. SCR SOUS UNE SOURCE DE SÉVÉRITÉ DONNÉE
# ---------------------------------------------------------------------------

def scr_under_source(source_name: str,
                      lambda_annual: float = None,
                      alpha: float = 0.995,
                      n_sim: int = 1_000_000,
                      seed: int = 42) -> dict:
    """
    Calcule le SCR (VaR_alpha) sous une source de sévérité donnée,
    en utilisant la fréquence ET la sévérité COHÉRENTES de cette même source.

    ⚠️ IMPORTANT : λ et p_u doivent provenir de la MÊME population.
    Mélanger le λ de la PRC avec le p_u d'OpRisk (ou inversement) est
    méthodologiquement incorrect : p_u est calibré sur le périmètre propre
    à chaque source (seuils différents, populations différentes — OpRisk
    est biaisée vers les grandes entités financières). Cette fonction
    utilise par défaut le λ propre à la source pour éviter cette erreur.

    Parameters
    ----------
    source_name   : 'PRC' ou 'OPRISK'
    lambda_annual : fréquence annuelle. Si None, utilise la fréquence
                    PROPRE à la source (PRC: FREQUENCY['lambda_ref'],
                    OpRisk: n_incidents / durée d'observation).
                    Ne forcer une valeur externe qu'en connaissance de cause
                    (cf. avertissement ci-dessus).
    alpha         : niveau VaR (défaut 99.5% Solvabilité 2)
    n_sim         : simulations Monte Carlo
    seed          : graine

    Returns
    -------
    dict : scr, source, params utilisés
    """
    source_map = {"PRC": PRC, "OPRISK": OPRISK}
    if source_name not in source_map:
        raise ValueError(f"source_name doit être 'PRC' ou 'OPRISK', reçu '{source_name}'")

    # Fréquence propre à la source si non fournie explicitement
    if lambda_annual is None:
        if source_name == "PRC":
            lambda_annual = FREQUENCY["lambda_ref"]
        else:  # OPRISK : n_incidents observés / durée de la fenêtre (2000-2026 = 27 ans)
            lambda_annual = OPRISK["n_incidents"] / 27

    gpd_params = _to_gpd_params(source_map[source_name])
    cap = _severity_cap_for(source_name)
    losses = simulate_lda_vectorized(lambda_annual, gpd_params, n_sim, seed,
                                      severity_cap=cap)
    scr = empirical_var(losses, alpha)

    return {
        "source": source_name,
        "scr": scr,
        "lambda_annual": lambda_annual,
        "alpha": alpha,
        "xi": gpd_params["xi"],
        "sigma": gpd_params["sigma"],
        "severity_cap": cap,
        "losses": losses,
    }


# ---------------------------------------------------------------------------
# 2. COMPARAISON PRC vs OPRISK — SCÉNARIO UNIQUE
# ---------------------------------------------------------------------------

def compare_sources(alpha: float = 0.995,
                     n_sim: int = 1_000_000,
                     scenario_label: str = "",
                     dora_multiplier: float = 1.0) -> dict:
    """
    Calcule le SCR sous PRC et sous OpRisk, CHACUN avec sa propre
    fréquence et sévérité cohérentes (pas de λ partagé entre sources,
    cf. avertissement dans scr_under_source).

    Parameters
    ----------
    dora_multiplier : multiplicateur de fréquence à appliquer aux DEUX
                       sources de façon identique (ex. issu d'un scénario
                       DORA S1/S2 calculé sur la PRC). Permet de comparer
                       les sources sous un même scénario de conformité,
                       sans mélanger leurs p_u respectifs.
    """
    print(f"\n{'='*60}")
    title = f"COMPARAISON SOURCES — {scenario_label}" if scenario_label else "COMPARAISON SOURCES"
    print(f"  {title}")
    print(f"{'='*60}")

    lam_prc = FREQUENCY["lambda_ref"] * dora_multiplier
    lam_op = (OPRISK["n_incidents"] / 27) * dora_multiplier

    print(f"  Multiplicateur DORA appliqué : ×{dora_multiplier:.2f}")
    print(f"  λ_PRC    = {lam_prc:.1f} incidents/an (population PRC)")
    print(f"  λ_OpRisk = {lam_op:.1f} incidents/an (population OpRisk, ~22/an de base)")

    res_prc = scr_under_source("PRC", lam_prc, alpha, n_sim, seed=1)
    res_op  = scr_under_source("OPRISK", lam_op, alpha, n_sim, seed=2)

    scr_min = min(res_prc["scr"], res_op["scr"])
    scr_max = max(res_prc["scr"], res_op["scr"])
    ratio = scr_max / scr_min if scr_min > 0 else None

    print(f"\n  Source      ξ̂      Cap (M€)   SCR (VaR {alpha*100:.1f}%)")
    print(f"  {'-'*48}")
    cap_prc = res_prc['severity_cap'] if res_prc['severity_cap'] else '—'
    cap_op = res_op['severity_cap'] if res_op['severity_cap'] else '—'
    print(f"  PRC      {res_prc['xi']:.4f}    {str(cap_prc):>8s}   {res_prc['scr']:>10.1f} M€")
    print(f"  OpRisk   {res_op['xi']:.4f}    {str(cap_op):>8s}   {res_op['scr']:>10.1f} M€")
    print(f"\n  Fourchette de robustesse (source) : [{scr_min:.1f}, {scr_max:.1f}] M€")
    print(f"  Ratio max/min : ×{ratio:.2f}")
    print(f"  → Cette fourchette s'ajoute à l'incertitude de paramètre (bootstrap)")
    print(f"    et à l'incertitude de scénario DORA (S0/S1/S2).")

    return {
        "scenario": scenario_label,
        "lambda_prc": lam_prc,
        "lambda_oprisk": lam_op,
        "scr_prc": res_prc["scr"],
        "scr_oprisk": res_op["scr"],
        "scr_min": scr_min,
        "scr_max": scr_max,
        "ratio": ratio,
    }


# ---------------------------------------------------------------------------
# 3. COMPARAISON COMPLÈTE — TOUS LES SCÉNARIOS DORA × DEUX SOURCES
# ---------------------------------------------------------------------------

def full_robustness_grid(lambda_ref: float = None,
                          alpha: float = 0.995,
                          n_sim: int = 500_000) -> pd.DataFrame:
    """
    Grille complète : 3 scénarios DORA (S0/S1/S2) × 2 sources sévérité (PRC/OpRisk).
    Produit 6 SCR, exposant à la fois l'incertitude de conformité et de source.

    C'est le tableau central pour le mémoire : il montre que le SCR_DORA
    n'est jamais un nombre, mais une grille de résultats selon les hypothèses.
    """
    lambda_ref = lambda_ref or FREQUENCY["lambda_ref"]
    scenarios = ["S0_conforme", "S1_partiel", "S2_non_conforme"]
    sources = ["PRC", "OPRISK"]

    rows = []
    print(f"\n{'='*70}")
    print(f"  GRILLE DE ROBUSTESSE COMPLÈTE — {len(scenarios)} scénarios × {len(sources)} sources")
    print(f"{'='*70}")

    for sc in scenarios:
        sc_res = compute_lambda_scenario(lambda_ref, sc)
        lam = sc_res["lambda_global"]
        for src in sources:
            res = scr_under_source(src, lam, alpha, n_sim, seed=hash((sc, src)) % 1000)
            rows.append({
                "Scénario": sc,
                "Source": src,
                "λ": lam,
                "SCR (M€)": res["scr"],
            })

    df = pd.DataFrame(rows)
    pivot = df.pivot(index="Scénario", columns="Source", values="SCR (M€)")
    pivot["Δ (Source)"] = pivot["OPRISK"] - pivot["PRC"]
    pivot["Ratio max/min"] = pivot[["PRC", "OPRISK"]].max(axis=1) / pivot[["PRC", "OPRISK"]].min(axis=1)

    print(f"\n{pivot.round(1).to_string()}")

    print(f"\n  Δ_DORA selon la source de sévérité :")
    for src in sources:
        s0 = pivot.loc["S0_conforme", src]
        s2 = pivot.loc["S2_non_conforme", src]
        print(f"    {src:8s} : Δ_DORA (S2-S0) = {s2-s0:.1f} M€")

    print(f"\n  → Le SCR_DORA varie selon scénario DE CONFORMITÉ ET selon source")
    print(f"     DE SÉVÉRITÉ. C'est cette double incertitude, assumée et quantifiée,")
    print(f"     qui constitue le résultat central du mémoire.")

    return df, pivot


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from src.utils.config import FREQUENCY

    print("Module robustness.py — exemple d'utilisation")
    print()

    # Comparaison simple sur le scénario de référence
    compare_sources(scenario_label="S0_conforme (référence)",
                    n_sim=200_000)

    # Grille complète (plus long)
    # df, pivot = full_robustness_grid(n_sim=200_000)
