"""
scenarios/bootstrap_delta_dora.py
-----------------------------------
Bootstrap à DEUX NIVEAUX sur le Delta_DORA :

Niveau 1 — incertitude des MULTIPLICATEURS de scénario (tirage dans les
           fourchettes sourcées via compute_lambda_scenario).
Niveau 2 — incertitude des PARAMÈTRES DE SÉVÉRITÉ (xi, sigma), par
           rééchantillonnage bootstrap des excès GPD lorsque des données
           brutes cohérentes sont réellement chargées.

TRANSPARENCE MÉTHODOLOGIQUE
- PRC : seules les valeurs calibrées (xi, sigma, u, p_u) sont disponibles
  dans cet environnement ; la sévérité reste donc à point fixe.
- OPRISK : bootstrap réel possible uniquement sur le périmètre effectivement
  chargé. Le script affiche explicitement le nombre d'observations et bloque
  par défaut les usages manifestement trop larges pour une lecture cyber/DORA.
- Le résultat final est une distribution de Delta_DORA, jamais un point unique.
"""

import os
import sys
import warnings
from typing import Optional, Tuple, Dict, Any # <-- Add this line
import numpy as np
import pandas as pd
from scipy.stats import genpareto

warnings.filterwarnings("ignore")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.frequency.negbin import compute_lambda_scenario
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA


# ---------------------------------------------------------------------------
# 1. SIMULATION D'UNE ANNEE DE PERTES
# ---------------------------------------------------------------------------

def simulate_year_losses(
    lambda_annual: float,
    xi: float,
    sigma: float,
    u: float,
    p_u: float,
    dispersion: float,
    n_sim: int,
    severity_cap: Optional[float],
    rng,
) -> np.ndarray:
    """
    Simule n_sim pertes agrégées annuelles.
    p_u représente la part des événements qui tombent dans la queue GPD ;
    le corps est ici approché à 0 par simplification conservée du modèle.
    """
    if lambda_annual <= 0 or n_sim <= 0:
        return np.zeros(max(n_sim, 0), dtype=float)

    r = lambda_annual / (dispersion - 1) if dispersion > 1 else lambda_annual
    r = max(r, 1e-12)
    p = r / (r + lambda_annual)
    p = min(max(p, 1e-12), 1 - 1e-12)

    freqs = rng.negative_binomial(r, p, size=n_sim)
    total_events = int(freqs.sum())
    if total_events == 0:
        return np.zeros(n_sim, dtype=float)

    is_tail = rng.random(total_events) < p_u
    severities = np.zeros(total_events, dtype=float)
    n_tail = int(is_tail.sum())

    if n_tail > 0:
        u_vals = rng.uniform(0, 1, n_tail)
        sev_tail = u + genpareto.ppf(u_vals, c=xi, scale=sigma)
        if severity_cap is not None:
            sev_tail = np.minimum(sev_tail, severity_cap)
        severities[is_tail] = sev_tail

    splits = np.cumsum(freqs)[:-1]
    annual = np.array([chunk.sum() for chunk in np.split(severities, splits)], dtype=float)
    if len(annual) != n_sim:
        raise RuntimeError("La simulation n'a pas retourné n_sim pertes annuelles.")
    return annual


