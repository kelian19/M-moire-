#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
40 : la decomposition W = S + A, lue comme la REVERSIBILITE d'un processus.

Le script 32 (Prop. 3) etablit un FAIT algebrique : toute matrice se decompose de facon
unique en une partie symetrique S = (W+W^T)/2 et une partie antisymetrique A = (W-W^T)/2,
la donnee identifie S (co-occurrence) et pas A (direction), placebo z = -0,33. Ce script
donne a ce fait sa RAISON probabiliste, celle que demande Hugo : le parallele avec la
decomposition d'un processus de Markov en une partie reversible et un courant irreversible,
c'est-a-dire avec la martingalisation (partie fluctuation) et son compensateur (partie derive).

--------------------------------------------------------------------------------------------
LE PARALLELE, EN TROIS IDENTITES VERIFIABLES.

On construit sur les 5 piliers la chaine de Markov qui SAUTE de i vers j proportionnellement
au jugement dirige TRANS[i][j] (row-stochastique P). Elle porte exactement la direction posee.
Soit pi sa loi stationnaire (pi P = pi).

(1) COURANT ET REVERSIBILITE. Le courant de probabilite J_ij = pi_i P_ij - pi_j P_ji est
    antisymetrique. La chaine est REVERSIBLE (equilibre detaille) si et seulement si J = 0.
    Le renversement du temps donne la chaine adjointe Ptilde_ij = pi_j P_ji / pi_i, et
        P_s = (P + Ptilde)/2   est invariante par renversement (la partie reversible),
        P_a = (P - Ptilde)/2   change de SIGNE par renversement (le courant, la direction).
    C'est le miroir exact de S et A : S = co-occurrence, invariante au sens du temps ;
    A = direction, ce qui distingue l'avant de l'apres.

(2) LA FLUCTUATION NE VOIT QUE S (c'est la martingalisation). Pour toute fonction test f,
    l'increment f(X_1) - (Pf)(X_0) est une difference de martingale ; sa variation, mesuree
    par la forme de Dirichlet E(f,f) = (1/2) somme pi_i P_ij (f_j - f_i)^2, ne depend QUE de
    la partie reversible : E_P(f,f) = E_{P_s}(f,f), la partie antisymetrique P_a y contribue
    exactement 0. La fluctuation (la martingale) est aveugle a la direction ; seule la derive
    (le compensateur (Pf - f), le courant) la porte. On le verifie a la 12e decimale.

(3) LA DIRECTION = PRODUCTION D'ENTROPIE. L'irreversibilite se resume en un scalaire, le taux
    de production d'entropie sigma = (1/2) somme (pi_i P_ij - pi_j P_ji) log(pi_i P_ij / pi_j P_ji)
    >= 0, nul si et seulement si la chaine est reversible. La chaine symetrisee a sigma = 0 et
    courant nul. Le placebo directionnel du memoire (z = -0,33) se relit alors PROPREMENT :
    la donnee ne permet pas de distinguer sigma de 0, c'est-a-dire qu'elle est compatible avec
    l'equilibre detaille. Non pas "on n'a pas su calibrer la direction", mais "les observations
    de co-occurrence sont compatibles avec une dynamique reversible".

--------------------------------------------------------------------------------------------
FAISABILITE ET HONNETETE (consigne Hugo). Le parallele est FAISABLE et il RENFORCE la these :
il fonde la limite d'identification sur un theoreme standard (une statistique invariante par
renversement du temps ne peut pas identifier le courant), au lieu de la constater. Deux reserves
a assumer, exactement dans l'esprit "Vasicheck" :
  - la version propre du courant est PONDEREE par pi (produit scalaire de L2(pi)) ; le S = (W+W^T)/2
    du memoire est le cas particulier pi uniforme. On rapporte les deux, l'ecart est mesure ici.
  - W est un noyau de contagion, pas litteralement un generateur de Markov : on EMPRUNTE l'algebre
    de la reversibilite comme analogie eclairante, on ne pretend pas que la cascade EST une chaine
    reversible. C'est une lecture, pas une hypothese ajoutee.

