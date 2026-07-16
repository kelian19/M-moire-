#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
16 : Vasicek multi-etats. SCR_DORA par etat de conformite + Delta_DORA en euros.

Prolonge 13 (2 etats) et remplace la variable latente statique de l'ancien memoire
(src/compliance/latent.py, decision A validee : le multi-etats remplace le latent).
Deux apports par rapport a 16a :

  1.1  LES ETATS VIENNENT DE SEUILS ORDONNES SUR UNE LATENTE, pas d'etiquettes posees.
       Une capacite de conformite latente C* ~ N(0,1) se decompose facteur systemique +
       idiosyncratique (Vasicek) :  C* = gamma*Theta + sqrt(1-gamma^2)*eps.  Deux seuils
       ordonnes K_bas < K_haut decoupent les trois etats :
           Non conforme (NC)         si  C* <= K_bas
           Partiellement conforme(PC) si  K_bas < C* <= K_haut
           Conforme (C)              si  C* >  K_haut
       Les seuils sont fixes par les probabilites d'etat ANCREES sur les enquetes de
       conformite (K_bas = Phi^-1(p_NC), K_haut = Phi^-1(p_NC+p_PC)). Le facteur Theta
       rend les probabilites d'etat CONDITIONNELLES a l'environnement : une crise cyber
       (Theta bas) fait basculer la masse vers NC (ce que faisait l'amplification
       systemique de l'ancien latent, ici a trois etats ordonnes).

  1.2  L'ETAT PILOTE LES TROIS CANAUX (pas seulement deux) :
       - FREQUENCE  lambda : multiplicateurs S0/S1/S2 de src.frequency.negbin ;
       - PROPAGATION g     : une entite plus conforme contient la contagion (g plus bas) ;
       - DETECTION  p_u    : le taux de MATERIALITE (script 04). Une entite conforme
         intercepte/remedie tot -> une moindre fraction d'incidents atteint la severite
         materielle (p_u plus bas) ; non conforme -> detection tardive -> p_u plus haut.
       Trois lectures emboitees rendent l'apport de chaque canal visible et evitent qu'un
       canal domine en silence :
         A frequence seule (comparable au memoire) ; B + propagation ; C + detection.

ETAT GLOBAL a l'entite (tous piliers alignes). Le passage PAR PILIER (latentes C*_j
correlees par Theta, canaux par pilier) est le script 16b, qui demande d'ouvrir le moteur
aux parametres par pilier.

