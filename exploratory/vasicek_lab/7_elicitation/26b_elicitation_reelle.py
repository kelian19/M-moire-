#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
26b : élicitation de W sur les VRAIES réponses des experts (moteur de Cooke du script 26).

26 démontrait la méthode sur des experts fictifs. 26b prend les réponses RÉELLES collectées
via le questionnaire (questionnaire_elicitation_w.pdf), les lit dans un CSV, et produit :
  - les poids de Cooke de chaque expert (calibration x information sur les 10 graines) ;
  - chaque lien dirigé de W avec son intervalle à 90 % (mélange pondéré = décideur).

CSV attendu (large) : une ligne par question (A1..A10 graines, B1..B6 cibles), colonnes
  id ; bloc ; libelle ; puis, par expert, <Nom>_q05, <Nom>_q50, <Nom>_q95.
Un expert n'est retenu que s'il a répondu aux 16 questions. Gabarit vide :
  cascade_qualitative/elicitation_reponses_TEMPLATE.csv

Usage : python 26b_elicitation_reelle.py [chemin_csv]   (défaut : le gabarit)
Sortie : diagnostics + figure V2_elicitation_reelle.png. Aucune donnée sous licence.
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import chi2
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV = os.path.abspath(os.path.join(
    HERE, "..", "cascade_qualitative", "elicitation_reponses_TEMPLATE.csv"))
W = 74
QP = np.array([0.05, 0.50, 0.95])
BIN_P = np.array([0.05, 0.45, 0.45, 0.05])
ALPHA = 0.05
KRANGE = 0.10

# verites des 10 graines (quantites mesurees dans les chapitres empiriques 08b-08g, 05)
SEED_TRUTH = np.array([20.0, 94.0, 85.0, 7.0, 0.90, 0.21, 117.0, 0.69, 191.0, 1.7])
SEED_IDS = [f"A{i}" for i in range(1, 11)]
TARGET_IDS = ["B1", "B2", "B3", "B4", "B5", "B6"]
TARGET_LABELS = {"B1": "P1->P2", "B2": "P2->P1", "B3": "P4->P2",
                 "B4": "P1->P4", "B5": "P3->P1", "B6": "P5->P2"}


def titre(s):
    print("\n" + "=" * W + f"\n{s}\n" + "=" * W)


# ============================================================ moteur de Cooke (identique a 26)
def bin_of(truth, q):
    return int(truth >= q[0]) + int(truth >= q[1]) + int(truth >= q[2])


def calibration(quants, truths):
    N = len(truths)
    counts = np.zeros(4)
    for i in range(N):
        counts[bin_of(truths[i], quants[i])] += 1
    s = counts / N
    mask = s > 0
    kl = np.sum(s[mask] * np.log(s[mask] / BIN_P[mask]))
    return float(chi2.sf(2.0 * N * kl, df=3))


def _range(q_all, truth=None):
    lo, hi = q_all.min(), q_all.max()
    if truth is not None:
        lo, hi = min(lo, truth), max(hi, truth)
    span = hi - lo if hi > lo else abs(hi) + 1.0
    return lo - KRANGE * span, hi + KRANGE * span


def item_ranges(seed_quants, truths):
    experts = list(seed_quants)
    ranges = []
    for i in range(len(truths)):
        qs = np.concatenate([seed_quants[e][i] for e in experts])
        ranges.append(_range(qs, truths[i]))
    return ranges


def information(quants, ranges):
    infos = []
    for i, (L, U) in enumerate(ranges):
        q = np.clip(quants[i], L, U)
        edges = np.array([L, q[0], q[1], q[2], U])
        widths = np.where(np.diff(edges) <= 0, 1e-9, np.diff(edges))
        dens = BIN_P / widths
        infos.append(np.sum(BIN_P * np.log(dens * (U - L))))
    return float(np.mean(infos))


def cooke_weights(seed_quants, seed_truths):
    ranges = item_ranges(seed_quants, seed_truths)
    cal = {e: calibration(q, seed_truths) for e, q in seed_quants.items()}
    inf = {e: information(q, ranges) for e, q in seed_quants.items()}
    raw = {e: (cal[e] * inf[e] if cal[e] >= ALPHA else 0.0) for e in seed_quants}
    tot = sum(raw.values())
    if tot == 0:
        raw = {e: 1.0 for e in seed_quants}
        tot = float(len(seed_quants))
    return {e: raw[e] / tot for e in seed_quants}, cal, inf


def pool_target(target_quants, weights, grid=2000):
    all_q = np.concatenate(list(target_quants.values()))
    L, U = _range(all_q)
    xs = np.linspace(L, U, grid)
    dens = np.zeros(grid)
    for e, q in target_quants.items():
        edges = np.array([L, q[0], q[1], q[2], U])
        widths = np.where(np.diff(edges) <= 0, 1e-9, np.diff(edges))
        d = np.zeros(grid)
        for k in range(4):
            m = (xs >= edges[k]) & (xs < edges[k + 1])
            d[m] = BIN_P[k] / widths[k]
        dens += weights[e] * d
    cdf = np.cumsum(dens)
    cdf /= cdf[-1]
    return tuple(float(np.interp(p, cdf, xs)) for p in QP)


