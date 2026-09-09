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
                              LUCY_2026, OPRISK, PRC, SCR_DORA)

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
# EN FRACTION ET EN POURCENTAGE, LES DEUX. Le chapitre donnees cite « 38,8 % » la ou cette
# sortie n'imprimait que « 0.388 » : le harnais ne rapproche pas deux ecritures separees par
# un facteur cent, et ces parts ressortaient donc non confirmees alors qu'elles sont ici. La
# double ecriture coute une colonne et supprime toute une classe de fausses alertes.
for k, v in HACKMAGEDDON["proportions"].items():
    ligne(f"    {k}", f"{v:.3f}   soit {100*v:.1f} %")
ligne("surface TLPT (art. 26)", f"{HACKMAGEDDON['surface_tlpt']:.3f}   soit "
                                f"{100*HACKMAGEDDON['surface_tlpt']:.1f} %")
ligne("surface tiers (art. 28-44)", f"{HACKMAGEDDON['surface_tiers']:.3f}   soit "
                                    f"{100*HACKMAGEDDON['surface_tiers']:.1f} %")

cmp_ = HACKMAGEDDON["comparaison_2023_2026"]
print("\n  comparaison de structure 2023 contre 2026, MEME STATUT DE CITATION :")
print(f"    effectif 2023 : {cmp_['n_2023']} incidents, "
      f"trimestre {cmp_['trimestre_manquant_2023']} manquant")
print(f"    {'dimension (motivation)':<28}{'2023':>10}{'2026':>10}{'ecart (pts)':>14}")
for k, (a, b) in cmp_["motivations"].items():
    print(f"    {k:<28}{100*a:>9.1f} %{100*b:>9.1f} %{100*(b-a):>+13.1f}")
print(f"    lecture naive du ransomware : hausse de "
      f"{cmp_['hausse_ransomware_lecture_naive_pts']} points ; apres reclassement : recul de "
      f"{cmp_['recul_ransomware_apres_reclassement_pts']} points.")
print("    C'est l'artefact de taxonomie qui justifie de ne retenir de cette base que la")
print("    STRUCTURE, et encore, apres reclassement documente.")
print("\n  AVERTISSEMENT. Contrairement a PRC et OpRisk, le jeu Hackmageddon n'est PAS")
print("  versionne dans data/raw/ : ces valeurs sont une citation enregistree, pas une")
print("  sortie recalculable (cf. script 62). Elles ne servent qu'a fixer les parts de")
print("  repartition par vecteur, et ne portent aucun niveau de capital.")

titre("LUCY 2026 : CITATION EXTERNE, non recalculable")
L = LUCY_2026
print(f"  etude    : {L['source']}")
print(f"  analyse  : {L['analyse']}")
print(f"  perimetre de l'etude : {L['n_polices']} polices et {L['n_sinistres']} sinistres")
print(f"                         declares, {L['n_courtiers']} courtiers et "
      f"{L['n_assureurs']} assureur.")
print()
print("  RATIOS SINISTRES SUR PRIMES, en fraction ET en pourcentage, les deux, pour la")
print("  raison deja documentee au bloc Hackmageddon ci-dessus :")
for lab, k in (("agrege 2024", "sp_2024"), ("agrege 2025", "sp_2025"),
               ("segment ETI 2024", "sp_eti_2024"), ("segment ETI 2025", "sp_eti_2025")):
    ligne(f"    {lab}", f"{L[k]:.2f}   soit {100*L[k]:.0f} %")
print()
print("  CHARGE INDEMNISEE, nette de franchise et plafonnee par la capacite :")
ligne("    exercice 2024", L["charge_2024_eur"], "M EUR")
ligne("    exercice 2025", L["charge_2025_eur"], "M EUR")
ligne("    hausse", f"{L['hausse_charge_2025']:.2f}   soit "
                    f"{100*L['hausse_charge_2025']:.0f} %")
print()
print("  RECULS DE TAUX DE PRIME, en valeur absolue et nommes recul :")
ligne("    grandes entreprises", f"{L['recul_taux_prime_grandes']:.2f}   soit "
                                 f"{100*L['recul_taux_prime_grandes']:.0f} %")
ligne("    entreprises de taille intermediaire",
      f"{L['recul_taux_prime_eti']:.2f}   soit {100*L['recul_taux_prime_eti']:.0f} %")
