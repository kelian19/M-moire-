"""
notebooks/01_oprisk_gpd_calibration.py
---------------------------------------
Exploration et calibration GPD sur SAS OpRisk Global Data.
À convertir en notebook Jupyter si besoin : jupyter nbconvert --to notebook

Usage : python notebooks/01_oprisk_gpd_calibration.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.severity.gpd import (
    mean_excess, fit_gpd, calibration_report,
    bootstrap_gpd, cross_validate, hill_estimator
)
from src.utils.config import OPRISK, PRC


# ---------------------------------------------------------------------------
# 1. CHARGEMENT ET FILTRAGE
# ---------------------------------------------------------------------------

def load_oprisk(path: str) -> pd.DataFrame:
    """
    Charge et filtre la base OpRisk sur le périmètre cyber × finance.
    Périmètre : Systems Security + Business Disruption, secteur Financial.
    """
    df = pd.read_excel(path, sheet_name='Datasets')

    cyber_cats = ['Systems Security', 'Systems']
    biz_cats   = ['Business Disruption and System Failures']

    df_cyber = df[
        (df['Sub Risk Category'].isin(cyber_cats) |
         df['Event Risk Category'].isin(biz_cats)) &
        (df['Industry Sector Name'].apply(
            lambda v: 'Financial' in str(v) if pd.notna(v) else False))
    ].copy()

    df_cyber['loss_eur_M'] = pd.to_numeric(
        df_cyber['Loss Amount ($M)'], errors='coerce') * 0.92  # USD→EUR

    df_cyber['year'] = pd.to_datetime(
        df_cyber['First Year of Event'], errors='coerce').dt.year

    # Filtrer >= 2000 pour limiter le biais inflation
    df_recent = df_cyber[
        (df_cyber['year'] >= 2000) &
        (df_cyber['loss_eur_M'] > 0)
    ].dropna(subset=['loss_eur_M'])

    print(f"OpRisk chargé : {len(df_recent)} incidents cyber×finance (2000–2026)")
    print(f"Pertes (M€) : médiane={df_recent['loss_eur_M'].median():.2f} | "
          f"max={df_recent['loss_eur_M'].max():.0f}")
    return df_recent


# ---------------------------------------------------------------------------
# 2. MEAN EXCESS PLOT
# ---------------------------------------------------------------------------

def plot_mean_excess(losses: np.ndarray, save_path: str = None):
    """Visualise le Mean Excess Plot pour choisir le seuil u."""
    thresholds = [np.percentile(losses, p) for p in range(50, 96, 2)]
    mep = mean_excess(losses, thresholds)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(mep['u'], mep['e_u'], 'o-', color='#2E5496', linewidth=2,
            markersize=5, label='e(u) = E[X−u | X>u]')
    ax.axvline(OPRISK['seuil_u_eur'], color='#C00000', linestyle='--', linewidth=1.5,
               label=f"Seuil retenu u = {OPRISK['seuil_u_eur']:.1f} M€ (pct 85%)")
    ax.set_xlabel('Seuil u (M€)', fontsize=11)
    ax.set_ylabel('Excès moyen e(u) (M€)', fontsize=11)
    ax.set_title('Mean Excess Plot — OpRisk Cyber×Finance', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure sauvegardée : {save_path}")
    else:
        plt.show()
    return fig


# ---------------------------------------------------------------------------
# 3. STABILITÉ DE ξ
# ---------------------------------------------------------------------------

def plot_xi_stability(losses: np.ndarray, save_path: str = None):
    """Visualise la stabilité de ξ̂ en fonction du seuil u."""
    from scipy.stats import genpareto

    pcts = range(60, 95, 2)
    data = []
    for p in pcts:
        u = np.percentile(losses, p)
        exc = losses[losses > u] - u
        if len(exc) < 20:
            continue
        xi, _, _ = genpareto.fit(exc, floc=0)
        data.append({'pct': p, 'u': u, 'xi': xi, 'n': len(exc)})

    df = pd.DataFrame(data)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(df['u'], df['xi'], 'o-', color='#2E5496', linewidth=2, markersize=5)
    ax1.axhline(1.0, color='#C00000', linestyle='--', alpha=0.7, label='ξ = 1 (E[X] = ∞)')
    ax1.axhline(0.0, color='grey', linestyle=':', alpha=0.5, label='ξ = 0 (exponentielle)')
    ax1.axvline(OPRISK['seuil_u_eur'], color='orange', linestyle='--',
                label=f'u retenu = {OPRISK["seuil_u_eur"]:.1f} M€')
    ax1.set_xlabel('Seuil u (M€)'); ax1.set_ylabel('ξ̂')
    ax1.set_title('Stabilité de ξ̂ vs seuil u'); ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3)

    ax2.plot(df['u'], df['n'], 's-', color='#1F3864', linewidth=2, markersize=5)
    ax2.axhline(30, color='#C00000', linestyle='--', alpha=0.7, label='n minimum = 30')
    ax2.set_xlabel('Seuil u (M€)'); ax2.set_ylabel('Nombre d\'excès')
    ax2.set_title('Nombre d\'excès vs seuil u'); ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

    plt.suptitle('Diagnostic GPD — OpRisk Cyber×Finance', fontsize=13, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    return fig


# ---------------------------------------------------------------------------
# 4. HILL PLOT (VALIDATION ALTERNATIVE)
# ---------------------------------------------------------------------------

def plot_hill(losses: np.ndarray, reference_xi: float = 0.60, save_path: str = None):
    """Trace le Hill Plot avec bande de confiance asymptotique à 90%."""
    df_hill = hill_estimator(losses, k_max=200)

    # Bande de confiance asymptotique : Var(xi_hill(k)) ~= xi_hill^2 / k (Hill, 1975)
    z90 = 1.645
    se = df_hill["xi_hill"] / np.sqrt(df_hill["k"])
    ic_low = df_hill["xi_hill"] - z90 * se
    ic_high = df_hill["xi_hill"] + z90 * se

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(df_hill["k"], ic_low, ic_high, color="#2563eb", alpha=0.15,
                     label="IC asymptotique 90%")
    ax.plot(df_hill["k"], df_hill["xi_hill"], color="#2563eb", linewidth=2, label="Estimateur de Hill")
    ax.axhline(y=reference_xi, color="#dc2626", linestyle="--", linewidth=1.5,
               label=f"MLE (Référence = {reference_xi:.2f})")
    ax.set_xlabel("Nombre d'extrêmes retenus (k)", fontsize=11)
    ax.set_ylabel("Estimation de ξ (Indice de queue)", fontsize=11)
    ax.set_title("Hill Plot avec IC90% - SAS OpRisk Global Data", fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure sauvegardée : {save_path}")
    else:
        plt.show()
    return fig


# ---------------------------------------------------------------------------
# 5. VALIDATION CROISÉE — TABLEAU COMPARATIF
# ---------------------------------------------------------------------------

def print_cross_validation():
    """Affiche la comparaison PRC vs OpRisk pour le mémoire."""
    print("\n" + "="*65)
    print("  VALIDATION CROISÉE — PRC 2025 vs SAS OpRisk Global")
    print("="*65)
    print(f"  {'Paramètre':20s} {'PRC 2025':>15s} {'OpRisk (2000–2026)':>20s}")
    print(f"  {'-'*55}")
    print(f"  {'Seuil u':20s} {'0.128 M€ (128k€)':>15s} {'20.03 M€':>20s}")
    print(f"  {'ξ̂ (queue)':20s} {'1.300':>15s} {OPRISK['xi']:>20.4f}")
    print(f"  {'IC90% ξ':20s} {'—':>15s} {str(OPRISK['xi_ic90']):>20s}")
    print(f"  {'σ̂':20s} {'0.257 M€':>15s} {OPRISK['sigma_eur']:>20.2f} M€")
    print(f"  {'VaR 99.5% IC90%':20s} {'—':>15s} {str(OPRISK['var_995_ic90']):>20s}")
    print(f"  {'n excès':20s} {'—':>15s} {OPRISK['n_excess']:>20d}")
    print()
    print("  Lecture :")
    print("  → Même famille Pareto (ξ > 0) confirmée sur deux sources indépendantes")
    print("  → ξ_PRC (1.30) > ξ_OpRisk (0.60) : cohérent avec le biais de taille OpRisk")
    print("     Les grandes entités absorbent mieux les chocs → queue apparemment plus légère")
    print("  → Validation QUALITATIVE : ✓  Validation QUANTITATIVE : impossible")
    print()
    print("  DEUX SOURCES COMPLÉMENTAIRES (pas de hiérarchie 'primaire') :")
    print("  • Sévérité : OpRisk fournit des montants RÉELS (biais grandes entités)")
    print("              PRC + Jacobs couvre un spectre de tailles plus large (sévérité dérivée)")
    print("  • Fréquence : PRC reste la source de référence (périmètre défini)")
    print("  → La convergence qualitative des deux renforce le choix d'une GPD à queue lourde")
    print("="*65 + "\n")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Charger OpRisk (adapter le chemin)
    OPRISK_PATH = "data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx"

    if not os.path.exists(OPRISK_PATH):
        print(f"⚠ Fichier non trouvé : {OPRISK_PATH}")
        print("  Placer le fichier dans data/raw/ (gitignored)")
        print("  Les paramètres calibrés sont dans src/utils/config.py")
        print_cross_validation()
    else:
        df = load_oprisk(OPRISK_PATH)
        losses = df['loss_eur_M'].values

        # 1. Mean Excess Plot
        plot_mean_excess(losses, save_path='outputs/figures/mean_excess_oprisk.png')

        # 2. Stabilité ξ (MLE) — diagnostic GPD (stabilité + nombre d'excès)
        plot_xi_stability(losses, save_path='outputs/figures/diagnostic_gpd_oprisk.png')

        # 3. Estimateur de Hill avec IC90% (Validation)
        plot_hill(losses, reference_xi=OPRISK['xi'], save_path='outputs/figures/hill_plot_ic90_oprisk.png')

        # 4. Calibration GPD (Rapport console)
        u = OPRISK['seuil_u_eur']
        report = calibration_report(losses, u,
                                    source='OpRisk Cyber×Finance (2000–2026)',
                                    currency='M€',
                                    n_boot=2000)

        # 5. Validation croisée
        print_cross_validation()