Sortie : diagnostics + figure Z11_reversibilite_martingale.png.
"""

import os
import sys

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
_CASCADE = os.path.abspath(os.path.join(_HERE, "..", "..", "cascade_qualitative"))
if _CASCADE not in sys.path:
    sys.path.insert(0, _CASCADE)
from cascade_model import TRANS, PILIERS  # noqa: E402

WID = 82
PIL = [1, 2, 3, 4, 5]
NP_ = len(PIL)
COL = {j: c for c, j in enumerate(PIL)}


def titre(s):
    print("\n" + "=" * WID + f"\n{s}\n" + "=" * WID)


# ============================================================ objets de base
def trans_matrix():
    """Matrice dirigee brute T_ij = TRANS[i][j] (0 sur la diagonale)."""
    T = np.zeros((NP_, NP_))
    for i in PIL:
        for j, w in TRANS[i].items():
            T[COL[i], COL[j]] = w
    return T


def markov_hop(T):
    """Chaine de saut inter-piliers : P_ij = T_ij / somme_j T_ij (row-stochastique)."""
    return T / T.sum(axis=1, keepdims=True)


def stationary(P):
    """Loi stationnaire pi : vecteur propre gauche de valeur propre 1, normalise."""
    w, V = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(w - 1.0)))
    pi = np.real(V[:, k])
    pi = np.abs(pi)
    return pi / pi.sum()


def reversed_chain(P, pi):
    """Chaine adjointe (renversee dans le temps) Ptilde_ij = pi_j P_ji / pi_i."""
    return (pi[None, :] * P.T) / pi[:, None]


def current(P, pi):
    """Courant de probabilite J_ij = pi_i P_ij - pi_j P_ji (antisymetrique)."""
    F = pi[:, None] * P
    return F - F.T


def entropy_production(P, pi):
    """Taux de production d'entropie sigma >= 0 ; nul ssi equilibre detaille."""
    F = pi[:, None] * P
    s = 0.0
    for a in range(NP_):
        for b in range(NP_):
            if a != b and F[a, b] > 0 and F[b, a] > 0:
                s += 0.5 * (F[a, b] - F[b, a]) * np.log(F[a, b] / F[b, a])
    return s


def dirichlet(P, pi, f):
    """Forme de Dirichlet E(f,f) = (1/2) somme pi_i P_ij (f_j - f_i)^2 (energie de la martingale)."""
    tot = 0.0
    for a in range(NP_):
        for b in range(NP_):
            tot += 0.5 * pi[a] * P[a, b] * (f[b] - f[a]) ** 2
    return tot


# ============================================================ calculs
T = trans_matrix()
P = markov_hop(T)
pi = stationary(P)
Pt = reversed_chain(P, pi)
Ps = 0.5 * (P + Pt)                     # partie reversible (invariante au renversement)
Pa = 0.5 * (P - Pt)                     # courant (change de signe au renversement)
J = current(P, pi)
sigma = entropy_production(P, pi)

# version Euclidienne du memoire (pi uniforme), pour le pont avec S/A du script 32
G = 0.90
maxs = T.sum(axis=1).max()
W = G * T / maxs
S_eucl = 0.5 * (W + W.T)
A_eucl = 0.5 * (W - W.T)

titre("Chaine de saut inter-piliers construite sur le jugement dirige TRANS")
print("  P_ij = TRANS[i][j] / somme_j TRANS[i][j] (proba de sauter de i vers j).")
print(f"\n  {'':>6}" + "".join(f"{'P'+str(j):>9}" for j in PIL) + f"{'pi':>10}")
for a, i in enumerate(PIL):
    print(f"  {'P'+str(i):>6}" + "".join(f"{P[a, b]:>9.3f}" for b in range(NP_))
          + f"{pi[a]:>10.3f}")
ordre = [PIL[c] for c in np.argsort(-pi)]
print(f"\n  Loi stationnaire : le saut sejourne surtout en "
      + ", ".join(f"P{j} ({pi[COL[j]]:.0%})" for j in ordre[:3]) + ".")
print("  Lecture : pi est un profil de RECEPTACLE (ou la marche s'accumule), a ne pas")
print("  confondre avec l'ordre des SOURCES (ROOT : P1>P4). Voir 34, l'aplatissement a u=0.")

titre("(1) Courant, reversibilite, renversement du temps")
rev_res = float(np.abs(J).max())
print(f"  Courant maximal max|J_ij| = {rev_res:.4f} > 0  =>  chaine IRREVERSIBLE :")
print("  le modele porte bien une direction (equilibre detaille NON satisfait).")
print("  Les trois plus forts courants nets (sens i -> j si J_ij > 0) :")
pairs = sorted(((J[a, b], PIL[a], PIL[b]) for a in range(NP_) for b in range(a + 1, NP_)),
               key=lambda x: -abs(x[0]))