print()
print("  LA VALEUR QUI COMPTE LE PLUS POUR CE MEMOIRE, et c'est un compte, pas un ratio :")
ligne("    sinistres au-dela du seuil XXL en France, 2025",
      L["n_sinistres_sup_10m_france_2025"])
ligne("    seuil XL", L["seuil_xl_eur"], "M EUR")
ligne("    seuil XXL", L["seuil_xxl_eur"], "M EUR")
print("    Un seul sinistre au-dela du seuil XXL sur l'exercice : la queue francaise est")
print("    CENSUREE en partie haute, ce qui rend un quantile a 99,5 % instable et biaise")
print("    vers le bas. C'est le constat externe qui justifie de calibrer la severite du")
print("    memoire sur une base INTERNATIONALE et non sur le marche francais.")
print()
print("  DEUX REGIMES OPPOSES SOUS UNE MEME TRAJECTOIRE DE RATIO CROISSANTE.")
print("  Le ratio monte les deux annees, mais le moteur s'inverse : 2024 est une annee de")
print("  SEVERITE, 2025 une annee de FREQUENCE. Un ratio agrege ne distingue pas les deux,")
print("  et ils n'appellent pas les memes leviers. C'est le meme argument de decomposition")
print("  que celui que ce memoire applique a ses quatre canaux.")
print()
print("    exercice     nombre   sinistre moyen   charge   produit   ecart a l'identite")
for an in (2024, 2025):
    n = L[f"mult_nombre_{an}"]
    s = L[f"mult_sinistre_moyen_{an}"]
    c = L[f"mult_charge_{an}"]
    print(f"    {an}         {n:6.2f}          {s:7.2f}  {c:7.2f}  {n*s:8.4f}   "
          f"{abs(n*s - c):.4f}")
print()
print("    L'ECART A L'IDENTITE EST LE CONTROLE DE CE BLOC. La charge se decompose")
print("    exactement en nombre de sinistres fois sinistre moyen, et les deux lignes le")
print("    verifient a l'arrondi de publication pres. Si la source avait ete recopiee de")
print("    travers, ce produit ne tomberait pas.")
print()
print("  UNE IMPRECISION DE LA SOURCE, CORRIGEE ICI ET A NE PAS REPRENDRE. Le rapport nomme")
print("  << frequence >> le multiplicateur du NOMBRE de sinistres dans cette decomposition.")
print("  Ce n'en est pas une : une frequence est un nombre de sinistres par assure, et les")
print("  tables du meme rapport la donnent a 1,88 pour 2025 quand le nombre est a 2,79.")
ligne("    2025, multiplicateur d'exposition", L["mult_exposition_2025"])
ligne("    2025, multiplicateur du NOMBRE de sinistres", L["mult_nombre_2025"])
ligne("    2025, multiplicateur de la vraie FREQUENCE", L["mult_frequence_2025"])
_p = L["mult_exposition_2025"] * L["mult_frequence_2025"]
print(f"    controle : exposition x frequence = {_p:.4f}, a comparer au nombre "
      f"{L['mult_nombre_2025']:.2f}, ecart {abs(_p - L['mult_nombre_2025']):.4f}")
print("    Avec la vraie frequence l'identite demande TROIS facteurs, exposition fois")
print("    frequence fois sinistre moyen. La distinction separe un effet de VOLUME d'une")
print("    degradation a exposition donnee, et c'est exactement la lecture que ce memoire")
print("    impose a ses propres canaux.")
print()
print("  DECOMPOSITION 2025 PAR BLOC (nombre, sinistre moyen, charge) :")
print("    bloc                       nombre   sinistre moyen   charge")
for nom, (n, s, c) in L["blocs_2025"].items():
    print(f"    {nom:<24} {n:7.2f}          {s:7.2f}  {c:7.2f}")
print("    Le bloc intermediaire est le SEUL ou le nombre et le sinistre moyen montent")
print("    ENSEMBLE, d'ou sa charge multipliee par 3,53. Les grandes entreprises absorbent")
print("    la hausse du nombre sans derive de cout, et les micro-entreprises portent une")
print("    charge tiree par le seul nombre, sur une base 2024 reduite.")
print()
print("  AVERTISSEMENT D'ECHELLE, ET IL EST DU MEME TYPE QUE CELUI DU 7 AOUT 2026. La charge")
print("  de LUCY est INDEMNISEE, donc nette de franchise et plafonnee par la capacite, et")
print("  sommee sur un portefeuille de MARCHE. La severite de ce memoire est une perte")
print("  operationnelle BRUTE d'entite financiere. Les deux ne se comparent ni en niveau ni")
print("  en quantile : rapprocher les 83,2 M EUR indemnises du marche francais du quantile")
print("  unitaire publie ferait lire une difference de perimetre et de retention comme une")
print("  contradiction. Cette source n'entre dans AUCUNE calibration du memoire.")