# ============================================================ lecture du CSV
def load_answers(path):
    df = pd.read_csv(path).set_index("id")
    experts = sorted({c[:-4] for c in df.columns if c.endswith("_q05")})
    seed_q, target_q, kept = {}, {}, []
    for e in experts:
        cols = [f"{e}_q05", f"{e}_q50", f"{e}_q95"]
        if not all(c in df.columns for c in cols):
            continue
        vals = df[cols].apply(pd.to_numeric, errors="coerce")
        sq = vals.loc[SEED_IDS].to_numpy()
        tq = vals.loc[TARGET_IDS].to_numpy()
        if np.isnan(sq).any() or np.isnan(tq).any():
            print(f"  expert '{e}' : réponses incomplètes -> ignoré")
            continue
        seed_q[e] = np.sort(sq, axis=1)
        target_q[e] = np.sort(tq, axis=1)
        kept.append(e)
    return seed_q, target_q, kept


# ============================================================ exécution
CSV = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
if not os.path.exists(CSV):
    sys.exit(f"CSV absent : {CSV}")
titre(f"Lecture des réponses : {os.path.basename(CSV)}")
seed_q, target_q, experts = load_answers(CSV)
if not experts:
    sys.exit("Aucun expert avec un questionnaire complet. Remplir le gabarit "
             "(cascade_qualitative/elicitation_reponses_TEMPLATE.csv) puis relancer.")
print(f"  experts retenus ({len(experts)}) : {', '.join(experts)}")

titre("Poids de Cooke (calibration x information sur les 10 graines)")
weights, cal, inf = cooke_weights(seed_q, SEED_TRUTH)
print(f"  {'expert':<26}{'calibration':>13}{'information':>13}{'poids DM':>12}")
for e in experts:
    flag = "" if cal[e] >= ALPHA else "  (sous alpha -> 0)"
    print(f"  {e:<26}{cal[e]:>13.3f}{inf[e]:>13.2f}{weights[e]:>11.1%}{flag}")

titre("W élicité : chaque lien dirigé avec son intervalle à 90 %")
pooled = {}
print(f"  {'lien':<10}{'DM 5%':>9}{'DM 50%':>9}{'DM 95%':>9}")
for k, tid in enumerate(TARGET_IDS):
    tq = {e: target_q[e][k] for e in experts}
    q05, q50, q95 = pool_target(tq, weights)
    pooled[tid] = (q05, q50, q95)
    print(f"  {TARGET_LABELS[tid]:<10}{q05:>9.2f}{q50:>9.2f}{q95:>9.2f}")
asym = pooled['B1'][1] - pooled['B2'][1]
print(f"\n  asymétrie causale P1->P2 vs P2->P1 (médianes) : {pooled['B1'][1]:.2f} "
      f"contre {pooled['B2'][1]:.2f}  (écart {asym:+.2f}).")
print("  Ces intervalles alimentent directement la sensibilité du SCR (scripts 24/25).")

# ============================================================ figure
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"], "font.size": 11,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb", "axes.edgecolor": "#c3c2b7",
    "axes.linewidth": 0.8, "text.color": "#0b0b0b", "axes.labelcolor": "#52514e",
    "xtick.color": "#898781", "ytick.color": "#898781", "axes.grid": False,
})
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
ACCENT = "#eb6834"
BL = ["#b7d3f6", "#3987e5", "#184f95"]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.6, 4.7),
                               gridspec_kw={"width_ratios": [1, 1.15]})
order = sorted(experts, key=lambda e: weights[e], reverse=True)
axA.barh(range(len(order)), [weights[e] for e in order], color=BL[2],
         edgecolor="#fcfcfb", height=0.6)
for i, e in enumerate(order):
    axA.text(weights[e] + 0.01, i, f"{weights[e]:.0%}", va="center", fontsize=8.6, color=INK2)
axA.set_yticks(range(len(order))); axA.set_yticklabels([e.split(" (")[0] for e in order], fontsize=9)
axA.invert_yaxis()
axA.set_xlim(0, max(max(weights.values()) * 1.25, 0.1))
axA.set_xlabel("poids de Cooke", color=INK2)
axA.set_title("(a)  Poids des experts (performance)", fontsize=11, color=INK, pad=8)
for s in ("top", "right", "left"):
    axA.spines[s].set_visible(False)
axA.tick_params(axis="y", length=0)

tids = TARGET_IDS[::-1]
yy = np.arange(len(tids))
lo = [pooled[t][0] for t in tids]
med = [pooled[t][1] for t in tids]
hi = [pooled[t][2] for t in tids]
axB.hlines(yy, lo, hi, color=BL[1], lw=3, zorder=2)
axB.scatter(med, yy, s=45, color=BL[2], zorder=3, label="médiane élicitée")
axB.set_yticks(yy); axB.set_yticklabels([TARGET_LABELS[t] for t in tids], fontsize=9)
axB.set_xlim(0, 1)
axB.set_xlabel("force du lien dirigé (intervalle à 90 %)", color=INK2)
axB.legend(frameon=False, fontsize=8.5, loc="lower right")
axB.set_title("(b)  $W$ élicité : chaque lien avec incertitude", fontsize=11, color=INK, pad=8)
for s in ("top", "right", "left"):
    axB.spines[s].set_visible(False)
axB.tick_params(axis="y", length=0)

fig.suptitle("V2 : W élicité sur les réponses réelles des experts (méthode de Cooke)",
             fontsize=12.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.93])
outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "V2_elicitation_reelle.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
plt.close(fig)
print("\nfigure ecrite :", path)
