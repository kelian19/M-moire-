#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
43 : des KPI DESCRIPTIFS aux KPI PILOTABLES, par attribution de l'ecart de capital DORA.

Les cas d'usage 08e/08f/08g et le script 39 ont produit des KPI OBSERVABLES par pilier :
  P2  delai de notification         (mediane 94 j, 85 % au-dela de l'echeance DORA d'un mois)
  P3  duree de confinement          (mediane 7 j, ~49 % au-dela d'une semaine)
  P4  concentration tiers           (Gini 0,69 ; 20 % des sinistres sur 1,7 % des jours)
  freq frequence d'entree           (calibree, 08b)
Ils DECRIVENT le risque. Ce script les rend PILOTABLES : chacun est rattache a un CANAL du
moteur de capital, et l'on mesure le CAPITAL EN JEU derriere ce KPI, c'est-a-dire l'ecart de
SCR entre l'etat conforme (cible DORA) et l'etat non conforme. On obtient un tableau de bord
de REMEDIATION : quel KPI, ramene a sa cible DORA, libere le plus de capital.

QUATRE CANAUX, QUATRE KPI (etats C -> NC deja dans le modele, scripts 16/39/38) :
  frequence    lam        S0 conforme      -> S2 non conforme
  detection    p_u        x0,85 (P2/P3)    -> x1,20
  propagation  g          0,45             -> 0,90         (le canal NON identifie : W)
  accumulation P4         choc commun 0    -> phi_cs = gamma = 0,68  (P4, script 38/42)

DISCIPLINE DU MEMOIRE. On isole chaque canal (les autres restant conformes) et on lit sa
contribution en BANDE, pas en point : detection et frequence sont calibrables (bande etroite),
propagation et accumulation ne le sont pas (bande large, = la limite d'identification). Le KPI
observable ancre l'entite sur l'echelle C..NC ; l'attribution dit ce que vaut, en capital, de
le ramener a la cible DORA.

Sortie : diagnostics + figure Z13_kpi_pilotables.png.
"""

import os
import sys
from itertools import combinations

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import euro_cascade_model as ec                                 # noqa: E402
from euro_cascade_model import PARAMS, var                      # noqa: E402
from src.aggregation.lda import simulate_remediation_severity   # noqa: E402
import scr_engine as eng                                        # noqa: E402

WID = 82
sp = PARAMS["OPRISK"]
PIL = eng.PIL
P4 = 4
_col = {j: c for c, j in enumerate(PIL)}
_others = [j for j in PIL if j != P4]
NY = 40_000
NSEED = 4
SEED0 = 20260727

# etats DORA par canal (C = cible conforme, NC = non conforme)
LAM_C = sp["lam_ref"]
try:
    LAM_NC = ec.lambda_scenario("OPRISK", "S2_non_conforme")
except Exception:
    LAM_NC = LAM_C * 1.30                                       # facteur_recalibration config
P_U0 = sp["p_u"]
PU_C, PU_NC = 0.85 * P_U0, 1.20 * P_U0                          # multiplicateur detection (16/39)
G_C, G_NC = 0.45, 0.90                                          # gain propagation (G_PROP C/NC)
PHICS_NC = 0.68                                                 # accumulation P4 (gamma, script 38)


def titre(s):
    print("\n" + "=" * WID + f"\n{s}\n" + "=" * WID)


# ------------------------------------------------------------------ tables de cascade
def table_amorce(j, g):
    dist = eng.cascade_set_dist(j, g)
    sets = list(dist.keys())
    probs = np.array([dist[s] for s in sets])
    ind = np.zeros((len(sets), 5))
    for r, s in enumerate(sets):
        for p in s:
            ind[r, _col[p]] = 1.0
    return ind, probs / probs.sum()


def table_p4_choc(phi_cs):
    """P4 en choc commun : P4 + chaque autre pilier inclus indep. avec proba phi_cs."""
    sets, probs = [], []
    for r in range(len(_others) + 1):
        for combo in combinations(_others, r):
            p = 1.0
            for k in _others:
                p *= phi_cs if k in combo else (1.0 - phi_cs)
            ind = np.zeros(5)
            for x in (P4,) + combo:
                ind[_col[x]] = 1.0
            sets.append(ind)
            probs.append(p)
    return np.array(sets), np.array(probs)


def scr_config(lam, g, p_u, phi_cs=None, nseed=NSEED, ny=NY):
    """SCR (VaR 99,5 %) moyenne sur nseed graines. phi_cs=None -> P4 noeud de cascade."""
    scrs = []
    for k in range(nseed):
        rng = np.random.default_rng(SEED0 + k)
        r = lam / (ec.PHI - 1.0)
        counts = rng.negative_binomial(r, r / (r + lam), size=ny)
        T = int(counts.sum())
        if T == 0:
            scrs.append(0.0)
            continue
        year_of = np.repeat(np.arange(ny), counts)
        w = np.array([eng.LAMBDA[j] for j in PIL], float)
        amorce = rng.choice(5, size=T, p=w / w.sum())
        U = rng.random(T)
        SEV = simulate_remediation_severity(T * 5, sp["xi"], sp["sigma"], sp["u"], p_u,
                                            sp["cap"], rng).reshape(T, 5)
        tables = {j: table_amorce(j, g) for j in PIL}
        if phi_cs is not None:
            tables[P4] = table_p4_choc(phi_cs)
        annual = np.zeros(ny)
        for c, j in enumerate(PIL):
            idx = np.where(amorce == c)[0]
            if idx.size == 0:
                continue
            ind, probs = tables[j]
            cdf = np.cumsum(probs)
            cdf[-1] = 1.0
            sel = np.searchsorted(cdf, U[idx], side="right")
            np.clip(sel, 0, len(probs) - 1, out=sel)
            loss = (SEV[idx] * ind[sel]).sum(axis=1)
            annual += np.bincount(year_of[idx], weights=loss, minlength=ny)
        scrs.append(var(annual))
    return float(np.mean(scrs))


# =====================================================================================
titre("1. Reperes : etat conforme (cible DORA) et etat non conforme")
# =====================================================================================
scr_C = scr_config(LAM_C, G_C, PU_C, phi_cs=None)
scr_NC = scr_config(LAM_NC, G_NC, PU_NC, phi_cs=PHICS_NC)
print(f"  lam : C={LAM_C:.1f} -> NC={LAM_NC:.1f} | p_u : C={PU_C:.3f} -> NC={PU_NC:.3f} | "
      f"g : {G_C} -> {G_NC} | phi_cs : 0 -> {PHICS_NC}")
print(f"\n  SCR conforme (cible DORA)   = {scr_C:.0f} M")
print(f"  SCR non conforme            = {scr_NC:.0f} M")
print(f"  Ecart de capital DORA total = {scr_NC - scr_C:.0f} M  (ce que la conformite met en jeu)")

# =====================================================================================
titre("2. Attribution : capital en jeu derriere chaque KPI (un canal a la fois)")
# =====================================================================================
# on part de l'etat conforme et on passe UN canal en non conforme
canaux = [
    ("frequence (KPI entree, 08b)", dict(lam=LAM_NC, g=G_C, p_u=PU_C, phi_cs=None), "calibrable"),
    ("detection (KPI P2 delai, P3 confinement)", dict(lam=LAM_C, g=G_C, p_u=PU_NC, phi_cs=None), "calibrable"),
    ("propagation (canal W, non identifie)", dict(lam=LAM_C, g=G_NC, p_u=PU_C, phi_cs=None), "borne"),
    ("accumulation (KPI P4 concentration)", dict(lam=LAM_C, g=G_C, p_u=PU_C, phi_cs=PHICS_NC), "borne"),
]
print(f"  {'KPI / canal':<44}{'SCR':>9}{'capital en jeu':>16}{'statut':>12}")
attrib = []
for name, cfg, statut in canaux:
    s = scr_config(**cfg)
    d = s - scr_C
    attrib.append((name, d, statut))
    print(f"  {name:<44}{s:>7.0f} M{d:>14.0f} M{statut:>12}")
somme = sum(d for _, d, _ in attrib)
interaction = (scr_NC - scr_C) - somme
print(f"\n  Somme des contributions isolees = {somme:.0f} M ; ecart total = {scr_NC-scr_C:.0f} M ;")
print(f"  interaction (canaux combines) = {interaction:+.0f} M "
      f"({100*interaction/(scr_NC-scr_C):+.0f} %). Les canaux ne sont pas additifs : la")
print("  non-conformite simultanee amplifie (ou attenue) la somme des effets isoles.")

# =====================================================================================
titre("3. Tableau de bord de remediation : KPI classes par capital libere")
# =====================================================================================
rank = sorted(attrib, key=lambda x: -x[1])
print("  Ramener un KPI a sa cible DORA libere (en isolant le canal) :")
for i, (name, d, statut) in enumerate(rank, 1):
    print(f"    {i}. {name:<44}{d:>7.0f} M   ({statut})")
print("\n  Lecture : les KPI a fort capital et CALIBRABLES (frequence, detection) sont les")
print("  leviers de remediation ACTIONNABLES en priorite ; ceux a fort capital mais BORNES")
print("  (propagation, accumulation) disent surtout l'incertitude, a piloter par la donnee")
print("  (registre DORA) plutot que par une action directe. Distinguer les deux est le point.")

# =====================================================================================
titre("VERDICT")
# =====================================================================================
print("  1. Chaque KPI descriptif devient un LEVIER DE CAPITAL rattache a un canal du moteur :")
print("     frequence->lam, detection (P2/P3)->p_u, accumulation (P4)->choc commun, W->g.")
print(f"  2. L'ecart de capital DORA ({scr_NC-scr_C:.0f} M) s'attribue par canal ; les canaux")
print(f"     ne sont pas additifs (interaction {interaction:+.0f} M).")
print("  3. Tableau de bord actionnable : classer par capital en jeu ET par statut (calibrable")
print("     vs borne). Les KPI calibrables se remedient ; les bornes se resorbent par la donnee.")
print("  4. C'est l'aval du fil : la meme discipline C..NC / bande / identification, exprimee")
print("     cette fois en KPI opposables a un souscripteur ou a un superviseur DORA.")

# =====================================================================================
# figure Z13
# =====================================================================================
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"], "font.size": 11,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb", "axes.edgecolor": "#c3c2b7",
    "axes.linewidth": 0.8, "text.color": "#0b0b0b", "axes.labelcolor": "#52514e",
    "xtick.color": "#898781", "ytick.color": "#898781", "axes.grid": False,
})
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
ACCENT, BLUE, GREEN = "#eb6834", "#256abf", "#3d8361"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.2),
                               gridspec_kw={"width_ratios": [1, 1.15]})

# (a) cascade d'attribution C -> NC
short = {"frequence (KPI entree, 08b)": "fréquence\n(entrée)",
         "detection (KPI P2 delai, P3 confinement)": "détection\n(P2/P3)",
         "propagation (canal W, non identifie)": "propagation\n(W)",
         "accumulation (KPI P4 concentration)": "accumulation\n(P4)"}
labels = (["conforme\n(cible DORA)"] + [short[n] for n, _, _ in attrib]
          + ["interaction\n(canaux liés)", "non conforme\n(cumul)"])
xs = np.arange(len(labels))
ax1.bar(0, scr_C, color=GREEN, alpha=0.9, width=0.6)
ax1.bar(len(labels) - 1, scr_NC, color=ACCENT, alpha=0.9, width=0.6)
base = scr_C
for i, (n, d, statut) in enumerate(attrib, 1):
    c = BLUE if statut == "calibrable" else MUTED
    ax1.bar(i, d, bottom=base, color=c, alpha=0.85, width=0.6)
    ax1.text(i, base + d + 120, f"+{d:.0f}", ha="center", fontsize=8, color=INK2)
    base += d
ax1.bar(len(labels) - 2, interaction, bottom=base, color=ACCENT, alpha=0.35, width=0.6)
ax1.text(len(labels) - 2, base + interaction + 120, f"+{interaction:.0f}", ha="center",
         fontsize=8, color=INK2)
ax1.text(0, scr_C + 120, f"{scr_C:.0f}", ha="center", fontsize=8.5, color=GREEN)
ax1.text(len(labels) - 1, scr_NC + 120, f"{scr_NC:.0f}", ha="center", fontsize=8.5, color=ACCENT)
ax1.set_xticks(xs); ax1.set_xticklabels(labels, fontsize=8)
ax1.set_ylabel("SCR (VaR 99,5 %, M€)", color=INK2)
ax1.set_title("(a)  L'écart de capital DORA attribué par KPI\n(bleu : calibrable · gris : borné)",
              fontsize=11, color=INK, pad=8)

# (b) tableau de bord : KPI classes par capital, couleur = statut
names = [short[n].replace("\n", " ") for n, _, _ in rank]
vals = [d for _, d, _ in rank]
cols = [BLUE if s == "calibrable" else MUTED for _, _, s in rank]
ypos = np.arange(len(rank))[::-1]
ax2.barh(ypos, vals, color=cols, alpha=0.88)
for y, v, (_, _, s) in zip(ypos, vals, rank):
    ax2.text(v + 20, y, f"{v:.0f} M  ({s})", va="center", fontsize=8.5, color=INK2)
ax2.set_yticks(ypos); ax2.set_yticklabels(names, fontsize=9)
ax2.set_xlabel("capital en jeu = SCR(non conforme) − SCR(conforme), canal isolé", color=INK2)
ax2.set_xlim(0, max(vals) * 1.35)
ax2.set_title("(b)  Tableau de bord de remédiation :\nquel KPI libère le plus de capital",
              fontsize=11, color=INK, pad=8)

for ax in (ax1, ax2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.suptitle("Z13 : des KPI descriptifs aux KPI pilotables, par attribution de l'écart de capital DORA",
             fontsize=12.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.92])
outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "Z13_kpi_pilotables.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
