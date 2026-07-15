# -*- coding: utf-8 -*-
"""Moteur d'agregation du SCR : assemble frequence, cascade et severite.

Partage par 09 (SCR chiffre) et 10 (surface de sensibilite). Trois briques :
  - frequence : frequence_model (Poisson melange, facteur Y commun) ;
  - cascade   : echantillonneur auto-evitant avec etat d'arret (noyau du draft
                probas_conditionnelles), pilote par le gain g ;
  - severite  : severite_model (loi de perte par pilier).

Boucle d'une annee : tirer Y -> tirer N_j | Y -> pour chaque incident amorce en j,
tirer l'ensemble cascade S (gain g) -> severite X(S) = somme des L_p -> perte annuelle.
Le SCR est la VaR 99,5 % de la perte annuelle (Solvabilite II art. 101).

Deux echelles de dependance disjointes (voir ossature_scr.tex) : Y = inter-incidents
(frequence + co-occurrence), cascade = intra-incident (etendue d'un incident). Aucun
troisieme canal : severites independantes sachant S.
"""

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CASCADE = os.path.abspath(os.path.join(_HERE, "..", "cascade_qualitative"))
for _p in (_CASCADE, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from cascade_model import ROOT, TRANS  # noqa: E402
import severite_model as sev           # noqa: E402
import frequence_model as freq         # noqa: E402

PIL = freq.PIL                          # [1,2,3,4,5]
LAMBDA = freq.LAMBDA
G_BASE = 0.90                           # gain de propagation en cas de base (cf. draft)

# rangs de colonne pour vectoriser (pilier -> indice 0..4)
_COL = {j: c for c, j in enumerate(PIL)}
_SROW = {j: sum(TRANS[j].values()) for j in PIL}   # s_j = somme de la ligne TRANS
_MAXS = max(_SROW.values())


# ============================================================ cascade auto-evitante
def cascade_set_dist(amorce, g):
    """Distribution EXACTE de l'ensemble S d'un incident amorce en `amorce`, gain g.

    Noyau auto-evitant avec etat d'arret : depuis j, on continue avec proba
    e_j = g*s_j/max_s vers un pilier tire ~ TRANS[j]/s_j ; un pilier deja tombe
    (ou l'arret, proba 1-e_j) eteint la cascade. Renvoie {frozenset(S): proba}.
    """
    dist = {}

    def rec(cur, visited, p):
        e = g * _SROW[cur] / _MAXS
        srow = _SROW[cur]
        # fin ici : arret pur (1-e) OU propagation vers un pilier deja visite
        p_rehit = e * sum(w for k, w in TRANS[cur].items() if k in visited) / srow
        key = frozenset(visited)
        dist[key] = dist.get(key, 0.0) + p * (1.0 - e + p_rehit)
        # propagation vers un nouveau pilier
        for k, w in TRANS[cur].items():
            if k not in visited:
                rec(k, visited | {k}, p * e * w / srow)

    rec(amorce, frozenset({amorce}), 1.0)
    return dist


def build_cascade_tables(g):
    """Pour chaque amorce : (indicateur [nsets x 5] 0/1, probas [nsets]). Somme=1."""
    tables = {}
    for j in PIL:
        dist = cascade_set_dist(j, g)
        sets = list(dist.keys())
        probs = np.array([dist[s] for s in sets])
        ind = np.zeros((len(sets), len(PIL)))
        for r, s in enumerate(sets):
            for p in s:
                ind[r, _COL[p]] = 1.0
        tables[j] = (ind, probs / probs.sum())   # renormalise (garde-fou numerique)
    return tables


# ============================================================ agregation Monte-Carlo
def simulate_annual_losses(n_years, rng, g=G_BASE, xi=sev.XI_BASE, a=freq.A_LOAD):
    """Perte annuelle agregee sur n_years annees (unites normalisees de severite)."""
    tables = build_cascade_tables(g)
    Y = rng.standard_normal(n_years)
    m = np.exp(a * Y - a * a / 2.0)              # facteur systemique commun
    annual = np.zeros(n_years)
    for j in PIL:
        Nj = rng.poisson(LAMBDA[j] * m)          # incidents amorces en j, par annee
        M = int(Nj.sum())
        if M == 0:
            continue
        year_of = np.repeat(np.arange(n_years), Nj)
        ind, probs = tables[j]
        idx = rng.choice(len(probs), size=M, p=probs)
        inc_ind = ind[idx]                        # M x 5 : piliers touches par incident
        # severite : tirer une perte par pilier, masquer, sommer
        L = np.column_stack([sev.draw_loss(p, M, rng, xi) for p in PIL])
        X = (L * inc_ind).sum(axis=1)             # severite par incident
        annual += np.bincount(year_of, weights=X, minlength=n_years)
    return annual


def simulate_losses_by_pillar(n_years, rng, g=G_BASE, xi=sev.XI_BASE, a=freq.A_LOAD):
    """Perte annuelle ventilee par pilier d'AMORCE : matrice [n_years x len(PIL)].

    Colonne c = perte des incidents amorces au pilier PIL[c] (severite de cascade
    incluse). La somme des colonnes redonne la perte agregee de simulate_annual_losses.
    Sert aux copules (marges par pilier) et a l'allocation d'Euler.
    """
    tables = build_cascade_tables(g)
    Y = rng.standard_normal(n_years)
    m = np.exp(a * Y - a * a / 2.0)
    mat = np.zeros((n_years, len(PIL)))
    for c, j in enumerate(PIL):
        Nj = rng.poisson(LAMBDA[j] * m)
        M = int(Nj.sum())
        if M == 0:
            continue
        year_of = np.repeat(np.arange(n_years), Nj)
        ind, probs = tables[j]
        idx = rng.choice(len(probs), size=M, p=probs)
        inc_ind = ind[idx]
        L = np.column_stack([sev.draw_loss(p, M, rng, xi) for p in PIL])
        X = (L * inc_ind).sum(axis=1)
        mat[:, c] = np.bincount(year_of, weights=X, minlength=n_years)
    return mat


# ============================================================ mesures de risque
def var(losses, alpha=0.995):
    return float(np.quantile(losses, alpha))


def tvar(losses, alpha=0.995):
    v = var(losses, alpha)
    tail = losses[losses >= v]
    return float(tail.mean()) if tail.size else float(v)


def scr(losses, alpha=0.995, centre=True):
    """SCR = VaR (capital economique = VaR - E si centre=True)."""
    v = var(losses, alpha)
    return v - float(losses.mean()) if centre else v


def var_ci(losses, alpha=0.995, n_boot=400, rng=None):
    """Intervalle de confiance bootstrap sur la VaR (percentiles 2,5 % / 97,5 %)."""
    rng = rng or np.random.default_rng(0)
    n = losses.size
    qs = np.empty(n_boot)
    for b in range(n_boot):
        qs[b] = np.quantile(losses[rng.integers(0, n, n)], alpha)
    return float(np.percentile(qs, 2.5)), float(np.percentile(qs, 97.5))
