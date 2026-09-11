#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construire_v3.py : fabrique les chapitres de main_v3 A PARTIR des chapitres partages.

POURQUOI CE SCRIPT EXISTE, ET POURQUOI main_v3 N'EST PAS ECRIT A LA MAIN.
main.tex et main_v2.tex appellent LES MEMES fichiers de chapitres, et la regle du
projet est de ne jamais dupliquer un chapitre pour faire evoluer une version :
deux textes a maintenir divergent en une semaine. main_v3 restructure pourtant le
corps, donc il lui faut des chapitres differents. La seule facon de tenir les deux
contraintes est de les DERIVER : ce script lit chapitres/, en retire des sections
entieres, et ecrit chapitres_v3/. Si un chapitre partage change, on relance et la
v3 suit. Aucun texte n'est retape.

CE QU'IL FAIT. Quatorze sections sont RETIREES du document, et remplacees chacune
par une section courte, le « pont », qui dit ce que la section etablissait et cite
le ou les scripts qui le portent.

POURQUOI RETIRER ET NON DEPLACER EN ANNEXE. La premiere version de ce script
deplacait les quatorze sections vers une annexe de complements. C'etait la bonne
reponse tant que la cible etait la norme de l'Institut, qui compte « environ
70 pages HORS ANNEXES » : deplacer suffisait alors a s'y conformer. Kelian a
ecarte cette norme le 11 septembre et demande a la place une reduction reelle de
20 %. Un deplacement ne reduit rien, il redistribue : l'annexe a donc ete
supprimee et les sections sortent du document.

CE QUI REND CE RETRAIT SANS PERTE, et c'est la seule raison pour laquelle il est
acceptable : main_v2 reste la version COMPLETE et n'est pas touche. Les quatorze
sections y figurent integralement, avec leurs tables, leurs figures et leurs
nombres. main_v3 est une version courte a cote, pas un remplacement.

CE QU'IL NE FAIT PAS. Il ne reecrit aucune phrase conservee, ne touche a aucun
nombre, ne modifie aucun fichier partage. Les ponts sont le seul texte neuf, et
ils ne portent presque aucun chiffre, par construction.

Usage :
    python construire_v3.py --reco     # reconnaissance, n'ecrit rien
    python construire_v3.py            # genere chapitres_v3/
"""

import io
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, "chapitres")
DST = os.path.join(ICI, "chapitres_v3")

# ---------------------------------------------------------------------------
# LES QUATORZE DEPLACEMENTS.
#
# Chaque entree : (fichier, motif du titre, titre du pont, texte du pont, label).
# Le motif doit identifier UNE section et une seule ; le script echoue sinon,
# plutot que de deplacer la mauvaise.
#
# Le texte du pont porte DELIBEREMENT tres peu de chiffres. Ceux qu'il porte sont
# repris de la section deplacee, et la ligne de sources de cette section est
# recopiee sous le pont : le bloc reste donc sous controle du harnais.
# ---------------------------------------------------------------------------
DEPLACEMENTS = [
    dict(
        fichier="05_donnees_limites",
        motif="Pourquoi ne pas multiplier les sources",
        pont_titre="Pourquoi le dispositif s'arrête à ces sources",
        label="ann:g:sources",
        pont=r"""
