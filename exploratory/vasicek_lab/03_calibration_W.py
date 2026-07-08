#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03 : Protocole de calibration de la matrice de contagion dirigee W.

Objectif : montrer COMMENT on estimera W sur des donnees reelles, et VALIDER la
methode sur des donnees simulees dont on connait la verite. Pret a brancher sur
un vrai panel d'incidents (entite x pilier x periode) le jour venu.

Idee cle : l'ASYMETRIE de W (qui entraine qui) n'est identifiable que par
l'information TEMPORELLE (qui declenche AVANT qui). La co-occurrence transversale
seule ne donne qu'une dependance symetrique. Le modele est donc dynamique :

  latent  X[i,j,t] = base_j + somme_k W[j,k] * D[i,k,t-1] + s_j * Y[j,t] + eps
  incident D[i,j,t] = 1 si X[i,j,t] >= 0

  D[i,k,t-1] : le pilier k a-t-il eu un incident a la periode precedente
  W[j,k]     : force dirigee de k vers j (ce qu'on veut estimer)
  Y[j,t]     : facteur systemique du pilier j a la periode t (choc commun)

Estimateur : pour chaque pilier j, une regression logistique de D[.,j,t] sur les
incidents retardes des autres piliers D[.,k,t-1], plus des effets fixes de periode
(qui absorbent le systemique Y[j,t]). Les coefficients estiment W[j,k].

Sortie : diagnostics + figures K1 (verite vs estimation) et K2 (taille d'echantillon,
sous-declaration).
"""

import os
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
import matplotlib as mpl
import matplotlib.pyplot as plt

RNG = np.random.default_rng(20260708)
J = 5
PIL = ["P1", "P2", "P3", "P4", "P5"]

# structure dirigee de reference (celle de TRANS : "k entraine j")
TRANS = {
    1: {2: 0.80, 3: 0.70, 4: 0.70, 5: 0.40},
    2: {1: 0.20, 3: 0.40, 4: 0.30, 5: 0.60},
    3: {1: 0.30, 2: 0.50, 4: 0.30, 5: 0.30},
    4: {1: 0.20, 2: 0.80, 3: 0.30, 5: 0.40},
    5: {1: 0.10, 2: 0.20, 3: 0.20, 4: 0.20},
}
GAIN = 0.9          # effet de contagion modere (signal realiste, pas trop facile)
W_TRUE = np.zeros((J, J))
for k in TRANS:                       # k -> j
    for j, v in TRANS[k].items():
        W_TRUE[j - 1, k - 1] = GAIN * v
BASE = np.full(J, -1.7)               # cale l'incidence de base (~ 6-9 %)
SLOAD = 0.5                           # charge du facteur systemique


def simulate(N, T, rng, w=W_TRUE, under=0.0):
    """Panel d'incidents D (N,J,T). under = proba de NON-declaration d'un petit incident."""
    D = np.zeros((N, J, T), dtype=np.int8)
    D[:, :, 0] = (rng.random((N, J)) < 0.08).astype(np.int8)
    for t in range(1, T):
        Y = rng.standard_normal(J)                        # systemique par pilier
        contagion = D[:, :, t - 1] @ w.T                  # (N,J) : somme_k W[j,k] D[i,k,t-1]
        X = BASE + contagion + SLOAD * Y + rng.standard_normal((N, J))
        D[:, :, t] = (X >= 0).astype(np.int8)
    if under > 0:                                         # sous-declaration (troncature)
        keep = rng.random((N, J, T)) >= under
        D = (D & keep).astype(np.int8)
    return D


def estimate_W(D):
    """Recupere W_hat (J,J, diagonale nulle) par regression logistique par pilier."""
    N, _, T = D.shape
    W_hat = np.zeros((J, J))
    # effets fixes de periode : one-hot des periodes 1..T-1
    per_idx = np.repeat(np.arange(T - 1), N)              # periode de chaque obs
    per_oh = np.eye(T - 1)[per_idx]
    for j in range(J):
        y = D[:, j, 1:].reshape(-1)                       # reponse (N*(T-1))
        others = [k for k in range(J) if k != j]
        lag = np.column_stack([D[:, k, :-1].reshape(-1) for k in others])
        Xd = np.column_stack([lag, per_oh])               # retards + effets periode
        if y.min() == y.max():                            # pilier degenere
            continue
        clf = LogisticRegression(fit_intercept=False, C=1e3, max_iter=400)
        clf.fit(Xd, y)
        for c, k in enumerate(others):
            W_hat[j, k] = clf.coef_[0, c]
    return W_hat


def offdiag(M):
    m = ~np.eye(J, dtype=bool)
    return M[m]


def direction_recovery(w_true, w_hat):
    """% de paires dont le SENS de l'asymetrie (j->k vs k->j) est bien retrouve."""
    ok = tot = 0
    for a in range(J):
        for b in range(a + 1, J):
            dt = w_true[a, b] - w_true[b, a]
            dh = w_hat[a, b] - w_hat[b, a]
            if abs(dt) < 1e-9:
                continue
            ok += (np.sign(dt) == np.sign(dh))
            tot += 1
    return ok / tot


# ============================================================ run principal
N0, T0 = 800, 60
D0 = simulate(N0, T0, RNG)
inc = D0.mean()
W_hat0 = estimate_W(D0)
corr0 = np.corrcoef(offdiag(W_TRUE), offdiag(W_hat0))[0, 1]
dir0 = direction_recovery(W_TRUE, W_hat0)
print(f"Panel : {N0} entites x {T0} periodes x {J} piliers ; incidence moyenne {inc:.1%}")
print(f"Correlation W_hat vs W_vrai (hors diagonale) = {corr0:.3f}")
print(f"Sens de l'asymetrie correctement retrouve      = {dir0:.0%} des paires\n")

# ============================================================ courbe taille d'echantillon
sizes = [50, 100, 200, 400, 800]
REP, TSW = 10, 50
corr_by_n, dir_by_n = [], []
for N in sizes:
    cs, ds = [], []
    for _ in range(REP):
        D = simulate(N, TSW, RNG)
        Wh = estimate_W(D)
        cs.append(np.corrcoef(offdiag(W_TRUE), offdiag(Wh))[0, 1])
        ds.append(direction_recovery(W_TRUE, Wh))
    corr_by_n.append(np.mean(cs)); dir_by_n.append(np.mean(ds))
    print(f"  N={N:4d} : corr {np.mean(cs):.2f} ; sens asymetrie {np.mean(ds):.0%}")

# ============================================================ robustesse sous-declaration
unders = [0.0, 0.2, 0.4, 0.6]
dir_by_u, corr_by_u = [], []
for u in unders:
    cs, ds = [], []
    for _ in range(REP):
        D = simulate(600, TSW, RNG, under=u)
        Wh = estimate_W(D)
        cs.append(np.corrcoef(offdiag(W_TRUE), offdiag(Wh))[0, 1])
        ds.append(direction_recovery(W_TRUE, Wh))
    corr_by_u.append(np.mean(cs)); dir_by_u.append(np.mean(ds))
    print(f"  sous-declaration {u:.0%} : corr {np.mean(cs):.2f} ; sens {np.mean(ds):.0%}")

# ============================================================ figures
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"],
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
})
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ACCENT = "#eb6834"
BLUES = ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SEQ = mpl.colors.LinearSegmentedColormap.from_list("b", BLUES)

