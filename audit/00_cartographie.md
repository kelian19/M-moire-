# Phase 0 — Cartographie

Audit du mémoire ENSAE / Institut des Actuaires. Document audité : `exploratory/memoire_cascade/main_ensae.tex`.
Relevé du **21 septembre 2026**. Tout ce qui suit est **vérifié** (lu, compilé ou recalculé) sauf mention
explicite « supposé ».

---

## 1. Écarts entre le prompt d'audit et le dépôt réel

C'est la réalité du dépôt qui fait foi. Cinq écarts, dont un qui annule une règle de conduite.

| # | Ce que dit le prompt | Ce que dit le dépôt | Conséquence |
|---|---|---|---|
| E1 | « Le projet a **quatre versions** qui appellent les mêmes chapitres » | **Un seul fichier maître.** `main.tex`, `main_v2.tex` et `main.pdf` ont été supprimés le 19 septembre 2026 (commit et journal à l'appui) | **La règle de conduite n°2 est sans objet** : il n'y a pas trois autres versions à faire compiler. Le risque multi-versions a disparu, et avec lui la principale source d'incohérence que la Phase 4 devait couvrir |
| E2 | Méthodologie : « agrégation par **copule de Gumbel** » | L'abstract dit l'inverse : la dépendance passe par « a directed cascade **rather than an a posteriori copula** ». Un paramètre θ de copule de Gumbel existe bien dans la table des notations (p. 191), mais il n'est pas le mécanisme central | À reconstruire en Phase 3. Ne pas auditer le mémoire comme un modèle à copule |
| E3 | « quantification du **SCR** » | Le mémoire requalifie explicitement : « This is an **ORSA-type capital need, not a regulatory SCR**, since the Standard Formula has no DORA module » (p. 5) | C'est une **force**, pas un défaut : le mémoire borne sa propre prétention. À protéger en Phase 5 |
| E4 | Vigilance : « si l'indice de queue dépasse 1, moyenne infinie » | ξ = **0,5954**. Le texte écrit « la variance des pertes est infinie, leur espérance finie » (p. 15), ce qui est **exact** pour 1/2 < ξ < 1 | L'attaque anticipée par le prompt ne porte pas. L'énoncé du mémoire est correct |
| E5 | Annexes : risque de lettrage cassé après suppression de B, D, E | Lettrage **A à E contigu et correct** dans le PDF : A démonstrations (p. 159), B adaptations (p. 164), C élicitation (p. 177), D paramètres (p. 187), E notations (p. 189). Les « annexe B/D/E » résiduels sont **tous dans des commentaires LaTeX**, donc hors PDF | **Point de vigilance n°3 levé.** Vérifié page par page |

---

## 2. Fichiers maîtres et arborescence

**Fichier maître unique du mémoire** : `exploratory/memoire_cascade/main_ensae.tex` (8 905 octets).

Deux autres `.tex` portent un `\documentclass` et pourraient être confondus avec lui :

- `memoire/main.tex` — version abandonnée **pré-cascade**. `CLAUDE.md` dit « ne jamais y toucher ».
- `exploratory/rapport_ensae/rapport_ensae.tex` — ancien rapport raccourci, conservé comme **archive**.

Ni l'un ni l'autre ne partage les chapitres du mémoire. Aucun des deux ne doit entrer dans l'audit.

| Élément | Emplacement | Compte |
|---|---|---|
| Préambule partagé | `preambule_v2.tex` (appelé par `main_ensae`) | 1 |
| Préambule orphelin | `preambule.tex` — plus appelé | 1 |
| Page de garde déposée | `page_de_garde_ensae.tex` | 1 |
| Page de garde orpheline | `page_de_garde.tex` (couverture Institut, conservée) | 1 |
| Chapitres appelés | `chapitres/` | **22** |
| Chapitre orphelin | `chapitres/02_introduction.tex` — absorbé par `02b` | 1 |
| Bibliographie | `references.bib`, style `plainnat-fr.bst` | 75 entrées |
| Figures incluses | `figures_externes/` (8), `vasicek_lab/figures/` (6), autres (3) | **17** |
| Scripts Python | `exploratory/vasicek_lab/` | 128 |
| Sorties versionnées | `sorties_verif/` | 112 |
| Matériel déporté | `materiel_complementaire/` | 3 `.tex` + README |

**Harnais de vérification** : `verif_chiffres.py` (bibliothèque standard uniquement) et son lanceur
`verif_tous_chapitres.ps1`. Trouvé, lu, exécuté — résultats en section 5.

**Les consignes de l'école et le barème ne sont pas dans le dépôt.** Aucun fichier ne correspond.
Je ne les invente pas ; ce qu'il faut que tu vérifies est listé en section 7.

---

## 3. Structure réelle du PDF, pages par chapitre

**196 pages physiques**, dernier folio imprimé 195 (décalage d'une page, couverture non numérotée).

| Partie / chapitre | Pages | Nombre |
|---|---|---|
| Couverture, remerciements | 1–3 | 3 |
| Résumé, abstract, table des matières | 4–11 | 8 |
| Glossaire | 12–13 | 2 |
| Note de synthèse (FR) | 14–17 | 4 |
| Executive summary (EN) | 18–21 | 4 |
| **I — Contexte et problématique** | 22–45 | **24** |
| 1 Risque cyber, résilience numérique et besoin de capital | 23–37 | 15 |
| 2 Le cadre prudentiel et son articulation avec DORA | 38–40 | **3** |
| 3 État de l'art et positionnement | 41–45 | 5 |
| **II — Les données et leurs limites** | 46–67 | **22** |
| 4 Données et limites | 47–67 | 21 |
| **III — Modélisation** | 68–106 | **39** |
| 5 Le socle mécaniste : fréquence et sévérité | 69–78 | 10 |
| 6 La cascade dirigée | 79–87 | 9 |
| 7 La conformité multi-états | 88–94 | 7 |
| 8 L'identifiabilité de la contagion dirigée | 95–106 | 12 |
| **IV — Résultats** | 107–132 | **26** |
| 9 Identification partielle et bornes de capital | 108–113 | 6 |
| 10 Résultats | 114–132 | 19 |
| **V — Robustesse, limites et perspectives** | 133–151 | **19** |
| 11 Robustesse et incertitude du chiffre reporté | 134–145 | 12 |
| 12 La donnée manquante comme livrable | 146–148 | 3 |
| 13 Conclusion | 149–151 | 3 |
| **VI — Le stage** | 152–156 | **5** |
| 14 Enseignements du stage | 153–156 | **4** |
| **Annexes** | 157–191 | **35** |
| Notice d'organisation | 158 | 1 |
| A Démonstrations : le modèle de cascade | 159–163 | 5 |
| B Adaptations par pilier | 164–176 | 13 |
| C Le protocole d'élicitation, préparé et non exécuté | 177–186 | 10 |
| D Table des paramètres | 187–188 | 2 |
| E Table des notations | 189–191 | 3 |
| Bibliographie | 192–196 | 5 |

**Deux déséquilibres structurels à retenir pour la suite.**

1. **Le chapitre du stage fait 4 pages sur 196**, soit 2 % du document — alors que le barème de
   l'école le note **sur 6 points sur 20**. C'est le plus fort écart entre l'effort investi et le
   rendement en points de toute la structure. À instruire en priorité en Phase 5.
2. **Le chapitre 2 (cadre prudentiel) tient en 3 pages.** L'en-tête de `main_ensae.tex` demande de
   le réduire « à la seule articulation avec Solvabilité II » pour cause de doublon avec la
   section 1.4. La réduction **semble faite** (supposé : je n'ai pas encore lu le contenu), mais
   son label `chap:reglementaire` est cité par cinq chapitres — cohérence à vérifier en Phase 2.

---

## 4. Liens entre le texte et le code

Le rattachement se fait par des commentaires `% SOURCES-SCRIPTS: NN` posés section par section.

- **157 blocs** `SOURCES-SCRIPTS` répartis sur **18 des 22 chapitres**.
- **4 chapitres ne citent aucun script** : `00_glossaire`, `04_cadre_reglementaire`,
  `03_etat_art_positionnement`, `15b_demonstrations_cascade`. Tous **déclarés** hors script par
  `% HARNAIS-HORS-SCRIPT` ou `% HARNAIS-HORS-SECTION` — c'est légitime et contrôlé.

---

## 5. Compilation et harnais

**Compilé ce jour** avec tectonic 0.17.0 (installé pendant cette session ; le poste n'avait ni
LaTeX ni `.venv`). Exit 0.

| Contrôle | Résultat | Ligne de base |
|---|---|---|
| Pages | 196 | 196 ✔ |
| Débordements par emplacement | 5 | 5 ✔ |
| `Overfull \vbox` | 0 | 0 ✔ |
| `??` comptés sur le PDF | 0 | 0 ✔ |
| Pages tournées | 0 | 0 ✔ |
| Annotations hors page | 0 | 0 ✔ |

La version de tectonic a changé par rapport au poste d'origine **sans déplacer les lignes de base** :
196 pages et 5 débordements sont reproduits à l'identique. Les contrôles sont donc portables.

**Harnais, 22 chapitres** : **1 824 nombres vérifiables, 1 824 confirmés (100 %)**, **zéro hors
contrôle non déclaré**. Couverture 1 824 sur 1 889 publiés (96,6 %) ; les 65 nombres de l'écart sont
tous dans des sections déclarées hors script. Le critère de fin de tâche du projet (« couverture
100 % **ou** zéro hors contrôle non déclaré ») est satisfait par le second terme.

**Bibliographie** : 56 clés citées, **toutes résolues** (0 citation sans entrée). 19 entrées de
`references.bib` ne sont citées nulle part — sans effet sur le PDF avec `plainnat-fr`, simple
ménage.

**Git** : arbre propre, branche `exploratory` synchronisée avec l'origine. Rien en cours de
modification.

---

## 6. Marqueurs de travail restants

| Où | Marqueur | Statut |
|---|---|---|
| `main_ensae.tex:139` | `\url{https://LIEN_VERS_LE_DEPOT.com}` | **Placeholder vivant, imprimé p. 158 du PDF déposé.** Point de vigilance n°1 confirmé |
| `main_ensae.tex:47` | « les trois champs à trancher avant le dépôt » | À instruire en Phase 1 |
| `remerciements.tex:15` | « Le champ à compléter » | **Faux positif** : le champ est renseigné (`Ali~BEHBAHANI`). Le commentaire décrit le dispositif, pas un manque |
| `a_integrer/` | `A_parametres.tex`, `B_elicitation.tex` : « Annexe à compléter » | **Orphelins**, non appelés par `main_ensae`. Sans effet sur le PDF |
| `chapitres/*.tex` | `TODO`, `FIXME`, `XXX` | **Aucun** |

Aucun `\marginpar`, aucun `\textcolor` de relecture : les `\textcolor{navy}` trouvés sont des
éléments de mise en forme de la table des notations, neutralisés par le préambule.

---

## 7. Trois constats qui pèsent déjà, avant la Phase 1

### C1 — Le matériel complémentaire n'est pas en état d'être lu par un jury · **critique**

**Où** : `materiel_complementaire/`, annoncé p. 158 du PDF.

**Constat** : le dossier contient **trois fichiers `.tex` et un README**, pas un PDF. Son propre
README dit que « ces fichiers ne sont pas autonomes », qu'ils exigent un préambule, des figures
situées ailleurs et une bibliographie, et qu'un document compilé à part « imprimera des `??` sur
ces renvois ». La notice du mémoire promet pourtant au jury un matériel « consultable et
téléchargeable ».

**Risque devant le jury** : le mémoire déporte des démonstrations et des pièces justificatives vers
une ressource qui, en l'état, n'existe pas sous forme lisible. Un juré qui suit le lien et trouve
des sources LaTeX non compilables conclut que la promesse n'est pas tenue. Combiné au placeholder
`LIEN_VERS_LE_DEPOT.com`, c'est le défaut le plus coûteux du dossier.

**Correction** : compiler le mémoire entier avec les trois `\input` rétablis, extraire les pages
d'annexe du PDF obtenu (procédure décrite par le README lui-même), déposer ce PDF, insérer l'URL
réelle. **Coût : 2 à 3 heures**, dépendant de la création du dépôt Zenodo ou GitHub.

### C2 — Un comptage faux, et il est écrit à trois endroits différents · **majeure**

**Où** : `main_ensae.tex:122`, `materiel_complementaire/README.md:11` et `:38`.

**Constat** : trois comptes inconciliables des renvois remplacés par `\matcomp`.

| Source | Compte annoncé |
|---|---|
| `README.md:11` | « cinquante et un » |
| `README.md:38` | « 54 renvois » |
| **Compté ce jour dans `chapitres/`** | **48**, dont 3 dans `02_introduction.tex` qui est orphelin |
| **Donc dans le PDF déposé** | **45** |

Le README se contredit **à lui seul**, à 27 lignes d'intervalle.

**Risque devant le jury** : faible directement — ces fichiers ne sont pas déposés. Mais c'est
exactement le défaut que la note d'honnêteté de `CLAUDE.md` vient de documenter : un comptage qui
s'écrit au lieu de se calculer, que le harnais ne voit pas parce qu'il ne porte pas sur un nombre
publié.

**Correction** : recompter et réécrire les trois mentions ; le README doit aussi cesser d'annoncer
« 1 490 nombres » (le harnais est à 1 824) et de parler de `main.tex` et `main_v2.tex` comme de
fichiers existants. **Coût : 15 minutes.**

### C3 — Le chapitre noté sur 6 points fait 4 pages · **majeure**

**Où** : `chapitres/19_enseignements_stage.tex`, p. 153–156.

**Constat** : 4 pages de contenu pour un chapitre que le barème de l'école note sur 6 points sur 20.

**Risque devant le jury** : l'ENSAE lit un rapport de stage. Un recul personnel de 4 pages face à
130 pages de corps scientifique donne l'impression que l'exigence de l'école a été traitée en
dernier. C'est le poste où le rendement en points est le plus élevé du dossier.

**Correction** : à instruire en Phase 5, après lecture du contenu. **Coût : à chiffrer.**

---

## 8. Chiffres clés du mémoire, et leur page

Liste de travail pour la Phase 4 (rapprochement texte / code). Tous relevés sur le PDF.

| Grandeur | Valeur | Page |
|---|---|---|
| Besoin de capital, état conforme | 6 049 M€ | 5, 16 |
| Besoin de capital, état non conforme | 20 188 M€ | 5, 16 |
| Facteur entre les deux états | 3,34 | 5, 16 |
| Écart | 14 139 M€ | 5, 16 |
| Part des canaux isolés | 9 138 M€ | 5 |
| Part des interactions | 5 001 M€ (35 %) | 5 |
| Seuil POT | 20,03 M€ | 15 |
| Excès au-dessus du seuil | 91 | 15 |
| Indice de queue ξ | 0,5954 | 15 |
| Pertes OpRisk Global | 582 sur 27 ans | 15 |
| Notifications PRC | 15 053 (2019–2025) | 15 |
| Rapports post-incident / transitions codées | 10 / 22 | 15 |
| Sommets de l'ensemble admissible | 1 024 | 16 |
| Bornes de capital | 6 858 – 8 697 M€ | 16 |
| Largeur des bornes (coût de l'ignorance) | 1 839 M€ | 16 |
| Couverture du backtest, loi de fréquence | 91,7 % pour 90 % annoncé | 16 |
| Couverture du niveau de charge | 75,0 % | 16 |
| Dérive d'échelle dans la queue | 4,00 % par an | 16 |
| VERIS, incidents renseignant les deux champs | 1 sur 10 591 | 16 |

---

## 9. Ce que tu dois vérifier toi-même

Ces éléments ne sont pas dans le dépôt. Je ne les invente pas.

1. **Les consignes de l'école** et son **barème** (le chapitre 19 noté sur 6 en vient — source à
   confirmer). Sans eux, la Phase 1 ne peut pas statuer sur l'emplacement des notes de synthèse
   (point de vigilance n°2 : l'en-tête du fichier dit « en fin de document comme les consignes
   l'imposent », le corps les place en tête depuis le 16 septembre — **les deux ne peuvent pas être
   vrais**).
2. **La trace écrite de la levée de la limite de 30 pages** du 16 septembre. Le document fait
   196 pages : sans cette trace, le dépassement est indéfendable.
3. **L'existence et l'accessibilité du dépôt numérique** au 30 septembre (voir C1).
4. **La décision de confidentialité de Nexialog** : suffixe `_CONF` ou non.
