#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
46 : le SCR est un quantile d'un objet incertain. VaR par branchement vs VaR predictive.

Remarque de Caroline Hillairet : estimer le SCR par un QUANTILE (VaR 99,5 %) est fragile parce
que les DONNEES elles-memes sont incertaines. \"Prendre le quantile de quelque chose d'incertain
est mauvais.\" Ce script traite la remarque de front sur la calibration OpRisk.

LE POINT. Le SCR est defini par la reglementation comme une VaR 99,5 % : on ne peut pas
l'abandonner. Mais aujourd'hui on prend le quantile d'une loi ESTIMEE en un point (plug-in) :
VaR(xi_hat). Or xi est mal connu (IC90 large), et le quantile a 99,5 % lit la queue la ou les
donnees sont les plus rares : l'operation AMPLIFIE l'incertitude.

LA REPONSE : integrer l'incertitude de parametre AVANT de prendre le quantile, c'est-a-dire
prendre le quantile de la loi PREDICTIVE (melange des lois GPD sur la distribution bootstrap de
(xi, sigma)). Melanger des queues donne une queue plus lourde que la queue moyenne : la VaR
predictive est PLUS HAUTE que la plug-in. Elle incorpore le risque d'estimation, ce que le
regulateur attend d'un modele interne. C'est la traduction exacte de la remarque : le bon
quantile est celui de l'objet incertain COMPLET, pas celui d'un point estime.

On rapporte alors le capital en INTERVALLE (bande bootstrap) et non en point, et on lit un
PROFIL VaR/TVaR par niveau plutot qu'un seul point.

