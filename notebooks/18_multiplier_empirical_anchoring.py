"""
18_multiplier_empirical_anchoring.py
------------------------------------
ANCRAGE EMPIRIQUE DES MULTIPLICATEURS DE MAPPING (chantier 3 « Prix SCOR »).

Le tornado (notebook 16) a montré que le verdict résiste à ±50 % sur les
multiplicateurs experts. On va plus loin : on ANCRE ces multiplicateurs sur des
effets de contrôle documentés dans la littérature, et l'on montre que les
valeurs expertes retenues sont des FRACTIONS CONSERVATRICES de ces effets — de
sorte qu'un ancrage empirique pousserait le Delta_DORA vers le HAUT, non vers
le bas. La réserve « multiplicateurs à dire d'expert » est ainsi retournée.

Dérivation transparente : si un contrôle (MFA, formation, patch) neutralise une
fraction e des attaques d'un vecteur, la fréquence d'incidents d'une entité
NON conforme (contrôle absent) rapportée à une entité conforme est le
multiplicateur impliqué m = 1/(1-e) ; pour une réduction de susceptibilité
d'un facteur k (ex. taux de clic phishing avant/après formation), m = k.

Sorties :
  outputs/tables/results_multiplier_anchoring.csv
  outputs/figures/multiplier_anchoring.png

Autonome.
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config import OPRISK, FREQUENCY, SCR_DORA
from src.frequency.negbin import HACKMAGEDDON_PROPORTIONS, MULTIPLICATEURS_DORA
from src.aggregation.lda import (simulate_year_3_briques, PROFILS_TYPES,
                                 ANCHORED_PARAMS, pcd_conditional)

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_GREEN = "#059669"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

ALPHA = 0.995
N_SIM = 100_000
SEED = 42
PILIER1 = 600.0

# --- Effets de contrôle documentés (littérature) -> multiplicateur impliqué ---
# m = 1/(1-e) pour une efficacité e ; m = k pour un ratio de susceptibilité k.
EXTERNAL = {
    "identifiants": dict(
        article="Art. 9 (MFA)",
        desc="MFA bloque ~99,2 % des compromissions de comptes",
        source="Microsoft (2019)",
        implied=1.0 / (1.0 - 0.992),          # ≈ 125
    ),
    "phishing_social_eng": dict(
        article="Art. 13 (formation)",
        desc="Formation : taux de clic phishing divisé par ~6",
        source="benchmarks simulation phishing / Ponemon",
        implied=6.0,
    ),
    "exploit_vuln": dict(
        article="Art. 26 (TLPT)",
        desc="Exploitation de vulnérabilités : ratio ~2,6",
        source="ENISA Threat Landscape",
        implied=2.6,
    ),
}


def model_center(vecteur, scenario="S2_non_conforme"):
    low, high = MULTIPLICATEURS_DORA[scenario][vecteur]
    return (low + high) / 2.0


def model_high(vecteur, scenario="S2_non_conforme"):
    return MULTIPLICATEURS_DORA[scenario][vecteur][1]


def lambda_ref_oprisk():
    return OPRISK["n_incidents"] / OPRISK["n_years"]


def lambda_global(overrides=None):
    """Multiplicateur global lambda_nc/lambda_ref, avec valeurs absolues
    imposées à certains vecteurs (overrides), sinon centre S2."""
    overrides = overrides or {}
    mult = 0.0
    for v, prop in HACKMAGEDDON_PROPORTIONS.items():
        m = overrides.get(v, model_center(v))
        mult += prop * m
    return mult


def delta_dora(overrides=None):
    src = OPRISK
    lam_ref = lambda_ref_oprisk()
    sev = {"xi": src["xi"], "sigma": src["sigma_eur"], "u": src["seuil_u_eur"],
           "p_u": src["p_u"], "dispersion_factor": FREQUENCY["dispersion_factor"],
           "severity_cap": None}
    lam_nc = lam_ref * lambda_global(overrides)
    lam_c = lam_ref * 1.0  # S0 : tous multiplicateurs = 1
    pcd_nc = pcd_conditional(PROFILS_TYPES["median"], 0.0, ANCHORED_PARAMS)
    pcd_c = pcd_conditional(PROFILS_TYPES["leader"], 0.0, ANCHORED_PARAMS)
    scr_nc = np.quantile(simulate_year_3_briques(lam_nc, sev, pcd_nc, N_SIM,
                         dependence="gumbel", theta=1.8, seed=SEED)["total"], ALPHA)
    scr_c = np.quantile(simulate_year_3_briques(lam_c, sev, pcd_c, N_SIM,
                        dependence="gumbel", theta=1.2, seed=SEED)["total"], ALPHA)
    return float(scr_nc - scr_c)


def main():
    print("=" * 80)
    print("  ANCRAGE EMPIRIQUE DES MULTIPLICATEURS DE MAPPING")
    print("=" * 80)

    # --- Comparaison multiplicateur impliqué vs modèle ---
    rows = []
    print(f"\n  {'vecteur':22} {'impliqué':>9} {'modèle(c)':>9} {'modèle/impliqué':>16}")
    for v, e in EXTERNAL.items():
        mc = model_center(v)
        frac = mc / e["implied"]
        rows.append(dict(vecteur=v, article=e["article"], source=e["source"],
                         implied=e["implied"], model_center=mc,
                         model_high=model_high(v), frac_pct=100 * frac))
        print(f"  {v:22} {e['implied']:>9.1f} {mc:>9.2f} {100*frac:>14.1f} %")

    base = delta_dora()
    print(f"\n  Delta_DORA baseline (multiplicateurs experts) = {base:.1f} M€ "
          f"({base/PILIER1:.1f}x Pilier 1)")

    # --- Scénario ancré : chaque vecteur ancré = min(impliqué, borne haute modèle) ---
    # (discipline : on ne dépasse pas la borne haute experte déjà bornée)
    ov_capped = {v: min(EXTERNAL[v]["implied"], model_high(v)) for v in EXTERNAL}
    d_capped = delta_dora(ov_capped)
    print(f"  Delta_DORA ancré (borné aux hautes valeurs expertes) = {d_capped:.1f} M€ "
          f"({d_capped/PILIER1:.1f}x)")

    # --- Scénario ancré littéral phishing (ratio 6, seul non aberrant) ---
    d_phish = delta_dora({"phishing_social_eng": EXTERNAL["phishing_social_eng"]["implied"]})
    print(f"  Delta_DORA ancré phishing=6 (littéral) = {d_phish:.1f} M€ "
          f"({d_phish/PILIER1:.1f}x)")

    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    df = pd.DataFrame(rows)
    df["delta_baseline"] = base
    df["delta_ancre_borne"] = d_capped
    df["delta_ancre_phishing"] = d_phish
    df.to_csv(os.path.join(out_dir, "results_multiplier_anchoring.csv"), index=False)
    print(f"\nCSV : {os.path.join(out_dir, 'results_multiplier_anchoring.csv')}")

    # --- Figure : multiplicateur impliqué vs modèle (échelle log) ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    labels = {"identifiants": "Identifiants\n(Art. 9 — MFA)",
              "phishing_social_eng": "Phishing\n(Art. 13 — formation)",
              "exploit_vuln": "Exploit vuln.\n(Art. 26 — TLPT)"}
    order = ["identifiants", "phishing_social_eng", "exploit_vuln"]
    x = np.arange(len(order))
    implied = [EXTERNAL[v]["implied"] for v in order]
    center = [model_center(v) for v in order]
    high = [model_high(v) for v in order]
    ax1.bar(x - 0.2, implied, 0.35, color=BRAND_ORANGE, label="impliqué (littérature)")
    ax1.bar(x + 0.2, center, 0.35, color=BRAND_BLUE, label="modèle (centre S2)")
    ax1.errorbar(x + 0.2, center, yerr=[np.zeros(len(order)),
                 np.array(high) - np.array(center)], fmt="none", ecolor=BRAND_DARK,
                 capsize=4, lw=1)
    ax1.set_yscale("log")
    ax1.set_xticks(x); ax1.set_xticklabels([labels[v] for v in order], fontsize=9)
    ax1.set_ylabel("Multiplicateur de fréquence (éch.\\ log)", fontsize=11)
    ax1.set_title("Multiplicateur impliqué par la littérature\nvs valeur experte du modèle",
                  fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9); ax1.grid(alpha=0.3, axis="y", which="both")
    for xi, (imp, ce) in enumerate(zip(implied, center)):
        ax1.text(xi - 0.2, imp, f"{imp:.0f}", ha="center", va="bottom", fontsize=8)
        ax1.text(xi + 0.2, ce, f"{ce:.1f}", ha="center", va="bottom", fontsize=8)

    # Delta_DORA sous les scénarios
    scen = ["Baseline\n(experts)", "Ancré\n(borné haut)", "Ancré phishing\n(littéral ×6)"]
    vals = [base, d_capped, d_phish]
    bars = ax2.bar(scen, vals, color=[BRAND_BLUE, BRAND_GREEN, BRAND_ORANGE],
                   edgecolor=BRAND_DARK, linewidth=0.6)
    ax2.axhline(PILIER1, color="#dc2626", ls=":", lw=2, label=f"forfait Pilier 1 = {PILIER1:.0f}")
    for b, v in zip(bars, vals):
        ax2.text(b.get_x() + b.get_width() / 2, v, f"{v:,.0f}\n({v/PILIER1:.1f}x)",
                 ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax2.set_ylabel(r"$\Delta_{DORA}$ (M€)", fontsize=11)
    ax2.set_title("$\\Delta_{DORA}$ sous ancrage empirique\n(l'ancrage renforce le verdict)",
                  fontsize=12, fontweight="bold")
    ax2.legend(fontsize=9); ax2.grid(alpha=0.3, axis="y")
    ax2.set_ylim(0, max(vals) * 1.25)

    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "multiplier_anchoring.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