Le dispositif de données ne cherche pas à empiler les sources, et ce n'est pas une
limite subie mais un choix. Une source supplémentaire n'ajoute de l'information que si
elle est indépendante des précédentes et si son périmètre est déclarable ; à défaut,
elle ajoute du volume et une incertitude de provenance. Le motif complet, source par
source, figure à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="06_socle_mecaniste",
        motif="Les deux théorèmes",
        pont_titre="Ce qui autorise l'extrapolation de queue",
        label="ann:g:theoremes",
        pont=r"""
L'extrapolation au-delà du plus grand sinistre observé n'est pas une commodité de
calcul : elle repose sur deux résultats classiques de la théorie des valeurs extrêmes,
qui disent sous quelles conditions la loi des excès au-dessus d'un seuil élevé converge
vers une loi de Pareto généralisée, et à quelle famille appartient alors la loi des
maxima. Ces deux énoncés, leurs conditions d'application et ce qu'ils n'autorisent pas
sont repris à l'annexe~\ref{%(label)s}. Ce qui importe ici est la conséquence : la forme
de la queue est \emph{héritée} d'un théorème, et non ajustée librement sur les données.
""",
    ),
    dict(
        fichier="06_socle_mecaniste",
        motif="Hill contre maximum de vraisemblance",
        pont_titre="Deux estimateurs de l'indice de queue, et ce que leur écart signifie",
        label="ann:g:hill",
        # Le Hill plot reste cite deux fois depuis du texte conserve du meme
        # chapitre : la figure repart donc avec le pont.
        flottants=["soc:fig:hill-ic"],
        pont=r"""
L'estimateur de Hill et le maximum de vraisemblance ne donnent pas le même indice de
queue sur ce périmètre, et l'écart est grand. Invoquer un biais d'échantillon fini
serait un argument d'autorité ; l'écart est donc \emph{simulé} sous le modèle publié
plutôt qu'invoqué. Le résultat est que les valeurs observées tombent dans l'intervalle
que la calibration retenue produit elle-même : l'écart est ce qu'il devrait être, et la
donnée corrobore la calibration par un chemin indépendant des tests d'adéquation. Le
protocole et les six valeurs sont à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="07_cascade_dirigee",
        motif="Vérification numérique des trois",
        pont_titre="Les trois propriétés, vérifiées numériquement",
        label="ann:g:verif-cascade",
        pont=r"""
Les trois propriétés démontrées ci-dessus sont aussi vérifiées numériquement, sur la
matrice calibrée et sur des matrices tirées au hasard : la dépendance à l'ordre est non
nulle, la normalisation borne effectivement la progéniture, et une matrice et sa
transposée donnent bien un capital différent. Les démonstrations figurent à
l'annexe~\ref{ann:cascade} et les vérifications numériques correspondantes à
l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="11_conformite_multietats",
        motif="sont posées",
        pont_titre="Le statut des valeurs du gain de propagation",
        label="ann:g:valeurs-g",
        pont=r"""
Les trois valeurs du gain de propagation associées aux états de conformité sont
\textbf{posées et non calibrées}, et le mémoire ne le dissimule pas. La thèse n'en dépend
pourtant pas, et la raison est structurelle : le capital est croissant en ce gain, donc
toute correspondance qui respecte l'\emph{ordre} des états produit l'écart, dès lors que
le forfait réglementaire reste plat. Seule l'\emph{amplitude} de l'écart est un scénario.
Le balayage qui établit cette monotonie, et la table des valeurs alternatives, sont à
l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="09_identifiabilite",
        motif="Le biais de narration",
        pont_titre="Le biais de narration du corpus",
        label="ann:g:narration",
        pont=r"""
Un corpus de rapports post-mortem ne décrit pas les incidents, il les raconte, et une
narration choisit un ordre. Ce biais est donc mesuré plutôt que déclaré : loi nulle
exacte, jackknife par incident, et recherche du point de rupture à partir duquel la
direction cesserait d'être significative. Le verdict est que le biais est \textbf{borné et
non levé} : il ne suffit pas à expliquer la direction observée, mais il n'est pas
éliminé, et c'est l'une des raisons pour lesquelles la direction reste bornée au lieu
d'être posée. Le protocole et les trois mesures sont à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="09_identifiabilite",
        motif="Les séquences ordonnées",
        pont_titre="Les séquences ordonnées, une voie refermée",
        label="ann:g:sequences",
        pont=r"""
Exploiter les triplets plutôt que les seules paires est une idée qui revient
naturellement, puisque des marges par paires ne déterminent pas une loi sur les
permutations. Elle ne donne rien sur ce corpus, pour trois raisons distinctes et
mesurées, et le critère qui permettrait de rouvrir la question est écrit. Le détail est
à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="09_identifiabilite",
        motif="La formalisation bayésienne",
        pont_titre="La lecture bayésienne de la direction",
        label="ann:g:bayes",
        pont=r"""