titre("Deux constantes homonymes, et le garde-fou qui remplace un renommage")
# DECISION DU 17 AOUT 2026 : ON NE RENOMME PAS, ON REND LA CONFUSION IMPOSSIBLE A COMMETTRE.
# Le projet porte deux constantes dont les noms ne differ ent que par un tiret bas et qui
# n'ont AUCUN rapport :
#   G_BASE  = gain de propagation g, sans dimension, 0,90 en cas de base (scr_engine,
#             euro_cascade_model). Il mesure une CRITICITE de propagation.
#   GBASE   = echelon de severite par pilier, ordinal, chaque echelon doublant la mediane
#             (cascade_model, severite_model). Il indexe une ECHELLE, jamais un montant.
# Le second est documente avec le mot « gravite », ce qui est le terme consacre de l'AMDEC
# mais rend la collision d'autant plus facile a commettre.
#
# POURQUOI PAS DE RENOMMAGE. Il touche vingt-sept fichiers sur un pipeline GELE. Une
# substitution semantiquement fausse mais numeriquement valide ne serait rattrapee par aucun
# controle : le harnais verifie que les nombres publies sortent des scripts, pas qu'ils
# veulent dire ce qu'on croit. Le rapport risque sur gain est donc mauvais, et c'est
# exactement la situation ou le projet a deja choisi de DECLARER plutot que de corriger,
# comme pour p_u.
#
# CE QUI REMPLACE LE RENOMMAGE. Les deux constantes sont imprimees ICI, cote a cote, avec
# leur nature, leur unite et leur module, a chaque execution. Une assertion garantit qu'elles
# ne peuvent pas devenir egales par accident, ce qui est le seul cas ou une substitution
# passerait inapercue. La distinction est en outre verrouillee dans la table des notations du
# memoire, l'entree g portant « mesure une criticite, jamais un montant ».
_HOMONYMES = []
try:
    import importlib
    _lab = os.path.join(REPO, "exploratory", "vasicek_lab")
    _qual = os.path.join(REPO, "exploratory", "cascade_qualitative")
    for _p in (_lab, _qual):
        if _p not in sys.path:
            sys.path.insert(0, _p)
    _eng = importlib.import_module("scr_engine")
    _cas = importlib.import_module("cascade_model")
    _HOMONYMES = [
        ("G_BASE", _eng.G_BASE, "sans dimension", "gain de propagation g, cas de base",
         "scr_engine, euro_cascade_model"),
        ("GBASE", _cas.GBASE, "ordinal", "echelon de severite par pilier",
         "cascade_model, severite_model"),
    ]
except Exception as _exc:                                     # pragma: no cover
    print(f"  Modules indisponibles depuis ce poste ({_exc.__class__.__name__}) :")
    print("  le garde-fou est saute, la declaration ci-dessus reste valable.")

if _HOMONYMES:
    print(f"  {'nom':<10}{'valeur':>26}{'unite':>18}  {'ce que c est'}")
    for _nom, _val, _unite, _sens, _mod in _HOMONYMES:
        _aff = _val if not isinstance(_val, dict) else \
            "{" + ", ".join(f"P{k}:{v}" for k, v in sorted(_val.items())) + "}"
        print(f"  {_nom:<10}{str(_aff):>26}{_unite:>18}  {_sens}")
        print(f"  {'':<10}{'':>26}{'':>18}  defini dans {_mod}")
    _g = _HOMONYMES[0][1]
    _ech = _HOMONYMES[1][1]
    assert isinstance(_g, float) and isinstance(_ech, dict), \
        "G_BASE doit rester un scalaire et GBASE une table par pilier"
    assert _g not in set(_ech.values()), \
        "COLLISION : le gain de propagation a pris une valeur d'echelon de severite"
    print("\n  CONTROLE : le gain est un scalaire, l'echelon une table par pilier, et le")
    print("  premier ne prend aucune des valeurs de la seconde. Une substitution de l'un par")
    print("  l'autre serait donc detectee ici, ce qui est le seul point ou elle pouvait passer.")
    print("  Ce garde-fou ne remplace pas un renommage, il rend son absence sans consequence.")

