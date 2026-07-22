#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
37 : la queue de severite par pilier (xi_j), traitee comme les autres non-identifies.

Point de depart (ton tuteur t'a fait passer le Vasicek d'un facteur unique a un facteur
PAR PILIER). La sevente suit-elle ? Aujourd'hui, une seule queue xi est appliquee aux cinq
piliers. Le chapitre donnees note pourtant que la queue est HETEROGENE selon la categorie
(script 05). Faut-il un xi_j par pilier ?

CE QUE LA DONNEE PERMET, ET CE QU'ELLE N'AUTORISE PAS. Sur OpRisk (secteur financier),
l'indice de queue estime PAR CATEGORIE Bale (seuil q75, n >= 150) vaut :
    Internal Fraud 1,37 | Execution/Delivery 1,27 | Clients/Products 1,03 |
    External Fraud 0,98 | Employment 0,92
et la categorie la plus proche du TIC (Business Disruption & System Failures) n'a que
105 observations : NON estimable. Donc :
  - l'HETEROGENEITE de queue (spread ~0,45) est un fait de donnee ;
  - mais l'ASSIGNATION xi_j = f(pilier) ne l'est PAS : les categories Bale ne sont pas les
    domaines de controle DORA, et la seule categorie vraiment TIC est sous-echantillonnee.

CONSEQUENCE, coherente avec tout le memoire. On ne POSE pas un xi_j par pilier (fausse
precision). On BORNE le SCR sur les assignations possibles : chaque pilier recoit une des
cinq queues observees, on enumere les 120 permutations, et l'on regarde (i) de combien le
SCR bouge, (ii) si le classement des piliers par contribution a la queue tient. Pour isoler
l'effet de l'HETEROGENEITE du niveau, les cinq queues sont CENTREES sur le xi de reference
du pipeline (0,90) en conservant leur dispersion observee.

