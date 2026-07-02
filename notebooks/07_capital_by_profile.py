"""
notebooks/07_capital_by_profile.py
----------------------------------
Reproduit de façon REPRODUCTIBLE :
  (1) le tableau 5.1 du mémoire : capital total VaR 99.5% et ES 99.5%,
      par profil (leader / médian / retard) × source (PRC / OpRisk) ;
  (2) les données de la figure 6 : décomposition d'Euler en 3 briques
      (remédiation / prestataire / sanction), cohérente avec le tableau 5.3.

Moteur : src/aggregation/lda.py::simulate_year_3_briques (moteur CANONIQUE).

Usage : python notebooks/07_capital_by_profile.py
"""

import os, sys, csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np

from src.aggregation.lda import simulate_year_3_briques
from src.aggregation.euler_allocation import (
    build_severity_params, euler_allocation_var, var_empirical, expected_shortfall,
)
from src.scenarios.latent_bridge import lambda_from_entity
from src.compliance.latent import PROFILS_TYPES, ANCHORED_PARAMS, pcd_conditional
from src.utils.config import FREQUENCY, OPRISK

ALPHA = 0.995
N_SIM = 100_000
SEED = 42
PROFILS = ["leader", "median", "retard"]
SOURCES = ["PRC", "OPRISK"]

PROFIL_LABEL = {"leader": "Leader", "median": "Médian", "retard": "Retardataire"}


def lambda_ref_for(source: str) -> float:
    if source == "PRC":
        return FREQUENCY["lambda_ref"]
    return OPRISK["n_incidents"] / OPRISK["n_years"]


def run_one(source: str, entity_key: str) -> dict:
    entity = PROFILS_TYPES[entity_key]
    lam = lambda_from_entity(
        entity, theta=0.0, lambda_ref=lambda_ref_for(source)
    )["lambda_global"]
    pcd = pcd_conditional(entity, 0.0, ANCHORED_PARAMS)
    sev = build_severity_params(source)

    sim = simulate_year_3_briques(
        lambda_annual=lam, severity_params=sev, pcd_sanction=pcd,
        n_sim=N_SIM, dependence="gumbel", theta=1.8, seed=SEED,
    )
    total = sim["total"]
    var = var_empirical(total, ALPHA)
    es = expected_shortfall(total, ALPHA)
    alloc = euler_allocation_var(sim, alpha=ALPHA)

    return {
        "source": source,
        "profil": PROFIL_LABEL[entity_key],
        "pcd": pcd,
        "lambda": lam,
        "var_995": var,
        "es_995": es,
        "remediation_pct": 100 * alloc["percent"]["remediation"],
        "prestataire_pct": 100 * alloc["percent"]["prestataire"],
        "sanction_pct": 100 * alloc["percent"]["sanction"],
    }


if __name__ == "__main__":
    rows = [run_one(src, key) for src in SOURCES for key in PROFILS]

    # --- Tableau 5.1 (capital par profil) ---
    print("\n" + "=" * 78)
    print("  TABLEAU 5.1 — Capital total par profil et source")
    print("=" * 78)
    print(f"  {'Source':8s} {'Profil':13s} {'PCD':>7s} "
          f"{'VaR 99.5%':>12s} {'ES 99.5%':>12s}")
    print("  " + "-" * 60)
    for r in rows:
        print(f"  {r['source']:8s} {r['profil']:13s} {r['pcd']:>6.2%} "
              f"{r['var_995']:>10.1f} M€ {r['es_995']:>10.1f} M€")

    # --- Figure 6 (décomposition Euler 3 briques, régime OpRisk médian) ---
    ref = next(r for r in rows if r["source"] == "OPRISK" and r["profil"] == "Médian")
    print("\n" + "=" * 78)
    print("  FIGURE 6 (données) — Allocation d'Euler 3 briques, OpRisk médian")
    print("=" * 78)
    print(f"  Remédiation : {ref['remediation_pct']:.1f} %")
    print(f"  Prestataire : {ref['prestataire_pct']:.1f} %")
    print(f"  Sanction    : {ref['sanction_pct']:.2f} %")
    print("  (somme = 100 % — PAS d'aggravation ici : c'est un différentiel, pas une brique)")

    # --- Export CSV ---
    out = os.path.join(os.path.dirname(__file__), "results_capital_by_profile.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nSauvegardé : {out}")