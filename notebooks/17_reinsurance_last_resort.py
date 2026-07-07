"""
17_reinsurance_last_resort.py
-----------------------------
IMPLICATIONS POUR LA RÉASSURANCE CYBER — L'ASSURABILITÉ DE DERNIER RECOURS
(chantier « Prix SCOR »).

Résultat central : pour une sévérité GPD, le coût espéré au-delà d'un point
d'attachement a est
        E[(X-a)_+] = ∫_a^∞ S(x) dx < ∞   ⇔   ξ < 1,
où S(x) = ζ_u (1 + ξ(x-u)/σ)^{-1/ξ} est la survie POT. La source PRC
(ξ = 1,03) est donc dans le régime d'ESPÉRANCE INFINIE : un traité en excédent
de sinistre ILLIMITÉ y a une prime pure infinie — seuls des layers PLAFONNÉS
sont tarifables. C'est le rôle structurel du réassureur (porter, mais borner,
la queue non assurable). La source OpRisk (ξ = 0,60) reste, elle, assurable.

Ce script quantifie :
  1. le coût espéré de cession E[(X-C)_+] par sinistre, selon le plafond C ;
  2. la prime pure d'un layer plafonné [C, C+ℓ] selon sa largeur ℓ ;
  3. l'effet d'un plafond sur l'Expected Shortfall retenu.

Sorties :
  outputs/tables/results_reinsurance.csv
  outputs/figures/reinsurance_last_resort.png

Autonome (calibrations figées dans config.py).
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import integrate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config import OPRISK, PRC

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_GREEN = "#059669"
BRAND_RED = "#dc2626"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

SOURCES = {
    "OpRisk": dict(xi=OPRISK["xi"], sigma=OPRISK["sigma_eur"], u=OPRISK["seuil_u_eur"],
                   zeta=OPRISK["p_u"], color=BRAND_BLUE),
    "PRC": dict(xi=PRC["xi"], sigma=PRC["sigma_eur"], u=PRC["seuil_u_eur"],
                zeta=PRC["p_u"], color=BRAND_ORANGE),
}
CAP_MODELE = 40.0  # plafond de sévérité PRC du mémoire (M€)


def survie(x, p):
    """Survie POT S(x) = zeta * (1 + xi (x-u)/sigma)^(-1/xi) pour x > u."""
    x = np.asarray(x, dtype=float)
    z = 1.0 + p["xi"] * (x - p["u"]) / p["sigma"]
    return np.where(x <= p["u"], p["zeta"], p["zeta"] * z ** (-1.0 / p["xi"]))


def excess_cost(a, p, upper):
    """E[(X-a)_+] tronqué à la borne 'upper' : ∫_a^upper S(x) dx (subdivisé pour
    rester stable sur de très grandes plages à queue lourde)."""
    a = max(a, p["u"])
    # découpe log pour éviter la sous-estimation de quad sur [a, 1e9]
    edges = [a] + [10.0 ** k for k in range(int(np.ceil(np.log10(max(a, 1) + 1))), 10)
                   if 10.0 ** k < upper] + [upper]
    edges = sorted(set(e for e in edges if a <= e <= upper))
    total = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        v, _ = integrate.quad(lambda x: survie(x, p), lo, hi, limit=200)
        total += v
    return total


def excess_cost_analytic(a, p):
    """Forme fermée E[(X-a)_+] = zeta*sigma*w_a^{1-1/xi}/(1-xi) si xi<1, sinon +inf."""
    if p["xi"] >= 1.0:
        return np.inf
    a = max(a, p["u"])
    w = 1.0 + p["xi"] * (a - p["u"]) / p["sigma"]
    return p["zeta"] * p["sigma"] * w ** (1.0 - 1.0 / p["xi"]) / (1.0 - p["xi"])


def layer_cost(a, l, p):
    """Prime pure d'un layer plafonné [a, a+l] : ∫_a^{a+l} S(x) dx (toujours finie)."""
    a = max(a, p["u"])
    val, _ = integrate.quad(lambda x: survie(x, p), a, a + l, limit=200)
    return val


