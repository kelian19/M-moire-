# Phase 5 — Rédaction, argumentation, et corrections appliquées

Relevé du 21 septembre 2026. Document : `main_ensae.pdf`, **204 pages** après corrections.

---

## 1. Qualité rédactionnelle : le dossier est propre

Contrôle automatisé sur **57 230 mots de prose**, maths et commandes LaTeX exclues.

| Contrôle | Résultat | Statut |
|---|---|---|
| Tournures de rédaction automatique | **11 occurrences au total**, soit 0,19 pour 1 000 mots | ✔ |
| « il est important de noter », « force est de constater », « joue un rôle clé » | **0** | ✔ |
| Superlatifs creux (« véritable », « crucial », « primordial ») | 1 | ✔ |
| Tirets cadratins | **0** | ✔ |
| Guillemets français (`\og`/`\fg`) | 47, aucun guillemet droit imprimé | ✔ |
| « je » / « nous » / « on » | 2 occurrences, **toutes deux légitimes** | ✔ |
| Phrases de plus de 60 mots | 45 relevées, dont **40 sont des artefacts de tableaux** que le filtre n'a pas su écarter | ✔ |

Les tournures les plus fréquentes sont « par ailleurs » (4), « au niveau de » (2), « dans le
cadre de » (1). À cette densité, il n'y a rien à corriger : le § 5.2 du référentiel demande un ton
impersonnel, et il est tenu.

**Cinq phrases longues sont réelles** et valent une relecture si le temps le permet :
`05_donnees_limites` (148 mots), `12b_adaptations_pilier` (116), `06_socle_mecaniste` (98),
`13b_donnee_manquante_livrable` (94), `13_inventaire_hypotheses` (84). Aucune n'est fautive, elles
sont seulement denses. *Coût : 30 min, facultatif.*

**Les deux « je » sont à leur place** : l'un dans une option de réponse citée du questionnaire
d'élicitation (« je ne peux pas trancher »), l'autre dans un titre du chapitre du stage, où la
première personne est assumée et documentée en tête de fichier.

---

## 2. Structure argumentative

### La conclusion porte les quatre éléments exigés

Le § 5.1.f attend un rappel de la problématique, les principaux résultats, les limites, et les
voies futures. Les quatre sont présents, et la conclusion fait **3 pages**, dans la fourchette de
2 à 3 que le référentiel donne.

Sa structure est plus forte que la structure attendue : « Ce qui est établi », « Ce qui est démontré
comme non mesurable », « Ce qui en découle pour le régulateur », « Ce qui en découle pour
l'entité », « Limites », « Ouvertures ». Séparer ce qui est établi de ce qui est démontré
**non mesurable** est exactement ce que le § 4.6 valorise.

### L'introduction : un écart de forme, pas de fond

Le § 5.1.d attend une introduction de 2 à 3 pages contenant un préambule, l'énoncé de la
problématique et les éléments différenciants. Le mémoire n'a pas de chapitre « Introduction » :
elle a été absorbée dans le chapitre 1, qui fait 15 pages.

**Ce n'est pas un défaut si les trois éléments sont dans les premières pages.** À vérifier à la
lecture, ce que je n'ai pas fait ligne à ligne. Si la problématique n'apparaît qu'en section 1.4,
un juré peut trouver l'entrée en matière longue. *À contrôler toi-même : les trois premières pages
du chapitre 1 posent-elles la question de recherche ?*

### Une question ouverte sur le chapitre du stage

`19_enseignements_stage.tex` porte en tête : « le barème de l'école note sur 6 l'analyse et la
réflexion sur le contexte et les outils ». Or tu m'as indiqué qu'il **n'existe pas de consignes
d'école distinctes**, et que le seul référentiel est celui de l'Institut.

Deux lectures possibles, et je ne peux pas trancher à ta place :

- **Le barème ENSAE existe** et tu le connais par un autre canal. Alors le chapitre, qui fait
  **4 pages sur 204**, est sous-dimensionné pour 6 points sur 20, et c'est le poste au plus fort
  rendement du dossier.
- **Il n'existe pas.** Alors ce chapitre n'est requis par rien : l'Institut ne le demande nulle
  part dans les Recommandations Jury. Il ne nuit pas, mais il ne rapporte rien non plus, et la
  phrase de son en-tête est à corriger car elle invoque un référentiel inexistant.

**Ce point doit être tranché avant le dépôt.** Dans les deux cas, l'en-tête du fichier est à
mettre à jour.

---

## 3. Les corrections appliquées

Tout ce qui suit est **fait, compilé et vérifié**.

### Exposition des meilleurs résultats

