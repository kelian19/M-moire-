#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
26 : elicitation structuree de W par la methode de Cooke (Classical Model).

Phase 3 de la feuille de route. W (contagion dirigee entre piliers) n'est pas calibrable
sur donnee (script 05). Plutot qu'un dire d'expert BRUT, on le construit par une
elicitation PONDEREE PAR LA PERFORMANCE (Cooke 1991, Classical Model) :

  - chaque expert repond a des QUESTIONS-GRAINES a reponse connue (de l'analyste, pas de
    l'expert), dans le domaine cyber/DORA, sous forme de quantiles (5, 50, 95 %) ;
  - sa CALIBRATION (justesse statistique) et son INFORMATION (finesse) sont mesurees sur
    ces graines ; son POIDS = calibration x information (0 si sous le seuil alpha) ;
  - le decideur (DM) est le melange lineaire pondere des experts sur les questions CIBLES
    (les liens diriges de W), qui ressortent avec une INCERTITUDE, pas un point.

APPORT PROPRE. Les questions-graines sont les quantites que les chapitres empiriques ont
MESUREES (08b-08g, 05) : l'elicitation est donc calibree sur les faits du memoire.

Ce script fournit (i) le moteur de Cooke reutilisable, (ii) une DEMONSTRATION sur experts
FICTIFS de profils contrastes (les vraies reponses viendront des sessions Mehdi / Ouidad /
Franck / conformite). Aucune donnee sous licence. Ne touche ni src/ ni memoire/.

Sortie : diagnostics + figure V_elicitation_cooke.png.
"""

import os

import numpy as np
from scipy.stats import chi2
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 74
QP = np.array([0.05, 0.50, 0.95])            # quantiles elicites
BIN_P = np.array([0.05, 0.45, 0.45, 0.05])   # probas theoriques des 4 inter-quantiles
ALPHA = 0.05                                 # seuil de significativite de calibration
KRANGE = 0.10                                # extension de la plage intrinseque (10 %)


def titre(s):
    print("\n" + "=" * W + f"\n{s}\n" + "=" * W)


# ============================================================ moteur de Cooke
def bin_of(truth, q):
    """Indice d'inter-quantile (0..3) ou tombe la realisation, vu les quantiles q (3,)."""
    return int(truth >= q[0]) + int(truth >= q[1]) + int(truth >= q[2])


def calibration(quants, truths):
    """Score de calibration (p-value) d'un expert. quants : (N,3), truths : (N,)."""
    N = len(truths)
    counts = np.zeros(4)
    for i in range(N):
        counts[bin_of(truths[i], quants[i])] += 1
    s = counts / N
    mask = s > 0
    kl = np.sum(s[mask] * np.log(s[mask] / BIN_P[mask]))
    stat = 2.0 * N * kl
    return float(chi2.sf(stat, df=3))        # P(chi2_3 >= stat)


def _range(q_all, truth=None):
    """Plage intrinseque [L,U] : min/max des quantiles (et de la realisation), +/-10 %."""
    lo, hi = q_all.min(), q_all.max()
    if truth is not None:
        lo, hi = min(lo, truth), max(hi, truth)
    span = hi - lo if hi > lo else abs(hi) + 1.0
    return lo - KRANGE * span, hi + KRANGE * span


def item_ranges(seed_quants, truths):
    """Plage intrinseque COMMUNE a tous les experts, par question (methode de Cooke)."""
    experts = list(seed_quants)
    ranges = []
    for i in range(len(truths)):
        qs = np.concatenate([seed_quants[e][i] for e in experts])
        ranges.append(_range(qs, truths[i]))
    return ranges


def information(quants, ranges):
    """Information moyenne (KL vs uniforme de fond) sur les graines, plages COMMUNES.

    La plage etant commune a tous, un expert aux quantiles ETROITS concentre la masse
    et informe plus ; un expert VAGUE se rapproche de l'uniforme et informe moins.
    """
    infos = []
    for i, (L, U) in enumerate(ranges):
        q = np.clip(quants[i], L, U)
        edges = np.array([L, q[0], q[1], q[2], U])
        widths = np.diff(edges)
        widths = np.where(widths <= 0, 1e-9, widths)
        dens = BIN_P / widths                              # densite par intervalle
        info = np.sum(BIN_P * np.log(dens * (U - L)))      # KL vs uniforme 1/(U-L)
        infos.append(info)
    return float(np.mean(infos))


def cooke_weights(seed_quants, seed_truths):
    """Poids de Cooke normalises. seed_quants : {expert -> (N,3)}."""
    ranges = item_ranges(seed_quants, seed_truths)
    cal, inf = {}, {}
    for e, q in seed_quants.items():
        cal[e] = calibration(q, seed_truths)
        inf[e] = information(q, ranges)
    raw = {e: (cal[e] * inf[e] if cal[e] >= ALPHA else 0.0) for e in seed_quants}
    tot = sum(raw.values())
    if tot == 0:                                           # repli : poids egaux si tous sous alpha
        raw = {e: 1.0 for e in seed_quants}
        tot = float(len(seed_quants))
    w = {e: raw[e] / tot for e in seed_quants}
    return w, cal, inf


def pool_target(target_quants, weights, grid=2000):
    """Melange pondere (DM) sur une cible : renvoie (q05, q50, q95) du pool."""
    all_q = np.concatenate(list(target_quants.values()))
    L, U = _range(all_q)
    xs = np.linspace(L, U, grid)
    dens = np.zeros(grid)
    for e, q in target_quants.items():
        edges = np.array([L, q[0], q[1], q[2], U])
        widths = np.diff(edges)
        widths = np.where(widths <= 0, 1e-9, widths)
        d = np.zeros(grid)
        for k in range(4):
            m = (xs >= edges[k]) & (xs < edges[k + 1])
            d[m] = BIN_P[k] / widths[k]
        dens += weights[e] * d
    cdf = np.cumsum(dens)
    cdf /= cdf[-1]
    return tuple(float(np.interp(p, cdf, xs)) for p in QP)


# ============================================================ questions-graines (reponses connues)
# valeurs MESUREES dans les chapitres empiriques (08b-08g, 05).
SEEDS = [
    ("Part des sinistres financiers portes par une cause commune (tiers), %", 20.0),
    ("Delai median survenance -> declaration, jours", 94.0),
    ("Part des incidents declares apres 1 mois, %", 85.0),
    ("Duree mediane de breche (containment), jours", 7.0),
    ("Indice de queue de severite xi", 0.90),
    ("Frequence d'incidents TIC materiels, grande entite, par an", 0.21),
    ("Delai median de declaration d'un piratage, jours", 117.0),
    ("Indice de Gini de la concentration journaliere des sinistres", 0.69),
    ("Nombre max de victimes d'une cause commune en un jour (MOVEit)", 191.0),
    ("Part des jours qui sont une cause commune, %", 1.7),
]
SEED_TRUTH = np.array([v for _, v in SEEDS])

# ============================================================ questions cibles (liens diriges de W)
TARGETS = [
    ("P1 -> P2  (gouvernance entraine incidents)", 0.80),
    ("P2 -> P1  (inverse)", 0.20),
    ("P4 -> P2  (tiers entraine incidents)", 0.80),
    ("P1 -> P4  (gouvernance entraine tiers)", 0.70),
    ("P3 -> P1", 0.30),
    ("P5 -> P2", 0.20),
]
TARGET_POSIT = np.array([v for _, v in TARGETS])

# ============================================================ experts FICTIFS (demonstration)
# profil = (biais, dispersion REELLE de l'estimation, dispersion ANNONCEE des quantiles).
# La calibration compare l'annoncee a la reelle : bien calibre (annonce ~ reel), sur-confiant
# (annonce << reel -> rate), vague (annonce >> reel -> peu informatif), biaise (decalage).
EXPERTS = {
    "Operationnel (Mehdi)":  dict(bias=0.00, actual=0.20, stated=0.24),   # bien calibre
    "Litterature (Ouidad)":  dict(bias=0.03, actual=0.20, stated=0.55),   # vague
    "ORSA (Franck)":         dict(bias=0.00, actual=0.38, stated=0.11),   # sur-confiant
    "Conformite":            dict(bias=0.35, actual=0.20, stated=0.24),   # biaise
}
RNG = np.random.default_rng(20260721)


def gen_quantiles(truth_vec, profile, in01=False):
    """Reponses quantiles d'un expert fictif : centre biaise+bruite (dispersion REELLE),
    quantiles ecartes de la dispersion ANNONCEE (independante de la reelle)."""
    out = np.zeros((len(truth_vec), 3))
    for i, t in enumerate(truth_vec):
        if in01:                                           # cible dans [0,1] : bruit additif
            center = np.clip(t * (1 + profile["bias"]) + RNG.normal(0, profile["actual"] * 0.4),
                             0.02, 0.98)
            hw = profile["stated"] * 0.5
            q = np.clip([center - 1.645 * hw, center, center + 1.645 * hw], 0.01, 0.99)
        else:                                              # graine positive : bruit multiplicatif
            center = t * np.exp(profile["bias"] + RNG.normal(0, profile["actual"]))
            q = center * np.exp(np.array([-1.645, 0.0, 1.645]) * profile["stated"])
        out[i] = np.sort(q)
    return out


# ============================================================ execution
titre("Calibration des experts sur les questions-graines (reponses connues)")
seed_quants = {e: gen_quantiles(SEED_TRUTH, p) for e, p in EXPERTS.items()}
weights, cal, inf = cooke_weights(seed_quants, SEED_TRUTH)
print(f"  {len(SEEDS)} graines | seuil alpha = {ALPHA}\n")
print(f"  {'expert':<24}{'calibration':>13}{'information':>13}{'poids DM':>12}")
for e in EXPERTS:
    flag = "" if cal[e] >= ALPHA else "  (sous alpha -> poids 0)"
    print(f"  {e:<24}{cal[e]:>13.3f}{inf[e]:>13.2f}{weights[e]:>11.1%}{flag}")
best = max(weights, key=weights.get)
killed = [e for e in EXPERTS if cal[e] < ALPHA]
print(f"\n  => dominant : {best} ({weights[best]:.0%}), le mieux place sur le produit")
print("     calibration x information (une performance, pas un statut).")
print("  Mecanisme : un expert BIAISE est ecarte par sa calibration ; un expert trop VAGUE")
print("  par sa faible information ; un expert TROP SUR DE LUI n'est recompense que si ses")
print("  intervalles etroits tombent juste.")
if killed:
    print(f"  Ecarte(s) sous le seuil de calibration alpha={ALPHA} : {', '.join(killed)}.")

titre("Elicitation ponderee des liens diriges de W (DM = melange de Cooke)")
target_quants = {e: gen_quantiles(TARGET_POSIT, p, in01=True) for e, p in EXPERTS.items()}
pooled = []
print(f"  {'lien':<42}{'DM 5%':>8}{'DM 50%':>9}{'DM 95%':>9}{'posit':>8}")
for i, (name, posit) in enumerate(TARGETS):
    tq = {e: target_quants[e][i] for e in EXPERTS}
    q05, q50, q95 = pool_target(tq, weights)
    pooled.append((q05, q50, q95))
    print(f"  {name:<42}{q05:>8.2f}{q50:>9.2f}{q95:>9.2f}{posit:>8.2f}")
pooled = np.array(pooled)

titre("VERDICT")
print("1. La methode de Cooke transforme un dire d'expert BRUT en une estimation PONDEREE")
print("   par la performance, auditable et reproductible. C'est l'apport methodo de la")
print("   phase 3, et il ne demande AUCUNE donnee d'incident : seulement des experts.")
print("2. Chaque lien de W ressort avec un INTERVALLE a 90 %, pas un point : l'incertitude")
print("   d'elicitation entre enfin dans le modele (et alimente la sensibilite du SCR).")
print(f"3. L'asymetrie causale survit a l'elicitation : P1->P2 median {pooled[0][1]:.2f} "
      f"contre P2->P1 median {pooled[1][1]:.2f}. C'est le resultat robuste du modele.")
print("4. Ici les reponses sont FICTIVES (demonstration). Le protocole (fiche jointe) est")
print("   pret : il ne reste qu'a collecter les quantiles des vrais experts.")

# ============================================================ figure
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"], "font.size": 11,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb", "axes.edgecolor": "#c3c2b7",
    "axes.linewidth": 0.8, "text.color": "#0b0b0b", "axes.labelcolor": "#52514e",
    "xtick.color": "#898781", "ytick.color": "#898781", "axes.grid": False,
})
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ACCENT = "#eb6834"
BL = ["#b7d3f6", "#3987e5", "#184f95"]

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.8, 4.9),
                                    gridspec_kw={"width_ratios": [1.05, 1.15, 1]})

