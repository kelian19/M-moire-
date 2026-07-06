"""
notebooks/10_mc_convergence.py
--------------------------------
Diagnostic de convergence Monte Carlo (section 5.4bis du mémoire).

Le mémoire ne documente nulle part le nombre de tirages nécessaire à la
stabilité de la VaR 99.5% rapportée : toute la largeur d'intervalle discutée
(bootstrap, sensibilité) est de l'incertitude de PARAMÈTRE, jamais de
l'erreur d'ÉCHANTILLONNAGE de la simulation elle-même. Ce script sépare les
deux : pour une grille croissante de n_sim (nombre d'années simulées), on
répète l'estimation de la VaR 99.5% sous plusieurs graines indépendantes et
on mesure la dispersion résiduelle — l'erreur Monte Carlo pure, à paramètres
figés.

Ne nécessite AUCUNE donnée brute : simulation paramétrique pure à partir des
calibrations déjà fixées dans src/utils/config.py.

Sortie : outputs/tables/results_mc_convergence.csv
         outputs/figures/mc_convergence.png

Usage : python notebooks/10_mc_convergence.py
"""

import os
import sys
import csv
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.aggregation.lda import simulate_year_3_briques
from src.frequency.negbin import compute_lambda_scenario
from src.compliance.latent import pcd_conditional, ANCHORED_PARAMS, PROFILS_TYPES
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

ALPHA = 0.995
SOURCE_COLORS = {"PRC": BRAND_BLUE, "OPRISK": BRAND_ORANGE}

# (n_sim, nombre de répétitions indépendantes) — moins de répétitions aux
# grandes tailles, où la variance Monte Carlo est de toute façon déjà faible.
GRID = [
    (1_000, 40),
    (3_000, 30),
    (10_000, 20),
    (30_000, 12),
    (100_000, 8),
    (300_000, 5),
]


def state_non_conforme(source: str):
    """
    Reproduit exactement l'état NON-CONFORME de scr_4_briques_report
    (S2_non_conforme, profil médian, θ=0) : mêmes paramètres, pour que la
    VaR de référence soit directement comparable aux résultats déjà publiés
    dans le mémoire (section 5.1).
    """
    source_map = {"PRC": PRC, "OPRISK": OPRISK}
    src = source_map[source]
    lambda_ref = FREQUENCY["lambda_ref"] if source == "PRC" else OPRISK["n_incidents"] / OPRISK["n_years"]

    severity_params = {
        "xi": src["xi"], "sigma": src["sigma_eur"], "u": src["seuil_u_eur"],
        "p_u": src["p_u"], "dispersion_factor": FREQUENCY["dispersion_factor"],
        "severity_cap": SCR_DORA.get("cap_eur", 40.0) if source == "PRC" else None,
    }
    sc_nc = compute_lambda_scenario(lambda_ref, "S2_non_conforme", mode="center")
    lam_nc = sc_nc["lambda_global"]
    pcd_nc = pcd_conditional(PROFILS_TYPES["median"], 0.0, ANCHORED_PARAMS)
    return lam_nc, severity_params, pcd_nc


def var_at(source: str, n_sim: int, seed: int) -> float:
    lam, sev, pcd = state_non_conforme(source)
    sim = simulate_year_3_briques(
        lambda_annual=lam, severity_params=sev, pcd_sanction=pcd,
        n_sim=n_sim, dependence="gumbel", theta=1.8, seed=seed,
    )
    return float(np.quantile(sim["total"], ALPHA))


def main():
    rows = []
    t0 = time.time()
    for source in ["PRC", "OPRISK"]:
        print(f"\n{'='*70}\n  CONVERGENCE MONTE CARLO — {source}\n{'='*70}")
        for n_sim, n_rep in GRID:
            vars_ = [var_at(source, n_sim, seed=1000 * n_sim + r) for r in range(n_rep)]
            mean_v = float(np.mean(vars_))
            std_v = float(np.std(vars_, ddof=1))
            cv_pct = 100 * std_v / mean_v
            rows.append({
                "source": source, "n_sim": n_sim, "n_rep": n_rep,
                "var_mean": mean_v, "var_std": std_v, "cv_pct": cv_pct,
                "var_min": float(np.min(vars_)), "var_max": float(np.max(vars_)),
            })
            print(f"  n_sim={n_sim:>7,} (x{n_rep:>2} runs) : "
                  f"VaR moyenne = {mean_v:>9.1f} M€  |  écart-type MC = {std_v:>7.1f} M€  "
                  f"(CV = {cv_pct:>5.2f}%)")

    print(f"\nTemps total : {time.time()-t0:.1f}s")

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "results_mc_convergence.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"CSV : {csv_path}")

    # --- Figure : deux panneaux (PRC, OpRisk), CV% vs n_sim (log-x) ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "mc_convergence.png")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, source in zip(axes, ["PRC", "OPRISK"]):
        sub = [r for r in rows if r["source"] == source]
        n_vals = [r["n_sim"] for r in sub]
        means = [r["var_mean"] for r in sub]
        lo = [r["var_min"] for r in sub]
        hi = [r["var_max"] for r in sub]
        color = SOURCE_COLORS[source]
        ax.plot(n_vals, means, "-o", color=color, linewidth=2, markersize=5,
                label="VaR 99,5% moyenne (sur répétitions)")
        ax.fill_between(n_vals, lo, hi, color=color, alpha=0.2, label="min–max sur répétitions")
        ax.axhline(means[-1], color=BRAND_DARK, linestyle="--", linewidth=1,
                   label=f"Référence grande taille ({n_vals[-1]:,})")
        ax.set_xscale("log")
        ax.set_xlabel("Nombre d'années simulées (n_sim, échelle log)", fontsize=10)
        ax.set_ylabel("VaR 99,5% (M€)", fontsize=10)
        ax.set_title(f"Source {source}", fontsize=13, fontweight="bold")
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
        ax.legend(fontsize=8, loc="best")

    fig.suptitle("Convergence Monte Carlo de la VaR 99,5% (erreur d'échantillonnage pure, "
                 "paramètres figés)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
