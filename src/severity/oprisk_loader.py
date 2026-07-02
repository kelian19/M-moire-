"""
severity/oprisk_loader.py
--------------------------
Chargement CENTRALISÉ des excès OpRisk. Remplace les deux versions divergentes
qui existaient dans notebooks/03 et scenarios/bootstrap_delta_dora.py.

Règles (une seule vérité) :
  - périmètre : cyber (Systems Security / Systems | Business Disruption) × Finance
  - conversion USD -> EUR appliquée UNE SEULE FOIS, à l'ingestion
  - retourne des excès EXPRIMÉS EN EUR au-dessus du seuil u (en M€)
"""

import os
from typing import Optional, Tuple, Dict, Any

import numpy as np
import pandas as pd

from src.utils.config import OPRISK

CYBER_SUB_CATS = ["Systems Security", "Systems"]
CYBER_EVENT_CATS = ["Business Disruption and System Failures"]
ABERRATION_THRESHOLD_MUSD = 100_000  # M$ — au-delà = erreur de saisie


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _default_path() -> str:
    return os.path.join(
        _project_root(), "data", "raw", "SAS_OpRisk_Global_Data_June_2026.xlsx"
    )


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )
    return df


def load_oprisk_excesses(
    u: Optional[float] = None,
    finance_only: bool = True,
    path: Optional[str] = None,
) -> Tuple[np.ndarray, float, Dict[str, Any]]:
    """
    Charge les excès OpRisk (cyber×finance) au-dessus du seuil u, EN EUR (M€).

    Returns
    -------
    excesses : np.ndarray  (montants EUR au-dessus de u, en M€)
    u        : float       (seuil effectif, M€)
    metadata : dict        (traçabilité du filtrage)
    """
    u = OPRISK["seuil_u_eur"] if u is None else float(u)
    path = path or _default_path()
    usd_eur = OPRISK.get("usd_eur", 0.92)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Fichier OpRisk introuvable : {path}\n"
            "Place la base sous data/raw/ (gitignorée car sous licence Nexialog)."
        )

    df = pd.read_excel(path, sheet_name="Datasets")
    df = _normalize_columns(df)

    # --- colonne de perte (USD, en M$) ---
    candidate_loss_cols = [
        "Loss Amount ($M)", "Current Value of Loss ($M)",
        "Loss Amount (M)", "Current Value of Loss (M)",
    ]
    loss_col = next((c for c in candidate_loss_cols if c in df.columns), None)
    if loss_col is None:
        raise ValueError("Aucune colonne de perte reconnue dans la feuille 'Datasets'.")

    initial_n = len(df)
    df["loss_musd"] = pd.to_numeric(df[loss_col], errors="coerce")
    df = df[(df["loss_musd"] > 0) & (df["loss_musd"] < ABERRATION_THRESHOLD_MUSD)]

    # --- filtre cyber ---
    mask_cyber = pd.Series(False, index=df.index)
    if "Sub Risk Category" in df.columns:
        mask_cyber |= df["Sub Risk Category"].isin(CYBER_SUB_CATS)
    if "Event Risk Category" in df.columns:
        mask_cyber |= df["Event Risk Category"].isin(CYBER_EVENT_CATS)
    df = df[mask_cyber].copy()

    # --- filtre finance ---
    sector_filter_applied = False
    sector_col = next(
        (c for c in ["Industry Sector Name", "Industry", "Sector", "Industry Sector"]
         if c in df.columns),
        None,
    )
    if finance_only and sector_col is not None:
        s = df[sector_col].astype(str).str.lower()
        mask_fin = (
            s.str.contains("financ", na=False)
            | s.str.contains("insurance", na=False)
            | s.str.contains("bank", na=False)
        )
        df = df[mask_fin].copy()
        sector_filter_applied = True

    # --- conversion EUR (UNE fois) et excès ---
    losses_eur = df["loss_musd"].to_numpy(dtype=float) * usd_eur
    excesses = losses_eur[losses_eur > u] - u

    if len(excesses) == 0:
        raise ValueError(f"Aucun excès au-dessus du seuil u={u} M€ (EUR).")

    metadata = {
        "path": path,
        "loss_column": loss_col,
        "sector_column": sector_col,
        "finance_only": finance_only,
        "sector_filter_applied": sector_filter_applied,
        "usd_eur": usd_eur,
        "initial_n_rows": int(initial_n),
        "n_incidents_scope": int(len(df)),
        "n_excesses": int(len(excesses)),
        "u": float(u),
    }
    return excesses, u, metadata
