#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12 : SCR en EUROS par la cascade, calibre COMME LE MEMOIRE (SAS OpRisk / PRC).

Objectif : produire, dans le track exploratory, un SCR chiffre en euros directement
comparable a celui du memoire, mais en passant par la CASCADE dirigee des piliers au
lieu de l'architecture a 4 briques + copule de Gumbel.

PRINCIPE (aucune recalibration nouvelle). On reutilise TELS QUELS les modules du vrai
modele :
  - severite : src.aggregation.lda.simulate_remediation_severity (GPD spliced en euros,
    parametres OpRisk xi=0,595 / PRC xi=1,033 de src.utils.config) ;
  - frequence : NegBin (sur-dispersion phi=9,2) et multiplicateurs de scenario DORA de
    src.frequency.negbin.
On ne remplace QUE l'agregation. Chez le memoire, un incident = un tirage de severite.
Ici, un incident AMORCE se propage a un ensemble S de piliers (noyau auto-evitant,
gain g) et chaque pilier touche tire sa severite ; la severite de l'incident est la
somme. La cascade internalise donc mecaniquement la co-occurrence que le memoire porte
par la brique prestataire + copule de Gumbel.

LECTURE. A g=0 (aucune propagation, |S|=1) la cascade se reduit a UN tirage de severite
par incident : c'est exactement le LDA du memoire sans propagation, et le SCR obtenu
retombe dans la bande du memoire (controle de coherence ; rappel : l'IC90% du memoire
sur la VaR vaut deja un facteur ~2,5, le SCR est une distribution large, pas un point).
A g>0, l'ecart est la PRIME DE PROPAGATION : le surcout de capital du a la contagion
inter-piliers d'un meme incident. C'est la vue structurelle (bottom-up) en regard de la
vue copule (top-down) du memoire.

