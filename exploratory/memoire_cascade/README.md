# memoire_cascade : organisation

Le mémoire. 51 pages, compile en un passage.

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
| `annexes/` | vide pour l'instant, les annexes actuelles sont des chapitres de fin |
| `a_integrer/` | ce qui n'est **pas** intégré : plans de rédaction en commentaire, `macros_requises.tex` (référence), `version_autonome/` (fiches compilables séparément) |
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