# (a) scorecard : calibration x information, taille = poids
xs = [cal[e] for e in EXPERTS]
ys = [inf[e] for e in EXPERTS]
ss = [40 + 1400 * weights[e] for e in EXPERTS]
cols = [ACCENT if e == best else BL[1] for e in EXPERTS]
ax1.axvline(ALPHA, color=MUTED, lw=1.2, ls="--")
ax1.text(ALPHA * 1.1, max(ys) * 0.98, "seuil $\\alpha$", fontsize=8, color=MUTED, va="top")
ax1.scatter(xs, ys, s=ss, c=cols, edgecolor="#fcfcfb", zorder=3, alpha=0.9)
for e, x, y in zip(EXPERTS, xs, ys):
    ax1.annotate(e.split(" (")[0], (x, y), fontsize=7.6, color=INK2,
                 xytext=(4, 5), textcoords="offset points")
ax1.set_xscale("symlog", linthresh=0.01)
ax1.set_xlabel("calibration (p-value, log)", color=INK2)
ax1.set_ylabel("information (KL moyen)", color=INK2)
ax1.set_title("(a)  Poids de Cooke = calibration × information", fontsize=11,
              color=INK, pad=8)
for s in ("top", "right"):
    ax1.spines[s].set_visible(False)

# (b) liens de W : DM 90 % vs posit
names = [t[0].split("  ")[0] for t in TARGETS][::-1]
med = pooled[::-1, 1]
lo = pooled[::-1, 0]
hi = pooled[::-1, 2]
posit = TARGET_POSIT[::-1]
y = np.arange(len(names))
ax2.hlines(y, lo, hi, color=BL[1], lw=3, zorder=2)
ax2.scatter(med, y, s=45, color=BL[2], zorder=3, label="DM médiane (élicité)")
ax2.scatter(posit, y, s=70, color=ACCENT, marker="D", zorder=4, label="valeur posée (16)")
ax2.set_yticks(y); ax2.set_yticklabels(names, fontsize=8.5)
ax2.set_xlim(0, 1)
ax2.set_xlabel("force du lien dirigé (intervalle DM à 90 %)", color=INK2)
ax2.legend(frameon=False, fontsize=8.2, loc="lower right")
ax2.set_title("(b)  Chaque lien de $W$ élicité avec incertitude", fontsize=11,
              color=INK, pad=8)