for val, i, j in pairs[:3]:
    src, dst = (i, j) if val > 0 else (j, i)
    print(f"     P{src} -> P{dst}   |J| = {abs(val):.4f}")
err_s = float(np.abs(Ps - reversed_chain(Ps, pi)).max())     # P_s = son propre renverse
Pa_of_Pt = 0.5 * (Pt - reversed_chain(Pt, pi))               # courant de la chaine renversee
err_a = float(np.abs(Pa_of_Pt + Pa).max())                   # doit valoir -Pa
print(f"\n  Renversement du temps : partie reversible P_s invariante "
      f"(ecart {err_s:.2e}),")
print(f"  courant P_a change de signe sous renversement (ecart a -P_a : {err_a:.2e}).")
print(f"  Courant de la chaine symetrisee P_s : "
      f"{float(np.abs(current(Ps, pi)).max()):.2e} (nul, elle est reversible).")

titre("(2) La fluctuation ne voit que S : la forme de Dirichlet ignore le courant")
rng = np.random.default_rng(20260727)
worst = 0.0
for _ in range(2000):
    f = rng.standard_normal(NP_)
    e_full = dirichlet(P, pi, f)
    e_sym = dirichlet(Ps, pi, f)
    worst = max(worst, abs(e_full - e_sym))
print("  Pour 2000 fonctions test f tirees au hasard :")
print(f"  ecart maximal |E_P(f,f) - E_Ps(f,f)| = {worst:.2e}  (numeriquement nul).")
print("  L'energie de la martingale (la fluctuation, la variation quadratique) ne depend")
print("  QUE de la partie reversible S. La partie antisymetrique A = le courant = la")
print("  derive ; c'est exactement ce que la martingalisation retire. La donnee de")
print("  co-occurrence mesure une fluctuation : elle voit S, jamais A.")

titre("(3) La direction = production d'entropie ; le placebo teste sigma = 0")
sigma_sym = entropy_production(Ps, pi)
print(f"  Production d'entropie de la chaine posee   : sigma   = {sigma:.4f}  (> 0, dirigee)")
print(f"  Production d'entropie de la chaine symetrisee : sigma_s = {sigma_sym:.2e}  (= 0, reversible)")
print("  L'irreversibilite tient dans ce seul scalaire. Le placebo directionnel du memoire")
print("  (asymetrie 119 SOUS le nul de permutation 128 +/- 27, z = -0,33) se relit alors")
print("  comme un test de sigma = 0 : la co-occurrence observee est COMPATIBLE avec une")
print("  dynamique reversible. Ce n'est pas un echec de calibration, c'est une limite de")
print("  principe : une statistique invariante par renversement du temps ne peut pas")
print("  identifier un courant qui, lui, change de signe sous ce renversement.")

titre("Pont avec le S/A Euclidien du script 32 (cas pi uniforme)")
frac_eucl = np.linalg.norm(A_eucl) / np.linalg.norm(W)
print(f"  Part antisymetrique Euclidienne ||A||/||W|| = {frac_eucl:.1%} de la matrice de contagion.")
print(f"  Ecart entre pi et l'uniforme (1/5) : max |pi_i - 0,2| = {float(np.abs(pi - 0.2).max()):.3f}.")
print("  Le S = (W+W^T)/2 du memoire est la version pi-uniforme du courant pondere ci-dessus :")
print("  meme objet, meme conclusion, la version ponderee en donne la lecture probabiliste propre.")

titre("VERDICT (faisabilite pour Hugo)")
print("  Le parallele est FAISABLE et il RENFORCE la these d'identification partielle :")
print("   - S <-> partie reversible (fluctuation, martingale) : identifiee par la co-occurrence ;")
print("   - A <-> courant irreversible (derive, compensateur) : non identifie, car il est")
print("     precisement ce qui s'annule sous la symetrisation par renversement du temps ;")
print("   - le placebo z = -0,33 = donnee compatible avec sigma = 0 (equilibre detaille).")
print("  A assumer explicitement (esprit Vasicheck) : produit scalaire pondere par pi, et")
print("  emprunt d'analogie (W n'est pas un generateur de Markov). C'est une lecture qui")
print("  fonde la limite sur un theoreme, pas une hypothese de plus.")

# ============================================================ figure Z11
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"], "font.size": 11,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb", "axes.edgecolor": "#c3c2b7",
    "axes.linewidth": 0.8, "text.color": "#0b0b0b", "axes.labelcolor": "#52514e",
    "xtick.color": "#898781", "ytick.color": "#898781", "axes.grid": False,
})
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
ACCENT, BLUE, GREEN = "#eb6834", "#256abf", "#3d8361"

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7.2, 9.9))

