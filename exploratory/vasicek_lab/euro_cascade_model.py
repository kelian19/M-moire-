# -*- coding: utf-8 -*-
"""Simulateur euro-cascade partage : severite/frequence du memoire, agregation cascade.

Source unique du moteur euro-cascade, importe par 12 (SCR euro) et 13 (Delta_DORA
bootstrap). Reutilise TELS QUELS les modules du vrai modele :
  - severite : src.aggregation.lda.simulate_remediation_severity (GPD euro spliced) ;
  - parametres OpRisk/PRC : src.utils.config ; sur-dispersion phi de FREQUENCY.
La seule difference avec le memoire est l'AGREGATION : un incident amorce se propage a
un ensemble S de piliers (Vasicek dirige : noyau e_j = g*s_j/max_s, ensemble auto-evitant,
cf. scr_engine / note_vasicek_dirige) et chaque pilier touche tire sa severite.
"""

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
for _p in (_REPO, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from src.aggregation.lda import simulate_remediation_severity   # noqa: E402
from src.utils.config import OPRISK, PRC, FREQUENCY, SCR_DORA    # noqa: E402
import scr_engine as eng                                          # noqa: E402  (cascade dirigee)

PHI = FREQUENCY["dispersion_factor"]        # 9.2
PIL = eng.PIL
G_BASE = eng.G_BASE                          # gain de propagation de base (0.90)

# parametres euro par source (severite GPD + frequence de reference), depuis la config figee
PARAMS = {
    "OPRISK": dict(xi=OPRISK["xi"], sigma=OPRISK["sigma_eur"], u=OPRISK["seuil_u_eur"],
                   p_u=OPRISK["p_u"], cap=None,
                   xi_ic90=OPRISK["xi_ic90"], sigma_ic90=OPRISK["sigma_ic90"],
                   lam_ref=OPRISK["n_incidents"] / OPRISK["n_years"]),
    "PRC":    dict(xi=PRC["xi"], sigma=PRC["sigma_eur"], u=PRC["seuil_u_eur"],
                   p_u=PRC["p_u"], cap=SCR_DORA["cap_eur"],
                   xi_ic90=PRC["xi_ic90"], sigma_ic90=PRC["sigma_ic90"],
                   lam_ref=FREQUENCY["lambda_ref"]),
}

MEMOIRE_TOTAL = {"OPRISK": 9259.5, "PRC": 2772.7}      # SCR total 4 briques (chap. 5, S2)
MEMOIRE_DELTA = {                                       # Delta_DORA median + IC90 (config)
    "OPRISK": {"median": 3879.3, "ic90": [1496.9, 22249.3]},
    "PRC":    {"median": 2014.7, "ic90": [1606.9, 2366.1]},
}


def simulate_euro(lam, g, xi, sigma, u, p_u, cap, n_years, rng):
    """Perte annuelle agregee (M€) par la cascade. lam = frequence annuelle d'AMORCES."""
    r = lam / (PHI - 1.0)
    p = r / (r + lam)
    counts = rng.negative_binomial(r, p, size=n_years)
    T = int(counts.sum())
    annual = np.zeros(n_years)
    if T == 0:
        return annual
    year_of_event = np.repeat(np.arange(n_years), counts)
    tables = eng.build_cascade_tables(g)
    w = np.array([eng.LAMBDA[j] for j in PIL], float)
    w /= w.sum()                                        # amorce ~ ROOT
    amorce = rng.choice(len(PIL), size=T, p=w)
    for c_am, j in enumerate(PIL):
        ev = np.where(amorce == c_am)[0]
        if ev.size == 0:
            continue
        yr = year_of_event[ev]
        ind, probs = tables[j]
        idx = rng.choice(len(probs), size=ev.size, p=probs)
        for s in range(len(probs)):
            sel = idx == s
            if not sel.any():
                continue
            yrs = yr[sel]
            for _ in range(int(ind[s].sum())):          # un tirage par pilier touche
                sev = simulate_remediation_severity(yrs.size, xi, sigma, u, p_u, cap, rng)
                annual += np.bincount(yrs, weights=sev, minlength=n_years)
    return annual


def var(x, alpha=0.995):
    return float(np.quantile(x, alpha))


def lambda_scenario(source, scenario, mode="center", rng=None):
    """Frequence annuelle sous un scenario DORA (multiplicateurs de src.frequency.negbin)."""
    from src.frequency.negbin import compute_lambda_scenario
    return compute_lambda_scenario(PARAMS[source]["lam_ref"], scenario,
                                   mode=mode, rng=rng)["lambda_global"]


def sample_severity_params(source, rng):
    """Tire (xi, sigma) dans leur IC90 (approx normale) : incertitude de severite bootstrap."""
    xi_lo, xi_hi = PARAMS[source]["xi_ic90"]
    sg_lo, sg_hi = PARAMS[source]["sigma_ic90"]
    xi = rng.normal((xi_lo + xi_hi) / 2, (xi_hi - xi_lo) / (2 * 1.645))
    sg = rng.normal((sg_lo + sg_hi) / 2, (sg_hi - sg_lo) / (2 * 1.645))
    return max(0.05, float(xi)), max(1.0, float(sg))
