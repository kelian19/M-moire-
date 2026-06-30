"""
scenarios/bootstrap_delta_dora.py
-----------------------------------
Bootstrap à DEUX NIVEAUX sur le Delta_DORA :

  Niveau 1 — incertitude des MULTIPLICATEURS de scénario (ENISA/Ponemon/
             Microsoft Research), tirage uniforme dans les fourchettes
             sourcées (cf. docs/calibration_multiplicateurs.md).
  Niveau 2 — incertitude des PARAMÈTRES DE SÉVÉRITÉ (ξ, σ), par
             rééchantillonnage bootstrap des excès GPD.

⚠️ TRANSPARENCE MÉTHODOLOGIQUE :
  - OpRisk : bootstrap RÉEL, rééchantillonnage des 570 incidents bruts
    (data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx, ou cache local).
  - PRC : SEUL le point de calibration (ξ=1.30, σ=0.257 M€) est disponible
    dans cet environnement — les données brutes PRC ne sont pas chargées.
    Le niveau 2 (incertitude de sévérité) n'est donc PAS bootstrappé pour
    PRC ; seul le niveau 1 (multiplicateurs) l'est. Ceci est signalé
    explicitement dans les résultats, conformément au principe : ne jamais
    présenter une incertitude qu'on n'a pas réellement quantifiée.

Résultat final : la distribution de Delta_DORA, pas un point.
"""

import numpy as np
import pandas as pd
from typing import Optional, Tuple
from scipy.stats import genpareto, nbinom
import sys, os, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.frequency.negbin import (
    HACKMAGEDDON_PROPORTIONS, MULTIPLICATEURS_DORA, compute_lambda_scenario
)
from src.utils.config import PRC, OPRISK, FREQUENCY, SCR_DORA


# ---------------------------------------------------------------------------
# 1. SIMULATION D'UNE ANNÉE DE PERTES (fréquence x sévérité, p_u appliqué)
# ---------------------------------------------------------------------------

def simulate_year_losses(lambda_annual: float, xi: float, sigma: float,
                          u: float, p_u: float, dispersion: float,
                          n_sim: int, severity_cap: float, rng) -> np.ndarray:
    """
    Simule n_sim pertes agrégées annuelles.
    p_u est appliqué correctement (fraction des événements en queue GPD,
    le reste en corps approximé à 0 — cf. correction du bug d'hier soir).
    """
    r = lambda_annual / (dispersion - 1) if dispersion > 1 else lambda_annual
    p = r / (r + lambda_annual)

    freqs = rng.negative_binomial(r, p, size=n_sim)
    total_events = int(freqs.sum())

    is_tail = rng.random(total_events) < p_u
    severities = np.zeros(total_events)
    n_tail = int(is_tail.sum())
    if n_tail > 0:
        u_vals = rng.uniform(0, 1, n_tail)
        sev_tail = u + genpareto.ppf(u_vals, c=xi, scale=sigma)
        if severity_cap is not None:
            sev_tail = np.minimum(sev_tail, severity_cap)
        severities[is_tail] = sev_tail

    splits = np.cumsum(freqs)[:-1]
    return np.array([s.sum() for s in np.split(severities, splits)])


# ---------------------------------------------------------------------------
# 2. BOOTSTRAP GPD SUR DONNÉES RÉELLES (OpRisk uniquement)
# ---------------------------------------------------------------------------

