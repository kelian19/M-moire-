"""
src/scenarios/sensitivity.py
----------------------------
Étude de sensibilité du SCR Cyber (modèle LDA).
Génère un graphique Tornado mesurant l'impact des hypothèses expertes :
  1. Choc sur la fréquence de base (λ ± 10%)
  2. Choc sur le paramètre de forme de la queue (ξ ± 10%)
  3. Modification du plafond de réassurance (Severity Cap : 30 M€ vs 60 M€)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.scenarios.delta_dora import simulate_lda_vectorized, empirical_var

# =====================================================================
# CONFIGURATION VISUELLE
# =====================================================================
BRAND_BLUE = "#2563eb"
BRAND_RED = "#dc2626"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Montserrat', 'Arial', 'sans-serif']
plt.rcParams['text.color'] = BRAND_DARK
plt.rcParams['axes.facecolor'] = BRAND_LIGHT
plt.rcParams['figure.facecolor'] = BRAND_LIGHT


# =====================================================================
# 1. MOTEUR DE SENSIBILITÉ
# =====================================================================
def run_sensitivity_analysis():
    print("Lancement de l'étude de sensibilité (Monte Carlo 500k sims)...")
    
    n_sim = 500_000
    alpha = 0.995
    
    # Paramètres de base (calibrés sur tes logs OpRisk S2)
    base_lambda = 52.5
    base_cap = 40.0
    base_gpd = {
        "xi": 0.60,
        "sigma": 20.0,
        "u": 20.03,
        "p_u": 0.05, 
        "dispersion_factor": 9.2
    }
    
    # 1. Calcul de la Baseline (Référence)
    losses_base = simulate_lda_vectorized(base_lambda, base_gpd, n_sim, seed=42, severity_cap=base_cap)
    scr_base = empirical_var(losses_base, alpha)
    print(f"SCR de Référence : {scr_base:.1f} M€")
    
    results = []
    
    # 2. Scénarios de Chocs
    scenarios = {
        "Fréquence (λ) ±10%": {
            "low": {"lambda": base_lambda * 0.9, "cap": base_cap, "xi": base_gpd["xi"]},
            "high": {"lambda": base_lambda * 1.1, "cap": base_cap, "xi": base_gpd["xi"]}
        },
        "Plafond Sévérité (Cap) [30 vs 60 M€]": {
            "low": {"lambda": base_lambda, "cap": 30.0, "xi": base_gpd["xi"]},
            "high": {"lambda": base_lambda, "cap": 60.0, "xi": base_gpd["xi"]}
        },
        "Épaisseur file d'attente (ξ) ±10%": {
            "low": {"lambda": base_lambda, "cap": base_cap, "xi": base_gpd["xi"] * 0.9},
            "high": {"lambda": base_lambda, "cap": base_cap, "xi": base_gpd["xi"] * 1.1}
        }
    }
    
    for param_name, shocks in scenarios.items():
        # Choc à la baisse
        gpd_low = base_gpd.copy(); gpd_low["xi"] = shocks["low"]["xi"]
        l_low = simulate_lda_vectorized(shocks["low"]["lambda"], gpd_low, n_sim, seed=42, severity_cap=shocks["low"]["cap"])
        scr_low = empirical_var(l_low, alpha)
        
        # Choc à la hausse
        gpd_high = base_gpd.copy(); gpd_high["xi"] = shocks["high"]["xi"]
        l_high = simulate_lda_vectorized(shocks["high"]["lambda"], gpd_high, n_sim, seed=42, severity_cap=shocks["high"]["cap"])
        scr_high = empirical_var(l_high, alpha)
        
        results.append({
            "Paramètre": param_name,
            "Baisse (SCR)": scr_low - scr_base,
            "Hausse (SCR)": scr_high - scr_base
        })
        print(f"  > {param_name} : [{scr_low:.1f} M€ ; {scr_high:.1f} M€]")
        
    return pd.DataFrame(results), scr_base

# =====================================================================
# 2. GRAPHIQUE TORNADO
# =====================================================================
def plot_tornado(df: pd.DataFrame, scr_base: float, save_name: str = "tornado_sensitivity.png"):
    # Trier par impact absolu maximum (pour la forme de la tornade)
    df['Max_Impact'] = df[['Baisse (SCR)', 'Hausse (SCR)']].abs().max(axis=1)
    df = df.sort_values('Max_Impact', ascending=True).drop('Max_Impact', axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    y_pos = np.arange(len(df))
    
    # Barres pour les chocs à la hausse
    ax.barh(y_pos, df['Hausse (SCR)'], color=BRAND_BLUE, height=0.5, label='Choc à la Hausse (Pire cas)')
    # Barres pour les chocs à la baisse
    ax.barh(y_pos, df['Baisse (SCR)'], color='#94a3b8', height=0.5, label='Choc à la Baisse (Cas favorable)')
    
    # Ligne de base (zéro)
    ax.axvline(0, color=BRAND_DARK, linewidth=1.5, linestyle='--')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['Paramètre'], fontsize=11, fontweight='semibold')
    
    ax.set_xlabel(f"Variation du SCR par rapport à la base ({scr_base:,.0f} M€)", fontsize=11, fontweight='semibold')
    ax.set_title("Analyse de Sensibilité du Capital Requis (Tornado Chart)", fontsize=14, fontweight='bold', pad=15)
    
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor=BRAND_LIGHT, edgecolor='#e2e8f0', loc='lower right')
    import seaborn as sns
    sns.despine(left=True)
    
    out_dir = os.path.join(PROJECT_ROOT, "outputs", "figures")
    os.makedirs(out_dir, exist_ok=True)
    save_path = os.path.join(out_dir, save_name)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nGraphique Tornado sauvegardé : {save_path}")

if __name__ == "__main__":
    df_results, base = run_sensitivity_analysis()
    plot_tornado(df_results, base)