| Correction | Où | Effet |
|---|---|---|
| **Bornes de capital portées dans le résumé et la conclusion** | `01_resume`, `14_conclusion` | 6 858 – 8 697 M€ et la largeur de 1 839 M€ apparaissent désormais là où un juré pressé les lira. Elles n'existaient que dans la note de synthèse |
| **Valeur d'information portée dans le résumé et la conclusion** | idem | Les 66 % et les 28,9 % sortent des trois pages du chapitre 13b. La conclusion énonce maintenant qu'un superviseur qui ne pourrait exiger qu'un champ sait lequel demander |
| **Seuil de bascule du classement publié** | `12_resultats` | Le classement tient jusqu'à une dégradation d'un quart de l'émission de P1 et bascule à la moitié ; le niveau ne perd que 24,8 % même à dégradation totale, soit 0,81 fois la largeur de bande |
| **Écart de 14 139 M€ rétabli** | `14_conclusion` | Ses deux composantes y figuraient sans le total |

### Conformité

| Correction | Où | Effet |
|---|---|---|
| Résumé français resserré | `01_resume` | **547 → 287 mots** |
| Abstract anglais resserré | `01_resume` | **367 → 274 mots** |
| Lien Hackmageddon / faible influence | `05_donnees_limites` | La source la moins traçable est désormais explicitement reliée aux trois mesures qui établissent que la catégorie ne porte pas de segmentation |

### Technique

| Correction | Où | Effet |
|---|---|---|
| Deux figures étiquetées et appelées | `07_cascade_dirigee` | `fig:reseau-W` et `fig:branchement-R0`, dont celle qui vérifie la condition de stabilité |
| Deux tables de résultats appelées | `12_resultats` | `tab:delta` et `tab:benchmark-sf`, qui portent le chiffre central |
| `pymupdf` déclaré | `requirements.txt` | Le contrôle documenté des `??` est de nouveau exécutable depuis un poste neuf |

### Contrôles après corrections

| Contrôle | Avant | Après |
|---|---|---|
| Pages | 196 | **204** |
| Débordements par emplacement | 5 | **5**, ligne de base tenue |
| `Overfull \vbox` | 0 | **0** |
| `??` | 0 | **0** |
| Harnais | 1 824 / 1 824 | **1 839 / 1 839** |
| Hors contrôle non déclaré | 0 | **0** |
| Matériel complémentaire | — | **71 pages, 0 renvoi cassé**, régénéré |

---

## 4. Deux corrections à mon propre travail

**J'ai surévalué un constat de la Phase 4.** J'avais classé « critique » l'absence du seuil de
bascule du classement. En lisant le chapitre 12, j'ai trouvé qu'il portait **déjà** une réponse
quantitative, par un autre chemin : sur l'ensemble admissible, P1 arrive premier dans 43,6 % des
configurations, P4 dans 37,7 %, et l'écart de regret maximal n'est que de 1,5 %. La défense
existait. Ce que j'ai ajouté est l'angle complémentaire, celui du biais du corpus, qui répond à une
attaque différente. Le constat valait « majeure, complément », pas « critique ».

**Deux entrées de ma liste F9 étaient des faux positifs.** `fig:presence-taux` et
`fig:presence-effectifs` sont des étiquettes de sous-figures, dont la légende parente explique les
panneaux (a) et (b). C'est la pratique correcte, et elles n'ont pas à être appelées par `\ref`. La
liste des flottants réellement orphelins compte donc **15 entrées, pas 17**.

---

## 5. Ce qui reste, et pourquoi

| # | Action | Gravité | Pourquoi ce n'est pas fait |
|---|---|---|---|
| **F8** | Ajouter `url` et `urldate` à 17 sources en ligne | majeure | **Je ne peux pas inventer une adresse.** La règle 4 du prompt l'interdit, et une URL fausse est pire qu'une URL absente. La liste des 17 clés est dans `02_latex.md` |
| **F9** | Appeler les 13 flottants orphelins restants | majeure | Fait pour les 4 qui comptent (2 tables de résultats, 2 figures du modèle). Les 13 autres demandent de lire le texte autour de chacun |
| **F7** | Note de synthèse séparée FR + EN | majeure | Extraction mécanique, mais elle doit se faire **après** le gel du contenu, sinon elle divergera |
| **F3** | Recréer le maître Institut | critique | À faire après le dépôt école du 30 septembre, avant la soutenance |
| **F4** | Blocs de signature sur la page de garde | critique | Tu as demandé de la laisser de côté. **À relancer : le délai de signature de Hugo Rapior est externe** |
| — | Cinq phrases de plus de 80 mots | mineure | Facultatif |
| — | Trancher la question du barème ENSAE (§ 2) | — | Te revient |

**Les deux résumés restent à environ 10 % au-dessus des 250 mots** (287 et 274, mesurés sur le PDF
avec un peu de débord d'en-tête). Ils venaient de 547 et 367. Resserrer davantage coûterait du
contenu que je juge utile : les bornes et la valeur d'information viennent d'y entrer. À toi de
voir si tu veux les ramener sous la barre.
