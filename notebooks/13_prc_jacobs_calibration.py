"""
notebooks/13_prc_jacobs_calibration.py
------------------------------------------
Première calibration GPD réalisée directement sur les données PRC brutes
(Data_Breach_Chronology.xlsx), via la conversion Jacobs (2014) records → $.

Contexte : les valeurs ξ=1.30 / u=0.128 M€ / σ=0.257 M€ présentes jusqu'ici
dans config.py provenaient d'une référence externe, jamais recalculées sur ce
fichier brut dans ce projet (n_records=None l'attestait). Une validation
empirique (log10 vs ln, coefficients Jacobs 2014 vs extension 2018, sur
plusieurs périodes et seuils) a montré qu'aucune combinaison ne reproduit
exactement ces 3 valeurs — signe qu'elles ont été transcrites d'ailleurs.
Ce notebook fournit une calibration FRAÎCHE, tracée de bout en bout sur les
données réelles, qui remplace ces valeurs externes dans config.py.

Choix méthodologiques (voir src/severity/prc_analysis.py pour la
justification détaillée) :
  - Formule : ln(L_usd) = 7.68 + 0.76*ln(X)  (Jacobs 2014, base naturelle)
  - Période : 2019-2025 (cohérent avec le libellé déjà présent dans config.py)
  - Seuil : percentile 85 de la sévérité dérivée (p_u=0.15, même convention
    que OpRisk et que l'ancienne valeur PRC)

Usage : python notebooks/13_prc_jacobs_calibration.py
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.severity.gpd import mean_excess, calibration_report, hill_estimator
from src.severity.prc_analysis import load_prc, jacobs_severity_eur_m, JACOBS_A, JACOBS_B

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

PRC_PATH = "data/raw/Data_Breach_Chronology.csv"


def plot_mean_excess(severities: np.ndarray, u_retained: float, save_path: str):
    thresholds = [np.percentile(severities, p) for p in range(50, 96, 2)]
    mep = mean_excess(severities, thresholds)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(mep["u"], mep["e_u"], "o-", color=BRAND_BLUE, linewidth=2,
            markersize=5, label="e(u) = E[X-u | X>u]")
    ax.axvline(u_retained, color=BRAND_ORANGE, linestyle="--", linewidth=1.5,
               label=f"Seuil retenu u = {u_retained:.3f} M€ (pct 85%)")
    ax.set_xlabel("Seuil u (M€)", fontsize=11)
    ax.set_ylabel("Excès moyen e(u) (M€)", fontsize=11)
    ax.set_title("Mean Excess Plot — PRC (sévérité dérivée Jacobs)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure sauvegardée : {save_path}")


def plot_xi_stability(severities: np.ndarray, u_retained: float, save_path: str):
    from scipy.stats import genpareto

    pcts = range(60, 95, 2)
    data = []
    for p in pcts:
        u = np.percentile(severities, p)
        exc = severities[severities > u] - u
        if len(exc) < 20:
            continue
        xi, _, _ = genpareto.fit(exc, floc=0)
        data.append({"pct": p, "u": u, "xi": xi, "n": len(exc)})

    df = pd.DataFrame(data)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(df["u"], df["xi"], "o-", color=BRAND_BLUE, linewidth=2, markersize=5)
    ax1.axhline(1.0, color="#dc2626", linestyle="--", alpha=0.7, label="ξ = 1 (E[X] = ∞)")
    ax1.axvline(u_retained, color=BRAND_ORANGE, linestyle="--", label=f"u retenu = {u_retained:.3f} M€")
    ax1.set_xlabel("Seuil u (M€)"); ax1.set_ylabel("ξ̂")
    ax1.set_title("Stabilité de ξ̂ vs seuil u"); ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3)

    ax2.plot(df["u"], df["n"], "s-", color=BRAND_DARK, linewidth=2, markersize=5)
    ax2.axhline(30, color="#dc2626", linestyle="--", alpha=0.7, label="n minimum = 30")
    ax2.set_xlabel("Seuil u (M€)"); ax2.set_ylabel("Nombre d'excès")
    ax2.set_title("Nombre d'excès vs seuil u"); ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

    plt.suptitle("Diagnostic GPD — PRC (sévérité dérivée Jacobs)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure sauvegardée : {save_path}")


def main():
    if not os.path.exists(PRC_PATH):
        print(f"Fichier non trouvé : {PRC_PATH}")
        return

    df = load_prc(PRC_PATH)
    severities = jacobs_severity_eur_m(df["total_affected"].values)

    print(f"\nFormule appliquée : ln(L_usd) = {JACOBS_A} + {JACOBS_B}*ln(X)")
    print(f"Sévérité dérivée (M€) : médiane={np.median(severities):.4f} | "
          f"P90={np.percentile(severities, 90):.4f} | max={severities.max():.1f}")

    u = float(np.percentile(severities, 85))

    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    plot_mean_excess(severities, u, os.path.join(fig_dir, "mean_excess_prc.png"))
    plot_xi_stability(severities, u, os.path.join(fig_dir, "diagnostic_gpd_prc.png"))

    report = calibration_report(severities, u, source="PRC 2019-2025 (Jacobs)",
                                currency="M€", n_boot=2000)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "results_prc_jacobs_calibration.csv")
    pd.DataFrame([{
        "n_total": report["n_total"], "n_excess": report["n_excess"],
        "u": report["threshold_u"], "p_u": report["p_u"],
        "xi": report["xi"], "sigma": report["sigma"],
        "xi_ic90_lo": report["bootstrap"]["xi_ci"][0],
        "xi_ic90_hi": report["bootstrap"]["xi_ci"][1],
        "sigma_ic90_lo": report["bootstrap"]["sigma_ci"][0],
        "sigma_ic90_hi": report["bootstrap"]["sigma_ci"][1],
        "var_995": report["quantiles"][0.995]["var"],
        "var_995_ic90_lo": report["bootstrap"]["var_ci"][0],
        "var_995_ic90_hi": report["bootstrap"]["var_ci"][1],
        "tvar_99": report["quantiles"][0.99]["tvar"],
    }]).to_csv(csv_path, index=False)
    print(f"CSV : {csv_path}")


if __name__ == "__main__":
    main()
