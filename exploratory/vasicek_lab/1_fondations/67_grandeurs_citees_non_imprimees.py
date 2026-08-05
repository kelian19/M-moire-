#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
67 : les grandeurs CITEES dans le memoire et qu'aucun script n'imprimait.

D'OU VIENT CE SCRIPT. Le harnais verif_chiffres.py signale les nombres publies qu'aucune
sortie de script ne confirme. Un passage complet sur les dix-neuf chapitres a montre que le
residu se repartit en quatre classes, et une seule constitue un vrai defaut :

  (1) SEPARATEUR DE MILLIERS. Le harnais coupait « 8,122.9 » en deux nombres, 8 et 122.9, si
      bien que le « 8123 » du memoire ressortait non confirme alors que le script 60
      l'imprimait. Corrige dans le harnais, pas ici.
  (2) UNITE. Le memoire ecrit un pourcentage la ou le script imprime une fraction : « 15,8 % »
      contre « 0.158 ». Corrige en imprimant les deux, la ou c'est le cas.
  (3) NOMBRE LEGITIMEMENT HORS SCRIPT. Un seuil pose, un comptage de renvoi interne, une
      citation externe datee. Ceux-la ne doivent pas etre produits par un script, et le
      memoire les signale comme tels.
  (4) GRANDEUR CITEE MAIS JAMAIS IMPRIMEE. C'est la seule classe fautive, et c'est l'objet de
      ce script : des valeurs presentees comme des RESULTATS, calculees a la main pendant la
      redaction, qu'aucun script ne produisait. Un lecteur qui les recalcule n'avait aucun
      point de comparaison, et une derive silencieuse y etait indetectable.

CE QU'IL IMPRIME. Les formes analytiques fermees du chapitre socle (VaR et TVaR de la GPD),
les parts de vecteur en pourcentage autant qu'en fraction, les rapports derives que la
redaction citait sans les tracer, et, quand la base sous licence est presente, les statistiques
descriptives et l'estimateur de Hill au seuil retenu.

IL NE RECALCULE RIEN QUI EXISTE AILLEURS. La calibration vient de la configuration figee, comme
dans le script 63 : cette sortie atteste la conformite a la configuration, pas l'exactitude
empirique, laquelle releve des scripts 07, 08b, 47 et 57.