La même question se reformule en termes bayésiens, en plaçant une loi a priori sur les
orientations admissibles plutôt qu'un ensemble. Cette reformulation est instructive mais
elle \textbf{ne déplace pas la frontière} : ce que la donnée n'identifie pas, un a priori
ne le révèle pas, il le remplace. Le développement est à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="12_resultats",
        motif="La sensibilité aux probabilités de propagation",
        pont_titre="La sensibilité au niveau de propagation",
        label="ann:g:sensibilite-prop",
        pont=r"""
La crainte que l'on adresse spontanément à un modèle de cascade est que son résultat
dépende du niveau de propagation retenu. La sensibilité mesurée dit l'inverse, et c'est
un résultat contre-intuitif qu'il faut énoncer tel quel : \textbf{le niveau de propagation
est le moins sensible des leviers}, et la fragilité du chiffre se situe dans l'ajustement
de valeurs extrêmes, pas dans la contagion. L'ignorance sur la direction, elle, ne se
stresse pas mais se gradue, et son coût maximal est connu d'avance. Les tables complètes
sont à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="12_resultats",
        motif="Un ordre de grandeur à l'épreuve du réel",
        pont_titre="Du secteur à l'entité : ce que la descente d'échelle permet",
        label="ann:g:descente",
        # La table des echelles est citee DEUX FOIS depuis le chapitre des donnees,
        # donc depuis un autre chapitre et depuis du texte conserve. Elle repart
        # avec le pont, dont elle est exactement le sujet.
        flottants=["tab:echelle"],
        pont=r"""
Les niveaux établis jusqu'ici valent à l'échelle du secteur. Les transposer à une entité
demande une descente d'échelle, dont les deux canaux, la fréquence et la sévérité, sont
estimés séparément et dont aucun n'a une élasticité de un à la taille. Cette descente a
une \textbf{borne inférieure de validité}, publiée, en dessous de laquelle le modèle
affirmerait qu'une entité de quelques milliards subit à peu près la sévérité d'une
institution mondiale. Le protocole, les élasticités et la borne sont à
l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="12_resultats",
        motif="Quatre entités réelles",
        pont_titre="Quatre bilans réels, et le statut du chiffre obtenu",
        label="ann:g:entites",
        pont=r"""
La méthode est appliquée à quatre bilans d'entités réelles, anonymisées en classes de
taille, à partir de leurs seuls états publiés. Le point à retenir n'est pas le montant
obtenu mais son statut : il s'agit d'une \textbf{borne supérieure d'ordre de grandeur et non
d'une mesure}, l'entité notionnelle tombant sous la borne inférieure de validité rappelée
ci-dessus. Le détail des quatre bilans, la table de correspondance des champs et le
motif de la requalification sont à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="12_resultats",
        motif="Détenir ou transférer",
        pont_titre="Détenir ou transférer, en deux phrases",
        label="ann:g:transfert",
        pont=r"""