def load_oprisk_excesses(u: Optional[float] = None) -> Tuple[np.ndarray, float]:
    """
    Charge les excès réels OpRisk au-dessus du seuil, sur le périmètre
    cyber×finance UNIQUEMENT (et non toute la base opérationnelle).

    Périmètre cyber×finance (582 incidents attendus) :
      - Sub Risk Category ∈ {Systems Security, Systems}
      - ET secteur financier (Industry Sector Name contient 'Financial')

    Le chemin est résolu relativement à la racine du projet, pas en dur,
    pour rester portable d'un environnement à l'autre.
    """
    u = OPRISK["seuil_u_eur"] if u is None else float(u)

    # Chemin robuste : racine projet = deux niveaux au-dessus de ce fichier
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    path = os.path.join(
        project_root, "data", "raw", "SAS_OpRisk_Global_Data_June_2026.xlsx"
    )
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Fichier OpRisk introuvable : {path}\n"
            "Place la base sous data/raw/ (gitignorée car sous licence)."
        )

    df = pd.read_excel(path, sheet_name="Datasets")

    # Normalisation des noms de colonnes
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )

    # --- Colonne de perte ---
    candidate_loss_cols = [
        "Loss Amount ($M)",
        "Current Value of Loss ($M)",
        "Loss Amount (M)",
        "Current Value of Loss (M)",
    ]
    chosen_col = next((c for c in candidate_loss_cols if c in df.columns), None)
    if chosen_col is None:
        raise ValueError("Aucune colonne de perte reconnue dans 'Datasets'.")

    # --- FILTRAGE PÉRIMÈTRE CYBER × FINANCE (la correction clé) ---
    df["loss_musd"] = pd.to_numeric(df[chosen_col], errors="coerce")
    df = df[(df["loss_musd"] > 0) & (df["loss_musd"] < 100_000)]  # retire aberrations

    mask_cyber = df["Sub Risk Category"].isin(["Systems Security", "Systems"])
    mask_fin = df["Industry Sector Name"].apply(
        lambda v: "Financial" in str(v) if pd.notna(v) else False
    )
    df_cyber = df[mask_cyber & mask_fin].copy()

    # Conversion USD → EUR
    usd_eur = OPRISK.get("usd_eur", 0.92)
    losses_eur = df_cyber["loss_musd"].to_numpy(dtype=float) * usd_eur

    excesses = losses_eur[losses_eur > u] - u

    if len(excesses) == 0:
        raise ValueError(f"Aucun excès au-dessus du seuil u={u} M€.")

    print(f"[OpRisk] Périmètre cyber×finance : {len(df_cyber)} incidents")
    print(f"[OpRisk] Colonne perte : {chosen_col} (×{usd_eur} USD→EUR)")
    print(f"[OpRisk] Excès > u={u} M€ : {len(excesses)}")

    return excesses, u


def bootstrap_gpd_params(excesses: np.ndarray, rng) -> tuple:
    """Un tirage bootstrap (ξ, σ) par rééchantillonnage des excès réels."""
    n = len(excesses)
    sample = rng.choice(excesses, size=n, replace=True)
    xi_b, _, sigma_b = genpareto.fit(sample, floc=0)
    return xi_b, sigma_b


# ---------------------------------------------------------------------------
# 3. BOOTSTRAP DEUX NIVEAUX — UNE SOURCE DE SÉVÉRITÉ
# ---------------------------------------------------------------------------

