# Phase 2 — Audit technique LaTeX

Document audité : `main_ensae.pdf`, **202 pages**, compilé le 21 septembre 2026 avec tectonic 0.17.0.
Tout ce qui suit est **vérifié** : compilé, extrait du PDF ou recompté sur les sources. Ce qui n'a
pas été contrôlé est dit en fin de note.

**La robustesse multi-versions est sans objet** : `main_ensae.tex` est le seul fichier maître depuis
le 19 septembre. Aucune modification proposée ici ne peut casser une autre version.

---

## 1. Compilation : rien à signaler

| Contrôle | Résultat |
|---|---|
| Sortie du compilateur | exit 0, **0 erreur** |
| Références non définies (`??` comptés sur le PDF) | **0** |
| Citations non résolues | **0** |
| Étiquettes dupliquées | **0** |
| `Overfull \hbox` par emplacement | **5**, ligne de base du projet |
| `Overfull \vbox` | **0** |
| `Underfull \vbox` | **0** |
| Annotations hors page, pages tournées | **0** |

Le seul avertissement non couvert par les contrôles du projet est `Object @page.1 already defined`,
émis par le pilote PDF et sans effet sur le rendu. Les avertissements de police (`ntxexx`, `ntxsym`…)
sont des notices de chargement, pas des substitutions.

**139 `Underfull \hbox` subsistent.** Ils ne figurent pas dans les contrôles du projet et c'est
défendable : un *underfull* produit un espacement lâche, jamais un débordement dans la marge. À ce
stade du calendrier, ils ne valent pas une passe.

---

## 2. Bibliographie

| Contrôle | Résultat | Statut |
|---|---|---|
| Entrées dans `references.bib` | 75 | — |
| Clés citées | 56 | — |
| **Citations sans entrée** | **0** | ✔ |
| Entrées citées sans champ de fond (auteur, titre, année, revue) | **0** | ✔ |
| Entrées non citées | 19 | ⚠ mineure |
| **Rapports et sources en ligne cités sans adresse** | **17** | ✘ **majeure** |

### F8 — Dix-sept sources en ligne sont citées sans adresse ni date de consultation · **majeure**

**Où** : `references.bib`, entrées de type `misc` et `techreport`.

**Constat.** Dix-sept entrées **effectivement citées** dans le mémoire ne portent ni `url` ni
`howpublished`. Ce sont pour l'essentiel les rapports de marché et les sources institutionnelles
sur lesquelles repose le chapitre de contexte :

`amraeLucy2026`, `cesin2026`, `franceassureurs2026`, `enisa2025`, `marsh2025`, `dsit2025`,
`esas2026_incidents`, `ecb2024_outsourcing`, `jpmorgan1997`, `RapiorKaddouri2026`, `Dountio2026`,
`Decupere2011`, `Ranguin2024`, `tasche1999`, `KherLopezRapior2023`,
`BoumezouedCherkaouiHillairet2023`, `HillairetReveillacRosenbaum2021`.

**Risque devant le jury.** Le § 5.1.g du référentiel donne le format attendu pour une référence
prise sur un site : « Adresse complète du site, "de quoi il s'agit", date de consultation. » Et le
§ 4.2 prévient que « la qualité de la recherche bibliographique et le contenu de la bibliographie
**pourront être éliminatoires** s'ils sont jugés insuffisants », tout en rappelant que l'étudiant
doit pouvoir prouver qu'il a lu ses références. Un juré qui veut vérifier le chiffre de marché
LUCY ou le baromètre CESIN ne peut pas remonter à la source.

Le cas de `Dountio2026` est le plus exposé : c'est un mémoire d'actuariat, et le § 4.2 renvoie
explicitement au site de l'Institut où ces mémoires sont déposés. Un juré peut le connaître.

**Correction.** Ajouter `url` et `urldate` aux dix-sept entrées. Le travail est mécanique et
n'affecte aucun chiffre. **Coût : 1 h 30.**

### Entrées non citées · **mineure**

Dix-neuf entrées de `references.bib` ne sont citées nulle part. Avec `plainnat-fr` et BibTeX, elles
**ne s'impriment pas** : la bibliographie du PDF ne contient que les 56 entrées citées, ce qui
satisfait le § 4.2 (« toute référence indiquée dans la bibliographie doit être citée dans le
mémoire »). C'est donc du ménage de fichier, pas un défaut du document. À laisser si le temps
manque.

---

## 3. Figures et tableaux

48 flottants dans les chapitres compilés. **Aucun sans légende.**

### F9 — Dix-sept flottants ne sont jamais appelés dans le texte · **majeure**

**Où** : voir la table ci-dessous.

**Constat.** Dix-sept figures et tableaux portent une étiquette qui n'est **jamais** reprise par un
`\ref`. Vérifié : le mémoire n'emploie que `\ref` (327 fois) et `\eqref` (8 fois), aucune macro de
renvoi maison ne pourrait les masquer, et chacune de ces étiquettes n'apparaît qu'une seule fois
dans toutes les sources, à sa propre déclaration.

| Fichier | Étiquette |
|---|---|
| `02b_cadre_cyber_dora` | `fig:wannacry`, `fig:lucy-ratio`, `fig:lucy-divergence`, `fig:lucy-taille`, `fig:carto-retro`, `fig:cesin-vecteurs` |
| `05_donnees_limites` | `fig:presence-taux`, `fig:composition-temporelle` |
| `09_identifiabilite` | `fig:moveit` |
| `10_identification_partielle` | `fig:partielle` |
| `11_conformite_multietats` | `fig:invariance-g` |
| `12_resultats` | `tab:delta`, `tab:benchmark-sf` |
| `12b_adaptations_pilier` | `fig:interaction-canaux`, `fig:roi` |

