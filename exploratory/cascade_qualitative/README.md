# cascade_qualitative : la carte

Modèle qualitatif de la cascade DORA (le classeur de jugement d'expert) et instrument
d'élicitation. C'est la couche amont : elle définit le jugement, `vasicek_lab` le
quantifie.

## Règles de structure, à ne pas casser

- **`cascade_model.py` reste à la racine.** C'est la source unique de `ROOT`, `TRANS`
  et `GBASE`. `vasicek_lab/scr_engine.py` l'importe par un chemin relatif
  (`../cascade_qualitative`). Le déplacer casserait tout le laboratoire.
- **`figures/` reste à la racine.** Le mémoire le vise en dur.

## Le contenu

### cascade_model.py
Le jugement d'expert, une seule fois : `ROOT` (propension d'amorce), `TRANS` (la matrice
dirigée « i entraîne j »), `GBASE` (gravité de base), et le barème ordinal. Tout le reste
en dérive.

### outils/
Générateurs. `build_figures` (F1 à F11), `build_tree_figure` (F12, la récursion),
`build_bout_de_chaine` (F13), `build_cascade_workbook` (le classeur Excel),
`sensitivity_analysis` (ancrage documentaire et sensibilité du modèle qualitatif).

### fiches/
Documents pédagogiques compilés : `fiche_pedagogique`, `bout_de_chaine`, `cas_usage_p2`,
`draft_probas_conditionnelles`.

### elicitation/
L'instrument complet de l'élicitation de Cooke.

| fichier | statut de diffusion |
|---|---|
| `questionnaire_elicitation_w.pdf` | **c'est CE fichier qu'on envoie aux experts** (version aveugle) |
| `elicitation_reponses_TEMPLATE.csv` | grille de saisie des réponses |
| `antiseche_animation_elicitation.pdf` | pour l'animateur, pendant la séance |
| `protocole_elicitation_w.pdf` | **NE JAMAIS ENVOYER À UN EXPERT** : contient les valeurs de référence des questions graines |

Le moteur de calcul est dans `../vasicek_lab/7_elicitation/`.

### donnees/
`cascade_piliers_DORA.csv` et `.xlsx` : le classeur des combinaisons de piliers.

## Où sont passés les chapitres du mémoire

Les trois chapitres rédigés (identifiabilité, robustesse, positionnement) ont été
déplacés vers `../memoire_cascade/a_integrer/`, avec leur version autonome compilable
dans `a_integrer/version_autonome/`. Ils n'ont plus de copie ici, pour éviter deux
versions divergentes.
