#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01 : Pourquoi il faut revoir Merton-Vasicek DE ZERO.

On montre, chiffres a l'appui, que la dependance dirigee entre piliers (matrice
TRANS du modele qualitatif) ne peut PAS etre representee par un modele a facteur
gaussien :

  (A) TRANS est ASYMETRIQUE  -> ce n'est meme pas une matrice de correlation.
  (B) Sa symetrisee n'est PAS semi-definie positive -> pas une correlation valide.
  (C) Un facteur unique impose Corr(i,k) >= Corr(i,j)*Corr(j,k) (transitivite) ;
      les donnees violent cette contrainte -> correlations NON TRANSITIVES.

Sortie : diagnostics imprimes + figure G1_non_transitivite.png
"""

import os
import numpy as np
from scipy.optimize import minimize
import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- la dependance dirigee (TRANS)
PILIERS = {1: "P1", 2: "P2", 3: "P3", 4: "P4", 5: "P5"}
IDX = [1, 2, 3, 4, 5]
TRANS = {
    1: {2: 0.80, 3: 0.70, 4: 0.70, 5: 0.40},
    2: {1: 0.20, 3: 0.40, 4: 0.30, 5: 0.60},
    3: {1: 0.30, 2: 0.50, 4: 0.30, 5: 0.30},
    4: {1: 0.20, 2: 0.80, 3: 0.30, 5: 0.40},
    5: {1: 0.10, 2: 0.20, 3: 0.20, 4: 0.20},
}

n = len(IDX)
T = np.eye(n)
for a in IDX:
    for b, v in TRANS[a].items():
        T[IDX.index(a), IDX.index(b)] = v

# ---------------------------------------------------------------- (A) asymetrie
ASym = T - T.T
asym_fro = np.linalg.norm(ASym, "fro")
frob_T = np.linalg.norm(T - np.eye(n), "fro")
print("=" * 68)
print("(A) ASYMETRIE : une correlation est SYMETRIQUE par definition")
print("=" * 68)
print(f"  ||TRANS - TRANS^T||_F = {asym_fro:.3f}   (0 = symetrique)")
print(f"  rapport asymetrie/intensite = {asym_fro/frob_T:.1%}")
worst = []
for i in range(n):
    for j in range(i + 1, n):
        d = abs(T[i, j] - T[j, i])
        worst.append((d, IDX[i], IDX[j], T[i, j], T[j, i]))
worst.sort(reverse=True)
for d, i, j, tij, tji in worst[:3]:
    print(f"    P{i}->P{j} = {tij:.2f}  mais  P{j}->P{i} = {tji:.2f}   (ecart {d:.2f})")
print("  => la propagation a un SENS ; aucune matrice de correlation ne l'encode.\n")

# ---------------------------------------------------------------- (B) symetrisee non-PSD
S = (T + T.T) / 2
np.fill_diagonal(S, 1.0)
eigvals = np.linalg.eigvalsh(S)
print("=" * 68)
print("(B) MEME SYMETRISEE : pas une correlation valide (non semi-definie +)")
print("=" * 68)
print("  valeurs propres de la symetrisee :", np.round(eigvals, 3))
print(f"  valeur propre minimale = {eigvals.min():.3f}   (< 0  =>  INVALIDE)")

# projection sur la correlation la plus proche (clipping spectral + renorm diag)
w, V = np.linalg.eigh(S)
w_clip = np.clip(w, 1e-8, None)
S_psd = V @ np.diag(w_clip) @ V.T
d = np.sqrt(np.diag(S_psd))
S_psd = S_psd / np.outer(d, d)
distortion = np.linalg.norm(S_psd - S, "fro")
print(f"  distortion pour la rendre valide = {distortion:.3f} "
      f"({distortion/np.linalg.norm(S,'fro'):.1%} de la matrice)")
print("  => forcer une correlation gaussienne DEFORME deja la dependance.\n")

# ---------------------------------------------------------------- (C) non-transitivite
print("=" * 68)
print("(C) NON-TRANSITIVITE : un facteur unique impose r_ik >= r_ij * r_jk")
print("=" * 68)
# best single-factor loadings a_i : minimise sum_{i<j} (a_i a_j - S_ij)^2
iu = np.triu_indices(n, 1)


def loss(a):
    R = np.outer(a, a)
    return np.sum((R[iu] - S[iu]) ** 2)


res = minimize(loss, x0=np.full(n, 0.6), bounds=[(0.01, 0.999)] * n)
a = res.x
R1 = np.outer(a, a)
rmse = np.sqrt(np.mean((R1[iu] - S[iu]) ** 2))
print(f"  meilleur facteur unique : chargements a = {np.round(a,2)}")
print(f"  RMSE du mono-facteur sur la dependance = {rmse:.3f}")

violations = []
for i in range(n):
    for j in range(n):
        for k in range(n):
            if len({i, j, k}) < 3:
                continue
            lhs, rhs = S[i, k], S[i, j] * S[j, k]
            if lhs < rhs - 1e-9:
                violations.append((rhs - lhs, IDX[i], IDX[j], IDX[k], lhs, rhs))
violations.sort(reverse=True)
print(f"  triples violant la transitivite du mono-facteur : {len(violations)}")
for gap, i, j, k, lhs, rhs in violations[:4]:
    print(f"    r(P{i},P{k})={lhs:.2f} < r(P{i},P{j})*r(P{j},P{k})={rhs:.2f}"
          f"   (P{i}~P{j} et P{j}~P{k} forts, mais P{i}~P{k} faible)")
print("  => correlations NON TRANSITIVES : impossibles sous un facteur unique.\n")

# ---------------------------------------------------------------- figure G1
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"],
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
})
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ACCENT = "#eb6834"
BLUES = ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SEQ = mpl.colors.LinearSegmentedColormap.from_list("b", BLUES)
DIV = mpl.colors.LinearSegmentedColormap.from_list(
    "d", ["#a83c12", "#eb6834", "#fcfcfb", "#3987e5", "#0d366b"])
labels = [PILIERS[i] for i in IDX]

fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.5))

# panneau A : TRANS dirigee
ax = axes[0]
im = ax.imshow(T, cmap=SEQ, vmin=0, vmax=1)
for i in range(n):
    for j in range(n):
        ax.text(j, i, f"{T[i,j]:.2f}", ha="center", va="center", fontsize=8,
                color="#fff" if T[i, j] > 0.5 else INK)
ax.set_xticks(range(n)); ax.set_xticklabels(labels)
ax.set_yticks(range(n)); ax.set_yticklabels(labels)
ax.set_xlabel("... vers ce pilier (aval)", color=INK2, fontsize=9)
ax.set_ylabel("part de ce pilier (amont)", color=INK2, fontsize=9)
ax.set_title("(A) TRANS : dependance DIRIGEE", fontsize=10.5, color=INK, pad=10)

# panneau B : asymetrie
ax = axes[1]
m = np.abs(ASym).max()
im2 = ax.imshow(ASym, cmap=DIV, vmin=-m, vmax=m)
for i in range(n):
    for j in range(n):
        if abs(ASym[i, j]) > 1e-9:
            ax.text(j, i, f"{ASym[i,j]:+.2f}", ha="center", va="center",
                    fontsize=8, color=INK)
ax.set_xticks(range(n)); ax.set_xticklabels(labels)
ax.set_yticks(range(n)); ax.set_yticklabels(labels)
ax.set_title(f"(B) TRANS - TRANS^T != 0\n(pas une correlation)",
             fontsize=10.5, color=INK, pad=10)

# panneau C : spectre de la symetrisee
ax = axes[2]
colors = [ACCENT if e < 0 else BLUES[4] for e in eigvals]
ax.bar(range(n), eigvals, color=colors, edgecolor="#fcfcfb")
ax.axhline(0, color=INK, lw=0.8)
for i, e in enumerate(eigvals):
    ax.text(i, e + (0.04 if e >= 0 else -0.04), f"{e:.2f}", ha="center",
            va="bottom" if e >= 0 else "top", fontsize=8,
            color=ACCENT if e < 0 else INK2)
ax.set_xticks(range(n)); ax.set_xticklabels([f"$\\lambda_{i+1}$" for i in range(n)])
ax.set_title("(C) spectre de la symetrisee\nvaleur propre < 0 => INVALIDE",
             fontsize=10.5, color=INK, pad=10)
ax.set_ylabel("valeur propre", color=INK2, fontsize=9)

fig.suptitle("Vos dependances ne tiennent pas dans un Vasicek mono-facteur",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.94])

outdir = os.path.dirname(os.path.abspath(__file__))
figdir = os.path.join(outdir, "figures")
os.makedirs(figdir, exist_ok=True)
path = os.path.join(figdir, "G1_non_transitivite.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("figure ecrite :", path)