Sortie : diagnostics + figure J2_var_predictive.png.
"""

import os
import sys

import numpy as np
from scipy.stats import genpareto
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for _p in (REPO, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from src.severity.oprisk_analysis import load_clean, filter_cyber, filter_finance, USD_EUR  # noqa: E402

WID = 82
LEVELS = [0.99, 0.995, 0.999]
B = 2000                      # rééchantillons bootstrap
N_SIM = 3_000_000             # tirages pour la loi prédictive
SEED = 20260727


def titre(s):
    print("\n" + "=" * WID + f"\n{s}\n" + "=" * WID)


def var_gpd(alpha, xi, sigma, u, zu):
    return u + (sigma / xi) * (((1 - alpha) / zu) ** (-xi) - 1)


def tvar_gpd(alpha, xi, sigma, u, zu):
    if xi >= 1:
        return np.nan
    V = var_gpd(alpha, xi, sigma, u, zu)
    return V / (1 - xi) + (sigma - xi * u) / (1 - xi)


# =====================================================================================
titre("Calibration OpRisk (cyber x finance), POT au percentile 85")
# =====================================================================================
df = filter_finance(filter_cyber(load_clean(
    os.path.join(REPO, "data", "raw", "SAS_OpRisk_Global_Data_June_2026.xlsx"))))
loss = df["loss"].to_numpy() * USD_EUR                 # M$ -> M€ (le shape xi est invariant)
u = float(np.quantile(loss, 0.85))
zu = float((loss > u).mean())
exc = loss[loss > u] - u
n = exc.size
xi_hat, _, sig_hat = genpareto.fit(exc, floc=0)
print(f"  n = {loss.size} pertes ; seuil u = {u:.2f} M€ (q85) ; zeta_u = {zu:.3f} ; "
      f"{n} exces.")
print(f"  GPD MLE : xi = {xi_hat:.3f}, sigma = {sig_hat:.2f} M€.")

# =====================================================================================
titre("Bootstrap : la distribution de la VaR (le quantile est lui-meme incertain)")
# =====================================================================================
rng = np.random.default_rng(SEED)
xb, sb = [], []
for _ in range(B):
    r = rng.choice(exc, size=n, replace=True)
    try:
        c, _, s = genpareto.fit(r, floc=0)
        if 0 < s < 1e6 and -0.5 < c < 3:
            xb.append(c); sb.append(s)
    except Exception:
        pass
xb, sb = np.array(xb), np.array(sb)
xi_lo, xi_hi = np.percentile(xb, [5, 95])
print(f"  {len(xb)} ajustements valides. xi : IC90 = [{xi_lo:.2f} ; {xi_hi:.2f}] "
      f"(point {xi_hat:.2f}).")

# =====================================================================================
titre("VaR par branchement vs VaR predictive vs intervalle")
# =====================================================================================
# loi predictive : melange GPD sur le bootstrap de (xi, sigma)
idx = rng.integers(0, len(xb), N_SIM)
exc_pred = genpareto.rvs(c=xb[idx], scale=sb[idx], random_state=rng)

print(f"  {'niveau':>8}{'plug-in':>11}{'IC90 bootstrap':>22}{'E[VaR]':>10}{'prédictive':>12}"
      f"{'écart':>8}")
res = {}
for a in LEVELS:
    v_plug = var_gpd(a, xi_hat, sig_hat, u, zu)
    v_boot = var_gpd(a, xb, sb, u, zu)
    lo, hi = np.percentile(v_boot, [5, 95])
    v_mean = v_boot.mean()
    q = 1 - (1 - a) / zu                                # quantile conditionnel aux exces
    v_pred = u + float(np.quantile(exc_pred, q))
    res[a] = dict(plug=v_plug, lo=lo, hi=hi, mean=v_mean, pred=v_pred)
    print(f"  {a:>8.3f}{v_plug:>9.0f} M[{lo:>6.0f} ;{hi:>6.0f}] M{v_mean:>8.0f} M"
          f"{v_pred:>10.0f} M{100*(v_pred/v_plug-1):>7.0f}%")

a0, a9 = 0.995, 0.999
r0, r9 = res[a0], res[a9]
print(f"\n  Au niveau reglementaire 99,5 % :")
print(f"    - VaR plug-in           = {r0['plug']:.0f} M€  (le point aujourd'hui)")
print(f"    - IC90 bootstrap        = [{r0['lo']:.0f} ; {r0['hi']:.0f}] M€  "
      f"(facteur {r0['hi']/r0['lo']:.1f}, dû a la seule incertitude de xi)")
print(f"    - VaR PREDICTIVE        = {r0['pred']:.0f} M€  ({100*(r0['pred']/r0['plug']-1):+.0f} % "
      f"vs plug-in)")
print("  Enseignement, plus subtil que prevu : a 99,5 % la VaR predictive est QUASI EGALE a la")
print("  plug-in. Le risque d'estimation ne cree pas un biais de POINT ici ; il gonfle la")
print(f"  LARGEUR de la bande (facteur {r0['hi']/r0['lo']:.1f}). Le chargement predictif n'apparait")
print(f"  que PLUS LOIN dans la queue : {100*(r9['pred']/r9['plug']-1):+.0f} % a 99,9 %. Autrement dit,")
print("  plus la mesure s'enfonce dans la queue, plus la donnee incertaine la rend fragile.")

# TVaR (profil complémentaire, défini pour xi < 1)
titre("Profil TVaR (moyenne de queue, moins ponctuelle que la VaR ; définie si xi<1)")
for a in LEVELS:
    t_plug = tvar_gpd(a, xi_hat, sig_hat, u, zu)
    share_ok = float((xb < 1).mean())
    t_boot = np.array([tvar_gpd(a, c, s, u, zu) for c, s in zip(xb, sb)])
    t_boot = t_boot[np.isfinite(t_boot)]
    lo, hi = np.percentile(t_boot, [5, 95])
    print(f"  {a:.3f} : TVaR plug-in = {t_plug:.0f} M€, IC90 = [{lo:.0f} ; {hi:.0f}] "
          f"({100*share_ok:.0f} % des bootstrap ont xi<1)")

# =====================================================================================
titre("VERDICT")
# =====================================================================================
print("  1. Caroline a raison : le SCR = VaR 99,5 % lit un point de queue sur donnee rare ;")
print(f"     son IC90 est un facteur {r0['hi']/r0['lo']:.1f} (et la TVaR, plus profonde, un facteur")
print(f"     bien plus grand). La fragilite est dans la LARGEUR de la bande.")
print("  2. La VaR predictive (quantile du melange sur l'incertitude) est le point PROPRE, mais")
print(f"     son ecart a la plug-in est faible a 99,5 % ({100*(r0['pred']/r0['plug']-1):+.0f} %) et ne")
print(f"     grandit qu'en profondeur ({100*(r9['pred']/r9['plug']-1):+.0f} % a 99,9 %) : le risque")
print("     d'estimation n'est pas un biais de point, c'est un elargissement.")
print("  3. Consequence : rapporter le capital en INTERVALLE, jamais en point ; lire un PROFIL")
print("     par niveau. C'est la justification meme de la these 'bande, pas point' du memoire.")
print("     On ne cite pas la VaR ; on cite [borne basse ; borne haute] et on l'assume.")

# =====================================================================================
# figure J2
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

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 4.9))

# (a) distribution bootstrap de xi : le parametre est incertain
ax1.hist(xb, bins=40, color=BLUE, alpha=0.55, edgecolor="#fcfcfb")
ax1.axvline(xi_hat, color=INK, lw=1.6, label=f"point $\\hat\\xi$={xi_hat:.2f}")
ax1.axvline(xi_lo, color=ACCENT, ls="--", lw=1.4)
ax1.axvline(xi_hi, color=ACCENT, ls="--", lw=1.4, label=f"IC90 [{xi_lo:.2f} ; {xi_hi:.2f}]")
ax1.axvline(1.0, color=MUTED, ls=":", lw=1)
ax1.text(1.02, ax1.get_ylim()[1]*0.6, "ξ=1\n(TVaR indéf.)", fontsize=7.5, color=MUTED)
ax1.set_xlabel("indice de queue $\\xi$ (bootstrap)", color=INK2)
ax1.set_ylabel("fréquence", color=INK2)
ax1.legend(frameon=False, fontsize=8)
ax1.set_title("(a)  Le paramètre est incertain :\nle quantile en hérite", fontsize=10.5, color=INK, pad=8)

# (b) survie conditionnelle : plug-in vs predictive ; divergence dans la queue profonde
xs = np.linspace(u, r9["pred"] * 1.25, 500)
S_plug = (1 + xi_hat * (xs - u) / sig_hat) ** (-1 / xi_hat)
S_pred = np.array([np.mean((1 + xb * (x - u) / sb) ** (-1 / xb)) for x in xs])
ax2.plot(xs, S_plug, color=BLUE, lw=2.2, label="plug-in $\\hat\\xi$")
ax2.plot(xs, S_pred, color=ACCENT, lw=2.2, label="prédictive (mélange)")
for a, txt in [(a0, "99,5 %"), (a9, "99,9 %")]:
    ax2.axhline((1 - a) / zu, color=MUTED, ls=":", lw=1)
    ax2.text(xs[-1], (1 - a) / zu, f" {txt}", fontsize=7.5, color=MUTED, va="center")
ax2.set_yscale("log")
ax2.set_xlabel("perte au-delà du seuil (M€)", color=INK2)
ax2.set_ylabel("survie conditionnelle $P(X>x\\,|\\,X>u)$", color=INK2, fontsize=9)
ax2.legend(frameon=False, fontsize=8.5)
ax2.set_title("(b)  Les queues ne divergent que loin\n(99,9 %), pas à 99,5 %",
              fontsize=10.5, color=INK, pad=8)

# (c) profil VaR par niveau : plug-in, predictive, bande bootstrap
xlv = np.arange(len(LEVELS))
plug = [res[a]["plug"] for a in LEVELS]
pred = [res[a]["pred"] for a in LEVELS]
lo = [res[a]["lo"] for a in LEVELS]; hi = [res[a]["hi"] for a in LEVELS]
ax3.fill_between(xlv, lo, hi, color=BLUE, alpha=0.15, label="IC90 bootstrap")
ax3.plot(xlv, plug, color=BLUE, lw=2, marker="o", ms=5, label="plug-in")
ax3.plot(xlv, pred, color=ACCENT, lw=2, marker="s", ms=5, label="prédictive")
ax3.set_xticks(xlv); ax3.set_xticklabels([f"{100*a:.1f} %" for a in LEVELS])
ax3.set_xlabel("niveau de la VaR", color=INK2)
ax3.set_ylabel("capital (M€)", color=INK2)
ax3.legend(frameon=False, fontsize=8.5)
ax3.set_title("(c)  Le capital en profil et en bande,\npas en point", fontsize=10.5, color=INK, pad=8)

for ax in (ax1, ax2, ax3):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.suptitle("J2 : le SCR est un quantile d'un objet incertain ; la VaR prédictive intègre le "
             "risque d'estimation, le capital se lit en bande",
             fontsize=11.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.92])
outdir = os.path.join(HERE, "figures")
os.makedirs(outdir, exist_ok=True)
path = os.path.join(outdir, "J2_var_predictive.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print("\nfigure ecrite :", path)
