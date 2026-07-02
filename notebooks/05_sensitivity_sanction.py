"""
notebooks/05_sensitivity_sanction.py
------------------------------------
Mini analyse de sensibilité sur la brique sanction :
- baseline : borne haute = 20 M€
- stress   : borne haute = 40 M€

Objectif :
vérifier si la faible contribution de la sanction est structurelle
ou simplement liée au calibrage de sa borne supérieure.
(Mis à jour pour l'architecture LDA à 3 briques additives)
"""

import os
import sys
import csv
import copy
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.aggregation.lda import simulate_year_3_briques, BRIQUE_PARAMS
from src.scenarios.latent_bridge import lambda_from_entity
from src.compliance.latent import PROFILS_TYPES
from src.utils.config import FREQUENCY, OPRISK, PRC, SCR_DORA


def get_source_params(source: str):
    source = source.upper()

    if source == "PRC":
        lambda_ref = FREQUENCY["lambda_ref"]
        src = PRC
        severity_cap = SCR_DORA.get("cap_eur", 40.0)
    elif source == "OPRISK":
        lambda_ref = OPRISK["n_incidents"] / 27
        src = OPRISK
        severity_cap = None
    else:
        raise ValueError("source doit être 'PRC' ou 'OPRISK'")

    severity_params = {
        "xi": src["xi"],
        "sigma": src["sigma_eur"],
        "u": src["seuil_u_eur"],
        "p_u": src["p_u"],
        "dispersion_factor": FREQUENCY["dispersion_factor"],
        "severity_cap": severity_cap,
    }

    return lambda_ref, severity_params


def run_sanction_case(
    source: str,
    entity_key: str,
    theta_env: float,
    sanction_high: float,
    alpha: float = 0.995,
    n_sim: int = 100_000,
    dependence: str = "gumbel",
    seed: int = 42,
):
    source = source.upper()

    lambda_ref, severity_params = get_source_params(source)
    entity = PROFILS_TYPES[entity_key]

    latent_res = lambda_from_entity(entity, theta=theta_env, lambda_ref=lambda_ref)
    lam = latent_res["lambda_global"]
    pcd = latent_res["pcd"]
    mult = latent_res["multiplicateur_global"]

    old_range = BRIQUE_PARAMS["sanction"]["montant_range_eur_m"]
    BRIQUE_PARAMS["sanction"]["montant_range_eur_m"] = (2.0, sanction_high)

    try:
        res = simulate_year_3_briques(
            lambda_annual=lam,
            severity_params=severity_params,
            pcd_sanction=pcd,
            n_sim=n_sim,
            pcd_prestataire=pcd,  # Ajout de la liaison avec le PCD prestataire
            dependence=dependence,
            seed=seed,
        )
    finally:
        BRIQUE_PARAMS["sanction"]["montant_range_eur_m"] = old_range

    total = res["total"]
    prestataire = res["prestataire"]
    remediation = res["remediation"]
    sanction = res["sanction"]

    var_alpha = float(np.quantile(total, alpha))
    tail = total >= var_alpha
    es_alpha = float(total[tail].mean())

    mean_total = float(total.mean())
    mean_prestataire = float(prestataire.mean())
    mean_remediation = float(remediation.mean())
    mean_sanction = float(sanction.mean())

    return {
        "source": source,
        "entity_key": entity_key,
        "theta_env": theta_env,
        "alpha": alpha,
        "n_sim": n_sim,
        "dependence": dependence,
        "pcd": pcd,
        "lambda_ref": lambda_ref,
        "lambda_annual": lam,
        "lambda_multiplier": mult,
        "sanction_low": 2.0,
        "sanction_high": sanction_high,
        "var_995": var_alpha,
        "es_995": es_alpha,
        "mean_total": mean_total,
        "mean_prestataire": mean_prestataire,
        "mean_remediation": mean_remediation,
        "mean_sanction": mean_sanction,
        "mean_prestataire_pct": 100 * mean_prestataire / mean_total if mean_total else 0.0,
        "mean_remediation_pct": 100 * mean_remediation / mean_total if mean_total else 0.0,
        "mean_sanction_pct": 100 * mean_sanction / mean_total if mean_total else 0.0,
    }


