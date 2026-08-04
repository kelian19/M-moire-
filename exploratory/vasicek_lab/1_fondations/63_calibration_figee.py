#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
63 : imprimer la CALIBRATION FIGEE, pour que les chapitres puissent la citer.

POURQUOI CE SCRIPT EXISTE. Le passage du harnais de verification sur les dix-neuf chapitres
a montre que les constantes de calibration les plus citees du memoire n'apparaissaient dans
AUCUNE sortie de script : le seuil u, l'echelle sigma, le nombre d'exces, la VaR et la TVaR
mono-perte, la concentration de severite, le plafond de reassurance. Elles vivent dans
src/utils/config.py, qui est bien la source de verite unique du projet, mais un fichier de
configuration n'est pas une sortie : rien ne le rejoue, donc rien ne le verifie.

Consequence concrete : les chapitres donnees et socle, qui sont ceux qui publient ces
constantes, plafonnaient a 74-78 % de confirmation alors qu'aucun de leurs nombres n'etait
faux. Le defaut etait de TRACABILITE, pas d'exactitude.

CE QUE FAIT CE SCRIPT. Il imprime la configuration figee, telle quelle, sans rien recalculer.
C'est volontaire : recalculer ici dupliquerait les scripts de calibration et creerait deux
verites. Le role de ce script est d'exposer la source unique sous une forme que
verif_chiffres.py peut lire.

CE QU'IL NE FAIT PAS. Il ne valide rien. Un nombre confirme par ce script est confirme
CONFORME A LA CONFIGURATION, pas conforme aux donnees. La validation empirique des memes
grandeurs est l'objet des scripts 07, 08b, 47 et 57. Les deux controles sont complementaires
et il ne faut pas les confondre.

