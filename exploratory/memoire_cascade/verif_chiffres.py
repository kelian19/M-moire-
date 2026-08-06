#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Non-régression des chiffres du mémoire.

MOTIVATION. Le script 01 a longtemps imprimé des conclusions codées en dur, contredites
par ses propres chiffres affichés juste au-dessus. Le contrôle qualité reposait sur la
relecture, qui ne passe pas à l'échelle sur plusieurs centaines de nombres. Ce script
remplace la relecture par une vérification : chaque nombre publié dans un chapitre est
recherché dans la sortie du script qui est censé le produire.

PRINCIPE. Pour chaque section du chapitre, on relève les scripts cités (\\texttt{16},
\\texttt{20}, ...) et tous les nombres du texte. Un nombre est CONFIRMÉ s'il apparaît,
à la tolérance d'arrondi près, dans la sortie d'au moins un des scripts cités par sa
section. Sinon il est signalé.

CE QUE CE SCRIPT NE FAIT PAS. Il ne vérifie pas qu'un nombre est au bon endroit ni qu'il
veut dire ce que la phrase prétend : un nombre confirmé peut être mal commenté. Il élimine
la classe d'erreurs la plus fréquente et la plus embarrassante (le chiffre périmé ou
inventé), pas toutes.

Usage :
    python verif_chiffres.py <dossier_des_sorties>
où le dossier contient 16.txt, 20.txt, ... produits en relançant les scripts cités.
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
CHAPITRE_DEFAUT = os.path.join(ICI, "chapitres", "12_resultats.tex")

# Nombres qui ne sont pas des résultats : niveaux de confiance, millésimes, tailles de
# grille, numéros d'article. Les comparer n'aurait aucun sens.
IGNORE = {99.5, 0.995, 97.5, 2.5, 90.0, 95.0, 5.0, 19.0, 1.0, 2.0, 3.0, 4.0, 5.0}
# Millesimes. La borne basse descend a 1900 pour couvrir les dates de theoremes citees dans
# le chapitre socle (Fisher-Tippett-Gnedenko 1928, 1943 ; Balkema-de Haan-Pickands 1974).
# Un montant de cet ordre s'ecrit toujours avec un separateur de milliers dans le memoire,
# donc la confusion avec un resultat reste improbable ; le cas echeant il faut le verifier
# a la main, ce que la liste de travail signale.
ANNEES = set(range(1900, 2036))