# ---------------------------------------------------------------------------
# 2. CHARGEMENT ET BOOTSTRAP GPD
# ---------------------------------------------------------------------------

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
    require_reasonable_scope: bool = True,
    max_excesses_without_filter_warning: int = 2000,
) -> Tuple[np.ndarray, float, Dict[str, Any]]:
    
    # ... [Code existant : initialisation et chargement excel] ...
    
    df = pd.read_excel(path, sheet_name="Datasets")
    df = _normalize_columns(df)

    # ---> AJOUTE LE FILTRE CYBER ICI <---
    cyber_cats = ['Systems Security', 'Systems']
    biz_cats   = ['Business Disruption and System Failures']
    
    if "Sub Risk Category" in df.columns and "Event Risk Category" in df.columns:
        mask_cyber = (
            df["Sub Risk Category"].isin(cyber_cats) |
            df["Event Risk Category"].isin(biz_cats)
        )
        df = df[mask_cyber].copy()

    candidate_loss_cols = [
        "Current Value of Loss ($M)",
        "Loss Amount ($M)",
        "Current Value of Loss (M)",
        "Loss Amount (M)",
        "Current Value of Loss",
        "Loss Amount",
    ]
    chosen_col = next((c for c in candidate_loss_cols if c in df.columns), None)
    if chosen_col is None:
        raise ValueError("Aucune colonne de perte reconnue dans la feuille 'Datasets'.")

    initial_n = len(df)
    sector_filter_applied = False
    sector_col = None

    possible_sector_cols = [
        "Industry Sector Name",
        "Industry",
        "Sector",
        "Industry Sector",
    ]
    sector_col = next((c for c in possible_sector_cols if c in df.columns), None)

    if finance_only and sector_col is not None:
        sector = df[sector_col].astype(str).str.lower()
        mask_fin = (
            sector.str.contains("finance", na=False)
            | sector.str.contains("financial", na=False)
            | sector.str.contains("insurance", na=False)
            | sector.str.contains("bank", na=False)
            | sector.str.contains("banking", na=False)
        )
        df = df.loc[mask_fin].copy()
        sector_filter_applied = True

    filtered_n = len(df)
    df["loss_musd"] = pd.to_numeric(df[chosen_col], errors="coerce")
    losses_musd = df["loss_musd"].dropna().to_numpy(dtype=float)
    excesses = losses_musd[losses_musd > u] - u

    if len(excesses) == 0:
        raise ValueError(f"Aucun excès au-dessus du seuil u={u} avec la colonne '{chosen_col}'.")

    metadata = {
        "sheet_name": "Datasets",
        "loss_column": chosen_col,
        "sector_column": sector_col,
        "finance_only": finance_only,
        "sector_filter_applied": sector_filter_applied,
        "initial_n_rows": int(initial_n),
        "filtered_n_rows": int(filtered_n),
        "n_losses": int(len(losses_musd)),
        "n_excesses": int(len(excesses)),
        "u": float(u),
    }

    print(f"[OpRisk] Feuille utilisée : {metadata['sheet_name']}")
    print(f"[OpRisk] Colonne utilisée : {metadata['loss_column']}")
    print(f"[OpRisk] Filtre finance demandé : {metadata['finance_only']}")
    print(f"[OpRisk] Filtre finance appliqué : {metadata['sector_filter_applied']}")
    if metadata["sector_column"] is not None:
        print(f"[OpRisk] Colonne secteur : {metadata['sector_column']}")
    print(f"[OpRisk] Lignes initiales : {metadata['initial_n_rows']}")
    print(f"[OpRisk] Lignes après filtre : {metadata['filtered_n_rows']}")
    print(f"[OpRisk] Nombre de pertes lues : {metadata['n_losses']}")
    print(f"[OpRisk] Nombre d'excès > u={u} : {metadata['n_excesses']}")

    if require_reasonable_scope and metadata["n_excesses"] > max_excesses_without_filter_warning:
        raise ValueError(
            "Périmètre OPRISK trop large pour une lecture cyber/DORA cohérente "
            f"({metadata['n_excesses']} excès > seuil d'alerte {max_excesses_without_filter_warning}). "
            "Ajoute un filtre explicite ou désactive require_reasonable_scope en assumant ce choix."
        )

    return excesses, u, metadata


def bootstrap_gpd_params(excesses: np.ndarray, rng) -> tuple:
    """Un tirage bootstrap (xi, sigma) par rééchantillonnage des excès réels."""
    n = len(excesses)
    sample = rng.choice(excesses, size=n, replace=True)
    xi_b, _, sigma_b = genpareto.fit(sample, floc=0)
    return float(xi_b), float(sigma_b)


# ---------------------------------------------------------------------------
# 3. BOOTSTRAP DEUX NIVEAUX
# ---------------------------------------------------------------------------