# (a) le courant J : heatmap divergente + fleches du sens net
vmax = np.abs(J).max()
im = ax1.imshow(J, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
ax1.set_xticks(range(NP_)); ax1.set_yticks(range(NP_))
ax1.set_xticklabels([f"P{j}" for j in PIL]); ax1.set_yticklabels([f"P{j}" for j in PIL])
for a in range(NP_):
    for b in range(NP_):
        if a != b:
            ax1.text(b, a, f"{J[a, b]:+.2f}", ha="center", va="center", fontsize=7.5,
                     color=INK if abs(J[a, b]) < 0.6 * vmax else "#fcfcfb")
ax1.set_title("(a)  Le courant $J_{ij}=\\pi_iP_{ij}-\\pi_jP_{ji}$\n= la direction, non identifiée",
              fontsize=10.5, color=INK, pad=8)
cb = fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
cb.ax.tick_params(labelsize=7)

# (b) la fluctuation ne voit que S ; production d'entropie
labels = ["énergie de\nfluctuation\n$E(f,f)$", "production\nd'entropie\n$\\sigma$"]
posee = [1.0, 1.0]                     # fluctuation et entropie de la chaine posee (base 1)
sym = [1.0, 0.0]                       # symetrisee : meme fluctuation, entropie nulle
x = np.arange(2)
ax2.bar(x - 0.19, posee, width=0.36, color=BLUE, alpha=0.9, label="chaîne posée")
ax2.bar(x + 0.19, sym, width=0.36, color=GREEN, alpha=0.9, label="chaîne symétrisée")
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=8.5)
ax2.set_ylabel("valeur (normalisée à la chaîne posée)", color=INK2, fontsize=9)
ax2.set_ylim(0, 1.25)
ax2.legend(frameon=False, fontsize=8, loc="upper center")
ax2.text(0.02, 0.42, "la fluctuation est\nIDENTIQUE\n(ne voit que S)", transform=ax2.transAxes,
         fontsize=8, color=MUTED, style="italic", ha="left")
ax2.text(0.62, 0.10, "l'irréversibilité\ns'efface\n(σ → 0)", transform=ax2.transAxes,
         fontsize=8, color=MUTED, style="italic", ha="left")
ax2.set_title("(b)  La martingale (fluctuation) ne voit que $S$ ;\n$A$ est toute la direction",
              fontsize=10.5, color=INK, pad=8)

# (c) le schema du renversement du temps
ax3.axis("off")
ax3.set_xlim(0, 1); ax3.set_ylim(0, 1)
ax3.set_title("(c)  Renversement du temps :\n$S$ invariante, $A$ change de signe",
              fontsize=10.5, color=INK, pad=8)
ax3.annotate("", xy=(0.86, 0.80), xytext=(0.14, 0.80),
             arrowprops=dict(arrowstyle="->", color=INK2, lw=1.4))
ax3.annotate("", xy=(0.14, 0.55), xytext=(0.86, 0.55),
             arrowprops=dict(arrowstyle="->", color=INK2, lw=1.4))
ax3.text(0.5, 0.86, "temps  $t \\to$", ha="center", fontsize=9, color=INK2)
ax3.text(0.5, 0.60, "$\\leftarrow t$  renversé", ha="center", fontsize=9, color=INK2)
ax3.text(0.02, 0.40, "$P = S + A$", fontsize=14, color=INK)
ax3.text(0.30, 0.40, "$S$ = co-occurrence,  $A$ = direction", fontsize=9, color=INK2)
ax3.text(0.02, 0.26, "$\\tilde{P} = S - A$", fontsize=14, color=INK)
ax3.text(0.30, 0.26, "(chaîne renversée : $A$ change de signe)", fontsize=9, color=INK2)
ax3.text(0.02, 0.09, "$S$ : identifiée.   $A$ : placebo $z=-0{,}33$,\n"
                     "compatible avec $\\sigma = 0$ (réversible).",
         fontsize=9.5, color=ACCENT)

fig.suptitle("Z11 : la direction $A$ est le courant irréversible d'un processus, "
             "ce que la martingalisation retire et que la co-occurrence ne voit pas",
             fontsize=12.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.92])
outdir = os.path.join(os.path.dirname(_HERE), "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "Z11_reversibilite_martingale.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