def nombres(txt, latex=True):
    """Nombres d'un fragment LaTeX, normalisés (8\\,301 -> 8301 ; 0{,}92 -> 0.92).

    On retire d'abord la MISE EN PAGE : un \\arraystretch de 1,25 ou une largeur de
    figure de 0,9\\linewidth ne sont pas des résultats et les compter comme tels
    fabriquerait de fausses alertes.
    """
    t = txt
    # LES COMMENTAIRES LATEX NE SONT PAS DU TEXTE PUBLIE. Sans ce filtre, un commentaire
    # de migration comme "% MIGRE depuis main.tex (plages 787-932)" fabrique quatre
    # nombres a confirmer qui n'apparaissent nulle part dans le PDF. C'etait la premiere
    # cause de faux positifs du chapitre socle.
    #
    # A NE SURTOUT PAS APPLIQUER AUX SORTIES DE SCRIPTS : elles ecrivent les pourcentages
    # avec un %, et couper la ligne au premier % y detruisait la moitie du pool de
    # reference. D'ou le drapeau `latex`, qui vaut False pour les fichiers NN.txt.
    if latex:
        t = re.sub(r"(?<!\\)%.*", " ", t)
    t = re.sub(r"\\renewcommand\{[^}]*\}\{[^}]*\}", " ", t)
    t = re.sub(r"\\includegraphics\[[^\]]*\]", " ", t)
    t = re.sub(r"\\(?:label|ref|eqref|cite[tp]?)\{[^}]*\}", " ", t)
    t = re.sub(r"\[[^\]]*(?:width|height|scale)[^\]]*\]", " ", t)
    # Un NUMERO DE SCRIPT n'est pas un resultat. Il vit toujours dans un \texttt{}, comme
    # les noms de fichier et de base : aucun chiffre publie n'est en fonte a chasse fixe.
    # Sans ce filtre, citer le script 27 fabrique un "27" a confirmer, et le rapport de
    # verification se remplit de faux positifs qui masquent les vraies erreurs.
    t = re.sub(r"\\texttt\{[^}]*\}", " ", t)
    # Les specifications de filet de tableau (\cmidrule{6-8}, \cline{2-4}) sont de la mise
    # en page : elles produisaient un 6 et un -8 dans chaque section a tableau.
    t = re.sub(r"\\c(?:midrule|line)\s*(?:\([^)]*\))?\s*\{[^}]*\}", " ", t)
    t = re.sub(r"\\multicolumn\{\d+\}", " ", t)
    # LA FRACTION COURTE. \tfrac12 s'ecrit sans accolades ; le nettoyage generique des
    # commandes LaTeX, quelques lignes plus bas, en retirait le \tfrac et laissait « 12 ».
    # Un demi devenait donc le nombre douze, a confirmer dans les sorties de scripts. Le
    # chapitre identifiabilite en fabriquait cinq a lui seul, sur la decomposition
    # P = S_pi + A_pi. La forme longue \frac{1}{2} n'a pas le probleme : elle laisse 1 et 2,
    # deja neutralises par IGNORE.
    t = re.sub(r"\\[tdc]?frac\s*\d\d", " ", t)
    # LES LARGEURS DE COLONNE. Un \begin{tabular}{@{}p{4.3cm} r r r r@{}} produisait 4.3,
    # de la mise en page au meme titre qu'un \arraystretch. Meme motif pour m{} et b{}.
    t = re.sub(r"\b[pmb]\{\s*[\d.]+\s*(?:cm|mm|in|pt|em|ex|\\[a-zA-Z]+)\s*\}", " ", t)
    t = t.replace("\\,", "").replace("~", " ").replace("{,}", ".")
    t = re.sub(r"\\[a-zA-Z]+", " ", t)          # commandes LaTeX restantes
    if not latex:
        # UN NUMERO DE SCRIPT N'EST PAS UN RESULTAT, DES DEUX COTES. Le filtre \texttt{} plus
        # haut l'assure pour le memoire ; rien ne l'assurait pour les sorties, ou une ligne
        # « P1 en tete de priorite (script 30) » versait un 30 dans le pool de reference. Ce
        # 30 confirmait alors, dans toute section citant ce script, le « minimum de 30 exces »
        # et le « k = 30 » du graphe de Hill du chapitre socle, deux valeurs qui n'ont aucun
        # rapport avec lui et que le harnais avait raison de signaler.
        t = re.sub(r"\bscripts?\s*n?o?s?\.?\s*\d+[a-z]?(?:\s*(?:,|et|;)\s*\d+[a-z]?)*",
                   " ", t, flags=re.IGNORECASE)
        # LE SEPARATEUR DE MILLIERS DES SORTIES DE SCRIPT. Le motif d'extraction ci-dessous
        # ne franchit pas la virgule : « 8,122.9 » y devenait DEUX nombres, 8 et 122.9, et le
        # « 8123 » du memoire ressortait donc non confirme alors que le script l'imprimait.
        # Toute la classe des montants a quatre chiffres et plus etait touchee, ce qui noyait
        # les vraies erreurs sous les fausses alertes.
        #
        # AMBIGUITE ASSUMEE, ET C'EST LE POINT DELICAT. Une virgule entre chiffres peut aussi
        # etre un separateur DECIMAL francais, que certaines chaines de narration emploient
        # (« z = +5,12 »). On ne colle donc que les groupes de la forme anglo-saxonne stricte :
        # 1 a 3 chiffres commencant par un chiffre NON NUL, puis exactement 3 chiffres. Cela
        # exclut « 0,807 » et « 0,505 ». Il reste un cas indecidable, « 2,150 » voulant dire
        # 2,150 en decimal francais ; le risque est alors une confirmation a tort, pas un
        # chiffre faux dans le memoire, et il est prefereable a un detecteur ignore parce
        # qu'il crie trop souvent.
        t = re.sub(r"(?<![\d.,])([1-9]\d{0,2})((?:,\d{3})+)(?!\d)",
                   lambda m: m.group(1) + m.group(2).replace(",", ""), t)
    out = []
    for m in re.finditer(r"-?\d+(?:\.\d+)?", t):
        try:
            v = float(m.group(0))
        except ValueError:
            continue
        if abs(v) in IGNORE or (v == int(v) and int(v) in ANNEES):
            continue
        out.append(v)
    return out


def charge_sorties(dossier):
    src = {}
    for f in os.listdir(dossier):
        if f.endswith(".txt"):
            with open(os.path.join(dossier, f), encoding="utf-8", errors="replace") as fh:
                src[f[:-4]] = nombres(fh.read(), latex=False)
    return src


def decimales(v):
    """Nombre de décimales significatives de v, tel qu'il a été écrit dans le mémoire."""
    s = repr(float(v))
    if "e" in s or "E" in s:
        return 0
    return len(s.split(".")[1].rstrip("0")) if "." in s else 0


