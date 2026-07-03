"""
notebooks/08_sensitivity_tornado.py
------------------------------------
Analyse de sensibilité du SCR (VaR 99.5%) aux hypothèses PORTEUSES du modèle.

Objectif : préempter la critique « ces paramètres sont libres » en montrant
COMBIEN chacun pèse réellement sur le capital. Chaque paramètre est perturbé
sur une plage plausible et documentée, toutes choses égales par ailleurs, et
l'on mesure la réponse de la VaR 99.5%. Le classement (tornado) sépare :
  - les paramètres DATA-DRIVEN (ξ, σ : IC90% bootstrap) ;
  - les hypothèses LIBRES / à dire d'expert (γ, p_ref, multiplicateurs,
    surcharge prestataire, dispersion, copule).

Cas de base : OpRisk, profil médian, θ=0, VaR 99.5%, graine figée.

Sortie : outputs/tables/results_sensitivity_tornado.csv
         outputs/figures/tornado_sensitivity.png

Usage : python notebooks/08_sensitivity_tornado.py
"""

import os
import sys
import csv
import copy

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.aggregation.lda import simulate_year_3_briques, BRIQUE_PARAMS
from src.scenarios.latent_bridge import lambda_from_entity
from src.compliance.latent import PROFILS_TYPES, ANCHORED_PARAMS
from src.frequency import negbin
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA

# Style cohérent avec src/visualization/plots.py
BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

ALPHA = 0.995
N_SIM = 100_000
SEED = 42
SOURCE = "OPRISK"
ENTITY_KEY = "median"
THETA_ENV = 0.0
GUMBEL_THETA_BASE = 1.8


# ---------------------------------------------------------------------------
# SCR sous jeu de paramètres arbitraire (contrôle total des leviers)
# ---------------------------------------------------------------------------

def base_severity_params():
    src = OPRISK if SOURCE == "OPRISK" else PRC
    cap = None if SOURCE == "OPRISK" else SCR_DORA.get("cap_eur", 40.0)
    return {
        "xi": src["xi"],
        "sigma": src["sigma_eur"],
        "u": src["seuil_u_eur"],
        "p_u": src["p_u"],
        "dispersion_factor": FREQUENCY["dispersion_factor"],
        "severity_cap": cap,
    }


def compute_scr(latent_params=None, severity_overrides=None,
                gumbel_theta=GUMBEL_THETA_BASE,
                mult_scale=1.0, surcharge_range=None,
                theta_env=THETA_ENV):
    """
    Calcule la VaR 99.5% sous un jeu de paramètres donné, en réutilisant
    exactement le moteur du pipeline (lambda_from_entity + simulate_year_3_briques).
    Les perturbations globales (multiplicateurs, surcharge) sont appliquées via
    save/restore pour ne pas polluer l'état des autres runs.
    """
    latent_params = latent_params or ANCHORED_PARAMS
    entity = PROFILS_TYPES[ENTITY_KEY]
    lambda_ref = OPRISK["n_incidents"] / 27 if SOURCE == "OPRISK" else FREQUENCY["lambda_ref"]

    sev = base_severity_params()
    if severity_overrides:
        sev.update(severity_overrides)

    # --- sauvegarde de l'état global mutable ---
    saved_mult = copy.deepcopy(negbin.MULTIPLICATEURS_DORA["S2_non_conforme"])
    saved_surcharge = BRIQUE_PARAMS["prestataire"]["surcharge_range"]
    try:
        if mult_scale != 1.0:
            for vec, (lo, hi) in negbin.MULTIPLICATEURS_DORA["S2_non_conforme"].items():
                negbin.MULTIPLICATEURS_DORA["S2_non_conforme"][vec] = (
                    1.0 + (lo - 1.0) * mult_scale, 1.0 + (hi - 1.0) * mult_scale
                )
        if surcharge_range is not None:
            BRIQUE_PARAMS["prestataire"]["surcharge_range"] = surcharge_range

        latent_res = lambda_from_entity(entity, theta=theta_env,
                                        lambda_ref=lambda_ref,
                                        latent_params=latent_params)
        lam = latent_res["lambda_global"]
        pcd = latent_res["pcd"]

        sim = simulate_year_3_briques(
            lambda_annual=lam, severity_params=sev, pcd_sanction=pcd,
            n_sim=N_SIM, dependence="gumbel", theta=gumbel_theta, seed=SEED,
        )
        return float(np.quantile(sim["total"], ALPHA))
    finally:
        negbin.MULTIPLICATEURS_DORA["S2_non_conforme"] = saved_mult
        BRIQUE_PARAMS["prestataire"]["surcharge_range"] = saved_surcharge


def with_latent(**overrides):
    p = copy.deepcopy(ANCHORED_PARAMS)
    p.update(overrides)
    return p


# ---------------------------------------------------------------------------
# Définition des perturbations (bornes plausibles, documentées)
# ---------------------------------------------------------------------------
# Chaque entrée : (label, catégorie, fn_low, fn_high, borne_basse, borne_haute)
# catégorie : "data" (IC bootstrap) ou "hypothèse" (libre / expert / structurel)