Le capital libéré par une remédiation peut être comparé au prix de marché du même risque.
Deux choses en ressortent, et une seule est une sortie du modèle. La valeur présente de
l'économie de portage vaut exactement la variation de capital, quel que soit le taux
retenu : la révision du coût du capital déplace le nombre d'années, pas l'économie. Et
le bénéfice a deux composantes dont une seule est monétisée, la sinistralité évitée
pesant plusieurs fois le portage, si bien que le retour calculé sur le seul portage est
un \textbf{majorant} et non un plancher. Le calcul complet est à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="13_inventaire_hypotheses",
        motif="De l'incertitude au chiffre reporté",
        pont_titre="Quelle grandeur reporter",
        label="ann:g:postures",
        pont=r"""
Une fois l'incertitude établie, il reste à choisir ce que le mémoire publie. Six postures
sont définies et chiffrées, du quantile ponctuel au pire cas à indice de queue posé. La
posture retenue est le \textbf{plug-in accompagné de sa bande}, et le motif est
réglementaire avant d'être d'opportunité : une borne haute sur un ensemble d'ambiguïté est
un suprémum sur une famille de lois, pas un quantile de la loi de perte, donc la
substituer répondrait à une autre question. Un point mérite d'être connu avant d'en
débattre : la posture robuste \textbf{est} la borne haute de l'intervalle déjà publié, de
sorte que reporter le plug-in avec sa bande publie déjà le chiffre robuste. La table des
six postures et leur bruit de simulation sont à l'annexe~\ref{%(label)s}.
""",
    ),
    dict(
        fichier="13_inventaire_hypotheses",
        motif="Un défaut de calibration",
        pont_titre="Un défaut de calibration, chiffré plutôt que corrigé",
        label="ann:g:defaut-calibration",
        pont=r"""
La calibration publiée porte une incohérence arithmétique connue : le taux de dépassement
et le nombre d'excès ne désignent pas le même échantillon, alors que la formule qui les
emploie n'a que deux degrés de liberté pour trois entrées. L'effet est \emph{calculé} et
non estimé, il vaut quelques pour cent sur le quantile unitaire, soit une fraction de la
largeur de l'intervalle publié sur cette même grandeur. La valeur reste gelée, et ce choix
est assumé : rejouer un pipeline stochastique pour un écart de cette taille déplacerait
des centaines de nombres publiés sans qu'aucun déplacement soit attribuable à la
correction, et la piste d'audit serait perdue pour un gain immatériel.

\textbf{Deux prudences à ne pas confondre.} Côté solvabilité l'écart est
anti-conservateur, il sous-estime le capital, et une sous-estimation se déclare ; côté
thèse il va dans l'autre sens, le chiffre avancé étant minoré et non gonflé. Seul le
premier engage. Le calcul, son signe et le contrôle qui le recalcule à chaque exécution
sont à l'annexe~\ref{%(label)s}.
""",
    ),
]


def lire(fichier):
    with io.open(os.path.join(SRC, fichier + ".tex"), encoding="utf-8") as fh:
        return fh.read().splitlines()


def bornes_section(lignes, motif):
    """Retourne (debut, fin) de l'unique section dont le titre contient motif."""
    debuts = [i for i, l in enumerate(lignes)
              if l.startswith("\\section{") and motif in l]
    if len(debuts) != 1:
        raise SystemExit(
            f"ECHEC : le motif {motif!r} designe {len(debuts)} sections, il en faut "
            f"exactement une. Aucun fichier n'a ete ecrit."
        )
    deb = debuts[0]
    fin = len(lignes)
    for j in range(deb + 1, len(lignes)):
        if lignes[j].startswith("\\section{"):
            fin = j
            break
    return deb, fin


# Les ponts ont ete rediges quand les sections partaient en annexe, et ils s'y
# referaient. L'annexe ayant ete supprimee au profit d'un retrait reel, le renvoi
# est reporte sur la version longue. La substitution est faite ici, a un seul
# endroit, plutot qu'en reecrivant les quatorze textes : une seule regle a relire.
# Le \ref{ann:cascade} du pont de la cascade n'est PAS touche, cette annexe-la
# existant toujours dans la v3.
# DEUX PIEGES ICI, TROUVES EN RELISANT LA SORTIE ET NON LE CODE.
# 1. la preposition part avec le renvoi, sinon on obtient « sont A la version
#    longue » au lieu de « sont DANS la version longue » ;
# 2. les ponts sont ecrits sur plusieurs lignes, et le renvoi peut etre coupe par
#    un retour a la ligne entre le « a » et « l'annexe ». Une comparaison de
#    chaines echoue alors en silence sur trois ponts sur quatorze : il faut une
#    expression reguliere tolerante a l'espace.
RENVOI_ANNEXE = re.compile(r"à\s+l'annexe~\\ref\{%\(label\)s\}")
RENVOI_V3 = "dans la version longue de ce mémoire"