# --- figure K1 : verite vs estimation
fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.6),
                         gridspec_kw={"width_ratios": [1, 1, 1.05]})


def heat(ax, M, title):
    vmax = max(M.max(), 1e-6)
    im = ax.imshow(M, cmap=SEQ, vmin=0, vmax=vmax)
    for a in range(J):
        for b in range(J):
            if a != b and M[a, b] > 1e-6:
                ax.text(b, a, f"{M[a,b]:.1f}", ha="center", va="center",
                        fontsize=8, color="#fff" if M[a, b] > 0.55 * vmax else INK)
    ax.set_xticks(range(J)); ax.set_xticklabels(PIL)
    ax.set_yticks(range(J)); ax.set_yticklabels(PIL)
    ax.set_xlabel("de ce pilier k", color=INK2, fontsize=9)
    ax.set_ylabel("vers ce pilier j", color=INK2, fontsize=9)
    ax.set_title(title, fontsize=10.5, color=INK, pad=8)


heat(axes[0], W_TRUE, "W vrai (simule)")
heat(axes[1], np.clip(W_hat0, 0, None), "W estime (logistique)")
ax = axes[2]
ax.scatter(offdiag(W_TRUE), offdiag(W_hat0), s=42, color=BLUES[3],
           edgecolor="#fcfcfb", zorder=3)
ax.set_xlabel("W vrai (hors diagonale)", color=INK2, fontsize=9)
ax.set_ylabel("W estime", color=INK2, fontsize=9)
ax.set_title(f"Correlation {corr0:.2f} ; sens {dir0:.0%}", fontsize=10.5, color=INK, pad=8)
ax.grid(True, color=GRID, lw=0.7)
fig.suptitle("K1 : le protocole retrouve la structure dirigee de W",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.94])
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(outdir, exist_ok=True)
p1 = os.path.join(outdir, "K1_calibration_W.png")
fig.savefig(p1, dpi=200, bbox_inches="tight"); print("\nfigure ecrite :", p1)

# --- figure K2 : taille d'echantillon et sous-declaration
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 4.6))
ax1.plot(sizes, corr_by_n, "-o", color=BLUES[4], lw=2, label="correlation W")
ax1.plot(sizes, dir_by_n, "-s", color=ACCENT, lw=2, label="sens de l'asymetrie")
ax1.set_xscale("log")
ax1.set_xticks(sizes); ax1.set_xticklabels([str(s) for s in sizes])
ax1.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
ax1.tick_params(axis="x", which="minor", bottom=False)
ax1.set_xlabel("nombre d'entites N (x 50 periodes)", color=INK2)
ax1.set_ylabel("qualite de recuperation", color=INK2)
ax1.set_ylim(0, 1.05); ax1.grid(True, color=GRID, lw=0.7)
ax1.legend(frameon=False, fontsize=9, loc="lower right")
ax1.set_title("(a) Combien de donnees faut-il ?", fontsize=11, color=INK, pad=8)

ax2.plot([u * 100 for u in unders], corr_by_u, "-o", color=BLUES[4], lw=2, label="correlation W")
ax2.plot([u * 100 for u in unders], dir_by_u, "-s", color=ACCENT, lw=2, label="sens de l'asymetrie")
ax2.set_xlabel("taux de sous-declaration (%)", color=INK2)
ax2.set_ylabel("qualite de recuperation", color=INK2)
ax2.set_ylim(0, 1.05); ax2.grid(True, color=GRID, lw=0.7)
ax2.legend(frameon=False, fontsize=9, loc="lower left")
ax2.set_title("(b) Robustesse a la sous-declaration", fontsize=11, color=INK, pad=8)
fig.suptitle("K2 : donnees necessaires et robustesse du protocole",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.94])
p2 = os.path.join(outdir, "K2_calibration_diagnostics.png")
fig.savefig(p2, dpi=200, bbox_inches="tight"); print("figure ecrite :", p2)
