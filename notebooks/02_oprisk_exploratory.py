"""
notebooks/02_oprisk_exploratory.py
-----------------------------------
Lance l'analyse exploratoire complète de la base SAS OpRisk Global.

Usage : python notebooks/02_oprisk_exploratory.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.severity.oprisk_analysis import full_report

OPRISK_PATH = "data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx"

if __name__ == "__main__":
    if not os.path.exists(OPRISK_PATH):
        print(f"⚠ Fichier non trouvé : {OPRISK_PATH}")
        print("  Placer le fichier dans data/raw/ (gitignored).")
    else:
        results = full_report(OPRISK_PATH)
        print(f"\nRésumé : {results['n_total']:,} incidents | "
              f"{results['n_cyber']:,} cyber/ICT | "
              f"{results['n_cyber_finance']} cyber×finance")
