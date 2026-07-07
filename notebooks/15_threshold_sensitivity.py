"""
15_threshold_sensitivity.py
---------------------------
DIAGNOSTIC DE CALIBRATION : stabilité du seuil POT (Piste 2).

Le seuil POT $u$ est choisi au percentile 85 par lecture graphique (mean excess
plot + Hill plot). Ce script quantifie la SENSIBILITÉ des estimateurs GPD
$(\\hat\\xi,\\hat\\sigma)$ et de la VaR 99,5 % au choix du seuil, pour les deux
sources (OpRisk et PRC/Jacobs), sur une grille de percentiles. Une queue GPD
bien spécifiée doit présenter un $\\hat\\xi$ ~stable~ sur un plateau de seuils.

Sorties :
  outputs/tables/results_threshold_sensitivity.csv
  outputs/figures/threshold_sensitivity.png

Nécessite les deux fichiers bruts (SAS OpRisk + PRC csv).
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.severity.gpd import fit_gpd, var_gpd
from src.severity.prc_analysis import load_prc, jacobs_severity_eur_m

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

OPRISK_PATH = "data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx"
PRC_PATH = "data/raw/Data_Breach_Chronology.csv"
USD_EUR = 0.92
PERCENTILES = [80, 82.5, 85, 87.5, 90]
ALPHA = 0.995


def load_oprisk_losses(path):
    df = pd.read_excel(path, sheet_name="Datasets")
    cyber = ["Systems Security", "Systems"]
    biz = ["Business Disruption and System Failures"]
    d = df[(df["Sub Risk Category"].isin(cyber) | df["Event Risk Category"].isin(biz)) &
           (df["Industry Sector Name"].apply(lambda v: "Financial" in str(v) if pd.notna(v) else False))].copy()
    d["loss_eur_M"] = pd.to_numeric(d["Loss Amount ($M)"], errors="coerce") * USD_EUR
    losses = d["loss_eur_M"].dropna()
    return losses[losses > 0].values


def sensitivity_table(losses, source):
    rows = []
    for p in PERCENTILES:
        u = float(np.percentile(losses, p))
        try:
            params = fit_gpd(losses, u)
            var = var_gpd(params, ALPHA)
            rows.append(dict(source=source, percentile=p, u=u,
                             n_excess=params["n_excess"], xi=params["xi"],
                             sigma=params["sigma"], var_995=var))
        except ValueError as e:
            rows.append(dict(source=source, percentile=p, u=u, n_excess=np.nan,
                             xi=np.nan, sigma=np.nan, var_995=np.nan))
    return pd.DataFrame(rows)


def main():
    tables = []
    if os.path.exists(OPRISK_PATH):
        opr = load_oprisk_losses(OPRISK_PATH)
        tables.append(sensitivity_table(opr, "OpRisk"))
        print(f"OpRisk : {len(opr)} pertes chargées")
    else:
        print(f"OpRisk sauté (absent) : {OPRISK_PATH}")

    if os.path.exists(PRC_PATH):
        df = load_prc(PRC_PATH)
        sev = jacobs_severity_eur_m(df["total_affected"].values)
        tables.append(sensitivity_table(sev, "PRC"))
        print(f"PRC : {len(sev)} sévérités dérivées")
    else:
        print(f"PRC sauté (absent) : {PRC_PATH}")

    if not tables:
        print("Aucune source disponible.")
        return

    tab = pd.concat(tables, ignore_index=True)
    print("\n" + "=" * 78)
    print("  SENSIBILITÉ AU SEUIL POT — xi, sigma, VaR 99,5 % par percentile")
    print("=" * 78)
    for src, g in tab.groupby("source"):
        print(f"\n  {src}")
        print(f"  {'pct':>5} {'u (M€)':>10} {'N_u':>6} {'xi':>8} {'sigma':>10} {'VaR99.5':>10}")
        for _, r in g.iterrows():
            print(f"  {r['percentile']:>5} {r['u']:>10.3f} {r['n_excess']:>6.0f} "
                  f"{r['xi']:>8.3f} {r['sigma']:>10.3f} {r['var_995']:>10.1f}")

    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    tab.to_csv(os.path.join(out_dir, "results_threshold_sensitivity.csv"), index=False)
    print(f"\nCSV : {os.path.join(out_dir, 'results_threshold_sensitivity.csv')}")

    # --- Figure : xi et VaR normalisée vs percentile, par source ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    colors = {"OpRisk": BRAND_BLUE, "PRC": BRAND_ORANGE}
    for src, g in tab.groupby("source"):
        ax1.plot(g["percentile"], g["xi"], "o-", color=colors.get(src, BRAND_DARK),
                 lw=2, markersize=6, label=src)
        ref = g[g["percentile"] == 85]["var_995"].values
        norm = g["var_995"] / ref[0] if len(ref) and ref[0] else g["var_995"]
        ax2.plot(g["percentile"], norm, "s-", color=colors.get(src, BRAND_DARK),
                 lw=2, markersize=6, label=src)
    ax1.axvline(85, color=BRAND_DARK, ls="--", lw=1, alpha=0.5, label="seuil retenu (pct 85)")
    ax1.set_xlabel("Percentile du seuil $u$", fontsize=11)
    ax1.set_ylabel(r"Indice de queue $\hat\xi$", fontsize=11)
    ax1.set_title("Stabilité de l'indice de queue selon le seuil POT", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9); ax1.grid(alpha=0.3)
    ax2.axvline(85, color=BRAND_DARK, ls="--", lw=1, alpha=0.5)
    ax2.axhline(1.0, color=BRAND_DARK, ls=":", lw=1, alpha=0.5)
    ax2.set_xlabel("Percentile du seuil $u$", fontsize=11)
    ax2.set_ylabel(r"VaR $99{,}5\%$ (normalisée au seuil retenu)", fontsize=11)
    ax2.set_title("Sensibilité de la VaR au choix du seuil", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=9); ax2.grid(alpha=0.3)
    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "threshold_sensitivity.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
