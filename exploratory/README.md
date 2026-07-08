# Chantier exploratoire : risque cyber / DORA

Deux chantiers complémentaires sur la modélisation du risque des cinq piliers DORA
(Règlement UE 2022/2554). L'intuition commune : **l'ordre d'apparition des piliers
pilote le risque** (cascade dirigée, asymétrique). Le premier chantier l'établit
qualitativement, le second le formalise quantitativement.

```
exploratory/
├── cascade_qualitative/     Modèle qualitatif : l'ordre pilote proba/gravité/criticité
└── vasicek_lab/             Modèle quantitatif : Vasicek dirigé + seuil K non gaussien
```

## 1. `cascade_qualitative/` : le modèle qualitatif

L'ordre d'une cascade de piliers décide de sa probabilité, sa gravité et sa criticité
conceptuelles, via trois barèmes d'expert (ROOT, TRANS asymétrique, GBASE).

| Fichier | Rôle |
|---|---|
| `build_cascade_workbook.py` | moteur de score → `cascade_piliers_DORA.xlsx` (326 scénarios) |
| `build_figures.py` | figures F1-F6 (messages cachés, carte des scores) |
| `build_tree_figure.py` | figure F12 (arbre récursif de la probabilité) |
| `sensitivity_analysis.py` | Monte-Carlo (3000 tirages) → F7-F11 (robustesse) |
| `fiche_pedagogique.tex/.pdf` | fiche : comment sont construits les scores (4 p.) |
| `figures/` | F1-F12 (PNG) |

**Résultats clés :** effet d'ordre robuste (jamais < 80 % sur 100 % des tirages),
classement robuste (84 %), plafond de criticité *fragile* (franchi dans 55 % des
tirages), l'asymétrie causale TRANS porte le résultat.

## 2. `vasicek_lab/` : le modèle quantitatif (Vasicek dirigé)

Refonte du Merton-Vasicek pour DORA : facteur systémique **par pilier**, contagion
**dirigée** `W`, seuil `K` **réglementaire + EVT** au lieu de `Phi^-1(PD)`.

| Fichier | Rôle |
|---|---|
| `note_vasicek_dirige.tex/.pdf` | note pédagogique complète (6 p.) : concept → modèle → preuve → limites |
| `01_non_transitivite.py` | figure G1 : TRANS asymétrique à 81 % → pas une corrélation |
| `build_network_figure.py` | figure H1 : réseau dirigé `W` + cascade `(I-W)^-1` |
| `02_seuil_Ki_horserace.py` | figure J : banc d'essai `Phi^-1(PD)` vs EVT |
| `03_calibration_W.py` | figures K1, K2 : protocole d'estimation de `W`, validé sur données simulées |
| `figures/` | G1, H1, J, K1, K2 (PNG) |

**Résultats clés :** la directionnalité (pas la non-transitivité) casse Vasicek ;
`Phi^-1(PD)` sous-provisionne (-14 %) et dérive dans le temps ; l'EVT est quasi sans
biais (-1,4 %) et robuste à la sous-déclaration. Le protocole de calibration de `W`
(régression logistique par pilier sur les incidents retardés, effets de période pour le
systémique) retrouve la structure dirigée (corrélation 0,97) : l'asymétrie n'est
identifiable que par l'information temporelle, et la méthode est prête à brancher sur un
vrai panel d'incidents (registres DORA, ANSSI/ENISA, RGPD).

## Compilation des PDF

Documents pdfLaTeX-standard, compilés avec Tectonic :
`tectonic -X compile <fichier>.tex --outdir <dossier>`. Les scripts Python tournent
dans le `.venv` du dépôt (numpy, scipy, pandas, matplotlib, openpyxl).
