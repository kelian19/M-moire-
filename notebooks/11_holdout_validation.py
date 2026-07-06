"""
notebooks/11_holdout_validation.py
-------------------------------------
Validation par découpage temporel (holdout) de la calibration GPD OpRisk.

Le mémoire écarte la validation out-of-sample du Δ_DORA en l'absence
d'historique de crise DORA (section 5.4, "Validation et perspectives de
robustesse") — limite réelle et non contournable. Mais rien n'empêche de
valider le modèle de SÉVÉRITÉ seul, en dehors de tout contexte DORA : caler
la GPD sur les incidents OpRisk antérieurs à une date de coupure, et vérifier
si elle décrit correctement la sévérité des incidents postérieurs, non vus
lors de la calibration.

Deux vérifications :
  1. STABILITÉ TEMPORELLE DE ξ : la GPD est recalibrée indépendamment sur la
     période d'entraînement et sur la période de test ; on compare les ξ̂
     obtenus (doivent être statistiquement compatibles pour que le modèle
     soit jugé stable dans le temps).
  2. ADÉQUATION HORS ÉCHANTILLON : les excès de la période de TEST au-delà du
     seuil retenu en ENTRAÎNEMENT sont confrontés à la loi GPD(ξ_train,
     σ_train) via un test de Kolmogorov-Smirnov sur la transformée intégrale
     de probabilité (PIT) — la vraie question actuarielle : le modèle calé
     sur le passé aurait-il correctement anticipé la sévérité future ?

Usage : python notebooks/11_holdout_validation.py
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

from src.severity.gpd import fit_gpd, bootstrap_gpd, var_gpd

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
CUTOFF_YEAR = 2017
USD_EUR = 0.92


def load_oprisk(path: str) -> pd.DataFrame:
    """Identique à 01_oprisk_gpd_calibration.py::load_oprisk (même périmètre,
    même conversion EUR, même filtre >= 2000), pour une stricte comparabilité
    avec la calibration officielle."""
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


def main():
    if not os.path.exists(OPRISK_PATH):
        print(f"Fichier non trouvé : {OPRISK_PATH}")
        return

    df = load_oprisk(OPRISK_PATH)
    train = df[df["year"] <= CUTOFF_YEAR]["loss_eur_M"].values
    test = df[df["year"] > CUTOFF_YEAR]["loss_eur_M"].values

    print("=" * 74)
    print(f"  VALIDATION HOLDOUT — coupure temporelle à {CUTOFF_YEAR}")
    print("=" * 74)
    print(f"  Entraînement (<= {CUTOFF_YEAR}) : n = {len(train)} incidents")
    print(f"  Test         (>  {CUTOFF_YEAR}) : n = {len(test)} incidents")

    # --- 1. Calibration indépendante train / test (seuil = percentile 85 propre) ---
    u_train = float(np.percentile(train, 85))
    u_test = float(np.percentile(test, 85))

    params_train = fit_gpd(train, u_train)
    params_test = fit_gpd(test, u_test)
    ci_train = bootstrap_gpd(train, u_train, n_boot=2000)
    ci_test = bootstrap_gpd(test, u_test, n_boot=2000)

    print(f"\n  --- Calibration ENTRAÎNEMENT (seuil propre, pct85) ---")
    print(f"  u_train = {u_train:.2f} M€ | n_excès = {params_train['n_excess']}")
    print(f"  ξ̂_train = {params_train['xi']:.4f}  IC90% = {ci_train['xi_ci']}")
    print(f"  σ̂_train = {params_train['sigma']:.2f} M€")

    print(f"\n  --- Calibration TEST (seuil propre, pct85) ---")
    print(f"  u_test  = {u_test:.2f} M€ | n_excès = {params_test['n_excess']}")
    print(f"  ξ̂_test  = {params_test['xi']:.4f}  IC90% = {ci_test['xi_ci']}")
    print(f"  σ̂_test  = {params_test['sigma']:.2f} M€")

    lo_tr, hi_tr = ci_train["xi_ci"]
    lo_te, hi_te = ci_test["xi_ci"]
    overlap = max(lo_tr, lo_te) <= min(hi_tr, hi_te)
    print(f"\n  Chevauchement des IC90% sur ξ (train vs test) : "
          f"{'OUI — stabilité temporelle confirmée' if overlap else 'NON — dérive détectée'}")

    # --- 2. Adéquation hors échantillon : excès TEST au-delà du seuil TRAIN ---
    exc_oos = test[test > u_train] - u_train
    n_oos = len(exc_oos)
    print(f"\n  --- Adéquation hors échantillon ---")
    print(f"  Excès de TEST au-delà du seuil TRAIN (u={u_train:.2f} M€) : n = {n_oos}")

    if n_oos >= 10:
        pit = genpareto.cdf(exc_oos, c=params_train["xi"], scale=params_train["sigma"])
        ks_stat, ks_p = kstest(pit, "uniform")
        print(f"  Test KS sur la PIT (doit suivre U[0,1] si le modèle TRAIN généralise) :")
        print(f"    statistique KS = {ks_stat:.4f}  |  p-value = {ks_p:.4f}")
        verdict = "NON REJETÉE (p>0.05) — le modèle calé sur le passé décrit correctement la sévérité future" \
            if ks_p > 0.05 else "REJETÉE (p<=0.05) — écart significatif entre calibration passée et sévérité future"
        print(f"    H0 (GPD_train décrit bien les excès TEST) : {verdict}")
    else:
        ks_stat, ks_p = None, None
        print("  n trop faible pour un test KS fiable (< 10 excès).")

    # Comparaison VaR 99.5% : GPD train (extrapolée) vs quantile empirique test
    var_train_995 = var_gpd(params_train, 0.995)
    if len(test) >= 50:
        # p_u recalculé sur le total train pour rester cohérent avec la définition
        var_test_empirical_995 = float(np.quantile(test, 0.995))
    else:
        var_test_empirical_995 = None

    print(f"\n  VaR 99.5% extrapolée (GPD train)      = {var_train_995:.1f} M€")
    if var_test_empirical_995 is not None:
        print(f"  Quantile 99.5% empirique observé (test) = {var_test_empirical_995:.1f} M€")

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "results_holdout_validation.csv")
    pd.DataFrame([
        {"periode": "train", "cutoff_year": CUTOFF_YEAR, "n": len(train),
         "u": u_train, "n_excess": params_train["n_excess"],
         "xi": params_train["xi"], "xi_ic90_lo": lo_tr, "xi_ic90_hi": hi_tr,
         "sigma": params_train["sigma"]},
        {"periode": "test", "cutoff_year": CUTOFF_YEAR, "n": len(test),
         "u": u_test, "n_excess": params_test["n_excess"],
         "xi": params_test["xi"], "xi_ic90_lo": lo_te, "xi_ic90_hi": hi_te,
         "sigma": params_test["sigma"]},
        {"periode": "oos_ks_test", "cutoff_year": CUTOFF_YEAR, "n": n_oos,
         "u": u_train, "n_excess": n_oos, "xi": ks_stat, "xi_ic90_lo": ks_p,
         "xi_ic90_hi": None, "sigma": None},
    ]).to_csv(csv_path, index=False)
    print(f"\nCSV : {csv_path}")

    # --- Figure : fonction de survie empirique (test, au-delà de u_train) vs GPD train ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "holdout_validation.png")

    fig, ax = plt.subplots(figsize=(8, 5.5))
    if n_oos >= 5:
        exc_sorted = np.sort(exc_oos)
        emp_surv = 1.0 - (np.arange(1, n_oos + 1) - 0.5) / n_oos
        ax.step(exc_sorted, emp_surv, where="post", color=BRAND_ORANGE, linewidth=2,
                label=f"Survie empirique — excès TEST (n={n_oos})")
        grid = np.linspace(0, exc_sorted.max() * 1.05, 200)
        theo_surv = genpareto.sf(grid, c=params_train["xi"], scale=params_train["sigma"])
        ax.plot(grid, theo_surv, color=BRAND_BLUE, linewidth=2, linestyle="--",
                label="GPD(ξ_train, σ_train) — prédiction hors échantillon")
        ax.set_yscale("log")
        ax.set_xlabel(f"Excès au-delà du seuil TRAIN (u={u_train:.1f} M€)", fontsize=11)
        ax.set_ylabel("Fonction de survie (échelle log)", fontsize=11)
        ax.set_title(f"Validation holdout — GPD calée avant {CUTOFF_YEAR}, "
                     f"testée sur les incidents après {CUTOFF_YEAR}",
                     fontsize=12, fontweight="bold")
        ax.legend(fontsize=9)
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
