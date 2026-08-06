#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
51 : le SCR robuste (pire-cas) sur l'ensemble d'ambiguite.

Reponse prudente a la remarque de Caroline (script 46) : plutot que le quantile d'un point
estime, on prend la BORNE HAUTE de la VaR sur un ensemble d'ambiguite, c'est-a-dire l'ensemble
des modeles plausibles compte tenu de l'incertitude. On la construit sur deux couches :
  - AMBIGUITE DE PARAMETRE : la region de confiance de (xi, sigma) (bootstrap OpRisk) ;
  - AMBIGUITE DE MODELE : la famille de queue (jusqu'a une GPD lourde xi=0,90, script 48).

VaR ROBUSTE au niveau de confiance beta = quantile beta de la loi bootstrap de la VaR
(= 'la VaR qu'on ne depasse pas avec probabilite beta, compte tenu du risque d'estimation').
C'est une VaR distributionnellement robuste sur la region de confiance des parametres.

L'echelle des postures : point < predictive < robuste(parametre) < robuste(parametre+modele).
Le niveau de robustesse beta est un CHOIX de politique prudentielle, a assumer explicitement.

Sortie : diagnostics + figure J7_scr_robuste.png.
"""

import os
import sys

import numpy as np
from scipy.stats import genpareto, norm
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for _p in (REPO, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from src.severity.oprisk_analysis import load_clean, filter_cyber, filter_finance, USD_EUR  # noqa: E402
from src.utils.config import OPRISK                                                        # noqa: E402

WID = 82
A = 0.995
B = 3000
N_SIM = 3_000_000
SEED = 20260727
rng = np.random.default_rng(SEED)


def titre(s):
    print("\n" + "=" * WID + f"\n{s}\n" + "=" * WID)


def var_gpd(a, xi, sig, u, zu):
    return u + (sig / xi) * (((1 - a) / zu) ** (-xi) - 1)


# ------------------------------------------------------------------ calibration + ambiguite
d = filter_finance(filter_cyber(load_clean(
    os.path.join(REPO, "data", "raw", "SAS_OpRisk_Global_Data_June_2026.xlsx"))))
loss = np.sort(d["loss"].to_numpy() * USD_EUR)
# SEUIL PUBLIE, PAS SEUIL REDERIVE. Comme les scripts 46 et 47, celui-ci prenait le q85 des
# donnees courantes (22,03 M€, 88 exces) alors que le memoire publie la calibration figee
# (20,03 M€, 91 exces) : la VaR robuste etait donc construite sur un ensemble d'ambiguite
# autour d'un ajustement autre que celui du memoire.
u = float(OPRISK["seuil_u_eur"]); zu = float((loss > u).mean())
exc = loss[loss > u] - u; n = exc.size
xi_hat, _, sig_hat = genpareto.fit(exc, floc=0)

xb, sb = [], []
for _ in range(B):
    r = rng.choice(exc, size=n, replace=True)
    try:
        c, _, s = genpareto.fit(r, floc=0)
        if 0 < s < 1e6 and -0.5 < c < 3:
            xb.append(c); sb.append(s)
    except Exception:
        pass
xb, sb = np.array(xb), np.array(sb)

titre("Calibration et ensemble d'ambiguite (OpRisk cyber x finance)")
print(f"  u = {u:.1f} M€, {n} exces ; xi = {xi_hat:.3f}, sigma = {sig_hat:.1f}.")
print(f"  Bootstrap : {len(xb)} ajustements ; xi IC90 = [{np.percentile(xb,5):.2f} ; "
      f"{np.percentile(xb,95):.2f}].")

# ------------------------------------------------------------------ l'echelle des postures
var_point = var_gpd(A, xi_hat, sig_hat, u, zu)
idx = rng.integers(0, len(xb), N_SIM)
exc_pred = genpareto.rvs(c=xb[idx], scale=sb[idx], random_state=rng)
var_pred = u + float(np.quantile(exc_pred, 1 - (1 - A) / zu))
var_boot = var_gpd(A, xb, sb, u, zu)                       # loi de la VaR sur l'ambiguite param.
rob = {b: float(np.percentile(var_boot, 100 * b)) for b in (0.90, 0.95, 0.99)}
var_heavy = var_gpd(A, 0.90, sig_hat, u, zu)               # pire-cas famille (queue lourde 48)

titre("L'echelle des postures : du point au pire-cas")
print(f"  {'posture':<40}{'VaR 99,5 % (M€)':>16}")
print(f"  {'point (branchement xi_hat)':<40}{var_point:>16.0f}")
print(f"  {'predictive (melange, script 46)':<40}{var_pred:>16.0f}")
for b, v in rob.items():
    print(f"  {'robuste parametre (beta=%.0f%%)' % (100*b):<40}{v:>16.0f}")
print(f"  {'robuste parametre+modele (xi=0,90)':<40}{var_heavy:>16.0f}")
print(f"\n  La VaR robuste a 95 % ({rob[0.95]:.0f} M€) est {rob[0.95]/var_point:.1f}x le point")
print(f"  ({var_point:.0f}) : c'est la marge de prudence pour le risque d'ESTIMATION. Le pire-cas")
print(f"  de MODELE (queue lourde, {var_heavy:.0f} M€) ajoute la prudence sur le CHOIX de famille.")

titre("VERDICT")
print("  1. Le SCR robuste = borne haute de la VaR sur l'ensemble d'ambiguite (parametre, puis")
print("     modele). Il repond a Caroline par la PRUDENCE : on ne parie pas sur un point.")
print(f"  2. Echelle : point {var_point:.0f} -> predictive {var_pred:.0f} -> robuste 95 % "
      f"{rob[0.95]:.0f} -> pire-cas modele {var_heavy:.0f} M€.")
print("  3. Le niveau de robustesse beta est un CHOIX prudentiel explicite, pas un calcul : on")
print("     l'affiche, on ne le cache pas. C'est l'exact complement de la lecture en bande.")

# ------------------------------------------------------------------ figure J7
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"], "font.size": 10.5,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb", "axes.edgecolor": "#c3c2b7",
    "axes.linewidth": 0.8, "text.color": "#0b0b0b", "axes.labelcolor": "#52514e",
    "xtick.color": "#898781", "ytick.color": "#898781", "axes.grid": False,
})
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
ACCENT, BLUE, GREEN = "#eb6834", "#256abf", "#3d8361"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 5.2))

# (a) loi de la VaR sur l'ambiguite de parametre, avec les postures
ax1.hist(var_boot, bins=60, color=BLUE, alpha=0.5, edgecolor="#fcfcfb")
for lab, v, c in [("point", var_point, INK), ("prédictive", var_pred, GREEN),
                  ("robuste 95 %", rob[0.95], ACCENT)]:
    ax1.axvline(v, color=c, lw=1.8, ls="--" if lab != "point" else "-")
    ax1.text(v, ax1.get_ylim()[1] * (0.9 if lab == "point" else 0.75 if lab == "prédictive" else 0.6),
             f" {lab}\n {v:.0f}", fontsize=8, color=c)
ax1.set_xlabel("VaR 99,5 % (M€) sur l'ambiguïté de paramètre", color=INK2)
ax1.set_ylabel("fréquence (bootstrap)", color=INK2)
ax1.set_title("(a)  La VaR est elle-même incertaine :\nle robuste en prend la borne haute",
              fontsize=11, color=INK, pad=8)

# (b) l'echelle des postures
labs = ["point", "prédictive", "robuste\n90 %", "robuste\n95 %", "robuste\n99 %", "pire-cas\nmodèle"]
vals = [var_point, var_pred, rob[0.90], rob[0.95], rob[0.99], var_heavy]
cols = [INK, GREEN, "#9dc3e6", BLUE, "#184f95", ACCENT]
xp = np.arange(len(labs))
ax2.bar(xp, vals, color=cols, alpha=0.9)
for x_, v in zip(xp, vals):
    ax2.text(x_, v + 30, f"{v:.0f}", ha="center", fontsize=8.5, color=INK2)
ax2.set_xticks(xp); ax2.set_xticklabels(labs, fontsize=8.5)
ax2.set_ylabel("VaR 99,5 % (M€)", color=INK2)
ax2.set_title("(b)  L'échelle des postures :\ndu point au pire-cas", fontsize=11, color=INK, pad=8)

for ax in (ax1, ax2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.suptitle("J7 : le SCR robuste, borne haute de la VaR sur l'ambiguïté ; la prudence sur le risque "
             "d'estimation et de modèle, assumée",
             fontsize=11.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.93])
outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "J7_scr_robuste.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
