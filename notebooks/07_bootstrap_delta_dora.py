"""
notebooks/07_bootstrap_delta_dora.py
-------------------------------------
Relance le bootstrap à deux niveaux sur le Delta_DORA (src/scenarios/bootstrap_delta_dora.py)
pour produire une grille Δ_DORA reproductible depuis le pipeline actuel (3 briques + copule).

Ce module n'était appelé par aucun notebook : les valeurs de DELTA_DORA_GRID dans
config.py dataient d'une exécution antérieure, non reproductible en l'état.

Note : la branche OPRISK nécessite data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx
(donnée sous licence, gitignorée). Si le fichier est absent, la branche OPRISK est
sautée avec un avertissement plutôt que de faire échouer toute la grille.

Usage : python notebooks/07_bootstrap_delta_dora.py
"""

import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.scenarios.bootstrap_delta_dora import bootstrap_delta_dora

N_BOOT = 200
N_SIM_PER_BOOT = 20_000

if __name__ == "__main__":
    rows = []

    for source in ["PRC", "OPRISK"]:
        for scenario_x in ["S1_partiel", "S2_non_conforme"]:
            try:
                res = bootstrap_delta_dora(
                    source, scenario_x,
                    n_boot=N_BOOT, n_sim_per_boot=N_SIM_PER_BOOT,
                )
            except FileNotFoundError as e:
                print(f"\n[SKIP] {source} / {scenario_x} : {e}\n")
                continue

            rows.append({
                "source": source,
                "scenario_x": scenario_x,
                "delta_median": res["delta_median"],
                "ic90_low": res["ic90"][0],
                "ic90_high": res["ic90"][1],
                "ic95_low": res["ic95"][0],
                "ic95_high": res["ic95"][1],
                "bootstrap_severity": res["bootstrap_severity"],
                "n_boot": res["n_boot"],
                "n_sim_per_boot": N_SIM_PER_BOOT,
            })

    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "results_delta_dora_bootstrap.csv")

    fieldnames = [
        "source", "scenario_x", "delta_median", "ic90_low", "ic90_high",
        "ic95_low", "ic95_high", "bootstrap_severity", "n_boot", "n_sim_per_boot",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "=" * 70)
    print(f"Résultats sauvegardés dans : {output_file}")
    if not any(r["source"] == "OPRISK" for r in rows):
        print("ATTENTION : branche OPRISK absente (fichier data/raw manquant).")
    print("=" * 70)
