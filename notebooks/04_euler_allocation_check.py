"""
notebooks/04_euler_allocation_check.py
--------------------------------------
Script de test pour lancer l'allocation d'Euler sur le modèle LDA à 4 briques,
avec fréquence pilotée par la variable latente de conformité (Option A).

Sorties :
- affichage console des rapports Euler
- sauvegarde d'un CSV de comparaison dans notebooks/results_euler_option_a.csv
"""

import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.aggregation.euler_allocation import run_euler_on_reference, print_euler_report
from src.utils.config import FREQUENCY, OPRISK
from src.scenarios.latent_bridge import lambda_from_entity
from src.compliance.latent import PROFILS_TYPES


def run_case(
    source: str,
    dependence: str = "gumbel",
    entity_key: str = "median",
    theta_env: float = 0.0,
    method: str = "var",
    alpha: float = 0.995,
    n_sim: int = 100_000,
    bandwidth: float = 0.002,
    seed: int = 42,
):
    """
    Lance un cas de test complet avec fréquence continue pilotée
    par la variable latente (profil d'entité + environnement).
    """
    source = source.upper()

    if source == "PRC":
        lambda_ref = FREQUENCY["lambda_ref"]
    elif source == "OPRISK":
        lambda_ref = OPRISK["n_incidents"] / 27
    else:
        raise ValueError("source doit être 'PRC' ou 'OPRISK'")

    entity = PROFILS_TYPES[entity_key]
    latent_res = lambda_from_entity(entity, theta=theta_env, lambda_ref=lambda_ref)
    lam = latent_res["lambda_global"]
    pcd = latent_res["pcd"]
    mult = latent_res["multiplicateur_global"]

    alloc = run_euler_on_reference(
        lambda_annual=lam,
        source=source,
        alpha=alpha,
        n_sim=n_sim,
        dependence=dependence,
        theta_env=theta_env,
        entity_key=entity_key,
        method=method,
        bandwidth=bandwidth,
        seed=seed,
    )

    print("\n" + "=" * 90)
    print(" CAS TEST — OPTION A (fréquence pilotée par la variable latente)")
    print(
        f" source={source} | dependence={dependence} | entity={entity_key} | "
        f"theta_env={theta_env} | method={method} | alpha={alpha}"
    )
    print(
        f" PCD={pcd:.1%} | lambda_ref={lambda_ref:.2f} | "
        f"lambda_annual={lam:.2f} | mult={mult:.2f}x"
    )
    print("=" * 90)
    print_euler_report(alloc)

    return {
        "source": source,
        "entity_key": entity_key,
        "theta_env": theta_env,
        "method": method,
        "alpha": alpha,
        "pcd": pcd,
        "lambda_ref": lambda_ref,
        "lambda_annual": lam,
        "lambda_multiplier": mult,
        "alloc": alloc,
    }


def safe_get(dct, *keys, default=None):
    """
    Récupération robuste d'une valeur dans un dictionnaire imbriqué.
    """
    cur = dct
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def build_row(res: dict) -> dict:
    """
    Construit une ligne propre pour le CSV à partir du résultat d'un cas.
    Compatible avec différentes structures possibles de alloc.
    """
    alloc = res["alloc"]

    capital_total = (
        safe_get(alloc, "capital_total")
        or safe_get(alloc, "capital")
        or safe_get(alloc, "scr_total")
        or 0.0
    )

    contributions = safe_get(alloc, "contribution", default={}) or {}

    aggravation = contributions.get("aggravation", 0.0)
    prestataire = contributions.get("prestataire", 0.0)
    remediation = contributions.get("remediation", 0.0)
    sanction = contributions.get("sanction", 0.0)

    denom = capital_total if capital_total not in (0, None) else 1.0

    return {
        "source": res["source"],
        "entity_key": res["entity_key"],
        "theta_env": res["theta_env"],
        "method": res["method"],
        "alpha": res["alpha"],
        "pcd": res["pcd"],
        "lambda_ref": res["lambda_ref"],
        "lambda_annual": res["lambda_annual"],
        "lambda_multiplier": res["lambda_multiplier"],
        "capital_total": capital_total,
        "aggravation_contrib": aggravation,
        "prestataire_contrib": prestataire,
        "remediation_contrib": remediation,
        "sanction_contrib": sanction,
        "aggravation_pct": 100 * aggravation / denom,
        "prestataire_pct": 100 * prestataire / denom,
        "remediation_pct": 100 * remediation / denom,
        "sanction_pct": 100 * sanction / denom,
    }


if __name__ == "__main__":
    latent_cases = [
        {"source": "OPRISK", "entity_key": "leader", "theta_env": 0.0},
        {"source": "OPRISK", "entity_key": "median", "theta_env": 0.0},
        {"source": "OPRISK", "entity_key": "retard", "theta_env": 0.0},
        {"source": "OPRISK", "entity_key": "leader", "theta_env": -2.5},
        {"source": "OPRISK", "entity_key": "median", "theta_env": -2.5},
        {"source": "OPRISK", "entity_key": "retard", "theta_env": -2.5},
        {"source": "PRC", "entity_key": "leader", "theta_env": 0.0},
        {"source": "PRC", "entity_key": "median", "theta_env": 0.0},
        {"source": "PRC", "entity_key": "retard", "theta_env": 0.0},
        {"source": "PRC", "entity_key": "leader", "theta_env": -2.5},
        {"source": "PRC", "entity_key": "median", "theta_env": -2.5},
        {"source": "PRC", "entity_key": "retard", "theta_env": -2.5},
    ]

    rows = []

    for case in latent_cases:
        for method in ["var", "es"]:
            res = run_case(
                source=case["source"],
                dependence="gumbel",
                entity_key=case["entity_key"],
                theta_env=case["theta_env"],
                method=method,
                alpha=0.995,
                n_sim=100_000,
                bandwidth=0.002,
                seed=42,
            )
            rows.append(build_row(res))

    output_file = os.path.join(os.path.dirname(__file__), "results_euler_option_a.csv")

    fieldnames = [
        "source",
        "entity_key",
        "theta_env",
        "method",
        "alpha",
        "pcd",
        "lambda_ref",
        "lambda_annual",
        "lambda_multiplier",
        "capital_total",
        "aggravation_contrib",
        "prestataire_contrib",
        "remediation_contrib",
        "sanction_contrib",
        "aggravation_pct",
        "prestataire_pct",
        "remediation_pct",
        "sanction_pct",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "=" * 90)
    print(f" Résultats sauvegardés dans : {output_file}")
    print("=" * 90)