def labels_de_section(bloc):
    """Les \\label de SECTION d'un bloc retire, a reprendre sur son pont.

    Retirer une section casse tous les \\ref qui la visent, y compris depuis des
    chapitres non modifies : la premiere compilation de la v3 a sorti sept renvois
    sans cible, soit vingt « ?? » dans le PDF. Le pont reprend donc les labels de
    la section qu'il remplace, et le renvoi pointe alors vers l'endroit ou le sujet
    vit desormais, ce qui est exact et non un rafistolage.

    Le filtre porte sur le PREFIXE et non sur la position : un label de section
    commence par sec: ou soc:sec: dans ce projet, un label de flottant par fig:,
    tab: ou eq:. Rediriger un \\ref de figure vers une section afficherait un
    numero de section la ou le texte annonce une figure, donc mentirait.
    """
    out = []
    for l in bloc:
        for m in re.finditer(r"\\label\{((?:soc:)?sec:[^}]+)\}", l):
            if m.group(1) not in out:
                out.append(m.group(1))
    return out


def extraire_flottant(bloc, label):
    """Le bloc \\begin{figure|table} ... \\end{...} qui porte ce label.

    Deux flottants retires restaient cites depuis du texte CONSERVE, et dans un cas
    depuis un autre chapitre : la table des echelles vit au chapitre des resultats
    et le chapitre des donnees la cite deux fois. Un document ne doit pas renvoyer a
    une figure qu'il ne contient pas : le flottant est donc repris avec le pont,
    dont il illustre precisement le propos.
    """
    deb = None
    for i, l in enumerate(bloc):
        if re.match(r"\s*\\begin\{(figure|table)\}", l):
            deb = i
        if "\\label{" + label + "}" in l and deb is not None:
            for j in range(i, len(bloc)):
                if re.match(r"\s*\\end\{(figure|table)\}", bloc[j]):
                    return bloc[deb:j + 1]
    raise SystemExit(f"flottant {label!r} introuvable dans le bloc retire")


def scripts_cites(bloc):
    """Les numeros de script cites dans un bloc, dedupliques et ordonnes.

    POURQUOI PAS LA LIGNE « Sources : ... » TELLE QUELLE. Premiere version de ce
    script : on recopiait sous le pont la derniere ligne du bloc contenant
    « Source ». Deux defauts, trouves en passant le mode reconnaissance. D'abord
    la plupart de ces lignes sont des fins de LEGENDE de figure, du genre
    « ... Source : script~47.}{fig:biais-narration} » : les recopier aurait injecte
    des accolades orphelines dans le corps. Ensuite quatre sections sur quatorze
    n'ont aucune ligne de ce type, leurs citations vivant dans le fil du texte.

    On releve donc les citations elles-memes, sous la forme \\texttt{NN}, et le pont
    reconstruit une ligne de sources propre.
    """
    vus = []
    for l in bloc:
        for m in re.finditer(r"\\texttt\{(\d{1,2}[a-z]?)\}", l):
            if m.group(1) not in vus:
                vus.append(m.group(1))
    return sorted(vus, key=lambda s: (int(re.match(r"\d+", s).group()), s))


def ligne_sources_pont(nums):
    """La ligne de sources a poser sous un pont, ou None s'il n'y a rien a citer."""
    if not nums:
        return None
    tete = ", ".join("\\texttt{" + n + "}" for n in nums[:-1])
    dernier = "\\texttt{" + nums[-1] + "}"
    corps = (tete + " et~" + dernier) if tete else dernier
    mot = "scripts" if len(nums) > 1 else "script"
    return "\\noindent Sources : " + mot + "~" + corps + "."


