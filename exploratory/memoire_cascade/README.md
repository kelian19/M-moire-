# memoire_cascade : organisation

Le mémoire. **169 pages au 3 septembre 2026**, dont 123 de corps, et il compile en un passage.
Ce compte se périme : le relever dans `main.toc` ou sur le PDF, jamais sur un index Spotlight.

La commande ci-dessous écrit dans `build/`, qui est ignoré par git, donc elle **ne met pas à jour
le `main.pdf` versionné**. Pour une compilation qui le met à jour, et pour les contrôles à passer
ensuite, la référence est la section « Comment construire » du `CLAUDE.md` à la racine.

```powershell
cd exploratory\memoire_cascade
New-Item -ItemType Directory -Force -Path build | Out-Null
..\..\memoire\tectonic.exe -X compile main.tex --outdir build
```

## Où est quoi

| Chemin | Rôle |
|---|---|
| `main.tex` | **chef d'orchestre uniquement** : la classe, le préambule, l'ordre de lecture. 30 lignes, aucun contenu rédactionnel. |
| `preambule.tex` | paquets, palette, encadrés (`cle`, `attention`, `migration`), macros de tableaux, environnements de théorème, notations |
| `chapitres/` | **un fichier par chapitre**, autoportant : il contient son propre `\chapter` et tout son contenu |
| `annexes/` | vide, et le rester : les six annexes sont des fichiers de `chapitres/`, nommés par leur numéro d'ordre et non par leur lettre. **Le nom du fichier ne dit pas la partie** : `12b_adaptations_pilier.tex` est l'annexe C, pas un chapitre du corps |
| `a_integrer/` | **MORT**, aucun `\input` ne le lit et son `STATUT.md` le dit. Ne pas y puiser |
| `references.bib` | bibliographie (natbib) |
| `build/` | sortie, ignoré par git |

## Ajouter ou déplacer un chapitre

Créer le fichier dans `chapitres/`, avec son `\chapter{...}` et son `\label{chap:...}` en
tête, puis ajouter une ligne `\input{chapitres/NN_slug}` dans `main.tex` à la bonne place.
L'ordre du document est l'ordre des lignes de `main.tex`, et rien d'autre.

## Règles à ne pas casser

- **`\graphicspath` vise trois dossiers** : `../vasicek_lab/figures/`,
  `../cascade_qualitative/figures/` et `../../outputs/`. Les figures s'appellent par leur
  seul nom (ou `figures/nom.png` pour celles du pipeline principal). Ne pas déplacer ces
  dossiers.
- **Pas de littéraux `«` `»` `§`** : glyphes faux sous Tectonic avec ce préambule.
  Utiliser `\og ... \fg{}` et `\S`. Les accents passent normalement.
- L'euro s'écrit `\euro{}`. Pas de tirets cadratins.
- **`W` n'est jamais présenté comme calibré**, et le niveau absolu du SCR est toujours
  cadré comme illustratif (c'est démontré au chapitre 10, pas seulement affirmé).