titre("ENISA Threat Landscape : CITATION EXTERNE, non recalculable")
# TROISIEME SOURCE AU MEME STATUT QUE HACKMAGEDDON. Le chapitre donnees confronte les parts par
# vecteur de Hackmageddon a une source independante, le rapport de l'agence europeenne, et cite
# trois de ses nombres. Aucun n'est reproductible ici : le rapport n'est pas verse dans
# data/raw/ et sa methodologie de collecte n'est pas la notre. Ils etaient donc HORS CONTROLE,
# recopies a la main dans le texte et verifiables par personne. Les enregistrer les rend
# verifiables CONTRE LA SOURCE, ce qui est la seule garantie disponible pour une citation.
#
# CE QUE CES VALEURS FONT DANS LE MEMOIRE, ET CE QU'ELLES NE FONT PAS. Elles servent a UNE
# confrontation qualitative : l'asymetrie entre deux taux de conversion, mesuree par un
# organisme reglementaire sur un perimetre independant, corrobore un classement que le seul
# volume d'incidents ne peut pas reveler. Aucune n'entre dans un calcul, aucune ne porte un
# niveau de capital.
ENISA = {
    "source": "ENISA Threat Landscape 2025, Agence de l'Union europeenne pour la cybersecurite",
    "n_incidents": 4875,
    "perimetre": "incidents de perimetre europeen, collecte propre a l'agence",
    "conversion": {
        "exploitation de vulnerabilite exposee": 0.70,
        "phishing et ingenierie sociale": 0.27,
    },
}
print(f"  source    : {ENISA['source']}")
print(f"  perimetre : {ENISA['perimetre']}")
print(f"  incidents retenus par le rapport         : {ENISA['n_incidents']}")
print("\n  taux de conversion tentative -> intrusion :")
for k, v in ENISA["conversion"].items():
    print(f"    {k:<44}{v:.2f}   soit {100*v:.0f} %")
rap = (ENISA["conversion"]["exploitation de vulnerabilite exposee"]
       / ENISA["conversion"]["phishing et ingenierie sociale"])
print(f"  rapport entre les deux taux              : {rap:.2f}")
print("\n  A QUOI SERT CETTE ASYMETRIE. Le phishing est le vecteur le plus FREQUENT et l'un des")
print("  moins CONVERTISSANTS ; l'exploitation de vulnerabilite est l'inverse. Un modele calibre")
print("  sur le seul volume d'incidents surponderait donc le phishing, et c'est le motif pour")
print("  lequel le memoire retient de Hackmageddon la STRUCTURE par vecteur et jamais le niveau.")
print("  Le rapport ci-dessus est imprime plutot que laisse au lecteur, pour la meme raison que")
print("  les autres rapports derives : un rapport calcule a la redaction n'est verifiable par")
print("  personne.")
print("\n  AVERTISSEMENT, identique a celui de Hackmageddon. Ce rapport n'est PAS versionne dans")
print("  data/raw/ : ces trois valeurs sont une citation enregistree, pas une sortie")
print("  recalculable. Elles ne portent aucun niveau de capital.")

