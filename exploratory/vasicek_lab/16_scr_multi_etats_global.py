#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
16a : SCR_DORA par etat de conformite (3 etats GLOBAUX) + Delta_DORA en euros.

Prolonge le script 13 : la ou 13 comparait 2 etats (conforme S0 vs non-conforme S2),
on etablit ici le SCR pour les TROIS etats de conformite de l'entite, alignes sur les
trois scenarios sources de src.frequency.negbin :

    C  (conforme)               <- S0_conforme     (multiplicateur 1,00)
    PC (partiellement conforme) <- S1_partiel       (multiplicateurs bornes S1)
    NC (non conforme)           <- S2_non_conforme  (multiplicateurs bornes S2)

Etat GLOBAL a l'entite (tous les piliers dans le meme etat). C'est le cas particulier
"piliers alignes" du modele par pilier (16b, a venir) : decision B validee, mise en
scene global d'abord. Aucun taux de transition ici : un etat est une configuration
figee, la dynamique markovienne est l'etape 17.

DEUX CANAUX de conformite (comme 13) :
  1. FREQUENCE : l'etat pilote lambda via les multiplicateurs sources (canal du memoire).
  2. PROPAGATION : une entite plus conforme CONTIENT mieux la contagion -> gain g plus
     faible. Canal propre a la cascade (Vasicek dirige).
On presente donc DEUX lectures :
  - lecture A (frequence seule) : g identique aux 3 etats (g=0,90), seul lambda change.
    C'est la lecture directement comparable au memoire.
  - lecture B (frequence + propagation) : g croit de C a NC (contenue -> relachee).
    C'est l'apport de la cascade.

Delta_DORA(etat) = SCR(etat) - SCR(C), a graine MC COMMUNE entre etats (common random
numbers : l'ecart ne vient que du changement d'etat, pas du bruit Monte-Carlo). Le
Delta_DORA de tete est NC vs C ; PC vs C donne le surcout intermediaire.
Bootstrap 2 niveaux (multiplicateurs + severite) comme 13/14 pour l'IC90 honnete.

PORTEE. Meme calibration euro et memes biais que le memoire. Severite euros = SAS OpRisk
(branche via euro_cascade_model). Le triplet de gains (g_C, g_PC, g_NC) de la lecture B
est un CHOIX de modelisation non calibre (monotone, g_NC=0,90 de base) : presente en
lecture separee, pas comme une mesure. Ne touche ni src/ ni memoire/.

Sortie : diagnostics (SCR par etat, 2 lectures ; Delta_DORA + IC90) + figure
S10_scr_multi_etats.png. Verifie exit 0.
"""

import os
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import euro_cascade_model as ec                              # noqa: E402
from euro_cascade_model import PARAMS, MEMOIRE_DELTA, var    # noqa: E402

W = 74

# --- les 3 etats globaux : scenario source + gain de propagation par lecture -------
ETATS = ["C", "PC", "NC"]
LABEL = {"C": "Conforme", "PC": "Partiellement conforme", "NC": "Non conforme"}
SCENARIO = {"C": "S0_conforme", "PC": "S1_partiel", "NC": "S2_non_conforme"}

G_FREQ = {"C": 0.90, "PC": 0.90, "NC": 0.90}     # lecture A : g constant (canal frequence seul)
G_PROP = {"C": 0.45, "PC": 0.68, "NC": 0.90}     # lecture B : g croit de C a NC (choix, non calibre)

BOOT = {"OPRISK": dict(B=120, ny=20_000), "PRC": dict(B=60, ny=3_000)}
NY_DET = 80_000                                   # resolution des SCR deterministes


def titre(s):
    print("\n" + "=" * W + f"\n{s}\n" + "=" * W)


def scr_state(source, etat, g, xi, sigma, ny, seed):
    """SCR (VaR 99,5 %) d'un etat de conformite, graine donnee (CRN entre etats)."""
    sp = PARAMS[source]
    lam = ec.lambda_scenario(source, SCENARIO[etat], mode="center")
    rng = np.random.default_rng(seed)
    return var(ec.simulate_euro(lam, g, xi, sigma, sp["u"], sp["p_u"], sp["cap"], ny, rng))


# ============================================================ SCR par etat (deterministe)
titre("SCR_DORA par etat de conformite (deterministe, graine MC commune entre etats)")
scr_det = {}   # scr_det[(source, lecture, etat)] = SCR
for source in ("OPRISK", "PRC"):
    sp = PARAMS[source]
    print(f"\n  {source}  (severite {source}, entite type du memoire)")
    print(f"  {'etat':<26}{'SCR lect.A (freq)':>20}{'SCR lect.B (freq+prop)':>24}")
    seed_src = 4242
    for etat in ETATS:
        va = scr_state(source, etat, G_FREQ[etat], sp["xi"], sp["sigma"], NY_DET, seed_src)
        vb = scr_state(source, etat, G_PROP[etat], sp["xi"], sp["sigma"], NY_DET, seed_src)
        scr_det[(source, "A", etat)] = va
        scr_det[(source, "B", etat)] = vb
        print(f"  {LABEL[etat]:<26}{va:>18.0f} M{vb:>22.0f} M")
    # deltas vs C
    for lect in ("A", "B"):
        c = scr_det[(source, lect, "C")]
        d_pc = scr_det[(source, lect, "PC")] - c
        d_nc = scr_det[(source, lect, "NC")] - c
        print(f"    lecture {lect} : Delta_DORA(PC vs C) = {d_pc:6.0f} M   "
              f"Delta_DORA(NC vs C) = {d_nc:6.0f} M")


