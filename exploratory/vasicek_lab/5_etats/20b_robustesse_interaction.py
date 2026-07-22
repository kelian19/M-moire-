#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
20b : Robustesse de l'INTERACTION (super/sous-additive) du Delta_DORA.

Question soulevee par le script 20. La somme des surcouts marginaux (un pilier NC a la
fois, 16b) ne somme pas au surcout total (tous NC) ; l'ecart est l'interaction. Or son
SIGNE change entre deux resolutions MC a graine identique (16b a NY=60k : +1395 M,
super-additif ; 20 a NY=25k : -1889 M, sous-additif, OpRisk). Le total bouge peu, ce
sont les marginaux, differences de VaR en queue lourde, qui portent le bruit : une
interaction est une DIFFERENCE DE DIFFERENCES, l'estimateur le plus bruite de tous.

Ce script tranche en separant deux metriques calculees sur les MEMES simulations :
  - interaction en VaR 99,5 %  : la quantite du memoire, bruitee en queue lourde ;
  - interaction en PERTE MOYENNE : estimateur bien moins bruite, ou le mecanisme
    suggere la super-additivite (un pilier NC amplifie AUSSI les cascades amorcees
    ailleurs qui le traversent : le gain g du pilier courant s'applique le long de la
    marche, cf. scr_engine.cascade_set_dist).

Un processus PAR GRAINE (parallele), meme protocole que 16b/20 (lecture C, 3 canaux,
CRN). Verdict attendu : signe stable ou non selon la metrique ; le classement des
marginaux doit rester ROOT partout.

Usage : python 20b_robustesse_interaction.py <seed> [ny=60000]
Sortie : diagnostics texte (pas de figure). Exit 0.
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import euro_cascade_model as ec                              # noqa: E402
from euro_cascade_model import PARAMS, var                   # noqa: E402
import scr_engine as eng                                      # noqa: E402

W = 74
PIL = eng.PIL
SCENARIO = {"C": "S0_conforme", "PC": "S1_partiel", "NC": "S2_non_conforme"}
G_PROP = {"C": 0.45, "PC": 0.68, "NC": 0.90}
PU_MULT = {"C": 0.85, "PC": 1.00, "NC": 1.20}
MULT_ETAT = {st: ec.lambda_scenario("OPRISK", sc, mode="center") / PARAMS["OPRISK"]["lam_ref"]
             for st, sc in SCENARIO.items()}
_SHARE = {j: eng.LAMBDA[j] for j in PIL}
_STOT = sum(_SHARE.values())
SHARE = {j: _SHARE[j] / _STOT for j in PIL}

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 909
NY = int(sys.argv[2]) if len(sys.argv) > 2 else 60_000


def annual_config(source, state_map, ny, seed):
    """Vecteur des pertes annuelles d'une configuration {pilier -> etat} (CRN)."""
    sp = PARAMS[source]
    lam_vec = {j: sp["lam_ref"] * SHARE[j] * MULT_ETAT[state_map[j]] for j in PIL}
    g_vec = {j: G_PROP[state_map[j]] for j in PIL}
    p_u_vec = {j: min(0.999, sp["p_u"] * PU_MULT[state_map[j]]) for j in PIL}
    rng = np.random.default_rng(seed)
    return ec.simulate_euro_pp(lam_vec, g_vec, sp["xi"], sp["sigma"], sp["u"],
                               p_u_vec, sp["cap"], ny, rng)


print("=" * W)
print(f"20b  interaction du Delta_DORA : seed={SEED}  ny={NY:,}")
print("=" * W)
for source in ("OPRISK", "PRC"):
    metr = {}                                                # config -> (VaR, mean)
    cfgs = {"C": {j: "C" for j in PIL}, "NC": {j: "NC" for j in PIL}}
    for k in PIL:
        c = {j: "C" for j in PIL}
        c[k] = "NC"
        cfgs[f"solo{k}"] = c
    for name, cfg in cfgs.items():
        a = annual_config(source, cfg, NY, SEED)
        metr[name] = (var(a), float(a.mean()))
    out = {}
    for m, lab in ((0, "VaR 99,5 %"), (1, "perte moyenne")):
        base = metr["C"][m]
        d_tot = metr["NC"][m] - base
        margs = {k: metr[f"solo{k}"][m] - base for k in PIL}
        inter = d_tot - sum(margs.values())
        order = sorted(PIL, key=lambda k: margs[k], reverse=True)
        out[m] = (d_tot, margs, inter, order)
        print(f"\n  {source}  [{lab}]")
        print(f"    Delta total = {d_tot:9.1f} M   somme marginaux = {sum(margs.values()):9.1f} M")
        print(f"    INTERACTION = {inter:+9.1f} M   "
              f"({'super' if inter > 0 else 'sous'}-additif)")
        print(f"    classement marginaux : {' > '.join(f'P{k}' for k in order)}")
print("\nEXIT 0")