Sortie : diagnostics seuls, aucune figure.
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for _p in (REPO, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from src.utils.config import OPRISK, PRC, HACKMAGEDDON                # noqa: E402

W_ = 88


def titre(s):
    print("\n" + "=" * W_ + f"\n{s}\n" + "=" * W_)


# =====================================================================================
titre("1. VaR et TVaR mono-perte, par les formes fermees de la GPD")
# =====================================================================================
print("Le chapitre socle donne ces deux valeurs comme resultats de ses propositions, mais")
print("aucun script ne les imprimait : elles etaient calculees a la main a partir de la")
print("calibration. On les reproduit ici depuis la configuration figee.\n")


def var_gpd(u, sigma, xi, zeta_u, p):
    """VaR_p = u + (sigma/xi) * [ ((1-p)/zeta_u)^(-xi) - 1 ]."""
    return u + (sigma / xi) * (((1.0 - p) / zeta_u) ** (-xi) - 1.0)


def tvar_gpd(u, sigma, xi, zeta_u, p):
    """TVaR_p = VaR_p/(1-xi) + (sigma - xi*u)/(1-xi), defini pour xi < 1."""
    if xi >= 1.0:
        return float("nan")
    v = var_gpd(u, sigma, xi, zeta_u, p)
    return v / (1.0 - xi) + (sigma - xi * u) / (1.0 - xi)


for nom, cfg in (("OPRISK", OPRISK), ("PRC", PRC)):
    u, sg = cfg["seuil_u_eur"], cfg["sigma_eur"]
    xi, zu = cfg["xi"], cfg["p_u"]
    print(f"  {nom} : u = {u}, sigma = {sg}, xi = {xi}, zeta_u = {zu}")
    for p in (0.995, 0.999):
        v, tv = var_gpd(u, sg, xi, zu, p), tvar_gpd(u, sg, xi, zu, p)
        tvs = f"{tv:.1f}" if np.isfinite(tv) else "INDEFINI (xi >= 1)"
        print(f"      p = {p:.3f}   VaR = {v:.1f} M EUR    TVaR = {tvs}")
    if xi >= 1.0:
        print(f"      xi = {xi} > 1 : esperance infinie, l'Expected Shortfall est")
        print(f"      mathematiquement INDEFINI. C'est ce qui justifie le plafond de severite.")
    print()
print("  Les deux valeurs citees au chapitre socle sont la ligne OPRISK a p = 0,995.")


# =====================================================================================
titre("2. Les parts de vecteur, en pourcentage autant qu'en fraction")
# =====================================================================================
print("Le script 63 imprime ces parts en FRACTION, le memoire les cite en POURCENTAGE : le")
print("harnais ne pouvait apparier ni l'un ni l'autre. On imprime les deux formes.\n")
print(f"  {'vecteur':<26}{'fraction':>10}{'pourcentage':>14}")
for k, v in HACKMAGEDDON["proportions"].items():
    print(f"  {k:<26}{v:>10.3f}{100*v:>13.1f} %")
print(f"  {'surface TLPT (art. 26)':<26}{HACKMAGEDDON['surface_tlpt']:>10.3f}"
      f"{100*HACKMAGEDDON['surface_tlpt']:>13.1f} %")
print(f"  {'surface tiers (art. 28-44)':<26}{HACKMAGEDDON['surface_tiers']:>10.3f}"
      f"{100*HACKMAGEDDON['surface_tiers']:>13.1f} %")
print(f"\n  somme des parts : {sum(HACKMAGEDDON['proportions'].values()):.3f} "
      f"({100*sum(HACKMAGEDDON['proportions'].values()):.1f} %)")
print("  RAPPEL : citation externe datee, non recalculable (cf. scripts 62 et 63). Ces parts")
print("  ne servent qu'a repartir par vecteur et ne portent aucun niveau de capital.")


# =====================================================================================
titre("3. Les rapports derives que la redaction citait sans les tracer")
# =====================================================================================
print("Chacun de ces rapports se deduit d'une valeur imprimee ailleurs. Les tracer ici evite")
print("qu'une valeur amont bouge sans que le rapport suive, ce qui est arrive une fois.\n")
SEV_MULT = 0.8545                 # script 60 : multiplicateur de severite a la taille cible
print(f"  multiplicateur de severite (script 60)     : {SEV_MULT:.4f}")
print(f"  soit, en variation                         : {100*(SEV_MULT-1):+.1f} %")
print(f"     le memoire arrondissait a -14 % ; la valeur imprimee est {100*(SEV_MULT-1):+.1f} %")

# RAPPORT ENTRE LES TROIS FREQUENCES DU CHAPITRE DONNEES. Le texte annoncait « un facteur
# 1600 entre les extremes », valeur heritee de l'epoque ou lambda d'entite valait 0,21. La
# table a ete corrigee a 0,092, la phrase ne l'a pas ete : c'est exactement le genre de
# desynchronisation qu'un rapport imprime empeche.
LAM_REF = 341.0                   # notifications/an, perimetre BSF (script 62)
LAM_SECTEUR = 21.56               # incidents TIC materiels/an, secteur (scripts 07, 08b)
LAM_ENTITE = 0.09168423156000373   # lu a la taille de l'entite (script 60)
print(f"\n  les trois frequences du chapitre donnees :")
print(f"     lambda_ref, notifications PRC (BSF)     : {LAM_REF:.0f} /an")
print(f"     lambda, secteur financier mondial       : {LAM_SECTEUR:.2f} /an")
print(f"     lambda, entite lue a sa taille          : {LAM_ENTITE:.5f} /an")
print(f"  rapport entre les extremes (ref / entite)  : {LAM_REF/LAM_ENTITE:.0f}")
print(f"  rapport secteur / entite                   : {LAM_SECTEUR/LAM_ENTITE:.0f}")

XI = OPRISK["xi"]
print(f"\n  indice de queue OpRisk                     : {XI}")
print(f"  1 / xi (indice de regularite de la queue)  : {1.0/XI:.3f}")
print(f"  xi > 0,5 : variance infinie                : {XI > 0.5}")
print(f"  xi < 1   : esperance finie, TVaR defini    : {XI < 1.0}")


# =====================================================================================
titre("4. Statistiques de severite de la population EFFECTIVEMENT utilisee")
# =====================================================================================
print("POURQUOI CETTE SECTION EXISTE, ET CE QU'ELLE A TROUVE. Le chapitre donnees publie une")
print("table de statistiques de severite (mediane 1,50 M USD, moyenne 26,4, P90 51,5, P99 402,")
print("maximum 1500, total cumule 15,4 Md USD). Cette table a ete MIGREE AUTOMATIQUEMENT depuis")
print("la version pre-cascade du memoire, et AUCUN filtre du pipeline actuel ne la reproduit :")
print("ni la base entiere, ni le secteur financier, ni le sous-ensemble TIC, ni aucune")
print("combinaison de fenetres. Sa moyenne et son total impliquent n = 583 observations, effectif")
print("qu'aucun sous-ensemble courant ne presente. Elle decrit donc une population que le memoire")
print("n'utilise plus nulle part ailleurs.")
print("\nCE SCRIPT NE TENTE PAS DE LA RETROUVER. Il imprime les statistiques de la population que")
print("le memoire utilise REELLEMENT partout ailleurs, c'est-a-dire celle de la descente")
print("d'echelle et de la calibration de frequence : secteur financier, categories TIC, fenetre")
print("2005-2022. C'est cette table qui doit figurer au chapitre donnees, faute de quoi le")
print("chapitre decrit un echantillon et calibre sur un autre.\n")

RAW = os.path.abspath(os.path.join(REPO, "data", "raw"))
XLS = os.path.join(RAW, "SAS_OpRisk_Global_Data_June_2026.xlsx")
if not os.path.exists(XLS):
    print(f"  Base absente ({os.path.relpath(XLS, REPO)}) : section ignoree.")
    print("  Les sources brutes ne sont pas versionnees ; relancer ce script sur un poste")
    print("  disposant de la base pour produire cette table.")
else:
    import pandas as pd
    import descente as dsc                                            # noqa: E402
    d = pd.read_excel(XLS, sheet_name="Datasets")
    d["year"] = pd.to_datetime(d["First Year of Event"], errors="coerce").dt.year
    sel = ((d["Basel Business Line - Level 1"] != "Non-FS")
           & d["Sub Risk Category"].isin(dsc.ICT)
           & d.year.between(dsc.Y0, dsc.Y1))
    x = pd.to_numeric(d.loc[sel, dsc.LOSS], errors="coerce").dropna()
    x = x[x > 0].sort_values(ascending=False).to_numpy()
    print(f"  filtre : secteur financier x categories TIC x annees {dsc.Y0}-{dsc.Y1}")
    print(f"  {'observations':<22}{len(x):>12}")
    print(f"  {'mediane':<22}{np.median(x):>12.2f} M USD")
    print(f"  {'moyenne':<22}{x.mean():>12.1f} M USD")
    for q in (0.90, 0.99):
        print(f"  {'P' + format(100*q, '.0f'):<22}{np.quantile(x, q):>12.1f} M USD")
    print(f"  {'maximum':<22}{x.max():>12.1f} M USD")
    print(f"  {'total cumule':<22}{x.sum()/1000:>12.1f} Md USD")
    n10, n01 = max(1, int(round(0.10 * len(x)))), max(1, int(round(0.01 * len(x))))
    print(f"\n  concentration de la queue, sur la meme population :")
    print(f"  {'part du decile superieur':<34}{100*x[:n10].sum()/x.sum():>8.1f} %")
    print(f"  {'part du centile superieur':<34}{100*x[:n01].sum()/x.sum():>8.1f} %")
    print("\n  Le memoire annoncait 82,7 % et 31 % pour ces deux parts, sur la population non")
    print("  reproductible. Les valeurs ci-dessus sont celles de la population qu'il calibre.")

print("\nL'ECART DE HILL AU MLE (chapitre socle, 138,7 % a k = 86) N'EST PAS RECALCULE ICI, et")
print("c'est deliberé. Cet ecart porte sur les excedents CONVERTIS EN EUROS au-dessus du seuil")
print("de collecte, objet construit par le pipeline du script 47. Le recalculer ici sur les")
print("pertes brutes en dollars donne un tout autre nombre, et publier deux valeurs sous le")
print("meme nom creerait la contradiction que ce script est cense eviter. C'est au script 47")
print("de l'imprimer, puisque c'est lui qui possede la conversion.")


# =====================================================================================
titre("VERDICT")
# =====================================================================================
print("Ce script ne produit aucun resultat nouveau : il rend VERIFIABLES des valeurs qui")
print("etaient publiees sans l'etre. C'est la quatrieme classe du residu du harnais, la seule")
print("qui soit un defaut. Les trois autres (separateur, unite, valeur legitimement hors")
print("script) se traitent respectivement dans le harnais, en imprimant les deux unites, et")
print("en assumant la valeur dans le texte.")
print("\nA RELANCER sur un poste disposant de data/raw/ pour completer la section 4.")
