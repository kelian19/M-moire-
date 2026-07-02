"""
notebooks/03_bootstrap_delta_dora.py  (ex 03_oprisk_sanity_check.py)
-------------------------------------------------------------------
Runner mince : lance le bootstrap Δ_DORA CANONIQUE (3 briques + copule).
Toute la logique vit dans src/scenarios/bootstrap_delta_dora.py — ce fichier
ne fait qu'orchestrer, il ne redéfinit PLUS le moteur.

Usage : python notebooks/03_bootstrap_delta_dora.py
"""

# Après `pip install -e .`, ces deux lignes sont inutiles. Gardées par sécurité.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scenarios.bootstrap_delta_dora import (
    bootstrap_delta_dora,
    full_bootstrap_grid,
)

if __name__ == "__main__":
    # Grille complète : 2 sources × 2 scénarios (reproduit le tableau §4.4)
    df = full_bootstrap_grid(n_boot=300, n_sim_per_boot=30_000)

    out = os.path.join(os.path.dirname(__file__), "results_delta_dora_grid.csv")
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"\nGrille Δ_DORA sauvegardée : {out}")