def confirme(v, pool):
    """Tolérance d'arrondi : 0,6 % en relatif, ou la demi-unité du dernier chiffre écrit.

    POURQUOI PAS UN PLANCHER ABSOLU FIXE. La version precedente prenait max(0,5 ; 0,6 %),
    et ce plancher de 0,5 etait ecrasant sur les petites valeurs : il rendait 0,9 apparie
    a tout ce qui tombe entre 0,4 et 1,4, donc confirme par un 0,99 sans rapport. Tout
    nombre publie sous 83 etait apparie plus largement que la tolerance relative annoncee.

    LA BONNE BORNE EST CELLE DE L'ARRONDI D'ECRITURE. Un nombre ecrit « 122 » vient d'une
    valeur dans [121,5 ; 122,5[ : la tolerance est 0,5. Ecrit « 2,1 », il vient de
    [2,05 ; 2,15[ : la tolerance est 0,05. Ecrit « 0,90 », elle est 0,005. On prend donc la
    demi-unite du dernier chiffre ECRIT, et l'on garde la tolerance relative de 0,6 % pour
    les grands nombres, ou le mémoire arrondit plus librement que le dernier chiffre.
    """
    tol = max(0.006 * abs(v), 0.5 * 10 ** (-decimales(v)))
    return any(abs(v - w) <= tol for w in pool)


def main():
    dossier = sys.argv[1] if len(sys.argv) > 1 else None
    chapitre = sys.argv[2] if len(sys.argv) > 2 else CHAPITRE_DEFAUT
    if not dossier or not os.path.isdir(dossier):
        print(__doc__)
        sys.exit(1)

    sorties = charge_sorties(dossier)
    print(f"sorties chargées : {', '.join(sorted(sorties))}")
    with open(chapitre, encoding="utf-8") as f:
        lignes = f.read().split("\n")

    # Découpage en sections. On coupe aussi sur \section* et \subsection(*) : deux
    # chapitres (données, socle) n'ont qu'une seule \section numérotée sur une dizaine de
    # pages et structurent le reste en sous-sections étoilées. Sans cela leur texte tombe
    # entier dans un seul bloc, dont le pool de scripts est l'union de tout ce qui y est
    # cité : le taux de confirmation s'effondre pour une raison de découpage, pas de fond.
    sections, cur, titre = [], [], "(préambule de chapitre)"
    coupe = re.compile(r"\\(?:sub)?section\*?\{(.+?)\}")
    for l in lignes:
        m = coupe.match(l.strip())
        if m:
            sections.append((titre, cur))
            titre, cur = m.group(1), []
        else:
            cur.append(l)
    sections.append((titre, cur))

    tot = ok = orphelins = 0
    sans_source = []
    detail = []
    for titre, corps in sections:
        txt = "\n".join(corps)
        # Tout \texttt{...} dont le contenu est un identifiant de script connu. Plus
        # robuste que d'exiger le mot "script" juste avant : les sections citent souvent
        # en liste (\og scripts 16b, 20b \fg), et le second serait alors manqué.
        cites = sorted({c for c in re.findall(r"\\texttt\{([0-9a-z]+)\}", txt)
                        if c in sorties})
        vals = nombres(txt)
        if not vals:
            continue
        if not cites:
            sans_source.append((titre, len(vals)))
            continue
        pool = [v for c in cites for v in sorties.get(c, [])]
        manquants = [v for v in vals if not confirme(v, pool)]
        tot += len(vals)
        ok += len(vals) - len(manquants)
        orphelins += len(manquants)
        detail.append((titre, cites, len(vals), manquants))

    print("\n" + "=" * 78)
    print("VÉRIFICATION SECTION PAR SECTION")
    print("=" * 78)
    for titre, cites, n, manquants in detail:
        etat = "OK" if not manquants else f"{len(manquants)} non confirmé(s)"
        print(f"\n  {titre[:58]:<58}")
        print(f"    scripts {','.join(cites):<14} {n:>3} nombres   -> {etat}")
        if manquants:
            aff = ", ".join(f"{v:g}" for v in manquants[:14])
            print(f"    non trouvés : {aff}" + (" ..." if len(manquants) > 14 else ""))

    if sans_source:
        print("\n  Sections SANS script cité (non vérifiables automatiquement) :")
        for t, n in sans_source:
            print(f"    {t[:56]:<56} {n:>3} nombres")

    print("\n" + "=" * 78)
    print(f"  {tot} nombres vérifiables, {ok} confirmés, {orphelins} non confirmés "
          f"({100*ok/tot:.1f} % de confirmation)" if tot else "  rien à vérifier")
    print("=" * 78)
    print("  Un nombre non confirmé n'est pas forcément faux : il peut venir d'un calcul")
    print("  intermédiaire non imprimé, d'un arrondi de rédaction, ou d'une autre source.")
    print("  Mais chacun doit être justifié à la main. C'est la liste de travail.")


if __name__ == "__main__":
    main()