PORTEE. Meme calibration euro que le memoire, memes biais (OpRisk = grandes entites ;
PRC = severite derivee Jacobs, plafonnee a 40 M€). L'amorce se repartit sur les 5 piliers
DORA selon ROOT (dire d'expert de la cascade), la ou le memoire decompose par vecteur
Hackmageddon : seuls le NIVEAU de frequence et la loi de severite sont communs, pas la
structure de propagation. Rien n'est lu dans data/raw : tout vient de la config figee.

Sortie : diagnostics (SCR euro par source x gain, prime de propagation) + figure
G7_scr_euro_cascade.png.
"""

import os
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for _p in (REPO, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from src.aggregation.lda import simulate_remediation_severity   # noqa: E402
from src.frequency.negbin import compute_lambda_scenario         # noqa: E402
from src.utils.config import OPRISK, PRC, FREQUENCY, SCR_DORA     # noqa: E402
import scr_engine as eng                                          # noqa: E402  (cascade)

RNG = np.random.default_rng(20260715)
W = 74
ALPHA = 0.995
PHI = FREQUENCY["dispersion_factor"]        # 9.2
PIL = eng.PIL

# reference memoire (chapitre 5, entite 15 000 M€) : SCR total 4 briques, scenario S2
MEMOIRE_TOTAL = {"OPRISK": 9259.5, "PRC": 2772.7}

SEV = {
    "OPRISK": dict(xi=OPRISK["xi"], sigma=OPRISK["sigma_eur"], u=OPRISK["seuil_u_eur"],
                   p_u=OPRISK["p_u"], cap=None,
                   lam_ref=OPRISK["n_incidents"] / OPRISK["n_years"]),
    "PRC":    dict(xi=PRC["xi"], sigma=PRC["sigma_eur"], u=PRC["seuil_u_eur"],
                   p_u=PRC["p_u"], cap=SCR_DORA["cap_eur"],
                   lam_ref=FREQUENCY["lambda_ref"]),
}
NY = {"OPRISK": 150_000, "PRC": 50_000}     # PRC : lambda ~30x => moins d'annees suffisent


def titre(s):
    print("\n" + "=" * W + f"\n{s}\n" + "=" * W)


def simulate_euro(source, g, scenario, n_years, rng):
    """Perte annuelle en M€ par la cascade (VaR = SCR). Renvoie le vecteur des pertes."""
    sp = SEV[source]
    lam = compute_lambda_scenario(sp["lam_ref"], scenario, mode="center")["lambda_global"]
    r = lam / (PHI - 1.0)
    p = r / (r + lam)
    counts = rng.negative_binomial(r, p, size=n_years)      # incidents amorces / an
    T = int(counts.sum())
    annual = np.zeros(n_years)
    if T == 0:
        return annual
    year_of_event = np.repeat(np.arange(n_years), counts)
    tables = eng.build_cascade_tables(g)
    w = np.array([eng.LAMBDA[j] for j in PIL], float)
    w /= w.sum()                                            # amorce ~ ROOT
    amorce = rng.choice(len(PIL), size=T, p=w)
    for c_am, j in enumerate(PIL):
        ev = np.where(amorce == c_am)[0]
        if ev.size == 0:
            continue
        yr = year_of_event[ev]
        ind, probs = tables[j]
        idx = rng.choice(len(probs), size=ev.size, p=probs)
        for s in range(len(probs)):
            sel = idx == s
            if not sel.any():
                continue
            yrs = yr[sel]
            n_touch = int(ind[s].sum())                     # |S| pour cet ensemble
            for _ in range(n_touch):                        # un tirage de severite par pilier touche
                sev = simulate_remediation_severity(yrs.size, sp["xi"], sp["sigma"],
                                                     sp["u"], sp["p_u"], sp["cap"], rng)
                annual += np.bincount(yrs, weights=sev, minlength=n_years)
    return annual


def var(x, a=ALPHA):
    return float(np.quantile(x, a))


# ============================================================ SCR euro : g=0 (controle) vs g=0.9
titre("SCR en euros par la cascade, scenario S2 non-conforme (comme le memoire)")
print("  g=0 : aucune propagation (|S|=1) = le LDA du memoire sans propagation.")
print("  g=0,90 : cascade de base -> prime de propagation.")
print(f"  {'source':<9}{'g':>6}{'SCR euro (M EUR)':>18}{'reference memoire':>22}")
res = {}
for source in ("OPRISK", "PRC"):
    for g in (0.0, eng.G_BASE):
        v = var(simulate_euro(source, g, "S2_non_conforme", NY[source], RNG))
        res[(source, g)] = v
        tag = f"~{MEMOIRE_TOTAL[source]:.0f} M EUR (total)" if g == 0 else ""
        print(f"  {source:<9}{g:>6.2f}{v:>18.0f}{tag:>22}")

titre("Prime de propagation (surcout de capital du a la cascade)")
for source in ("OPRISK", "PRC"):
    v0, v9 = res[(source, 0.0)], res[(source, eng.G_BASE)]
    print(f"  {source:<9}: g=0 -> {v0:>8.0f}   g=0,90 -> {v9:>8.0f} M EUR   "
          f"prime = +{100*(v9/v0-1):.0f} %")
print("  g=0 tombe dans la bande du memoire (controle) ; la propagation inter-piliers")
print("  d'un incident rencherit le capital : contrepartie mecaniste de la brique")
print("  prestataire + copule de Gumbel du memoire (dependance modelisee, non ajoutee).")

# ============================================================ balayage du gain g (OpRisk)
titre("Effet du gain de propagation g sur le SCR euro (OpRisk, S2)")
print(f"  {'g':>6}{'SCR euro (M EUR)':>18}")
gcurve = {}
for g in (0.0, 0.3, 0.6, 0.9, 1.0):
    gcurve[g] = var(simulate_euro("OPRISK", g, "S2_non_conforme", 80_000, RNG))
    print(f"  {g:>6.2f}{gcurve[g]:>18.0f}")

# ============================================================ figure
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"],
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
})
INK, INK2 = "#0b0b0b", "#52514e"
ACCENT, BLUE, GREY = "#eb6834", "#2E5496", "#a9a79e"

fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.2, 5.2))

# panneau A : SCR euro vs g (OpRisk), avec repere memoire (total S2)
gs = sorted(gcurve)
axA.plot(gs, [gcurve[g] for g in gs], "-o", color=BLUE, lw=2.0, ms=4.5,
         label="cascade (OpRisk)")
axA.axhline(MEMOIRE_TOTAL["OPRISK"], color=ACCENT, ls="--", lw=1.3)
axA.text(1.0, MEMOIRE_TOTAL["OPRISK"], " SCR memoire (4 briques + copule)",
         ha="right", va="bottom", fontsize=8.5, color=ACCENT)
axA.set_xlabel("gain de propagation g", fontsize=9.5, color=INK2)
axA.set_ylabel("SCR = VaR 99,5 % (M€)", fontsize=9.5, color=INK2)
axA.set_title("(A)  A g=0, la cascade rejoint le memoire ; g>0 = prime de propagation",
              fontsize=10, color=INK, pad=6)
axA.legend(fontsize=8.6, frameon=False, loc="lower right")
axA.grid(alpha=0.25, lw=0.5)

# panneau B : barres memoire / cascade g=0 / cascade g=0.9, par source
srcs = ["OPRISK", "PRC"]
x = np.arange(len(srcs))
wbar = 0.26
mem = [MEMOIRE_TOTAL[s] for s in srcs]
c0 = [res[(s, 0.0)] for s in srcs]
c9 = [res[(s, eng.G_BASE)] for s in srcs]
axB.bar(x - wbar, mem, wbar, color=GREY, label="memoire (4 briques)")
axB.bar(x, c0, wbar, color=BLUE, label="cascade g=0 (sans propagation)")
axB.bar(x + wbar, c9, wbar, color=ACCENT, label="cascade g=0,90")
for i in range(len(srcs)):
    for xx, val in [(x[i]-wbar, mem[i]), (x[i], c0[i]), (x[i]+wbar, c9[i])]:
        axB.text(xx, val, f"{val:.0f}", ha="center", va="bottom", fontsize=7.8, color=INK)
axB.set_xticks(x)
axB.set_xticklabels(["OpRisk", "PRC"])
axB.set_ylabel("SCR = VaR 99,5 % (M€)", fontsize=9.5, color=INK2)
axB.set_title("(B)  SCR euro : memoire vs cascade, par source de severite",
              fontsize=10, color=INK, pad=6)
axB.legend(fontsize=8.2, frameon=False)
axB.grid(alpha=0.25, lw=0.5, axis="y")

fig.suptitle("SCR en euros par la cascade, calibre comme le memoire (SAS OpRisk / PRC)",
             fontsize=12.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.95])

outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "G7_scr_euro_cascade.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