**Risque devant le jury.** Le référentiel demande que chaque élément « puisse être compréhensible
sans avoir recours au corps du texte » — ce que les légendes de ce mémoire font bien. Mais
l'inverse n'est pas vrai : un flottant que le texte n'appelle jamais laisse le lecteur décider seul
du moment où le regarder, et LaTeX le place où il veut. Six des dix-sept sont dans le chapitre 1,
celui que le jury lit en premier. Deux sont des **tableaux de résultats** du chapitre 12,
`tab:delta` et `tab:benchmark-sf`, qui portent le chiffre central du mémoire : ne pas les annoncer
est un gâchis d'argumentation.

**Correction.** Insérer un renvoi dans la phrase qui traite du sujet. Aucune réécriture : une
parenthèse `(figure~\ref{...})` suffit, comme le chapitre 12 le fait déjà ailleurs. Traiter en
priorité les deux tableaux du chapitre 12 et les six figures du chapitre 1. **Coût : 1 h.**

### F10 — Deux figures sans étiquette, donc non citables · **mineure**

**Où** : `chapitres/07_cascade_dirigee.tex`, deux environnements `figure` sans `\label`.

1. « Structure dirigée de $W$ sur les cinq piliers (P1 émet fort et reçoit peu) et propagation… »
2. « (a) Sur le domaine admissible $g\le1$, les deux rayons spectraux restent $<1$ ; les seuils… »

**Constat.** Elles ont une légende mais aucune étiquette, donc le texte ne peut pas les appeler,
même s'il le voulait. La seconde illustre la **condition de stabilité** — le rayon spectral
inférieur à 1 — qui est l'une des trois propriétés démontrées du modèle. C'est une figure que le
jury voudra relier à sa démonstration.

**Correction.** Ajouter `\label{fig:...}` aux deux, puis les appeler. **Coût : 15 minutes.**

---

## 4. Typographie française

| Contrôle | Résultat | Statut |
|---|---|---|
| Guillemets français (`\og`/`\fg`) | 47 emplois | ✔ |
| Guillemets droits dans le texte imprimé | **0** (les 10 trouvés sont dans des commentaires) | ✔ |
| **Tirets cadratins** | **0** | ✔ **après correction, voir ci-dessous** |
| Tirets demi-cadratins | 0 | ✔ |
| Espaces insécables avant `: ; ? !` | gérés par babel français | ✔ |

### Une correction sur mon propre travail

Les six seuls tirets cadratins du dépôt se trouvaient dans l'annexe F que j'ai écrite au tour
précédent, en violation de la charte du projet. Ils sont supprimés, remplacés par des virgules, un
deux-points et une paire de parenthèses. Le mémoire lui-même n'en contenait aucun : la règle était
tenue avant mon intervention, et elle l'est de nouveau.

Le `\NoAutoSpacing` appliqué à la bibliographie est un choix délibéré et correct : il empêche
babel-français d'insérer des espaces fines devant la ponctuation des titres anglais. Le rendu de la
bibliographie a été relu sur le PDF, l'espacement français est conservé là où il doit l'être.

---

## 5. Un point du référentiel qui va à contre-courant du document

Le § 5.1.e conseille d'« **éviter les renvois systématiques** entre les paragraphes et les parties
ou chapitres qui perturbent inutilement la lecture et la compréhension ».

Le mémoire compte **327 `\ref`** sur 202 pages, soit environ un renvoi et demi par page, auxquels
s'ajoutent 45 `\matcomp` qui renvoient hors du document. C'est beaucoup, et c'est la conséquence
directe d'un texte qui refuse de se répéter.

Je ne recommande pas de les réduire : la densité de renvois est ici le prix de la traçabilité, et
la retirer coûterait plus qu'elle ne rapporterait à neuf jours du dépôt. Mais **c'est une remarque
que le jury peut faire**, et il vaut mieux avoir la réponse prête : chaque renvoi remplace une
redite, et le mémoire préfère renvoyer que paraphraser.

---

## 6. Ce que cette phase n'a pas contrôlé

À traiter en Phase 3, où le modèle sera reconstruit à partir des chapitres :

- **Cohérence des notations** sur tout le document, définition avant premier usage, et concordance
  entre le texte, la table des notations (annexe E) et la table des paramètres (annexe D). Ce
  contrôle demande de comprendre le modèle, pas seulement de compter des symboles.
- **Numérotation, alignement et ponctuation des équations**, et hypothèses posées avant usage.
- **Lisibilité des figures en noir et blanc**, et caractère vectoriel : les 17 illustrations sont
  des PNG, ce qui est un choix assumé du projet (elles sont produites par script et retaillées),
  mais leur résolution effective à l'impression n'a pas été mesurée ici.

---

## 7. Récapitulatif des actions de la Phase 2

| # | Action | Gravité | Coût |
|---|---|---|---|
| F8 | Ajouter `url` et `urldate` aux 17 sources en ligne citées | majeure | 1 h 30 |
| F9 | Appeler les 17 flottants orphelins, en commençant par `tab:delta` et `tab:benchmark-sf` | majeure | 1 h |
| F10 | Étiqueter et appeler les deux figures de `07_cascade_dirigee` | mineure | 15 min |
| — | Retirer les 19 entrées `.bib` non citées | mineure | 15 min, facultatif |

Total : **environ 3 heures**, dont 2 h 30 qui comptent.