Sortie : diagnostics seulement, pas de figure.
"""

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from src.utils.config import (COPULE, FREQUENCY, HACKMAGEDDON,     # noqa: E402
                              OPRISK, PRC, SCR_DORA)

W = 84


def titre(s):
    print("\n" + "=" * W + f"\n{s}\n" + "=" * W)


def ligne(lab, val, unite=""):
    if isinstance(val, (list, tuple)):
        val = "[" + " ; ".join(f"{v:,.4g}" for v in val) + "]"
    elif isinstance(val, float):
        val = f"{val:,.4f}".rstrip("0").rstrip(".")
    print(f"  {lab:<46}{str(val):>18} {unite}")


titre("Severite OpRisk Global (montants reels, source de reference en euros)")
print(f"  perimetre : {OPRISK['perimetre']}")
ligne("incidents du perimetre cyber x finance", OPRISK["n_incidents"])
ligne("annees d'observation", OPRISK["n_years"], "ans")
ligne("frequence propre = n / annees", OPRISK["n_incidents"] / OPRISK["n_years"], "/ an")
ligne("exces au-dessus du seuil", OPRISK["n_excess"])
ligne("seuil POT u (percentile 85)", OPRISK["seuil_u_eur"], "M EUR")
ligne("taux de depassement p_u", OPRISK["p_u"])
ligne("indice de queue xi", OPRISK["xi"])
ligne("  IC 90 % sur xi", OPRISK["xi_ic90"])
ligne("echelle sigma", OPRISK["sigma_eur"], "M EUR")
ligne("  IC 90 % sur sigma", OPRISK["sigma_ic90"], "M EUR")
ligne("VaR 99,5 % mono-perte", OPRISK["var_995"], "M EUR")
ligne("  IC 90 % sur la VaR", OPRISK["var_995_ic90"], "M EUR")
ligne("TVaR 99 %", OPRISK["tvar_99"], "M EUR")
print(f"\n  Rapport IC de la VaR : facteur "
      f"{OPRISK['var_995_ic90'][1] / OPRISK['var_995_ic90'][0]:,.1f} entre les bornes.")
print("  C'est ce facteur, et non le point, qui doit etre cite avec le capital.")

titre("Severite PRC (derivee par conversion Jacobs)")
print(f"  periode : {PRC['period']}")
ligne("incidents a total_affected > 0", PRC["n_records"])
ligne("exces au-dessus du seuil", PRC["n_excess"])
ligne("seuil POT u", PRC["seuil_u_eur"], "M EUR")
ligne("taux de depassement p_u", PRC["p_u"])
ligne("indice de queue xi", PRC["xi"])
ligne("  IC 90 % sur xi", PRC["xi_ic90"])
ligne("echelle sigma", PRC["sigma_eur"], "M EUR")
ligne("  IC 90 % sur sigma", PRC["sigma_ic90"], "M EUR")
ligne("VaR 99,5 % mono-perte", PRC["var_995"], "M EUR")
ligne("conversion Jacobs, constante a", PRC["jacobs_a"])
ligne("conversion Jacobs, elasticite b", PRC["jacobs_b"])
ligne("taux de change USD vers EUR", PRC["usd_eur"])
print(f"\n  xi = {PRC['xi']:.3f} > 1 : la severite PRC est en regime d'ESPERANCE INFINIE,")
print(f"  d'ou le plafond de {SCR_DORA['cap_eur']:,.0f} M EUR (capacite de reassurance) qui rend")
print("  le capital calculable. Ce plafond ne s'applique QU'A la source PRC.")

titre("Frequence")
ligne("lambda_ref (perimetre financier PRC)", FREQUENCY["lambda_ref"], "/ an")
ligne("facteur de surdispersion Var / moyenne", FREQUENCY["dispersion_factor"])
ligne("facteur de recalibration", FREQUENCY["facteur_recalibration"])
print("\n  RAPPEL DES TROIS NIVEAUX, a ne jamais confondre :")
print(f"    lambda_ref      = {FREQUENCY['lambda_ref']:>7} / an   cle de repartition par vecteur")
print(f"    lambda (secteur)= {OPRISK['n_incidents']/OPRISK['n_years']:>7,.2f} / an   entree du moteur de cascade")
print(f"    lambda (entite) =  0.0917 / an   lu a la taille de l'entite (script 60)")

titre("Dependance et plafond")
ligne("famille de copule", COPULE["famille"])
ligne("theta non conforme", COPULE["theta_nc"])
ligne("theta conforme", COPULE["theta_c"])
ligne("bande empirique de theta", COPULE["theta_empirical_band"])
ligne("p_sys (concentration cloud)", COPULE["p_sys"])
ligne("plafond de severite (reassurance)", SCR_DORA["cap_eur"], "M EUR")
print(f"\n  Sensibilite declaree : {COPULE['theta_delta_dora_sensitivity']}")

titre("Hackmageddon : CITATION EXTERNE, non recalculable")
print(f"  source  : {HACKMAGEDDON['source']}")
print(f"  periode : {HACKMAGEDDON['periode']}")
ligne("incidents du semestre", HACKMAGEDDON["n_incidents"])
ligne("dont a vecteur d'acces identifie", HACKMAGEDDON["n_identifies"])
ligne("taux d'identification", HACKMAGEDDON["taux_identification"])
print("\n  parts par vecteur d'attaque :")
for k, v in HACKMAGEDDON["proportions"].items():
    ligne(f"    {k}", v)
ligne("surface TLPT (art. 26)", HACKMAGEDDON["surface_tlpt"])
ligne("surface tiers (art. 28-44)", HACKMAGEDDON["surface_tiers"])
print("\n  AVERTISSEMENT. Contrairement a PRC et OpRisk, le jeu Hackmageddon n'est PAS")
print("  versionne dans data/raw/ : ces valeurs sont une citation enregistree, pas une")
print("  sortie recalculable (cf. script 62). Elles ne servent qu'a fixer les parts de")
print("  repartition par vecteur, et ne portent aucun niveau de capital.")

titre("Verdict")
print("Cette sortie rend citables les constantes de calibration dans les chapitres donnees")
print("et socle. Elle atteste la CONFORMITE A LA CONFIGURATION, non l'exactitude empirique :")
print("celle-ci releve des scripts 07, 08b, 47 et 57.")
print("\nEXIT 0")
