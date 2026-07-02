"""
notebooks/06_build_summary_table.py
-----------------------------------
Fusionne :
- results_euler_option_a.csv
- results_sensitivity_sanction.csv

pour produire un tableau final de synthèse.
"""

import os
import csv

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
os.makedirs(BASE_DIR, exist_ok=True)
euler_file = os.path.join(BASE_DIR, "results_euler_option_a.csv")
sens_file = os.path.join(BASE_DIR, "results_sensitivity_sanction.csv")
output_file = os.path.join(BASE_DIR, "results_summary_option_a.csv")


def read_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


euler_rows = read_csv(euler_file)
sens_rows = read_csv(sens_file)

sens_index = {}
for row in sens_rows:
    key = (row["source"], row["entity_key"], row["theta_env"])
    sens_index[key] = row

summary_rows = []

for row in euler_rows:
    key = (row["source"], row["entity_key"], row["theta_env"])
    sens = sens_index.get(key)

    if sens is None:
        continue

    summary_rows.append({
        "source": row["source"],
        "entity_key": row["entity_key"],
        "theta_env": row["theta_env"],
        "method": row["method"],
        "pcd": row["pcd"],
        "lambda_annual": row["lambda_annual"],
        "capital_total": row["capital_total"],
        "prestataire_pct": row["prestataire_pct"],
        "remediation_pct": row["remediation_pct"],
        "sanction_pct": row["sanction_pct"],
        "baseline_var_995": sens["baseline_var_995"],
        "baseline_es_995": sens["baseline_es_995"],
        "stress_var_995": sens["stress_var_995"],
        "stress_es_995": sens["stress_es_995"],
        "delta_var_995": sens["delta_var_995"],
        "delta_es_995": sens["delta_es_995"],
        "baseline_mean_sanction_pct": sens["baseline_mean_sanction_pct"],
        "stress_mean_sanction_pct": sens["stress_mean_sanction_pct"],
    })

fieldnames = [
    "source",
    "entity_key",
    "theta_env",
    "method",
    "pcd",
    "lambda_annual",
    "capital_total",
    "prestataire_pct",
    "remediation_pct",
    "sanction_pct",
    "baseline_var_995",
    "baseline_es_995",
    "stress_var_995",
    "stress_es_995",
    "delta_var_995",
    "delta_es_995",
    "baseline_mean_sanction_pct",
    "stress_mean_sanction_pct",
]

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(summary_rows)

print(f"Tableau final sauvegardé dans : {output_file}")