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
ANNEES = set(range(1990, 2036))


def nombres(txt):
    """Nombres d'un fragment LaTeX, normalisés (8\\,301 -> 8301 ; 0{,}92 -> 0.92).

    On retire d'abord la MISE EN PAGE : un \\arraystretch de 1,25 ou une largeur de
    figure de 0,9\\linewidth ne sont pas des résultats et les compter comme tels
    fabriquerait de fausses alertes.
    """
    t = txt
    t = re.sub(r"\\renewcommand\{[^}]*\}\{[^}]*\}", " ", t)
    t = re.sub(r"\\includegraphics\[[^\]]*\]", " ", t)
    t = re.sub(r"\\(?:label|ref|eqref|cite[tp]?)\{[^}]*\}", " ", t)
    t = re.sub(r"\[[^\]]*(?:width|height|scale)[^\]]*\]", " ", t)
    t = t.replace("\\,", "").replace("~", " ").replace("{,}", ".")
    t = re.sub(r"\\[a-zA-Z]+", " ", t)          # commandes LaTeX restantes
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
                src[f[:-4]] = nombres(fh.read())
    return src


def confirme(v, pool):
    """Tolérance d'arrondi : 0,6 % en relatif, au moins 0,5 en absolu."""
    tol = max(0.5, 0.006 * abs(v))
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

    # découpage en sections
    sections, cur, titre = [], [], "(préambule de chapitre)"
    for l in lignes:
        m = re.match(r"\\section\{(.+?)\}", l)
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
