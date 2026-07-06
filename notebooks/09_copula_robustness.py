"""
notebooks/09_copula_robustness.py
-----------------------------------
Test de robustesse sur la FAMILLE de copule (section 5.4bis du mémoire).

Le mémoire justifie qualitativement le choix de la copule de Gumbel
(dépendance de queue supérieure) sans jamais tester quantitativement si un
autre choix de famille changerait matériellement le capital simulé. Ce script
comble ce trou en rejouant le pipeline officiel (scr_4_briques_report) sous
quatre familles de dépendance, chacune appariée sur le MÊME tau de Kendall
que la copule de Gumbel de référence (theta=1.8 en régime non-conforme,
theta=1.2 en régime conforme) pour isoler l'effet de la FORME fonctionnelle
de la dépendance, et non de son intensité :

  - gumbel     : référence du mémoire (dépendance de queue supérieure)
  - clayton    : rotée à 180° (dépendance de queue supérieure, forme différente)
  - frank      : AUCUNE dépendance de queue (cas de contraste)
  - student_t  : dépendance de queue symétrique haute/basse (df=4)

Ne nécessite AUCUNE donnée brute : le moteur simule à partir des paramètres
déjà calibrés dans src/utils/config.py (xi, sigma, lambda_ref, etc.).

Sortie : outputs/tables/results_copula_robustness.csv
         outputs/figures/copula_robustness.png

Usage : python notebooks/09_copula_robustness.py
"""

import os
import sys
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.aggregation.lda import scr_4_briques_report
from src.aggregation.copule import (
    clayton_tau, solve_clayton_theta,
    frank_tau, solve_frank_theta,
    rho_from_kendall_tau,
)

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_GREEN = "#16a34a"
BRAND_RED = "#dc2626"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

ALPHA = 0.995
N_SIM = 100_000
SOURCES = ["PRC", "OPRISK"]

GUMBEL_THETA_NC = 1.8
GUMBEL_THETA_C = 1.2

FAMILY_COLORS = {
    "gumbel": BRAND_BLUE,
    "clayton": BRAND_GREEN,
    "frank": BRAND_RED,
    "student_t": BRAND_ORANGE,
}


def kendall_tau_gumbel(theta: float) -> float:
    return 1.0 - 1.0 / theta


def build_family_params():
    """
    Pour chaque famille, calcule le paramètre natif (theta ou rho) reproduisant
    EXACTEMENT le même tau de Kendall que Gumbel, en régime non-conforme (NC)
    et conforme (C). Frank et Student-t sont appariés numériquement (pas de
    formule fermée pour Frank).
    """
    tau_nc = kendall_tau_gumbel(GUMBEL_THETA_NC)
    tau_c = kendall_tau_gumbel(GUMBEL_THETA_C)

    return {
        "gumbel": {
            "theta_nc": GUMBEL_THETA_NC, "theta_c": GUMBEL_THETA_C,
            "tau_nc": tau_nc, "tau_c": tau_c,
        },
        "clayton": {
            "theta_nc": solve_clayton_theta(tau_nc),
            "theta_c": solve_clayton_theta(tau_c),
            "tau_nc": tau_nc, "tau_c": tau_c,
        },
        "frank": {
            "theta_nc": solve_frank_theta(tau_nc),
            "theta_c": solve_frank_theta(tau_c),
            "tau_nc": tau_nc, "tau_c": tau_c,
        },
        "student_t": {
            "theta_nc": rho_from_kendall_tau(tau_nc),
            "theta_c": rho_from_kendall_tau(tau_c),
            "tau_nc": tau_nc, "tau_c": tau_c,
        },
    }


def main():
    families = build_family_params()

    print("=" * 78)
    print("  TEST DE ROBUSTESSE — FAMILLE DE COPULE (tau de Kendall apparié)")
    print("=" * 78)
    for fam, p in families.items():
        print(f"  {fam:10s} : theta_nc={p['theta_nc']:.4f}  theta_c={p['theta_c']:.4f}  "
              f"(tau_nc={p['tau_nc']:.4f}, tau_c={p['tau_c']:.4f})")

    rows = []
    for source in SOURCES:
        for fam, p in families.items():
            res = scr_4_briques_report(
                source=source, alpha=ALPHA, n_sim=N_SIM, dependence=fam,
                theta_nc=p["theta_nc"], theta_c=p["theta_c"], verbose=False,
            )
            scr_nc = res["scr_total"]
            delta = res["scr_aggravation"]
            total_mean = res["total"].mean()
            share_remediation = 100 * res["remediation"].mean() / total_mean
            share_prestataire = 100 * res["prestataire"].mean() / total_mean
            share_sanction = 100 * res["sanction"].mean() / total_mean

            rows.append({
                "source": source, "famille": fam,
                "tau_kendall_nc": p["tau_nc"], "theta_nc": p["theta_nc"],
                "var_995_non_conforme": scr_nc,
                "delta_dora": delta,
                "part_remediation_pct": share_remediation,
                "part_prestataire_pct": share_prestataire,
                "part_sanction_pct": share_sanction,
            })
            print(f"\n  [{source} / {fam}] VaR99.5% non-conforme = {scr_nc:>9.1f} M€ | "
                  f"Delta_DORA = {delta:>8.1f} M€ | "
                  f"remediation={share_remediation:.1f}% prestataire={share_prestataire:.1f}%")

    # --- Synthèse : écart relatif à Gumbel (référence du mémoire) ---
    print("\n" + "=" * 78)
    print("  ÉCART RELATIF À GUMBEL (référence du mémoire), par source")
    print("=" * 78)
    for source in SOURCES:
        ref = next(r for r in rows if r["source"] == source and r["famille"] == "gumbel")
        for r in rows:
            if r["source"] != source:
                continue
            ecart_var = 100 * (r["var_995_non_conforme"] - ref["var_995_non_conforme"]) / ref["var_995_non_conforme"]
            ecart_delta = 100 * (r["delta_dora"] - ref["delta_dora"]) / ref["delta_dora"]
            r["ecart_var_vs_gumbel_pct"] = ecart_var
            r["ecart_delta_vs_gumbel_pct"] = ecart_delta
            print(f"  {source:7s} {r['famille']:10s} : "
                  f"VaR {ecart_var:+6.1f}%   Delta_DORA {ecart_delta:+6.1f}%")

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "results_copula_robustness.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nCSV : {csv_path}")

    # --- Figure : VaR par famille x source ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "copula_robustness.png")

    fam_order = ["gumbel", "clayton", "frank", "student_t"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), sharey=False)
    for ax, source in zip(axes, SOURCES):
        vals = [next(r for r in rows if r["source"] == source and r["famille"] == f)["var_995_non_conforme"]
                for f in fam_order]
        colors = [FAMILY_COLORS[f] for f in fam_order]
        bars = ax.bar(fam_order, vals, color=colors, edgecolor="white", linewidth=0.5)
        ref_val = next(r for r in rows if r["source"] == source and r["famille"] == "gumbel")["var_995_non_conforme"]
        ax.axhline(ref_val, color=BRAND_DARK, linestyle="--", linewidth=1.2)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v, f"{v:,.0f}",
                    ha="center", va="bottom", fontsize=9)
        ax.set_title(f"Source {source}", fontsize=13, fontweight="bold")
        ax.set_ylabel("VaR 99,5% non-conforme (M€)", fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.suptitle("Robustesse du SCR à la famille de copule (tau de Kendall apparié à Gumbel)",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