def bootstrap_delta_dora(
    source: str,
    scenario_x: str = "S2_non_conforme",
    scenario_ref: str = "S0_conforme",
    alpha: float = 0.995,
    n_boot: int = 500,
    n_sim_per_boot: int = 50_000,
    seed: int = 42,
    finance_only: bool = True,
    allow_large_oprisk_scope: bool = False,
) -> dict:
    rng = np.random.default_rng(seed)
    dispersion = FREQUENCY["dispersion_factor"]

    severity_note = ""
    severity_n_obs = None
    severity_scope = None
    excesses = None

    if source == "PRC":
        lambda_ref = FREQUENCY["lambda_ref"]
        xi0 = PRC["xi"]
        sigma0 = PRC["sigma_eur"]
        u0 = PRC["seuil_u_eur"]
        p_u0 = PRC["p_u"]
        cap = SCR_DORA.get("cap_eur", 40.0)
        bootstrap_severity = False
        severity_note = "point fixe (pas de données brutes PRC chargées ici)"
        severity_scope = "PRC calibrée"

    elif source == "OPRISK":
        lambda_ref = OPRISK["n_incidents"] / 27
        excesses, u0, meta = load_oprisk_excesses(
            u=OPRISK["seuil_u_eur"],
            finance_only=finance_only,
            require_reasonable_scope=not allow_large_oprisk_scope,
        )
        xi_fit, _, sigma_fit = genpareto.fit(excesses, floc=0)
        xi0 = float(xi_fit)
        sigma0 = float(sigma_fit)
        p_u0 = OPRISK["p_u"]
        cap = None
        bootstrap_severity = True
        severity_n_obs = int(len(excesses))
        severity_scope = (
            "OpRisk filtré finance" if meta.get("sector_filter_applied") else "OpRisk non filtré sectoriellement"
        )
        severity_note = f"bootstrap réel ({severity_n_obs} excès)"

    else:
        raise ValueError("source doit être 'PRC' ou 'OPRISK'")

    deltas, scr_ref_list, scr_x_list = [], [], []
    lambda_ref_list, lambda_x_list, mult_x_list = [], [], []

    for _ in range(n_boot):
        res_ref = compute_lambda_scenario(lambda_ref, scenario_ref, mode="sample", rng=rng)
        res_x = compute_lambda_scenario(lambda_ref, scenario_x, mode="sample", rng=rng)

        lam_ref = float(res_ref["lambda_global"])
        lam_x = float(res_x["lambda_global"])
        lambda_ref_list.append(lam_ref)
        lambda_x_list.append(lam_x)

        if "multiplicateur_global" in res_x:
            mult_x_list.append(float(res_x["multiplicateur_global"]))
        elif lambda_ref > 0:
            mult_x_list.append(lam_x / lambda_ref)
        else:
            mult_x_list.append(np.nan)

        if bootstrap_severity:
            xi_b, sigma_b = bootstrap_gpd_params(excesses, rng)
        else:
            xi_b, sigma_b = xi0, sigma0

        losses_ref = simulate_year_losses(
            lam_ref, xi_b, sigma_b, u0, p_u0, dispersion, n_sim_per_boot, cap, rng
        )
        losses_x = simulate_year_losses(
            lam_x, xi_b, sigma_b, u0, p_u0, dispersion, n_sim_per_boot, cap, rng
        )

        scr_ref = float(np.quantile(losses_ref, alpha))
        scr_x = float(np.quantile(losses_x, alpha))
        scr_ref_list.append(scr_ref)
        scr_x_list.append(scr_x)
        deltas.append(scr_x - scr_ref)

    deltas = np.array(deltas, dtype=float)
    lambda_ref_arr = np.array(lambda_ref_list, dtype=float)
    lambda_x_arr = np.array(lambda_x_list, dtype=float)
    mult_x_arr = np.array(mult_x_list, dtype=float)

    result = {
        "source": source,
        "scenario_x": scenario_x,
        "scenario_ref": scenario_ref,
        "bootstrap_severity": bootstrap_severity,
        "severity_note": severity_note,
        "severity_scope": severity_scope,
        "severity_n_obs": severity_n_obs,
        "n_boot": int(n_boot),
        "delta_median": float(np.median(deltas)),
        "delta_mean": float(np.mean(deltas)),
        "delta_std": float(np.std(deltas)),
        "ic90": np.percentile(deltas, [5, 95]).tolist(),
        "ic95": np.percentile(deltas, [2.5, 97.5]).tolist(),
        "scr_ref_median": float(np.median(scr_ref_list)),
        "scr_x_median": float(np.median(scr_x_list)),
        "lambda_ref_median": float(np.median(lambda_ref_arr)),
        "lambda_x_median": float(np.median(lambda_x_arr)),
        "mult_x_median": float(np.nanmedian(mult_x_arr)),
        "mult_x_ic90": np.nanpercentile(mult_x_arr, [5, 95]).tolist(),
        "distribution": deltas,
    }

    print(f"\n{'=' * 62}")
    print(f"  Δ_DORA — {source} — {scenario_ref} → {scenario_x}")
    print(f"{'=' * 62}")
    print(f"  Sévérité (niveau 2)        : {severity_note}")
    print(f"  Périmètre sévérité         : {severity_scope}")
    print(f"  Multiplicateurs (niveau 1) : ✓ bootstrap réel (fourchettes sourcées)")
    print(f"  λ {scenario_ref:18s} médian = {result['lambda_ref_median']:.3f}")
    print(f"  λ {scenario_x:18s} médian = {result['lambda_x_median']:.3f}")
    print(f"  Mult. {scenario_x:14s} médian = {result['mult_x_median']:.3f}")
    print(
        f"  Mult. {scenario_x:14s} IC90%  = "
        f"[{result['mult_x_ic90'][0]:.3f} ; {result['mult_x_ic90'][1]:.3f}]"
    )
    print(f"  n_boot = {n_boot} × n_sim = {n_sim_per_boot:,}")
    print(f"\n  SCR {scenario_ref:18s} (médiane) = {result['scr_ref_median']:>10.1f} M€")
    print(f"  SCR {scenario_x:18s} (médiane) = {result['scr_x_median']:>10.1f} M€")
    print(f"\n  Δ_DORA médiane = {result['delta_median']:.1f} M€")
    print(f"  Δ_DORA IC90%   = [{result['ic90'][0]:.1f} ; {result['ic90'][1]:.1f}] M€")
    print(f"  Δ_DORA IC95%   = [{result['ic95'][0]:.1f} ; {result['ic95'][1]:.1f}] M€")
    print(f"{'=' * 62}\n")

    return result