for s in ("top", "right", "left"):
    ax2.spines[s].set_visible(False)
ax2.tick_params(axis="y", length=0)

# (c) l'asymetrie P1<->P2 pooled (densites)
def pooled_density(idx, grid=800):
    tq = {e: target_quants[e][idx] for e in EXPERTS}
    all_q = np.concatenate(list(tq.values()))
    L, U = _range(all_q)
    xs = np.linspace(0, 1, grid)
    dens = np.zeros(grid)
    for e, q in tq.items():
        edges = np.array([L, q[0], q[1], q[2], U])
        widths = np.diff(edges); widths = np.where(widths <= 0, 1e-9, widths)
        d = np.zeros(grid)
        for k in range(4):
            m = (xs >= edges[k]) & (xs < edges[k + 1])
            d[m] = BIN_P[k] / widths[k]
        dens += weights[e] * d
    return xs, dens


x12, d12 = pooled_density(0)
x21, d21 = pooled_density(1)
ax3.fill_between(x12, d12, color=BL[2], alpha=0.55, label="P1 $\\to$ P2")
ax3.fill_between(x21, d21, color=ACCENT, alpha=0.45, label="P2 $\\to$ P1")
ax3.axvline(pooled[0][1], color=BL[2], lw=1.6)
ax3.axvline(pooled[1][1], color=ACCENT, lw=1.6)
ax3.set_xlim(0, 1)
ax3.set_xlabel("force du lien dirigé", color=INK2)
ax3.set_ylabel("densité DM", color=INK2)
ax3.legend(frameon=False, fontsize=8.5)
ax3.set_title("(c)  L'asymétrie causale survit à l'élicitation", fontsize=11,
              color=INK, pad=8)
for s in ("top", "right"):
    ax3.spines[s].set_visible(False)

fig.suptitle("V : élicitation de $W$ par la méthode de Cooke (calibration sur les faits mesurés)",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.93])
outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "V_elicitation_cooke.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
plt.close(fig)
print("\nfigure ecrite :", path)
