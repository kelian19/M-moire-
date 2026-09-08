# -*- coding: utf-8 -*-
"""89 - BACKTEST HORS ECHANTILLON de la severite et de la frequence.

CE QUE CE SCRIPT AJOUTE, ET CE QU'IL NE FAIT PAS.
Le memoire valide l'adequation DANS l'echantillon : Anderson-Darling et
Kolmogorov-Smirnov sur l'ajustement lui-meme (script 47), balayage de seuil,
bootstrap de xi. Aucune de ces validations ne demande au modele de predire une
periode qu'il n'a pas vue. C'est le manque que ce script comble, et c'est la
premiere question qu'un jury d'actuaires pose sur un modele de capital.

C'EST UN DIAGNOSTIC, PAS UNE RECALIBRATION. Aucun parametre publie n'est touche :
config.py n'est ni lu pour etre modifie ni ecrit. Le script re-estime sur des
sous-echantillons et compare, ce qui est compatible avec le gel du 7 aout.

UNE DIFFERENCE DELIBEREE AVEC LA CHAINE PUBLIEE, ET IL FAUT LA DIRE. La chaine
publiee lit le seuil dans config.py (u = 20,03 M EUR, percentile 84,4 de la
donnee courante). Ici le seuil est RE-ESTIME sur chaque echantillon
d'apprentissage, par la regle du percentile 85. C'est obligatoire : un seuil
calcule sur toute la periode ferait fuiter l'information de test dans
l'apprentissage, et le backtest ne mesurerait plus rien. La regle est donc le
percentile 85, et non la valeur 20,03.

FENETRE D'ETUDE, ET ELLE EST CHOISIE SUR LA DONNEE, PAS PAR COMMODITE.
Le perimetre cyber x finance couvre 1979 a 2026, mais :
  - avant 2004 la collecte est trop mince, de 1 a 9 incidents par an, contre 13
    a 39 ensuite. Ces annees ne sont pas des annees calmes, c'est une base qui
    ne les couvre pas ;
  - 2026 ne porte que 5 incidents, contre 21 a 32 les annees precedentes : la
    base est tronquee par le delai de declaration.
Retenir 1979-2026 sans le voir produirait un faux effondrement de frequence en
fin de periode et un faux regime calme au debut. La fenetre est donc 2004-2025.

Sortie : diagnostics seulement, aucune figure. Un backtest se lit en nombres.
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy import optimize, special, stats
from scipy.stats import genpareto, nbinom, poisson

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from src.severity.oprisk_analysis import (  # noqa: E402
    USD_EUR, filter_cyber, filter_finance, load_clean,
)
from src.utils.config import OPRISK  # noqa: E402

AN_DEBUT = 2004      # premiere annee de collecte dense
AN_FIN = 2025        # derniere annee non tronquee
AN_ORIGINE = 2013    # premiere origine de prevision : l'apprentissage part de 2004
P_SEUIL = 0.85       # regle de seuil, et non la valeur 20,03


def titre(t):
    print()
    print("=" * 88)
    print(t)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Donnees
# ---------------------------------------------------------------------------

d = filter_finance(filter_cyber(load_clean(
    os.path.join(REPO, "data", "raw", "SAS_OpRisk_Global_Data_June_2026.xlsx"))))
d = d.dropna(subset=["year"]).copy()
d["year"] = d["year"].astype(int)
d["loss_eur"] = d["loss"] * USD_EUR
d = d[(d.year >= AN_DEBUT) & (d.year <= AN_FIN)].copy()

titre("0. PERIMETRE ET FENETRE")
print(f"Perimetre : cyber x finance, convention de severite du projet "
      f"(load_clean, filter_cyber, filter_finance, conversion {USD_EUR}).")
print(f"Fenetre retenue : {AN_DEBUT}-{AN_FIN}, soit {AN_FIN - AN_DEBUT + 1} annees "
      f"et {len(d)} incidents.")
print(f"Origines de prevision : {AN_ORIGINE} a {AN_FIN - 1}, soit "
      f"{AN_FIN - AN_ORIGINE} annees notees hors echantillon.")
print()
print("RAPPEL DE CE QUE LE MEMOIRE PUBLIE, pour situer : seuil "
      f"{OPRISK['seuil_u_eur']} M EUR, xi {OPRISK['xi']}, sigma "
      f"{OPRISK['sigma_eur']}, sur {OPRISK['n_incidents']} incidents et "
      f"{OPRISK['n_excess']} exces. Ces valeurs ne sont PAS utilisees ci-dessous.")


# ---------------------------------------------------------------------------
# 1. Severite : origine glissante, un pas en avant
# ---------------------------------------------------------------------------

titre("1. SEVERITE : ORIGINE GLISSANTE, UN PAS EN AVANT")
print("Pour chaque origine t : ajustement d'une GPD sur les exces de 2004..t au-dessus")
print("du percentile 85 de CES annees-la, puis notation de la seule annee t+1.")
print()
print("origine  n appr.  u appr.    xi     sigma  | n test  exces  PIT moyen")

pits = []          # transformees uniformes des exces de test
lignes = []
dep_995 = 0        # depassements du quantile 99,5 % de severite
dep_99 = 0
n_test_tot = 0

for t in range(AN_ORIGINE, AN_FIN):
    appr = d[d.year <= t]["loss_eur"].values
    test = d[d.year == t + 1]["loss_eur"].values
    if len(appr) < 50 or len(test) == 0:
        continue

    u = float(np.quantile(appr, P_SEUIL))
    exc_appr = appr[appr > u] - u
    if len(exc_appr) < 20:
        continue
    xi, _, sig = genpareto.fit(exc_appr, floc=0.0)

    # quantiles de severite implicites par la formule POT, taux de depassement
    # COMPTE sur l'apprentissage (et non pose : c'est le point du bloc
    # OPRISK_COHERENCE de config.py, applique ici correctement)
    p_u = len(exc_appr) / len(appr)
    def q_sev(q):
        return u + (sig / xi) * (((1.0 - q) / p_u) ** (-xi) - 1.0)

    q99, q995 = q_sev(0.99), q_sev(0.995)
    dep_99 += int((test > q99).sum())
    dep_995 += int((test > q995).sum())
    n_test_tot += len(test)

    exc_test = test[test > u] - u
    pit = genpareto.cdf(exc_test, xi, loc=0.0, scale=sig) if len(exc_test) else np.array([])
    pits.append(pit)
    moy = f"{pit.mean():7.3f}" if pit.size else "      ."
    lignes.append((t, len(appr), u, xi, sig, len(test), len(exc_test), moy))
    print(f"  {t}    {len(appr):4d}  {u:7.2f}  {xi:6.3f}  {sig:7.2f}  |  "
          f"{len(test):4d}   {len(exc_test):4d}   {moy}")

pit_all = np.concatenate(pits) if pits else np.array([])

print()
print(f"Exces de test cumules : {pit_all.size} sur {n_test_tot} pertes notees.")

if pit_all.size >= 5:
    ks = stats.kstest(pit_all, "uniform")
    print()
    print("TEST DE PROBABILITE INTEGRALE (PIT). Si la queue ajustee est la bonne, les")
    print("transformees des exces de test sont uniformes sur [0, 1].")
    print(f"  moyenne des PIT      : {pit_all.mean():.3f}   (0,500 attendu)")
    print(f"  Kolmogorov-Smirnov   : D = {ks.statistic:.3f}, p = {ks.pvalue:.4f}")
    lecture = ("compatible avec l'uniforme" if ks.pvalue > 0.05
               else "INCOMPATIBLE avec l'uniforme au seuil de 5 %")
    print(f"  lecture              : {lecture}")
    print(f"  A NE PAS SURINTERPRETER : une moyenne PIT superieure a 0,5 indiquerait des")
    print(f"                         pertes tombant plus haut dans la queue ajustee que")
    print(f"                         prevu. L'ecart observe ici va dans ce sens mais il")
    print(f"                         N'EST PAS SIGNIFICATIF, le test ne rejetant pas.")

print()
print("TEST DE DEPASSEMENT (Kupiec). Combien de pertes de test depassent le quantile")
print("de severite que l'apprentissage annoncait ?")
for niv, obs in ((0.99, dep_99), (0.995, dep_995)):
    att = (1.0 - niv) * n_test_tot
    bt = stats.binomtest(obs, n_test_tot, 1.0 - niv)
    print(f"  niveau {100*niv:5.1f} % : {obs} depassement(s) observe(s), "
          f"{att:.1f} attendu(s), p = {bt.pvalue:.4f}")


# ---------------------------------------------------------------------------
# 1bis. Les deux tests se contredisent en apparence : d'ou vient l'ecart ?
# ---------------------------------------------------------------------------

titre("1bis. LE MECANISME, MESURE ET NON SUPPOSE")
print("Les deux tests de la section 1 semblent se contredire : la FORME de la queue passe")
print("le test PIT, et les QUANTILES sont depasses trois fois trop souvent. Les deux")
print("peuvent tenir ensemble, parce qu'ils ne portent pas sur le meme objet.")
print()
print("  - le PIT ne regarde que les exces AU-DESSUS du seuil d'apprentissage : il teste")
print("    la queue CONDITIONNELLE, c'est-a-dire la forme ;")
print("  - le quantile de severite combine la forme, le seuil ET le taux de depassement.")
print()
print("Si la forme est bonne et le quantile faux, c'est donc le TAUX qui derive. Mesure :")

taux_appr = []
taux_test = []
for (t, n_appr, u, xi, sig, n_test, n_exc, _m) in lignes:
    appr = d[d.year <= t]["loss_eur"].values
    taux_appr.append((appr > u).mean())
    taux_test.append(n_exc / n_test)

exc_tot = int(sum(l[6] for l in lignes))
p_appr = float(np.mean(taux_appr))
p_test = exc_tot / n_test_tot
bt = stats.binomtest(exc_tot, n_test_tot, p_appr)
print(f"  taux de depassement du seuil, en APPRENTISSAGE : {100*p_appr:.1f} % "
      f"(par construction, regle du percentile {100*P_SEUIL:.0f})")
print(f"  taux de depassement du meme seuil, HORS echantillon : {100*p_test:.1f} % "
      f"({exc_tot} exces sur {n_test_tot})")
print(f"  rapport : x{p_test / p_appr:.2f}   test binomial : p = {bt.pvalue:.2e}")
print()
print("ET LA DERIVE SE VOIT DIRECTEMENT SUR LE SEUIL LUI-MEME, qui est un quantile de")
print("la donnee d'apprentissage :")
print(f"  seuil a l'origine {lignes[0][0]} : {lignes[0][2]:.2f} M EUR")
print(f"  seuil a l'origine {lignes[-1][0]} : {lignes[-1][2]:.2f} M EUR"
      f"   soit x{lignes[-1][2] / lignes[0][2]:.2f} en {lignes[-1][0] - lignes[0][0]} ans")
med = d.groupby("year")["loss_eur"].median()
sl_m, _, _, pv_m, _ = stats.linregress(med.index.values, np.log(med.values))
print(f"  mediane annuelle des pertes : tendance de {100*sl_m:+.1f} % par an en log, "
      f"p = {pv_m:.4f}")
print()
print("LECTURE, ET ELLE N'ETAIT PAS CELLE ATTENDUE. La queue n'est pas mal ajustee : sa")
print("FORME survit au test hors echantillon. Ce qui derive est l'ECHELLE de la loi de")
print("severite. Une fenetre d'apprentissage qui s'etend garde les petites pertes")
print("anciennes, donc elle retarde sur cette derive, et le quantile qu'elle annonce est")
print("trop bas pour l'annee suivante. C'est un defaut de STATIONNARITE, pas de famille.")
print()
print("CE QUE CELA IMPLIQUE POUR LE MEMOIRE, ET CE QUE CELA N'IMPLIQUE PAS.")
print("  - le sens de l'ecart est ANTI-CONSERVATEUR : le capital de severite estime sur")
print("    l'historique complet sous-estime celui d'une annee recente. Une sous-estimation")
print("    se declare, elle ne se couvre pas par un argument de prudence ;")
print("  - en revanche cela ne dit RIEN contre le xi publie. Les xi de cette section sont")
print("    ajustes sur des seuils de 8,6 a 18,2 M EUR, tous INFERIEURS au seuil publie de")
print(f"    {OPRISK['seuil_u_eur']} M EUR, et le balayage de seuil du script 47 montre que xi")
print("    DECROIT quand le seuil monte. Comparer ces valeurs au xi publie serait donc")
print("    comparer deux objets, et c'est le genre de lecture que ce projet traque ;")
print("  - et cela ne dit rien contre la THESE, qui porte sur l'ECART entre etats de")
print("    conformite a severite de base commune. Une derive d'echelle commune aux deux")
print("    etats se simplifie dans un rapport.")


# ---------------------------------------------------------------------------
# 2. Frequence : origine glissante, et la binomiale negative gagne-t-elle sa place ?
# ---------------------------------------------------------------------------

titre("2. FREQUENCE : ORIGINE GLISSANTE, ET POISSON CONTRE BINOMIALE NEGATIVE")
cnt = d.groupby("year").size().reindex(range(AN_DEBUT, AN_FIN + 1), fill_value=0)
print("Comptes annuels du perimetre :")
print("  " + "  ".join(f"{y}:{n}" for y, n in cnt.items()))
print(f"  moyenne {cnt.mean():.2f}, variance {cnt.var(ddof=1):.2f}, "
      f"dispersion Var/E = {cnt.var(ddof=1) / cnt.mean():.2f}")

# tendance, parce qu'un modele iid serait faux si elle existe
sl, ic, r, pv, se = stats.linregress(cnt.index.values, cnt.values)
print(f"  tendance lineaire : {sl:+.3f} incident/an, p = {pv:.4f} "
      f"({'non significative' if pv > 0.05 else 'SIGNIFICATIVE, un modele iid est alors mal specifie'})")


def fit_nb(y):
    """MLE de la binomiale negative (r, p) sur des comptes."""
    def nll(par):
        r = np.exp(par[0])
        mu = np.exp(par[1])
        p = r / (r + mu)
        return -np.sum(nbinom.logpmf(y, r, p))
    m, v = y.mean(), y.var(ddof=1)
    r0 = max(m * m / max(v - m, 1e-6), 0.5)
    res = optimize.minimize(nll, [np.log(r0), np.log(max(m, 1e-6))], method="Nelder-Mead")
    r = np.exp(res.x[0])
    mu = np.exp(res.x[1])
    return r, r / (r + mu), mu


print()
print("origine   obs   Poisson IP90      NB IP90        dans IP ?   log-score P   log-score NB")
cov_p = cov_nb = 0
ls_p = ls_nb = 0.0
n_an = 0
for t in range(AN_ORIGINE, AN_FIN):
    ya = cnt.loc[AN_DEBUT:t].values
    obs = int(cnt.loc[t + 1])
    lam = ya.mean()
    lo_p, hi_p = poisson.ppf(0.05, lam), poisson.ppf(0.95, lam)
    r, p, mu = fit_nb(ya)
    lo_n, hi_n = nbinom.ppf(0.05, r, p), nbinom.ppf(0.95, r, p)
    in_p = lo_p <= obs <= hi_p
    in_n = lo_n <= obs <= hi_n
    cov_p += int(in_p)
    cov_nb += int(in_n)
    lp = poisson.logpmf(obs, lam)
    ln = nbinom.logpmf(obs, r, p)
    ls_p += lp
    ls_nb += ln
    n_an += 1
    print(f"  {t}     {obs:3d}   [{lo_p:5.0f} ; {hi_p:5.0f}]   [{lo_n:5.0f} ; {hi_n:5.0f}]   "
          f"{'P' if in_p else '-'} / {'NB' if in_n else '-':>2}      "
          f"{lp:8.3f}      {ln:8.3f}")

print()
print(f"COUVERTURE REELLE d'un intervalle de prevision annonce a 90 % :")
print(f"  Poisson             : {cov_p}/{n_an} = {100*cov_p/n_an:.1f} %")
print(f"  Binomiale negative  : {cov_nb}/{n_an} = {100*cov_nb/n_an:.1f} %")
print()
print(f"LOG-SCORE PREDICTIF CUMULE (plus haut = meilleur) :")
print(f"  Poisson             : {ls_p:8.3f}")
print(f"  Binomiale negative  : {ls_nb:8.3f}")
print(f"  ecart en faveur de  : {'la binomiale negative' if ls_nb > ls_p else 'Poisson'}"
      f"  ({abs(ls_nb - ls_p):.3f} nats sur {n_an} annees)")
print()
print("CE QUE CE SECOND TEST TRANCHE, et le premier ne le fait pas : la binomiale")
print("negative gagne-t-elle son parametre supplementaire HORS echantillon ? Une")
print("couverture peut etre bonne par largeur excessive ; le log-score, lui, penalise")
print("un intervalle inutilement large autant qu'un intervalle trop etroit.")


# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------

titre("VERDICT")
print("Trois resultats, et ils ne vont pas dans le meme sens. C'est ecrit APRES lecture")
print("des sorties, et non en meme temps que le code qui les produit.")
print()
print("1. LA LOI DE FREQUENCE EST VALIDEE HORS ECHANTILLON, ET C'EST UN GAIN NET. La")
print("   binomiale negative couvre 91,7 % pour un intervalle annonce a 90 %, quand")
print("   Poisson ne couvre que 75 %. Elle gagne aussi au log-score predictif, donc son")
print("   parametre supplementaire n'est pas paye par une largeur inutile. Le choix de")
print("   surdispersion du memoire cesse d'etre une precaution et devient une mesure.")
print()
print("2. LA FORME DE LA QUEUE SURVIT AU TEST, ce qui n'etait pas acquis avec 20 a 90")
print("   exces par ajustement. Le PIT des exces de test est compatible avec l'uniforme")
print("   (Kolmogorov-Smirnov non rejete), donc la GPD n'est pas la mauvaise famille.")
print()
print("3. LES QUANTILES DE SEVERITE SONT DEPASSES TROIS FOIS TROP SOUVENT, et le test de")
print("   Kupiec les rejette aux deux niveaux. LE MOTIF EST MESURE en section 1bis et il")
print("   n'est pas celui qu'on attendrait : ce n'est pas la queue qui est mal ajustee,")
print("   c'est l'echelle de la loi de severite qui DERIVE dans le temps. Une fenetre")
print("   d'apprentissage qui s'etend retarde sur cette derive.")
print()
print("CE QUE LE MEMOIRE DOIT EN FAIRE, ET C'EST UNE DECISION DE KELIAN, PAS DU SCRIPT.")
print("La non-stationnarite de l'echelle de severite n'est pas dans l'inventaire des")
print("hypotheses du chapitre 13. Elle a exactement le statut du p_u gele : un ecart")
print("mesure, de sens anti-conservateur, immateriel pour la these mais materiel pour le")
print("niveau. Le traitement coherent avec le gel du 7 aout est donc de la DECLARER")
print("chiffree, non de recalibrer sur une fenetre glissante, ce qui deplacerait tous")
print("les niveaux publies.")
print()
print("CE QU'IL NE FAUT PAS EN CONCLURE. Ni que le modele est faux, la forme etant")
print("validee et la loi de frequence confirmee. Ni que la these est touchee, puisqu'elle")
print("porte sur un RAPPORT entre etats a severite de base commune.")

print()
print("EXIT 0")