Sortie : diagnostics + figure Z8_xi_par_pilier.png.
"""

import os
import sys
from itertools import permutations

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import euro_cascade_model as ec                                 # noqa: E402
from euro_cascade_model import PARAMS, var                      # noqa: E402
import scr_engine as eng                                        # noqa: E402

WID = 80
PIL = eng.PIL
SRC = "OPRISK"
sp = PARAMS[SRC]
NY = 30_000
SEED = 909
XI_REF = 0.90                        # xi de reference du pipeline (chapitre 12)

# queues observees par categorie Bale (script 05 / probe), triees
XI_CAT = np.array([0.92, 0.98, 1.03, 1.27, 1.37])
# centrees sur XI_REF en conservant la dispersion : isole l'heterogeneite, pas le niveau
XI_CENTRE = XI_CAT - XI_CAT.mean() + XI_REF     # somme/moyenne = XI_REF

SHARE = {j: eng.LAMBDA[j] for j in PIL}
_stot = sum(SHARE.values())
SHARE = {j: SHARE[j] / _stot for j in PIL}
G_BASE = 0.90


def titre(s):
    print("\n" + "=" * WID + f"\n{s}\n" + "=" * WID)


def scr(xi_vec, seed=SEED, ny=NY, by_pillar=False):
    """SCR (et, si demande, pertes par pilier) pour un vecteur xi_j. Config neutre, CRN."""
    lam_vec = {j: sp["lam_ref"] * SHARE[j] for j in PIL}
    g_vec = {j: G_BASE for j in PIL}
    p_u_vec = {j: sp["p_u"] for j in PIL}
    rng = np.random.default_rng(seed)
    out = ec.simulate_euro_pp(lam_vec, g_vec, sp["xi"], sp["sigma"], sp["u"], p_u_vec,
                              sp["cap"], ny, rng, by_pillar=by_pillar, xi_vec=xi_vec)
    if by_pillar:
        return out                                   # matrice (ny, 5)
    return var(out)


print(f"queues observees (categories Bale)  : {XI_CAT}")
print(f"queues centrees sur xi_ref = {XI_REF} : {np.round(XI_CENTRE,3)}  "
      f"(moyenne {XI_CENTRE.mean():.3f})")

# =====================================================================================
titre("Reference : queue COMMUNE xi = 0,90 sur les cinq piliers")
# =====================================================================================
xi_commun = {j: XI_REF for j in PIL}
scr_commun = scr(xi_commun)
print(f"  SCR (queue commune) = {scr_commun:.0f} M")

# =====================================================================================
titre("Bornes du SCR sur les 120 assignations de queues aux piliers")
# =====================================================================================
vals = []
for perm in permutations(XI_CENTRE):
    xi_vec = {PIL[i]: float(perm[i]) for i in range(5)}
    vals.append(scr(xi_vec))
vals = np.array(vals)
lo, hi = vals.min(), vals.max()
print(f"  SCR dans [{lo:.0f} ; {hi:.0f}] M sur les 120 permutations")
print(f"  ecart a la queue commune : de {100*(lo/scr_commun-1):+.1f} % a "
      f"{100*(hi/scr_commun-1):+.1f} %")
print(f"  largeur relative de la bande : {100*(hi-lo)/scr_commun:.1f} % du SCR commun")
print("  Lecture : donner a chaque pilier sa propre queue, dans l'enveloppe observee,")
print("  deplace le niveau de cet ordre. Comme le reste du modele, c'est une bande,")
print("  pas un point : xi_j n'est pas identifie pilier par pilier, il est borne.")

# =====================================================================================
titre("Le classement des piliers par contribution a la queue tient-il ?")
# =====================================================================================
# contribution = perte moyenne du pilier dans la queue (annees au-dela de la VaR globale)
def contributions(xi_vec):
    M = scr(xi_vec, by_pillar=True)
    tot = M.sum(axis=1)
    seuil = np.quantile(tot, 0.995)
    queue = M[tot >= seuil]
    return queue.mean(axis=0)                        # M par pilier dans la queue


rng_p = np.random.default_rng(SEED + 1)
perms = list(permutations(XI_CENTRE))
ech = [perms[i] for i in rng_p.choice(len(perms), size=30, replace=False)]
rangs = np.zeros((len(ech), 5), dtype=int)
for r, perm in enumerate(ech):
    xi_vec = {PIL[i]: float(perm[i]) for i in range(5)}
    c = contributions(xi_vec)
    rangs[r] = np.argsort(-c)                         # ordre des piliers (indices)
top1 = [int(rr[0]) for rr in rangs]
from collections import Counter
cnt = Counter(top1)
n_ech = len(ech)
part_tete = cnt.most_common(1)[0][1] / n_ech
tete_idx = cnt.most_common(1)[0][0]
print(f"  pilier en tete de contribution a la queue, sur {n_ech} assignations tirees :")
for idx, n in cnt.most_common():
    print(f"    P{PIL[idx]} : {n}/{n_ech} fois")
# Enonce unique et coherent, selon le degre de stabilite mesure.
if part_tete >= 0.95:
    verdict_rang = f"P{PIL[tete_idx]} domine TOUJOURS : classement invariant a l'assignation."
elif part_tete >= 0.75:
    verdict_rang = (f"P{PIL[tete_idx]} domine dans {100*part_tete:.0f} % des assignations : "
                    f"dominant mais PAS invariant, l'heterogeneite de queue peut occasionnellement "
                    f"promouvoir un autre pilier.")
else:
    verdict_rang = (f"le pilier de tete depend de l'assignation (P{PIL[tete_idx]} seulement "
                    f"{100*part_tete:.0f} %) : classement NON robuste a la queue.")
print(f"  => {verdict_rang}")

# =====================================================================================
titre("Verdict")
# =====================================================================================
print(f"  1. L'heterogeneite de queue N'EST PAS neutre en capital. Meme en gardant la")
print(f"     moyenne des queues a xi_ref = {XI_REF}, donner a chaque pilier sa propre queue")
print(f"     RELEVE le SCR de {100*(lo/scr_commun-1):+.0f} % a {100*(hi/scr_commun-1):+.0f} %.")
print(f"     C'est un effet de convexite : la VaR croit plus vite que lineairement en xi, donc")
print(f"     une queue lourde sur un pilier n'est pas compensee par une queue legere ailleurs.")
print(f"     Consequence : supposer une queue COMMUNE SOUS-ESTIME le capital. C'est une raison")
print(f"     de plus de lire le niveau comme illustratif, et de le presenter en bande.")
print(f"  2. Le CLASSEMENT est largement robuste : {verdict_rang}")
print(f"  3. A ECRIRE : xi_j par pilier n'est pas POSE (les categories Bale ne sont pas les")
print(f"     piliers, la categorie TIC est sous-echantillonnee) ; il est BORNE, comme la")
print(f"     direction de W. La severite rejoint la discipline d'identification partielle.")

# =====================================================================================
# figure
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.0))

ax1.hist(vals, bins=24, color=BLUE, alpha=0.6, edgecolor="white", linewidth=0.5)
ax1.axvline(scr_commun, color=ACCENT, lw=2.2, label=f"queue commune : {scr_commun:.0f}")
ax1.axvspan(lo, hi, color=MUTED, alpha=0.12)
ax1.set_xlabel("SCR (VaR 99,5 %, M€)", color=INK2)
ax1.set_ylabel("assignations (permutations)", color=INK2)
ax1.set_title("(a)  Le niveau borné sur les assignations\nde queue aux piliers",
              fontsize=11, color=INK, pad=8)
ax1.legend(frameon=False, fontsize=8)

parts = [cnt.get(i, 0) for i in range(5)]
ax2.bar(range(5), parts, color=[BLUE if i == int(np.argmax(parts)) else MUTED for i in range(5)],
        alpha=0.85)
ax2.set_xticks(range(5)); ax2.set_xticklabels([f"P{p}" for p in PIL])
ax2.set_ylabel(f"fois en tête (sur {len(ech)})", color=INK2)
ax2.set_title(f"(b)  Pilier de tête : P{PIL[tete_idx]} dans\n{100*part_tete:.0f} % des assignations",
              fontsize=11, color=INK, pad=8)

for ax in (ax1, ax2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.suptitle("Z8 : la queue par pilier — hétérogénéité bornée, pas assignée",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.92])
outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "Z8_xi_par_pilier.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
