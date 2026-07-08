#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02 — Banc d'essai du seuil K_i : Phi^-1(PD) vs EVT.

On simule des severites cyber REELLEMENT a queue lourde (Pareto generalisee) avec
SOUS-DECLARATION (les petits incidents sont rarement declares). On compare trois
facons d'estimer le capital de queue (VaR 99,5 %) et la stabilite du seuil.

  M1  monde gaussien/lognormal : on ajuste une loi lognormale (queue fine) et on
      lit son quantile 99,5 % — l'esprit de K = Phi^-1(PD).
  M2  quantile empirique 99,5 % des pertes observees.
  M3  EVT / POT : loi de Pareto generalisee (GPD) sur les depassements d'un seuil
      haut — n'utilise que les GROS incidents, fiablement declares.

Deux resultats :
  (J1)  la sous-declaration des PETITS incidents ne biaise PAS l'indice de queue
        (invariance par troncature a gauche) -> EVT robuste ; lognormal biaise.
  (J2)  le seuil classique Phi^-1(PD) DERIVE dans le temps (non-stationnarite) ;
        l'indice de queue EVT reste stable.

Sortie : diagnostics + figure J_seuil_Ki.png
"""

import os
import numpy as np
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260708)

# ---------------------------------------------------------------- verite (DGP)
XI, SCALE = 0.40, 1.0          # GPD : queue lourde (Frechet), variance finie
P = 0.995                      # niveau de capital DORA-like
S0, AREP = 0.6, 1.3            # sous-declaration : q(s) croit avec la taille


def q_report(s):               # proba qu'un incident de taille s soit declare
    return 1.0 / (1.0 + np.exp(-AREP * (np.log(s + 1e-9) - np.log(S0))))


def draw_true(n):
    return stats.genpareto.rvs(c=XI, scale=SCALE, size=n, random_state=rng)


def thin(sev):                 # applique la sous-declaration
    keep = rng.random(sev.size) < q_report(sev)
    return sev[keep]


# verite = quantile 99,5 % de la loi DECLAREE (celle qu'on observe reellement)
big = draw_true(4_000_000)
big_obs = thin(big)
TRUTH = np.quantile(big_obs, P)
print(f"Verite : VaR99,5 de la severite declaree = {TRUTH:.2f} M EUR")
print(f"  (indice de queue vrai xi = {XI})\n")


# ---------------------------------------------------------------- estimateurs
def m1_lognormal(x):
    s, loc, sc = stats.lognorm.fit(x, floc=0)
    return stats.lognorm.ppf(P, s, loc=0, scale=sc)


def m2_empirique(x):
    return np.quantile(x, P)


def m3_evt_pot(x, u_q=0.80):
    u = np.quantile(x, u_q)
    exc = x[x > u] - u
    if exc.size < 30:
        return np.nan, np.nan
    c, _, beta = stats.genpareto.fit(exc, floc=0)
    n, nu = x.size, exc.size
    var = u + (beta / c) * ((n / nu * (1 - P)) ** (-c) - 1)
    return var, c                # renvoie aussi l'indice de queue estime


# ---------------------------------------------------------------- (J2) course au capital
NREP, NOBS = 500, 800
res = {"M1 lognormal": [], "M2 empirique": [], "M3 EVT-POT": []}
xis_full, xis_obs = [], []
for _ in range(NREP):
    true_sev = draw_true(NOBS)
    obs = thin(true_sev)
    if obs.size < 100:
        continue
    res["M1 lognormal"].append(m1_lognormal(obs) / TRUTH)
    res["M2 empirique"].append(m2_empirique(obs) / TRUTH)
    var3, xi3 = m3_evt_pot(obs)
    res["M3 EVT-POT"].append(var3 / TRUTH)
    xis_obs.append(xi3)
    # indice de queue sur l'echantillon COMPLET (sans sous-declaration)
    _, xif = m3_evt_pot(true_sev)
    xis_full.append(xif)

print("Course au capital (estimation / verite, sur %d tirages) :" % NREP)
print(f"{'methode':<16}{'biais median':>14}{'RMSE':>10}")
for k, v in res.items():
    v = np.array(v)
    v = v[np.isfinite(v)]
    biais = np.median(v) - 1
    rmse = np.sqrt(np.mean((v - 1) ** 2))
    print(f"{k:<16}{biais:>+13.1%}{rmse:>10.2f}")

print("\nInvariance de l'indice de queue a la sous-declaration (J1) :")
print(f"  xi estime sur donnees COMPLETES  = {np.nanmedian(xis_full):.3f}")
print(f"  xi estime sur donnees DECLAREES  = {np.nanmedian(xis_obs):.3f}")
print(f"  (vrai xi = {XI} : la troncature des petits ne biaise pas la queue)\n")

# ---------------------------------------------------------------- (J1bis) derive temporelle
T, RPER = 12, 8
U_REG = 3.0                     # barre de materialite fixe (DORA)
K_class, xi_time = [], []
for t in range(T):
    scale_t = SCALE * (1 + 0.6 * t / (T - 1))      # menace qui monte
    ks, xs = [], []
    for _ in range(RPER):                          # moyenne pour debruiter
        sev = stats.genpareto.rvs(c=XI, scale=scale_t, size=8000, random_state=rng)
        obs = thin(sev)
        pd_hat = min(max(np.mean(obs > U_REG), 1e-4), 0.5)
        ks.append(stats.norm.ppf(1 - pd_hat))      # K = Phi^-1(1-PD)
        xs.append(m3_evt_pot(obs)[1])
    K_class.append(np.mean(ks))
    xi_time.append(np.nanmean(xs))
print("Derive du seuil dans le temps :")
print(f"  K classique Phi^-1 : de {K_class[0]:.2f} a {K_class[-1]:.2f} "
      f"(amplitude {max(K_class)-min(K_class):.2f})")
print(f"  indice de queue EVT : de {xi_time[0]:.2f} a {xi_time[-1]:.2f} "
      f"(amplitude {max(xi_time)-min(xi_time):.2f})")

# ---------------------------------------------------------------- figure
mpl.rcParams.update({
    "font.family": ["DejaVu Sans", "Segoe UI", "sans-serif"],
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb",
})
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
ACCENT = "#eb6834"
BL = ["#b7d3f6", "#3987e5", "#184f95"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.2),
                               gridspec_kw={"width_ratios": [1.1, 1]})

# panneau 1 : course au capital
data = [np.clip(np.array(res[k])[np.isfinite(res[k])], 0, 3)
        for k in res]
bp = ax1.boxplot(data, orientation="vertical", patch_artist=True, widths=0.6,
                 showfliers=False, medianprops=dict(color=INK, lw=1.6))
for patch, c in zip(bp["boxes"], BL):
    patch.set_facecolor(c); patch.set_edgecolor("#fcfcfb")
ax1.axhline(1.0, color=ACCENT, lw=2, zorder=0)
ax1.text(3.35, 1.0, "verite", color=ACCENT, va="center", fontsize=9, fontweight="bold")
ax1.set_xticklabels(list(res.keys()), fontsize=9.5)
ax1.set_ylabel("capital estime / capital vrai", color=INK2)
ax1.set_ylim(0, 2.4)
ax1.set_title("(J2)  La course au capital  (VaR 99,5 %)", fontsize=11, color=INK, pad=8)
ax1.yaxis.grid(True, color=GRID, lw=0.8)

# panneau 2 : derive temporelle
tt = np.arange(1, T + 1)
axb = ax2.twinx()
l1, = ax2.plot(tt, K_class, "-o", color=ACCENT, lw=2, ms=5, label="K classique $\\Phi^{-1}$")
l2, = axb.plot(tt, xi_time, "-s", color=BL[2], lw=2, ms=5, label="indice de queue EVT $\\xi$")
ax2.set_xlabel("periode (menace croissante →)", color=INK2)
ax2.set_ylabel("seuil classique K", color=ACCENT)
axb.set_ylabel("indice de queue EVT", color=BL[2])
axb.set_ylim(0, 0.8)
ax2.tick_params(axis="y", colors=ACCENT)
axb.tick_params(axis="y", colors=BL[2])
ax2.set_title("(J1)  Le seuil classique derive, la queue EVT est stable",
              fontsize=11, color=INK, pad=8)
ax2.legend(handles=[l1, l2], loc="upper center", frameon=False, fontsize=9)

fig.suptitle("Seuil K_i : pourquoi Phi^-1(PD) tombe et l'EVT tient",
             fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.94])

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "J_seuil_Ki.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
