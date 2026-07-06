"""
notebooks/12_gpd_goodness_of_fit.py
--------------------------------------
Test d'adéquation formel de la calibration GPD sur OpRisk Global (in-sample).

Le choix du seuil POT (u = 20,03 M€, percentile 85) repose aujourd'hui sur
une lecture graphique (mean excess plot, section 2.7 ; diagnostic de
stabilité de ξ et Hill plot, section 3.3) — jamais sur un test statistique
formel. Ce script comble ce trou avec deux diagnostics quantitatifs
classiques en EVT :

  1. QQ-PLOT : quantiles empiriques des excès vs quantiles théoriques de la
     GPD(ξ̂, σ̂) ajustée — inspection visuelle rigoureuse de l'adéquation en
     queue, là où l'oeil est le moins fiable.
  2. TEST DE KOLMOGOROV-SMIRNOV sur la transformée intégrale de probabilité
     (PIT) : si le modèle est bien spécifié, G(excès_i; ξ̂, σ̂) doit suivre une
     loi Uniforme(0,1). Le test est reporté à titre indicatif : les
     paramètres étant estimés SUR LE MÊME échantillon que celui testé, la loi
     exacte de la statistique KS n'est pas celle du cas i.i.d. simple
     (paramètres connus a priori) — les p-values sont donc conservatrices, et
     interprétées comme un ordre de grandeur, non comme un test exact.

Usage : python notebooks/12_gpd_goodness_of_fit.py
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import genpareto, kstest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.severity.gpd import fit_gpd, bootstrap_gpd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

OPRISK_PATH = "data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx"
USD_EUR = 0.92


def load_oprisk(path: str) -> pd.DataFrame:
    """Identique à 01_oprisk_gpd_calibration.py::load_oprisk."""
    df = pd.read_excel(path, sheet_name="Datasets")
    cyber_cats = ["Systems Security", "Systems"]
    biz_cats = ["Business Disruption and System Failures"]

    df_cyber = df[
        (df["Sub Risk Category"].isin(cyber_cats) | df["Event Risk Category"].isin(biz_cats)) &
        (df["Industry Sector Name"].apply(lambda v: "Financial" in str(v) if pd.notna(v) else False))
    ].copy()

    df_cyber["loss_eur_M"] = pd.to_numeric(df_cyber["Loss Amount ($M)"], errors="coerce") * USD_EUR
    df_cyber["year"] = pd.to_datetime(df_cyber["First Year of Event"], errors="coerce").dt.year

    df_recent = df_cyber[
        (df_cyber["year"] >= 2000) & (df_cyber["loss_eur_M"] > 0)
    ].dropna(subset=["loss_eur_M"])
    return df_recent


def anderson_darling_uniformity(u: np.ndarray) -> float:
    """
    Statistique d'Anderson-Darling pour l'adéquation à Uniforme(0,1),
    calculée directement (scipy.stats.anderson ne supporte pas la loi
    uniforme). Formule standard (Anderson & Darling, 1952) :

        A^2 = -n - (1/n) * sum_{i=1}^{n} (2i-1) * [ln(u_(i)) + ln(1-u_(n+1-i))]

    où u_(i) sont les valeurs triées. Valeur critique usuelle (paramètres
    connus a priori) à 5% : 2.492 (Stephens, 1974) — donnée ici à titre de
    repère, avec la réserve méthodologique mentionnée en tête de fichier.
    """
    n = len(u)
    u_sorted = np.sort(np.clip(u, 1e-12, 1 - 1e-12))
    i = np.arange(1, n + 1)
    s = np.sum((2 * i - 1) * (np.log(u_sorted) + np.log(1 - u_sorted[::-1])))
    return -n - s / n


def main():
    if not os.path.exists(OPRISK_PATH):
        print(f"Fichier non trouvé : {OPRISK_PATH}")
        return

    df = load_oprisk(OPRISK_PATH)
    losses = df["loss_eur_M"].values

    u = float(np.percentile(losses, 85))
    params = fit_gpd(losses, u)
    ci = bootstrap_gpd(losses, u, n_boot=2000)
    xi, sigma = params["xi"], params["sigma"]
    excesses = losses[losses > u] - u
    n = params["n_excess"]

    print("=" * 74)
    print("  TEST D'ADÉQUATION FORMEL — GPD sur OpRisk Cyber×Finance")
    print("=" * 74)
    print(f"  n total = {params['n_total']} | seuil u = {u:.2f} M€ | n excès = {n}")
    print(f"  ξ̂ = {xi:.4f}  IC90% = {ci['xi_ci']}")
    print(f"  σ̂ = {sigma:.2f} M€  IC90% = {ci['sigma_ci']}")

    # --- PIT + KS ---
    pit = genpareto.cdf(excesses, c=xi, scale=sigma)
    ks_stat, ks_p = kstest(pit, "uniform")
    print(f"\n  --- Test de Kolmogorov-Smirnov sur la PIT ---")
    print(f"  statistique KS = {ks_stat:.4f}  |  p-value (indicative) = {ks_p:.4f}")
    verdict_ks = "NON REJETÉE" if ks_p > 0.05 else "REJETÉE"
    print(f"  H0 (les excès suivent GPD(ξ̂,σ̂)) : {verdict_ks} au seuil 5% (lecture indicative)")

    # --- Anderson-Darling ---
    ad_stat = anderson_darling_uniformity(pit)
    ad_crit_5pct = 2.492
    print(f"\n  --- Statistique d'Anderson-Darling (adéquation à U[0,1] de la PIT) ---")
    print(f"  A^2 = {ad_stat:.4f}  (valeur critique usuelle à 5% ≈ {ad_crit_5pct}, à titre de repère)")
    verdict_ad = "en-deçà" if ad_stat < ad_crit_5pct else "au-delà"
    print(f"  A^2 est {verdict_ad} du repère critique : lecture cohérente avec le test KS ci-dessus")

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "results_gpd_goodness_of_fit.csv")
    pd.DataFrame([{
        "u": u, "n_total": params["n_total"], "n_excess": n,
        "xi": xi, "sigma": sigma,
        "xi_ic90_lo": ci["xi_ci"][0], "xi_ic90_hi": ci["xi_ci"][1],
        "ks_stat": ks_stat, "ks_pvalue": ks_p,
        "ad_stat": ad_stat, "ad_crit_5pct_indicatif": ad_crit_5pct,
    }]).to_csv(csv_path, index=False)
    print(f"\nCSV : {csv_path}")

    # --- Figure : QQ-plot + histogramme PIT ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "gpd_goodness_of_fit.png")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

    exc_sorted = np.sort(excesses)
    plot_pos = (np.arange(1, n + 1) - 0.5) / n
    theo_q = genpareto.ppf(plot_pos, c=xi, scale=sigma)
    ax1.scatter(theo_q, exc_sorted, color=BRAND_BLUE, s=28, alpha=0.8, edgecolor="white")
    lims = [0, max(theo_q.max(), exc_sorted.max()) * 1.05]
    ax1.plot(lims, lims, color=BRAND_DARK, linestyle="--", linewidth=1.2, label="Adéquation parfaite (y=x)")
    ax1.set_xlabel("Quantiles théoriques GPD(ξ̂, σ̂) (M€)", fontsize=10)
    ax1.set_ylabel("Quantiles empiriques des excès (M€)", fontsize=10)
    ax1.set_title("QQ-plot — excès OpRisk vs GPD ajustée", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2.hist(pit, bins=12, color=BRAND_ORANGE, edgecolor="white", alpha=0.85,
             density=True, label=f"PIT empirique (n={n})")
    ax2.axhline(1.0, color=BRAND_DARK, linestyle="--", linewidth=1.2,
                label="Densité U[0,1] attendue")
    ax2.set_xlabel("G(excès ; ξ̂, σ̂) — transformée intégrale de probabilité", fontsize=10)
    ax2.set_ylabel("Densité", fontsize=10)
    ax2.set_title(f"KS={ks_stat:.3f} (p≈{ks_p:.2f})  |  A²={ad_stat:.2f}",
                  fontsize=12, fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