def main():
    print("=" * 78)
    print("  RÉASSURANCE CYBER : ASSURABILITÉ DE DERNIER RECOURS")
    print("=" * 78)

    # --- 1. Divergence du coût illimité E[(X-C)_+] selon la borne ---
    print("\n  Coût espéré illimité E[(X-C)_+] par sinistre, C = 40 M€,")
    print("  intégré jusqu'à une borne croissante (met en évidence la divergence PRC) :")
    print(f"  {'borne (M€)':>12} {'OpRisk':>12} {'PRC':>12}")
    rows = []
    for upper in [1e3, 1e4, 1e5, 1e6, 1e8]:
        c_op = excess_cost(CAP_MODELE, SOURCES["OpRisk"], upper)
        c_prc = excess_cost(CAP_MODELE, SOURCES["PRC"], upper)
        print(f"  {upper:>12.0e} {c_op:>12.3f} {c_prc:>12.3f}")
        rows.append(dict(borne=upper, excess_oprisk=c_op, excess_prc=c_prc))

    # Coût illimité "convergé" (forme analytique)
    c_op_inf = excess_cost_analytic(CAP_MODELE, SOURCES["OpRisk"])
    c_prc_inf = excess_cost_analytic(CAP_MODELE, SOURCES["PRC"])
    print(f"\n  OpRisk (xi<1) : E[(X-40)_+] converge -> {c_op_inf:.3f} M€/sinistre (fini)")
    print(f"  PRC   (xi>=1) : E[(X-40)_+] = {c_prc_inf} -> non assurable en excédent illimité")

    # --- 2. Prime pure d'un layer plafonné [40, 40+l] selon la largeur l ---
    print("\n  Prime pure d'un layer [40, 40+l] (M€/sinistre) :")
    print(f"  {'largeur l':>12} {'OpRisk':>12} {'PRC':>12}")
    layer_rows = []
    for l in [40, 160, 460, 960, 9960]:  # plafonds 80, 200, 500, 1000, 10000
        lo = layer_cost(CAP_MODELE, l, SOURCES["OpRisk"])
        lp = layer_cost(CAP_MODELE, l, SOURCES["PRC"])
        print(f"  {l:>12.0f} {lo:>12.3f} {lp:>12.3f}")
        layer_rows.append(dict(largeur=l, layer_oprisk=lo, layer_prc=lp))

    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    pd.DataFrame(rows).to_csv(os.path.join(out_dir, "results_reinsurance.csv"), index=False)
    print(f"\nCSV : {os.path.join(out_dir, 'results_reinsurance.csv')}")

    # --- Figure : 2 panneaux ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Panneau A : DIVERGENCE PAR TRONCATURE — coût E[(X-40)_+] tronqué à T, vs T
    Ts = np.logspace(3, 12, 60)
    for name, p in SOURCES.items():
        vals = [excess_cost(CAP_MODELE, p, T) for T in Ts]
        ax1.plot(Ts, vals, lw=2.2, color=p["color"],
                 label=f"{name} ($\\xi={p['xi']:.2f}$)")
    # asymptote finie OpRisk
    ax1.axhline(c_op_inf, color=BRAND_BLUE, ls=":", lw=1.2,
                label=f"asymptote OpRisk = {c_op_inf:.1f} M€ (finie)")
    ax1.set_xscale("log")
    ax1.set_xlabel("Borne de troncature $T$ (M€, éch.\\ log)", fontsize=11)
    ax1.set_ylabel(r"$\int_{40}^{T} S(x)\,dx$ — co\^ut cédé tronqué (M€/sinistre)", fontsize=10)
    ax1.set_title("Divergence du coût de cession illimité\n"
                  "(OpRisk plafonne ; PRC croît sans borne $\\Rightarrow$ non assurable)",
                  fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9); ax1.grid(alpha=0.3, which="both")

    # Panneau B : prime pure d'un layer plafonné [40, 40+l] vs largeur l
    ls = np.linspace(10, 5000, 120)
    for name, p in SOURCES.items():
        vals = [layer_cost(CAP_MODELE, l, p) for l in ls]
        ax2.plot(CAP_MODELE + ls, vals, lw=2.2, color=p["color"],
                 label=f"{name} ($\\xi={p['xi']:.2f}$)")
    ax2.set_xlabel(r"Plafond supérieur du layer $C+\ell$ (M€)", fontsize=11)
    ax2.set_ylabel(r"Prime pure du layer $[40,\,C+\ell]$ (M€/sinistre)", fontsize=10)
    ax2.set_title("Prime d'un layer plafonné selon sa hauteur\n"
                  "(OpRisk plafonne ; PRC croît sans borne = divergence)",
                  fontsize=12, fontweight="bold")
    ax2.legend(fontsize=10); ax2.grid(alpha=0.3)

    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "reinsurance_last_resort.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")


if __name__ == "__main__":
    main()