PORTEE. Severite euros = SAS OpRisk (branche via euro_cascade_model). Choix de modelisation
NON calibres, presentes en lecture separee ou en sensibilite : le triplet de gains
(g_C<g_PC<g_NC), le triplet de detection (p_u croissant de C a NC), les probabilites d'etat
ancrees et gamma. Delta_DORA a graine MC COMMUNE entre etats (l'ecart ne vient que du
changement d'etat). Ne touche ni src/ ni memoire/.

Sortie : diagnostics (probas d'etat normal/crise ; SCR par etat, 3 lectures ; SCR espere ;
Delta_DORA + IC90) + figure S10_scr_multi_etats.png. Verifie exit 0.
"""

import os
import sys

import numpy as np
from scipy.stats import norm
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import euro_cascade_model as ec                              # noqa: E402
from euro_cascade_model import PARAMS, MEMOIRE_DELTA, var    # noqa: E402

W = 74
ETATS = ["C", "PC", "NC"]
LABEL = {"C": "Conforme", "PC": "Partiellement conforme", "NC": "Non conforme"}
SCENARIO = {"C": "S0_conforme", "PC": "S1_partiel", "NC": "S2_non_conforme"}

# --- 1.1 latente : probas d'etat ancrees + facteur systemique -----------------------
# Ancrage (illustratif, sources des enquetes de l'ancien latent.py : Deloitte European
# Survey 2025, ESA dry-run 2024 ; ~50 % pas pleinement conformes fin 2025).
P_ETAT = {"NC": 0.35, "PC": 0.35, "C": 0.30}     # somme = 1
GAMMA = 0.68                                      # charge systemique (proxy concentration cloud)
K_BAS = norm.ppf(P_ETAT["NC"])                    # C* <= K_bas -> NC
K_HAUT = norm.ppf(P_ETAT["NC"] + P_ETAT["PC"])    # C* > K_haut -> C
THETA_CRISE = -2.5                                # environnement de crise systemique

# --- 1.2 les trois canaux, par etat --------------------------------------------------
G_FREQ = {"C": 0.90, "PC": 0.90, "NC": 0.90}      # lecture A : g constant (frequence seule)
G_PROP = {"C": 0.45, "PC": 0.68, "NC": 0.90}      # lecture B : g croit de C a NC (non calibre)
PU_MULT = {"C": 0.85, "PC": 1.00, "NC": 1.20}     # lecture C : detection (p_u module, non calibre)

BOOT = {"OPRISK": dict(B=120, ny=20_000), "PRC": dict(B=60, ny=3_000)}
NY_DET = 80_000


def titre(s):
    print("\n" + "=" * W + f"\n{s}\n" + "=" * W)


def etat_probs(theta):
    """Probabilites (NC, PC, C) conditionnelles au facteur systemique theta (Vasicek)."""
    denom = np.sqrt(1.0 - GAMMA ** 2)
    p_nc = norm.cdf((K_BAS - GAMMA * theta) / denom)
    p_ncpc = norm.cdf((K_HAUT - GAMMA * theta) / denom)
    return {"NC": p_nc, "PC": p_ncpc - p_nc, "C": 1.0 - p_ncpc}


def scr_state(source, etat, g, pu_mult, xi, sigma, ny, seed):
    """SCR (VaR 99,5 %) d'un etat, canaux (lambda, g, p_u) ; graine donnee (CRN entre etats)."""
    sp = PARAMS[source]
    lam = ec.lambda_scenario(source, SCENARIO[etat], mode="center")
    p_u = min(0.999, sp["p_u"] * pu_mult)
    rng = np.random.default_rng(seed)
    return var(ec.simulate_euro(lam, g, xi, sigma, sp["u"], p_u, sp["cap"], ny, rng))


# ============================================================ 1.1 la latente et ses etats
titre("1.1  Latente de conformite : seuils ordonnes et probabilites d'etat")
print(f"  C* = gamma*Theta + sqrt(1-gamma^2)*eps,  gamma = {GAMMA}")
print(f"  seuils : K_bas = Phi^-1(p_NC) = {K_BAS:+.3f}   K_haut = Phi^-1(p_NC+p_PC) = {K_HAUT:+.3f}")
print(f"  ancrage probas d'etat : NC {P_ETAT['NC']:.0%}  PC {P_ETAT['PC']:.0%}  C {P_ETAT['C']:.0%}")
pn = P_ETAT                                       # marginale = ancrage (par construction)
pc = etat_probs(THETA_CRISE)                      # conditionnelle a une crise systemique
print(f"\n  {'etat':<26}{'P (normal, marginale)':>22}{'P (crise, Theta=-2,5)':>24}")
for e in ETATS:
    print(f"  {LABEL[e]:<26}{pn[e]:>21.1%}{pc[e]:>23.1%}")
print("  La marginale (integree sur Theta) redonne l'ancrage : controle de coherence.")
print("  Lecture : une crise systemique deplace la masse vers Non conforme (bascule DORA).")


# ============================================================ 1.2 + SCR par etat (3 lectures)
titre("1.2  SCR_DORA par etat, 3 canaux emboites (graine MC commune entre etats)")
LECTURES = {"A": (G_FREQ, {e: 1.0 for e in ETATS}),   # frequence seule
            "B": (G_PROP, {e: 1.0 for e in ETATS}),   # + propagation
            "C": (G_PROP, PU_MULT)}                     # + detection
LEC_LAB = {"A": "freq", "B": "freq+prop", "C": "freq+prop+detec"}
scr_det = {}
for source in ("OPRISK", "PRC"):
    sp = PARAMS[source]
    print(f"\n  {source}  (severite {source})")
    print(f"  {'etat':<26}{'SCR A (freq)':>15}{'SCR B (+prop)':>15}{'SCR C (+detec)':>16}")
    seed_src = 4242
    for e in ETATS:
        row = []
        for lect in ("A", "B", "C"):
            gmap, pumap = LECTURES[lect]
            v = scr_state(source, e, gmap[e], pumap[e], sp["xi"], sp["sigma"], NY_DET, seed_src)
            scr_det[(source, lect, e)] = v
            row.append(v)
        print(f"  {LABEL[e]:<26}{row[0]:>13.0f} M{row[1]:>13.0f} M{row[2]:>14.0f} M")
    # Delta et SCR espere (lecture C, la plus complete), poids = probas d'etat normal
    for lect in ("A", "C"):
        c = scr_det[(source, lect, "C")]
        d_pc = scr_det[(source, lect, "PC")] - c
        d_nc = scr_det[(source, lect, "NC")] - c
        esp_n = sum(pn[e] * scr_det[(source, lect, e)] for e in ETATS)
        esp_c = sum(pc[e] * scr_det[(source, lect, e)] for e in ETATS)
        print(f"    lecture {lect} ({LEC_LAB[lect]}): Delta(PC vs C)={d_pc:6.0f}  Delta(NC vs C)={d_nc:6.0f}"
              f"  |  SCR espere normal={esp_n:6.0f}  crise={esp_c:6.0f} M")


# ============================================================ Delta_DORA bootstrap (canal frequence)
titre("Delta_DORA bootstrap 2 niveaux (canal FREQUENCE, lecture A, g=0,90 fixe)")
print("  Comparable au memoire : la conformite agit sur la frequence (S0/S1/S2).")
boot = {}
for source in ("OPRISK", "PRC"):
    cfg = BOOT[source]
    sp = PARAMS[source]
    orng = np.random.default_rng(20260716)
    acc = {"PC": [], "NC": []}
    for b in range(cfg["B"]):
        lam = {e: ec.lambda_scenario(source, SCENARIO[e], mode="sample", rng=orng) for e in ETATS}
        xi_b, sg_b = ec.sample_severity_params(source, orng)
        seed_b = 2000 + b
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
        print(f"\n  {source} - Delta_DORA({cible} vs C)  ({cfg['B']} tirages x {cfg['ny']:,} annees) :")
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

# panneau A : echelle du SCR sur les 3 etats (OpRisk), 3 lectures emboitees
x = np.arange(len(ETATS))
ya = [scr_det[("OPRISK", "A", e)] for e in ETATS]
yb = [scr_det[("OPRISK", "B", e)] for e in ETATS]
ycc = [scr_det[("OPRISK", "C", e)] for e in ETATS]
axA.plot(x, ya, "-o", color=BLUE, lw=2.0, ms=6, label="A frequence seule")
axA.plot(x, yb, "-s", color=GREEN, lw=2.0, ms=6, label="B + propagation")
axA.plot(x, ycc, "-^", color=ACCENT, lw=2.0, ms=6, label="C + detection")
_lo = min(min(ya), min(yb), min(ycc))
_hi = max(max(ya), max(yb), max(ycc))
axA.set_ylim(_lo - 0.10 * (_hi - _lo), _hi + 0.10 * (_hi - _lo))
axA.set_xlim(-0.25, len(ETATS) - 0.75)
axA.set_xticks(x)
axA.set_xticklabels([LABEL[e] for e in ETATS], fontsize=9)
axA.set_ylabel("SCR_DORA (M€)", fontsize=9.5, color=INK2)
axA.set_title("(A)  SCR par etat, 3 canaux emboites (OpRisk)", fontsize=10, color=INK, pad=6)
axA.legend(fontsize=8.2, frameon=False, loc="upper left")
axA.grid(alpha=0.25, lw=0.5)

# panneau B : la latente -> probabilites d'etat, normal vs crise
xb = np.arange(len(ETATS))
wbar = 0.38
pn_v = [pn[e] for e in ETATS]
pc_v = [pc[e] for e in ETATS]
axB.bar(xb - wbar / 2, pn_v, wbar, color=BLUE, alpha=0.85, label="normal (marginale)")
axB.bar(xb + wbar / 2, pc_v, wbar, color=ACCENT, alpha=0.85, label="crise (Theta=-2,5)")
for xi_, v in zip(xb - wbar / 2, pn_v):
    axB.annotate(f"{v:.0%}", (xi_, v), textcoords="offset points", xytext=(0, 3),
                 ha="center", fontsize=8, color=BLUE)
for xi_, v in zip(xb + wbar / 2, pc_v):
    axB.annotate(f"{v:.0%}", (xi_, v), textcoords="offset points", xytext=(0, 3),
                 ha="center", fontsize=8, color=ACCENT)
axB.set_xticks(xb)
axB.set_xticklabels([LABEL[e] for e in ETATS], fontsize=9)
axB.set_ylabel("probabilite d'etat", fontsize=9.5, color=INK2)
axB.set_ylim(0, max(pc_v) * 1.25)
axB.set_title("(B)  1.1 latente -> etats : la crise bascule vers Non conforme",
              fontsize=10, color=INK, pad=6)
axB.legend(fontsize=8.2, frameon=False, loc="upper left")
axB.grid(alpha=0.25, lw=0.5, axis="y")

fig.suptitle("Vasicek multi-etats : latente a seuils ordonnes, 3 canaux, SCR_DORA par etat",
             fontsize=12.3, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.95])

outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "S10_scr_multi_etats.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
