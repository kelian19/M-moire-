#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H1 : Le reseau dirige W et un mini-exemple de cascade.

Panneau A : la structure DIRIGEE de W sur les 5 piliers (derivee de TRANS).
            Les fleches epaisses partent de P1 (super-emetteur) ; peu reviennent
            vers lui -> asymetrie visible.
Panneau B : le sous-reseau {P1,P2,P4} de l'exemple chiffre de la note, avec ses
            poids ILLUSTRATIFS (arrondis pour le calcul a la main, ce ne sont pas
            les entrees calibrees de W) et la propagation d'un choc +2 sur P1.
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

# ---------------------------------------------------------------- style
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"],
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
})
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ACCENT = "#eb6834"
PCOL = {1: "#184f95", 2: "#3987e5", 3: "#86b6ef", 4: "#eb6834", 5: "#a9a79e"}

TRANS = {
    1: {2: 0.80, 3: 0.70, 4: 0.70, 5: 0.40},
    2: {1: 0.20, 3: 0.40, 4: 0.30, 5: 0.60},
    3: {1: 0.30, 2: 0.50, 4: 0.30, 5: 0.30},
    4: {1: 0.20, 2: 0.80, 3: 0.30, 5: 0.40},
    5: {1: 0.10, 2: 0.20, 3: 0.20, 4: 0.20},
}


def node(ax, xy, label, color, r=0.15, big=False):
    rr = r * (1.25 if big else 1.0)
    ax.add_patch(Circle(xy, rr, facecolor=color, edgecolor="#fcfcfb",
                        lw=2, zorder=4))
    ax.text(*xy, label, ha="center", va="center", color="#fff",
            fontsize=12 if big else 11, fontweight="bold", zorder=5)


def arrow(ax, p0, p1, w, color, rad=0.16, r=0.16):
    # raccourcit aux bords des cercles
    d = np.array(p1) - np.array(p0)
    L = np.hypot(*d)
    u = d / L
    a = np.array(p0) + u * r
    b = np.array(p1) - u * r
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>", mutation_scale=13, lw=w, color=color,
                 alpha=0.85, zorder=3))


fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.2, 5.6),
                               gridspec_kw={"width_ratios": [1.15, 1]})

# ---------------------------------------------------------------- panneau A : W sur 5 piliers
ang = {1: 90, 2: 90 - 72, 3: 90 - 144, 4: 90 + 144, 5: 90 + 72}
pos = {p: (np.cos(np.radians(a)), np.sin(np.radians(a))) for p, a in ang.items()}
for i in TRANS:
    for j, v in TRANS[i].items():
        if v >= 0.4:                      # on ne trace que les liens marques
            arrow(axA, pos[i], pos[j], w=0.6 + 4.2 * (v - 0.4), color=PCOL[i])
for p, xy in pos.items():
    node(axA, xy, f"P{p}", PCOL[p], big=(p == 1))
axA.text(*pos[1], "", zorder=6)
axA.set_xlim(-1.5, 1.5); axA.set_ylim(-1.5, 1.6)
axA.set_aspect("equal"); axA.axis("off")
axA.set_title("(A)  Le reseau dirige W  (structure de TRANS)",
              fontsize=11, color=INK, pad=6)
axA.text(0, -1.5, "fleche i→j = i entraine j ;  epaisseur ∝ force.  "
         "P1 emet fort, recoit peu  →  asymetrie.",
         ha="center", va="top", fontsize=8.4, color=INK2)

# ---------------------------------------------------------------- panneau B : sous-reseau + calcul
pB = {1: (0.0, 0.0), 2: (2.0, -0.7), 4: (2.0, 0.9)}
W = {(2, 1): 0.5, (2, 4): 0.4, (4, 1): 0.3}   # W_jk : j recoit de k
for (j, k), w in W.items():
    arrow(axB, pB[k], pB[j], w=0.8 + 4.0 * w, color=PCOL[k], rad=0.10, r=0.22)
    mid = (np.array(pB[k]) + np.array(pB[j])) / 2
    axB.text(mid[0], mid[1] + 0.12, f"{w:.1f}", ha="center", va="bottom",
             fontsize=9, color=INK,
             bbox=dict(boxstyle="round,pad=0.1", fc="#fcfcfb", ec="none"))
Xval = {1: 2.0, 2: 1.24, 4: 0.6}
for p, xy in pB.items():
    node(axB, xy, f"P{p}", PCOL[p], r=0.22, big=(p == 1))
    axB.text(xy[0], xy[1] - 0.36, f"X = {Xval[p]:.2f}", ha="center", va="top",
             fontsize=9.2, color=ACCENT if Xval[p] >= 1 else MUTED,
             fontweight="bold")
axB.text(pB[1][0], pB[1][0] + 0.55, "choc +2", ha="center", va="bottom",
         fontsize=9, color=INK, style="italic")
axB.annotate("", xy=(pB[1][0], 0.30), xytext=(pB[1][0], 0.75),
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
axB.set_xlim(-0.7, 2.9); axB.set_ylim(-1.6, 1.7)
axB.set_aspect("equal"); axB.axis("off")
axB.set_title("(B)  Cascade d'un choc +2 sur P1  (exemple chiffre)",
              fontsize=11, color=INK, pad=6)
axB.text(1.1, -1.5, "seuil K = 1  →  P1 et P2 declenchent, pas P4.\n"
         "Meme choc place sur P2  →  reste local (1 seul incident).",
         ha="center", va="top", fontsize=8.4, color=INK2)

fig.suptitle("La propagation dirigee W : qui entraine qui, et de combien",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.95])

outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "H1_reseau_W.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("figure ecrite :", path)