def build_cases():
    xi_lo, xi_hi = OPRISK["xi_ic90"]           # [0.3044, 0.8313]
    sig_lo, sig_hi = OPRISK["sigma_ic90"]      # [41.88, 82.80]
    return [
        ("ξ — indice de queue (IC90% bootstrap)", "data",
         lambda: compute_scr(severity_overrides={"xi": xi_lo}),
         lambda: compute_scr(severity_overrides={"xi": xi_hi}),
         f"{xi_lo:.2f}", f"{xi_hi:.2f}"),

        ("σ — échelle GPD (IC90% bootstrap)", "data",
         lambda: compute_scr(severity_overrides={"sigma": sig_lo}),
         lambda: compute_scr(severity_overrides={"sigma": sig_hi}),
         f"{sig_lo:.0f}", f"{sig_hi:.0f}"),

        ("Multiplicateurs S2 (±15% calibration)", "hypothèse",
         lambda: compute_scr(mult_scale=0.85),
         lambda: compute_scr(mult_scale=1.15),
         "-15%", "+15%"),

        ("φ — sur-dispersion NegBin", "hypothèse",
         lambda: compute_scr(severity_overrides={"dispersion_factor": 6.0}),
         lambda: compute_scr(severity_overrides={"dispersion_factor": 12.0}),
         "6.0", "12.0"),

        # γ est inerte à θ=0 (terme γ·θ nul) : sa sensibilité n'a de sens que
        # sous choc systémique -> évaluée à θ=-2.5, où le facteur commun agit.
        ("γ — corrélation Vasicek (sous choc θ=-2,5)", "hypothèse",
         lambda: compute_scr(latent_params=with_latent(gamma=0.50), theta_env=-2.5),
         lambda: compute_scr(latent_params=with_latent(gamma=0.85), theta_env=-2.5),
         "0.50", "0.85"),

        ("p_ref — non-conformité de référence", "hypothèse",
         lambda: compute_scr(latent_params=with_latent(p_ref=0.35)),
         lambda: compute_scr(latent_params=with_latent(p_ref=0.65)),
         "0.35", "0.65"),

        ("θ — dépendance copule de Gumbel", "hypothèse",
         lambda: compute_scr(gumbel_theta=1.2),
         lambda: compute_scr(gumbel_theta=2.5),
         "1.2", "2.5"),

        ("Surcharge prestataire (tiers ICT)", "hypothèse",
         lambda: compute_scr(surcharge_range=(0.05, 0.05)),
         lambda: compute_scr(surcharge_range=(0.15, 0.15)),
         "+5%", "+15%"),
    ]


def main():
    base = compute_scr()
    print(f"SCR de base (OpRisk, médian, θ=0, VaR 99.5%) = {base:,.1f} M€\n")

    rows = []
    for label, cat, fn_lo, fn_hi, blo, bhi in build_cases():
        scr_lo = fn_lo()
        scr_hi = fn_hi()
        swing = abs(scr_hi - scr_lo)
        rows.append({
            "parametre": label, "categorie": cat,
            "borne_basse": blo, "borne_haute": bhi,
            "scr_low": scr_lo, "scr_high": scr_hi,
            "scr_base": base, "swing": swing,
            "swing_pct": 100 * swing / base,
        })
        print(f"{label:44s} [{cat:9s}] "
              f"SCR: {min(scr_lo,scr_hi):>8.0f} — {max(scr_lo,scr_hi):>8.0f} M€  "
              f"(swing {100*swing/base:>6.1f}%)")

    rows.sort(key=lambda r: r["swing"], reverse=True)

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "results_sensitivity_tornado.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nCSV : {csv_path}")

    # --- Tornado ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "tornado_sensitivity.png")

    labels = [r["parametre"] for r in rows]
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(11, 6))
    for i, r in enumerate(rows):
        lo, hi = min(r["scr_low"], r["scr_high"]), max(r["scr_low"], r["scr_high"])
        color = BRAND_BLUE if r["categorie"] == "data" else BRAND_ORANGE
        ax.barh(i, hi - lo, left=lo, color=color, height=0.62,
                edgecolor="white", linewidth=0.5)
    ax.axvline(base, color=BRAND_DARK, linestyle="--", linewidth=1.5,
               label=f"SCR de base = {base:,.0f} M€")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("VaR 99,5% (M€)", fontsize=12, fontweight="semibold")
    ax.set_title("Sensibilité du SCR aux hypothèses porteuses (tornado)",
                 fontsize=15, fontweight="bold", pad=14)
    from matplotlib.patches import Patch
    handles = [
        Patch(color=BRAND_BLUE, label="Paramètre data-driven (IC90% bootstrap)"),
        Patch(color=BRAND_ORANGE, label="Hypothèse libre / à dire d'expert"),
        plt.Line2D([0], [0], color=BRAND_DARK, linestyle="--",
                   label=f"SCR de base = {base:,.0f} M€"),
    ]
    ax.legend(handles=handles, fontsize=9, loc="lower right",
              frameon=True, facecolor=BRAND_LIGHT, edgecolor="#e2e8f0")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