def main():
    reco = "--reco" in sys.argv
    if not reco:
        os.makedirs(DST, exist_ok=True)

    par_fichier = {}
    for d in DEPLACEMENTS:
        par_fichier.setdefault(d["fichier"], []).append(d)

    extraits = []          # (ordre, titre, bloc) pour l'annexe
    for fichier, liste in par_fichier.items():
        lignes = lire(fichier)
        coupes = []
        for d in liste:
            deb, fin = bornes_section(lignes, d["motif"])
            bloc = lignes[deb:fin]
            src = ligne_sources_pont(scripts_cites(bloc))
            coupes.append((deb, fin, d, bloc, src))
            if reco:
                print(f"--- {fichier} | l.{deb+1}-{fin} | {fin-deb} lignes")
                print(f"    titre  : {lignes[deb][:96]}")
                print(f"    scripts: {', '.join(scripts_cites(bloc)) or 'aucun'}")

        if reco:
            continue

        # Reconstruction du chapitre : on remplace chaque bloc par son pont.
        coupes.sort(key=lambda c: c[0])
        sortie, curseur = [], 0
        for deb, fin, d, bloc, src in coupes:
            sortie.extend(lignes[curseur:deb])
            sortie.append("\\section{" + d["pont_titre"] + "}")
            sortie.append("% PONT v3 : la section complete est dans main_v2, version")
            sortie.append("% longue et non modifiee. Genere par construire_v3.py.")
            # Les labels de la section retiree sont repris ici, sans quoi tout
            # \ref qui la visait sortirait en « ?? » dans le PDF.
            for lab in labels_de_section(bloc):
                sortie.append("\\label{" + lab + "}")
            texte = RENVOI_ANNEXE.sub(RENVOI_V3, d["pont"].strip())
            # Pas de formatage %(...)s ici : un pont peut contenir un « \% » LaTeX,
            # que l'operateur % de Python prendrait pour un marqueur et ferait
            # echouer. La substitution ci-dessus a deja retire le seul marqueur.
            if "%(label)s" in texte:
                raise SystemExit(f"pont non substitue : {d['motif']!r}")
            sortie.append(texte)
            sortie.append("")
            if src:
                sortie.append(src)
                sortie.append("")
            # Les flottants encore cites depuis du texte conserve repartent avec
            # le pont, dont ils illustrent le propos.
            for lab in d.get("flottants", []):
                sortie.extend(extraire_flottant(bloc, lab))
                sortie.append("")
            curseur = fin
        sortie.extend(lignes[curseur:])

        chemin = os.path.join(DST, fichier + "_v3.tex")
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("% FICHIER GENERE PAR construire_v3.py, NE PAS EDITER A LA MAIN.\n")
            fh.write("% Source : chapitres/" + fichier + ".tex, moins les sections\n")
            fh.write("% retirees, qui restent integralement dans main_v2. Toute correction\n")
            fh.write("% se fait dans le fichier source puis par relance du script, sinon\n")
            fh.write("% les deux divergent.\n")
            fh.write("\n".join(sortie) + "\n")
        print(f"ecrit  {os.path.relpath(chemin, ICI)}  ({len(sortie)} lignes, "
              f"{len(lignes) - len(sortie)} de moins)")

        for deb, fin, d, bloc, src in coupes:
            extraits.append((DEPLACEMENTS.index(d), d, bloc))

    if reco:
        return

    # Aucune annexe de complements n'est ecrite : les quatorze sections sortent du
    # document. Elles restent integralement dans main_v2, qui n'est pas touche.
    retire = sum(len(b) for _, _, b in extraits)
    print(f"\n{len(extraits)} sections retirees du corps, {retire} lignes au total.")
    print("Elles ne sont PAS recopiees ailleurs : main_v2 reste la version longue.")


if __name__ == "__main__":
    main()