def bootstrap_delta_dora(source: str, scenario_x: str = "S2_non_conforme",
                         scenario_ref: str = "S0_conforme",
                         alpha: float = 0.995,
                         n_boot: int = 500,
                         n_sim_per_boot: int = 50_000,
                         seed: int = 42) -> dict:

    rng = np.random.default_rng(seed)
    dispersion = FREQUENCY["dispersion_factor"]

    if source == "PRC":
        lambda_ref = FREQUENCY["lambda_ref"]
        xi0, sigma0, u0, p_u0 = PRC["xi"], PRC["sigma_eur"], PRC["seuil_u_eur"], PRC["p_u"]
        cap = SCR_DORA.get("cap_eur", 40.0)
        bootstrap_severity = False
        excesses = None
    elif source == "OPRISK":
        lambda_ref = OPRISK["n_incidents"] / 27
        excesses, u0 = load_oprisk_excesses()
        xi_fit, _, sigma_fit = genpareto.fit(excesses, floc=0)
        xi0, sigma0 = xi_fit, sigma_fit
        p_u0 = OPRISK["p_u"]
        cap = None
        bootstrap_severity = True
    else:
        raise ValueError("source doit être 'PRC' ou 'OPRISK'")

    deltas, scr_ref_list, scr_x_list = [], [], []
    lambda_ref_list, lambda_x_list = [], []
    mult_x_list = []

    for i in range(n_boot):
        res_ref = compute_lambda_scenario(lambda_ref, scenario_ref, mode="sample", rng=rng)
        res_x = compute_lambda_scenario(lambda_ref, scenario_x, mode="sample", rng=rng)

        lam_ref, lam_x = res_ref["lambda_global"], res_x["lambda_global"]
        lambda_ref_list.append(lam_ref)
        lambda_x_list.append(lam_x)

        if "multiplicateur_global" in res_x:
            mult_x_list.append(res_x["multiplicateur_global"])
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

        scr_ref = np.quantile(losses_ref, alpha)
        scr_x = np.quantile(losses_x, alpha)

        scr_ref_list.append(scr_ref)
        scr_x_list.append(scr_x)
        deltas.append(scr_x - scr_ref)

    deltas = np.array(deltas)
    lambda_ref_arr = np.array(lambda_ref_list)
    lambda_x_arr = np.array(lambda_x_list)
    mult_x_arr = np.array(mult_x_list, dtype=float)

    result = {
        "source": source,
        "scenario_x": scenario_x,
        "scenario_ref": scenario_ref,
        "bootstrap_severity": bootstrap_severity,
        "n_boot": n_boot,
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

    flag = "✓ bootstrap réel (570 obs)" if bootstrap_severity else "⚠ point fixe (pas de données brutes ici)"
    print(f"\n{'='*62}")
    print(f"  Δ_DORA — {source} — {scenario_ref} → {scenario_x}")
    print(f"{'='*62}")
    print(f"  Sévérité (niveau 2)        : {flag}")
    print(f"  Multiplicateurs (niveau 1) : ✓ bootstrap réel (fourchettes sourcées)")
    print(f"  λ {scenario_ref:18s} médian = {result['lambda_ref_median']:.3f}")
    print(f"  λ {scenario_x:18s} médian = {result['lambda_x_median']:.3f}")
    print(f"  Mult. {scenario_x:14s} médian = {result['mult_x_median']:.3f}")
    print(f"  Mult. {scenario_x:14s} IC90%  = [{result['mult_x_ic90'][0]:.3f} ; {result['mult_x_ic90'][1]:.3f}]")
    print(f"  n_boot = {n_boot} × n_sim = {n_sim_per_boot:,}")
    print(f"\n  SCR {scenario_ref:18s} (médiane) = {result['scr_ref_median']:>10.1f} M€")
    print(f"  SCR {scenario_x:18s} (médiane) = {result['scr_x_median']:>10.1f} M€")
    print(f"\n  Δ_DORA médiane = {result['delta_median']:.1f} M€")
    print(f"  Δ_DORA IC90%   = [{result['ic90'][0]:.1f} ; {result['ic90'][1]:.1f}] M€")
    print(f"  Δ_DORA IC95%   = [{result['ic95'][0]:.1f} ; {result['ic95'][1]:.1f}] M€")
    print(f"{'='*62}\n")

    return result


# ---------------------------------------------------------------------------
# 4. GRILLE COMPLÈTE — DEUX SOURCES x DEUX SCÉNARIOS
# ---------------------------------------------------------------------------

def full_bootstrap_grid(n_boot: int = 300, n_sim_per_boot: int = 30_000) -> pd.DataFrame:
    """
    Exécute le bootstrap deux niveaux pour {PRC, OpRisk} x {S1, S2}.
    Produit le tableau central du mémoire : la distribution du Δ_DORA
    sous chaque combinaison source x scénario, jamais un point unique.
    """
    rows = []
    for source in ["PRC", "OPRISK"]:
        for scenario_x in ["S1_partiel", "S2_non_conforme"]:
            res = bootstrap_delta_dora(source, scenario_x,
                                        n_boot=n_boot, n_sim_per_boot=n_sim_per_boot)
            rows.append({
                "Source": source,
                "Scénario": scenario_x,
                "Δ médiane (M€)": res["delta_median"],
                "IC90% bas": res["ic90"][0],
                "IC90% haut": res["ic90"][1],
                "Bootstrap sévérité": "Oui" if res["bootstrap_severity"] else "Non (point fixe)",
            })

    df = pd.DataFrame(rows)
    print("\n" + "="*70)
    print("  GRILLE FINALE — Δ_DORA (M€), deux sources x deux scénarios")
    print("="*70)
    print(df.to_string(index=False))
    print("\n  → Le Δ_DORA n'est jamais un nombre : il varie selon le scénario")
    print("    de conformité ET selon la source de sévérité retenue.")
    return df


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    bootstrap_delta_dora("OPRISK", "S1_partiel", n_boot=200, n_sim_per_boot=30_000)
    bootstrap_delta_dora("PRC", "S1_partiel", n_boot=200, n_sim_per_boot=30_000)
