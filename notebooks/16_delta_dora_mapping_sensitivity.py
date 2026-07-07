"""
16_delta_dora_mapping_sensitivity.py
------------------------------------
ROBUSTESSE DU VERDICT AUX HYPOTHÈSES DE MAPPING (chantier « Prix SCOR »).

Le Delta_DORA hérite des multiplicateurs de fréquence S0/S1/S2 par vecteur
d'attaque (mapping expert vers les articles DORA). C'est l'hypothèse porteuse
du mémoire. Ce script en teste la sensibilité :

  1. TORNADO : chaque multiplicateur S2 est perturbé de ±50 % (les autres
     figés), et l'on mesure l'oscillation de Delta_DORA. Cela révèle QUEL
     article DORA gouverne le résultat.
  2. BANDE GLOBALE : tous les multiplicateurs sont abaissés de 50 % (mapping
     « prudent ») puis relevés de 50 % (mapping « sévère »), pour borner
     Delta_DORA et vérifier que le VERDICT QUALITATIF (capital >> forfait de
     Pilier 1) survit aux deux extrêmes.

Graines communes (seed figé) entre toutes les variantes : l'écart mesuré
reflète le multiplicateur, non le bruit Monte Carlo.

Sorties :
  outputs/tables/results_delta_dora_mapping.csv
  outputs/figures/delta_dora_mapping_tornado.png

Autonome (calibrations figées dans config.py).
"""

import os
import sys
import copy

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config import OPRISK, PRC, FREQUENCY, SCR_DORA
from src.frequency.negbin import (HACKMAGEDDON_PROPORTIONS, MULTIPLICATEURS_DORA,
                                  DORA_MAPPING)
from src.aggregation.lda import (simulate_year_3_briques, PROFILS_TYPES,
                                 ANCHORED_PARAMS, pcd_conditional)

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_GREEN = "#059669"
BRAND_RED = "#dc2626"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

ALPHA = 0.995
N_SIM = 100_000
SEED = 42
PILIER1_FORFAIT = 600.0   # 0,04 x 15 000 M€ de CA (formule standard Solva II)

VECTEURS = list(HACKMAGEDDON_PROPORTIONS.keys())


def lambda_center(scenario, scale=None):
    """lambda_global = lambda_ref implicite=1 ; renvoie le multiplicateur global.
    scale : dict {vecteur: facteur} appliqué au multiplicateur central du vecteur."""
    scale = scale or {}
    bounds = MULTIPLICATEURS_DORA[scenario]
    mult = 0.0
    for v, prop in HACKMAGEDDON_PROPORTIONS.items():
        low, high = bounds[v]
        m = (low + high) / 2.0
        m *= scale.get(v, 1.0)
        mult += prop * m
    return mult   # multiplicateur global (lambda_global / lambda_ref)


def delta_dora(source, scale=None):
    """Delta_DORA = VaR_S2(multiplicateurs perturbés) - VaR_S0, source donnée.
    Seule la fréquence non-conforme varie ; tout le reste est figé (graine commune)."""
    src = {"OPRISK": OPRISK, "PRC": PRC}[source]
    lambda_ref = (OPRISK["n_incidents"] / OPRISK["n_years"] if source == "OPRISK"
                  else FREQUENCY["lambda_ref"])
    sev = {"xi": src["xi"], "sigma": src["sigma_eur"], "u": src["seuil_u_eur"],
           "p_u": src["p_u"], "dispersion_factor": FREQUENCY["dispersion_factor"],
           "severity_cap": SCR_DORA.get("cap_eur", 40.0) if source == "PRC" else None}

    lam_nc = lambda_ref * lambda_center("S2_non_conforme", scale)
    lam_c = lambda_ref * lambda_center("S0_conforme")   # tous multiplicateurs = 1
    pcd_nc = pcd_conditional(PROFILS_TYPES["median"], 0.0, ANCHORED_PARAMS)
    pcd_c = pcd_conditional(PROFILS_TYPES["leader"], 0.0, ANCHORED_PARAMS)

    res_nc = simulate_year_3_briques(lam_nc, sev, pcd_nc, N_SIM,
                                     dependence="gumbel", theta=1.8, seed=SEED)
    res_c = simulate_year_3_briques(lam_c, sev, pcd_c, N_SIM,
                                    dependence="gumbel", theta=1.2, seed=SEED)
    scr_nc = float(np.quantile(res_nc["total"], ALPHA))
    scr_c = float(np.quantile(res_c["total"], ALPHA))
    return scr_nc - scr_c, scr_nc, scr_c