# ---------------------------------------------------------------------------
# 4. GRILLE COMPLETE
# ---------------------------------------------------------------------------

def full_bootstrap_grid(
    n_boot: int = 300,
    n_sim_per_boot: int = 30_000,
    finance_only: bool = True,
    allow_large_oprisk_scope: bool = False,
) -> pd.DataFrame:
    rows = []
    for source in ["PRC", "OPRISK"]:
        for scenario_x in ["S1_partiel", "S2_non_conforme"]:
            res = bootstrap_delta_dora(
                source=source,
                scenario_x=scenario_x,
                n_boot=n_boot,
                n_sim_per_boot=n_sim_per_boot,
                finance_only=finance_only,
                allow_large_oprisk_scope=allow_large_oprisk_scope,
            )
            rows.append(
                {
                    "Source": source,
                    "Scénario": scenario_x,
                    "Δ médiane (M€)": res["delta_median"],
                    "IC90% bas": res["ic90"][0],
                    "IC90% haut": res["ic90"][1],
                    "Bootstrap sévérité": "Oui" if res["bootstrap_severity"] else "Non",
                    "Note sévérité": res["severity_note"],
                    "Périmètre": res["severity_scope"],
                }
            )

    df = pd.DataFrame(rows)
    print("\n" + "=" * 70)
    print("  GRILLE FINALE — Δ_DORA (M€), deux sources x deux scénarios")
    print("=" * 70)
    print(df.to_string(index=False))
    print("\n  → Le Δ_DORA n'est jamais un nombre unique : il dépend du scénario")
    print("    de conformité et de la source/périmètre de sévérité retenu.")
    return df


if __name__ == "__main__":
    bootstrap_delta_dora("PRC", "S1_partiel", n_boot=200, n_sim_per_boot=30_000)
    bootstrap_delta_dora("OPRISK", "S1_partiel", n_boot=200, n_sim_per_boot=30_000)