if __name__ == "__main__":
    cases = [
        {"source": "OPRISK", "entity_key": "leader", "theta_env": 0.0},
        {"source": "OPRISK", "entity_key": "median", "theta_env": 0.0},
        {"source": "OPRISK", "entity_key": "retard", "theta_env": 0.0},
        {"source": "PRC", "entity_key": "leader", "theta_env": 0.0},
        {"source": "PRC", "entity_key": "median", "theta_env": 0.0},
        {"source": "PRC", "entity_key": "retard", "theta_env": 0.0},
    ]

    rows = []

    for case in cases:
        baseline = run_sanction_case(
            source=case["source"],
            entity_key=case["entity_key"],
            theta_env=case["theta_env"],
            sanction_high=20.0,
            alpha=0.995,
            n_sim=100_000,
            dependence="gumbel",
            seed=42,
        )

        stress = run_sanction_case(
            source=case["source"],
            entity_key=case["entity_key"],
            theta_env=case["theta_env"],
            sanction_high=40.0,
            alpha=0.995,
            n_sim=100_000,
            dependence="gumbel",
            seed=42,
        )

        delta_var = stress["var_995"] - baseline["var_995"]
        delta_es = stress["es_995"] - baseline["es_995"]
        delta_sanction_mean = stress["mean_sanction"] - baseline["mean_sanction"]

        rows.append({
            "source": baseline["source"],
            "entity_key": baseline["entity_key"],
            "theta_env": baseline["theta_env"],
            "pcd": baseline["pcd"],
            "lambda_annual": baseline["lambda_annual"],

            "baseline_sanction_high": baseline["sanction_high"],
            "baseline_var_995": baseline["var_995"],
            "baseline_es_995": baseline["es_995"],
            "baseline_mean_sanction": baseline["mean_sanction"],
            "baseline_mean_sanction_pct": baseline["mean_sanction_pct"],

            "stress_sanction_high": stress["sanction_high"],
            "stress_var_995": stress["var_995"],
            "stress_es_995": stress["es_995"],
            "stress_mean_sanction": stress["mean_sanction"],
            "stress_mean_sanction_pct": stress["mean_sanction_pct"],

            "delta_var_995": delta_var,
            "delta_es_995": delta_es,
            "delta_mean_sanction": delta_sanction_mean,
        })

        print("\n" + "=" * 88)
        print(
            f"SENSITIVITY | source={baseline['source']} | entity={baseline['entity_key']} "
            f"| theta={baseline['theta_env']} | pcd={baseline['pcd']:.1%} "
            f"| lambda={baseline['lambda_annual']:.2f}"
        )
        print("-" * 88)
        print(
            f"Baseline sanction [2,20] : VaR={baseline['var_995']:.1f} | "
            f"ES={baseline['es_995']:.1f} | sanction_mean={baseline['mean_sanction']:.1f} "
            f"({baseline['mean_sanction_pct']:.2f}%)"
        )
        print(
            f"Stress   sanction [2,40] : VaR={stress['var_995']:.1f} | "
            f"ES={stress['es_995']:.1f} | sanction_mean={stress['mean_sanction']:.1f} "
            f"({stress['mean_sanction_pct']:.2f}%)"
        )
        print(
            f"Delta                      ΔVaR={delta_var:.1f} | ΔES={delta_es:.1f} | "
            f"Δsanction_mean={delta_sanction_mean:.1f}"
        )
        print("=" * 88)

    output_file = os.path.join(os.path.dirname(__file__), "results_sensitivity_sanction.csv")

    fieldnames = [
        "source",
        "entity_key",
        "theta_env",
        "pcd",
        "lambda_annual",
        "baseline_sanction_high",
        "baseline_var_995",
        "baseline_es_995",
        "baseline_mean_sanction",
        "baseline_mean_sanction_pct",
        "stress_sanction_high",
        "stress_var_995",
        "stress_es_995",
        "stress_mean_sanction",
        "stress_mean_sanction_pct",
        "delta_var_995",
        "delta_es_995",
        "delta_mean_sanction",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "=" * 88)
    print(f"Résultats sauvegardés dans : {output_file}")
    print("=" * 88)