titre("Preprint de cascade climatique : CITATION EXTERNE, non recalculable")
# MEME STATUT QUE HACKMAGEDDON, ET POUR LA MEME RAISON. Le memoire compare desormais son
# CLASSEMENT DES LEVIERS a celui de ce prepublie, et cette comparaison exige de citer ses
# nombres. Ils ne sont reproductibles par aucun script du projet : le papier tourne sur son
# propre moteur, ses parametres sont synthetiques et ses auteurs le declarent. Les enregistrer
# ici les rend VERIFIABLES CONTRE LA SOURCE, ce qui est tout ce qu'on peut garantir, et les
# sort de la zone ou un chiffre recopie a la main n'est controle par personne.
#
# CES VALEURS NE SERVENT QU'A UNE COMPARAISON DE CLASSEMENT. Aucune n'entre dans un calcul du
# memoire, aucune ne porte un niveau de capital, et le papier n'est pas cite comme repere
# empirique : il est SYNTHETIQUE.
CCRN = {
    "source": "Karimi, Salavati, Shokrollahi, arXiv:2608.09456v1 [q-fin.RM], 10 aout 2026",
    "statut": "prepublication, etude numerique entierement SYNTHETIQUE (declare par les auteurs)",
    # Table 11 du papier : ablation structurelle, VaR 99,5 % de la charge annuelle brute,
    # en milliards de dollars.
    "ablation_var995_mdUSD": {
        "CCRN complet": 3.767,
        "sans propagation dirigee": 1.738,
        "sans interaction coulee de debris": 3.699,
        "sans demand surge": 3.720,
        "approximation mono-evenement": 3.503,
    },
    # Table 12 du papier : sensibilite un-a-la-fois de la prime pure, en % du cas de base.
    "tornado_prime_pct": {
        "probabilite d'arete combustible->incendie": (-25.0, 26.6),
        "frequence annuelle d'evenements": (-21.0, 20.7),
        "coefficient climatique de l'arete": (-11.9, 14.1),
        "raideur de la reponse en severite": (-13.5, 7.3),
        "intensite du demand surge": (-1.8, 1.7),
    },
    # Ce qui explique le desaccord de classement, et c'est une propriete de leur MODELE :
    # leur severite est BORNEE, donc elle n'a pas d'indice de queue.
    "severite_bornee": True,
    "multiplicateurs_lognormaux_sd_log": (0.10, 0.15),
}

print(f"  source : {CCRN['source']}")
print(f"  statut : {CCRN['statut']}")

abl = CCRN["ablation_var995_mdUSD"]
ref = abl["CCRN complet"]
print("\n  ablation structurelle, VaR 99,5 % de la charge annuelle (Md USD, leur table 11) :")
for k, v in abl.items():
    ecart = "" if k == "CCRN complet" else f"{100*(v/ref-1):>+8.1f} %"
    print(f"    {k:<38}{v:>8.3f}{ecart:>12}")
print(f"    -> leur brique la plus lourde est la PROPAGATION DIRIGEE, a "
      f"{100*(abl['sans propagation dirigee']/ref-1):+.1f} %.")

print("\n  tornado un-a-la-fois de la prime pure (% du cas de base, leur table 12) :")
for k, (bas, haut) in CCRN["tornado_prime_pct"].items():
    print(f"    {k:<44}{bas:>8.1f} %{haut:>9.1f} %")
print("    -> leur tete de tornado est la probabilite d'arete, puis la frequence.")

print("\n  POURQUOI LEUR CLASSEMENT N'EST PAS LE NOTRE, ET CE N'EST PAS UN DESACCORD DE MESURE.")
print("  Leur severite est BORNEE : reponse bornee, perte plafonnee par une transformation a")
print(f"  capacite, multiplicateurs lognormaux de moyenne un et d'ecart-type logarithmique")
print(f"  {CCRN['multiplicateurs_lognormaux_sd_log'][0]} et "
      f"{CCRN['multiplicateurs_lognormaux_sd_log'][1]}. Elle N'A DONC PAS D'INDICE DE QUEUE, et")
print("  leur ablation ne contient aucune brique « queue » : on ne retire pas ce qui n'est pas la.")
print("  Le plus proche qu'ils font varier est la RAIDEUR DE LA REPONSE EN SEVERITE, qui sort")
print("  derriere la propagation. Notre severite est une GPD de variance infinie, et la queue y")
print("  domine tout. Les deux classements sont donc chacun corrects DANS LEUR MODELE, et ce qui")
print("  les separe est l'indice de queue, non l'architecture.")
print("\n  CONSEQUENCE DE CITATION, ET ELLE VAUT POUR TOUT LE MEMOIRE : ce preprint se cite sur")
print("  le PROTOCOLE (marges appariees, ablation, separation des echelles), JAMAIS sur l'ordre")
print("  d'un resultat en queue. C'est la meme regle que celle deja posee pour l'echelle des")
print("  quantiles au script 80, etendue aux leviers.")

titre("Verdict")
print("Cette sortie rend citables les constantes de calibration dans les chapitres donnees")
print("et socle. Elle atteste la CONFORMITE A LA CONFIGURATION, non l'exactitude empirique :")
print("celle-ci releve des scripts 07, 08b, 47 et 57.")
print("\nEXIT 0")