def main():
    source = "OPRISK"
    print("=" * 78)
    print(f"  SENSIBILITÉ DU Delta_DORA AUX MULTIPLICATEURS DE MAPPING — {source}")
    print("=" * 78)

    base, scr_nc0, scr_c0 = delta_dora(source)
    print(f"  Baseline : Delta_DORA = {base:.1f} M€  (VaR_S2={scr_nc0:.1f}, VaR_S0={scr_c0:.1f})")
    print(f"  Forfait Pilier 1 (Solva II) = {PILIER1_FORFAIT:.0f} M€  "
          f"=> ratio baseline = {base/PILIER1_FORFAIT:.1f}x")

    # --- 1. TORNADO : ±50 % par vecteur ---
    rows = []
    print("\n  --- Tornado : ±50 % sur chaque multiplicateur S2 (autres figés) ---")
    for v in VECTEURS:
        d_lo, _, _ = delta_dora(source, scale={v: 0.5})
        d_hi, _, _ = delta_dora(source, scale={v: 1.5})
        swing = abs(d_hi - d_lo)
        rows.append(dict(vecteur=v, article=DORA_MAPPING.get(v, ""),
                         poids=HACKMAGEDDON_PROPORTIONS[v],
                         delta_low=d_lo, delta_high=d_hi, swing=swing))
        print(f"    {v:22s} [-50%]={d_lo:8.1f}  [+50%]={d_hi:8.1f}  "
              f"amplitude={swing:7.1f}")

    rows.sort(key=lambda r: r["swing"], reverse=True)

    # --- 2. BANDE GLOBALE : tous les multiplicateurs ±50 % ---
    all_lo, _, _ = delta_dora(source, scale={v: 0.5 for v in VECTEURS})
    all_hi, _, _ = delta_dora(source, scale={v: 1.5 for v in VECTEURS})
    print("\n  --- Bande globale (TOUS les multiplicateurs) ---")
    print(f"    mapping prudent (-50%)  : Delta_DORA = {all_lo:8.1f} M€  "
          f"=> {all_lo/PILIER1_FORFAIT:.1f}x le forfait Pilier 1")
    print(f"    mapping sévère  (+50%)  : Delta_DORA = {all_hi:8.1f} M€  "
          f"=> {all_hi/PILIER1_FORFAIT:.1f}x le forfait Pilier 1")
    verdict = "ROBUSTE" if all_lo > PILIER1_FORFAIT else "FRAGILE"
    print(f"    => Verdict qualitatif (Delta_DORA > forfait) : {verdict}")

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    df = pd.DataFrame(rows)
    df["baseline"] = base
    df.to_csv(os.path.join(out_dir, "results_delta_dora_mapping.csv"), index=False)
    print(f"\nCSV : {os.path.join(out_dir, 'results_delta_dora_mapping.csv')}")

    # --- Figure : tornado horizontal ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 6))
    labels_short = {
        "phishing_social_eng": "Phishing / ingénierie sociale\n(Art. 13 — formation)",
        "exploit_vuln": "Exploit vulnérabilité\n(Art. 26 — TLPT)",
        "supply_chain_tiers": "Chaîne d'appro. / tiers\n(Art. 28-44 — tiers ICT)",
        "identifiants": "Identifiants / accès\n(Art. 9 — MFA)",
        "autres": "Autres (transverse)",
    }
    y = np.arange(len(rows))
    for i, r in enumerate(rows):
        lo, hi = r["delta_low"], r["delta_high"]
        ax.barh(i, hi - lo, left=min(lo, hi), height=0.6,
                color=BRAND_BLUE, alpha=0.75, edgecolor=BRAND_DARK, linewidth=0.6)
        ax.text(max(lo, hi) + 40, i, f"±{r['swing']/2:.0f}", va="center", fontsize=9)
    ax.axvline(base, color=BRAND_DARK, ls="--", lw=1.5, label=f"baseline = {base:.0f} M€")
    ax.axvline(PILIER1_FORFAIT, color=BRAND_RED, ls=":", lw=2,
               label=f"forfait Pilier 1 = {PILIER1_FORFAIT:.0f} M€")
    ax.set_yticks(y)
    ax.set_yticklabels([labels_short.get(r["vecteur"], r["vecteur"]) for r in rows],
                       fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(r"$\Delta_{DORA}$ (M€) — profil médian, source OpRisk", fontsize=11)
    ax.set_title("Tornado : sensibilité du $\\Delta_{DORA}$ aux multiplicateurs\n"
                 "de mapping DORA (±50 % par vecteur, graines communes)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10, loc="lower right")
    ax.grid(True, axis="x", alpha=0.3)
    # bande globale en annotation
    ax.annotate(f"Bande globale (tous ±50 %) : [{all_lo:.0f} ; {all_hi:.0f}] M€\n"
                f"soit [{all_lo/PILIER1_FORFAIT:.1f}x ; {all_hi/PILIER1_FORFAIT:.1f}x] "
                f"le forfait Pilier 1  →  verdict {verdict}",
                xy=(0.02, 0.02), xycoords="axes fraction", fontsize=9,
                bbox=dict(boxstyle="round", fc="white", ec=BRAND_GREEN))
    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "delta_dora_mapping_tornado.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