# ============================================================ Delta_DORA bootstrap (canal frequence)
titre("Delta_DORA bootstrap 2 niveaux (canal FREQUENCE, lecture A, g=0,90 fixe)")
print("  Comparable au memoire : la conformite agit sur la frequence (S0/S1/S2).")
boot = {}   # boot[(source, cible)] = array de Delta_DORA, cible in {PC, NC}
for source in ("OPRISK", "PRC"):
    cfg = BOOT[source]
    sp = PARAMS[source]
    orng = np.random.default_rng(20260716)
    acc = {"PC": [], "NC": []}
    for b in range(cfg["B"]):
        # niveau 1 : multiplicateurs (S0 fixe (1,1) ; S1, S2 tires dans leurs bornes)
        lam = {e: ec.lambda_scenario(source, SCENARIO[e], mode="sample", rng=orng) for e in ETATS}
        # niveau 2 : severite (xi, sigma dans IC90)
        xi_b, sg_b = ec.sample_severity_params(source, orng)
        seed_b = 2000 + b                                    # meme graine tous etats -> CRN
        v = {}
        for e in ETATS:
            rng_e = np.random.default_rng(seed_b)
            v[e] = var(ec.simulate_euro(lam[e], G_FREQ[e], xi_b, sg_b,
                                        sp["u"], sp["p_u"], sp["cap"], cfg["ny"], rng_e))
        acc["PC"].append(v["PC"] - v["C"])
        acc["NC"].append(v["NC"] - v["C"])
    for cible in ("PC", "NC"):
        d = np.array(acc[cible])
        boot[(source, cible)] = d
        med = np.median(d)
        lo, hi = np.percentile(d, [5, 95])
        print(f"\n  {source} - Delta_DORA({cible} vs C)  "
              f"({cfg['B']} tirages x {cfg['ny']:,} annees) :")
        print(f"    median = {med:8.0f} M EUR   IC90% [{lo:.0f} ; {hi:.0f}]   "
              f"part > 0 : {100.0 * (d > 0).mean():.0f}%")
    ref = MEMOIRE_DELTA[source]
    print(f"    memoire (NC vs C, 07) = {ref['median']:8.0f} M EUR   "
          f"IC90% [{ref['ic90'][0]:.0f} ; {ref['ic90'][1]:.0f}]")


# ============================================================ figure
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"],
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
})
INK, INK2 = "#0b0b0b", "#52514e"
ACCENT, BLUE, GREEN, GREY = "#eb6834", "#2E5496", "#2E6B4F", "#a9a79e"

fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.4, 5.3))

# panneau A : echelle du SCR sur les 3 etats (OpRisk), 2 lectures
x = np.arange(len(ETATS))
ya = [scr_det[("OPRISK", "A", e)] for e in ETATS]
yb = [scr_det[("OPRISK", "B", e)] for e in ETATS]
axA.plot(x, ya, "-o", color=BLUE, lw=2.0, ms=6, label="lecture A (frequence seule)")
axA.plot(x, yb, "-s", color=GREEN, lw=2.0, ms=6, label="lecture B (frequence + propagation)")
for xi_, va_, vb_ in zip(x, ya, yb):
    axA.annotate(f"{va_:.0f}", (xi_, va_), textcoords="offset points", xytext=(0, 8),
                 ha="center", fontsize=8, color=BLUE)
    axA.annotate(f"{vb_:.0f}", (xi_, vb_), textcoords="offset points", xytext=(0, -14),
                 ha="center", fontsize=8, color=GREEN)
_lo = min(min(ya), min(yb))
_hi = max(max(ya), max(yb))
axA.set_ylim(_lo - 0.10 * (_hi - _lo), _hi + 0.08 * (_hi - _lo))
axA.set_xlim(-0.25, len(ETATS) - 0.75)
axA.set_xticks(x)
axA.set_xticklabels([LABEL[e] for e in ETATS], fontsize=9)
axA.set_ylabel("SCR_DORA (M€)", fontsize=9.5, color=INK2)
axA.set_title("(A)  SCR par etat de conformite (OpRisk)", fontsize=10, color=INK, pad=6)
axA.legend(fontsize=8.2, frameon=False, loc="upper left")
axA.grid(alpha=0.25, lw=0.5)

# panneau B : distribution bootstrap du Delta_DORA (NC vs C, OpRisk) + repere memoire
d_op = boot[("OPRISK", "NC")]
cut = float(np.percentile(d_op, 95))
n_omis = int((d_op > cut).sum())
axB.hist(d_op[d_op <= cut], bins=40, density=True, color=BLUE, alpha=0.55,
         label="cascade (bootstrap)")
axB.axvline(np.median(d_op), color=BLUE, lw=1.6, label=f"median cascade {np.median(d_op):.0f}")
ref = MEMOIRE_DELTA["OPRISK"]
axB.axvline(ref["median"], color=ACCENT, lw=1.6, ls="--", label=f"median memoire {ref['median']:.0f}")
axB.set_xlim(0, cut)
axB.text(0.98, 0.55, f"{n_omis}/{len(d_op)} tirages > {cut:.0f}\nomis (lisibilite)",
         transform=axB.transAxes, ha="right", va="top", fontsize=7.8, color=INK2)
axB.set_xlabel("Delta_DORA NC vs C (M€)", fontsize=9.5, color=INK2)
axB.set_ylabel("densite", fontsize=9.5, color=INK2)
axB.set_title("(B)  Delta_DORA bootstrap, canal frequence (OpRisk)", fontsize=10, color=INK, pad=6)
axB.legend(fontsize=8.2, frameon=False)
axB.grid(alpha=0.25, lw=0.5)

fig.suptitle("SCR_DORA par etat de conformite (3 etats globaux) et Delta_DORA par la cascade",
             fontsize=12.3, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.95])

outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "S10_scr_multi_etats.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
