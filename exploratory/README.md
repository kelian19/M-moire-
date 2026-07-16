# Chantier exploratoire : risque cyber / DORA

Deux chantiers complémentaires sur la modélisation du risque des cinq piliers DORA
(Règlement UE 2022/2554). L'intuition commune : **l'ordre d'apparition des piliers
pilote le risque** (cascade dirigée, asymétrique). Le premier chantier l'établit
qualitativement, le second le formalise quantitativement puis le chiffre en euros.

```
exploratory/
├── cascade_qualitative/     Modèle qualitatif : l'ordre pilote proba/gravité/criticité
└── vasicek_lab/             Modèle quantitatif : Vasicek dirigé -> SCR euro par la cascade
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
**dirigée** `W`, seuil `K` **réglementaire + EVT** au lieu de `Phi^-1(PD)`. Le chantier
avance en quatre étapes : fondations du Vasicek dirigé (2.1), passage en unités
monétaires normalisées (2.4), dépendance de queue et allocation (2.5), puis chiffrage
en euros calibré sur l'entité et sur DORA (2.6).

### 2.1 Fondations : le Vasicek dirigé (01-06)

| Fichier | Rôle |
|---|---|
| `note_vasicek_dirige.tex/.pdf` | note pédagogique complète : concept → modèle → preuve → limites |
| `01_non_transitivite.py` | figure G1_non_transitivite : TRANS asymétrique à 81 % → pas une corrélation |
| `build_network_figure.py` | figure H1 : réseau dirigé `W` + sous-réseau d'exemple |
| `02_seuil_Ki_horserace.py` | figure J : banc d'essai `Phi^-1(PD)` vs EVT sur le capital |
| `03_calibration_W.py` | figures K1, K2, K3 : estimation probit de `W`, `R0`, progéniture |
| `04_seuil_Kj.py` | figure L : d'où vient le biais de `K_j`, et ce que l'EVT ne fait pas |
| `05_faisabilite_donnees.py` | figure M : **verdict de faisabilité** sur les deux sources réelles (détail en 2.3) |
| `06_facteur_systemique.py` | figure N : calibration de `Y_j`, `s_j`, `Sigma_Y` (routes A et B, détail en 2.2) |
| `synthese_methode_systemique.tex/.pdf` | synthèse : ancienne vs nouvelle méthode (5 p.) |
| `figures/` | G1_non_transitivite, H1, J, K1, K2, K3, L, M, N (PNG) |

`W` est une **matrice de parts**, normalisée comme la matrice technique de Leontief :

```
W = g · TRANS / max_j(somme de la ligne j),     g ∈ (0, 1]
```

`g` est la part de contagion du pilier le plus exposé, bornée par la décomposition de
variance de Vasicek (contagion + systémique + idiosyncratique = 1). Alors `rho(W) ≤ g < 1` :
**la stabilité est garantie, pas supposée**, exactement comme la valeur ajoutée positive
garantit `rho(A) < 1` chez Leontief. Sans cette normalisation, `rho(TRANS) = 1,461 > 1` et
`(I-W)^-1` a 21 entrées négatives sur 25 (une erreur de catégorie, pas de calibration).

La forme retardée est un **processus de branchement multitype**, dont l'extinction est
gouvernée par `R0 = rho(M)`, où `M` est la matrice de génération suivante (des incidents,
pas des écarts-types latents).

**Résultats clés.**
- La directionnalité (pas la non-transitivité) est ce qui casse Vasicek.
- Sur le domaine admissible `g ≤ 1`, les deux lectures sont stables (`rho(W) = 0,635 g`,
  `R0 ≤ 0,07`). Les seuils critiques sont dehors : `rho(W) = 1` à `g = 1,57`, `R0 = 1` à
  `g = 7,2`. La forme simultanée reste **structurellement alarmiste**, d'un facteur 5.
- La progéniture `(I-M)^-1` reproduit **exactement** le classement ROOT du modèle qualitatif
  (Spearman = 1,00), pour **toute** valeur de `g`, et validée contre une simulation directe
  du branchement. ROOT est donc **redondant** : il se déduit de TRANS. Cinq paramètres
  d'expert en moins.
- L'estimateur est un **probit**, pas un logit : le modèle générateur a un bruit gaussien et
  un seuil, donc c'est littéralement un probit. Le probit rend `W` dans ses propres unités
  (corrélation 0,92, pente 1,08, sens de l'asymétrie retrouvé à 100 %) ; le logit gonfle les
  magnitudes (pente 2,11).
- **La normalisation durcit la calibration, et c'est une information.** Le coefficient
  maximal de `W` tombe de 0,72 à 0,31 : le signal est trois fois plus faible. Il faut
  `N = 400` entités pour atteindre une corrélation de 0,90. La contagion admissible est
  faible, donc l'exigence en données est plus lourde que ne le laissait croire la version non
  normalisée.
- Tests de falsification : la permutation temporelle intra-entité effondre l'asymétrie
  (1,57 → 0,38) ; en temps inversé la corrélation devient −0,70 (le sens s'inverse bien).
- Sur le seuil : `K_j = F^-1(1 - p_j)` (on inverse **toujours** une répartition). C'est
  exactement ce que fait CreditMetrics (Morgan et coll., 1997), dont le seuil de migration
  vaut `L = Phi^-1(fréquence cumulée observée)`. Le biais de `K_j` vaut exactement le taux de
  sous-déclaration à la barre, `E[q(S) | S >= u_j]`, et s'effondre quand la barre monte
  (+0,369 à `u=0,5` ; +0,001 à `u=40`). **La barre DORA est défendable parce qu'elle est
  haute, pas parce qu'elle est réglementaire.** Tension à gérer : trop haut, `p_j → 0` et le
  seuil diverge (d'où l'écrêtage de la littérature, Engelmann 2021).
- Résultat négatif assumé : extrapoler le *taux* par EVT depuis un seuil haut vers la barre
  **n'est pas pilotable**. Le biais se décompose en un plancher de déclaration `E[q|S>v]`
  (qui tend vers 1) et une erreur de ratio (qui diverge). Un `v` optimal existe mais n'est
  pas localisable sans connaître la vérité. Le rôle de l'EVT reste la **sévérité** au-dessus
  de la barre, donc le capital : `-0,8 %` de biais contre `-63,9 %` pour la lognormale.
- La lognormale est **précise et fausse** (IQR 0,09, biais −64 %) ; l'EVT est **juste et
  imprécise** (IQR 0,62, biais −0,8 %). Avec `ξ = 0,9 > 0,5` la variance de la sévérité est
  infinie, donc le RMSE n'a plus de contenu : lire le biais médian et l'IQR.

### 2.2 Calibrer le systémique : `Y_j`, `s_j`, `Sigma_Y`

`06_facteur_systemique.py`. La généralisation A était **posée sans protocole d'estimation**.
Elle en a désormais deux, validés sur données simulées (`N = 1200`, `T = 70`).

| Route | Donnée requise | `corr(Y_est, Y_vrai)` | erreur `Sigma_Y` |
|---|---|---|---|
| A — effets fixes de période | panel individuel horodaté | **0,981** | 0,095 |
| B — distance de Frobenius | **comptages agrégés seuls** | **0,969** | 0,093 |

- Route A : les effets fixes du probit valent exactement `phi[j,t] = base_j + s_j·Y[j,t]`.
  Il n'y avait rien à estimer de plus, il suffisait de les **lire**.
- Route B : transposition de Pineau & Zuñiga (2023, éq. 5). Pour chaque période, on résout
  30 moments (25 co-incidences + 5 incidences marginales) pour 5 inconnues. **Aucun
  identifiant d'entité requis.**
- Les 5 moments **marginaux** sont indispensables. Sans eux (25 moments seuls), `corr(Y)`
  tombe à 0,835 et `s_j` double : les co-incidences ne portent que sur les ~6 % d'entités
  déjà touchées, et l'estimateur y absorbe le systémique **retardé** (résidu corrélé à +0,36
  avec `Y[t-1]`). Le fractionnement d'échantillon ne corrigeait rien, le biais était
  structurel, pas aléatoire.
- **Le verrou est plus étroit qu'annoncé.** `W` exige un panel individuel horodaté au mois
  (introuvable). `Y_j`, `s_j`, `Sigma_Y` s'obtiennent sur des **statistiques agrégées
  publiques** (exactement ce que publient les registres DORA, l'ENISA et les CERT). La
  généralisation A est calibrable dès aujourd'hui ; seule la généralisation B attend sa donnée.
- Réserves : tout est établi sur données simulées ; la route B suppose `W` connue ; et
  `Sigma_Y` est le maillon faible (corrélation vrai/estimé de seulement 0,67 sur les dix
  coefficients hors-diagonale, on retrouve le *niveau* des dépendances, pas leur *structure*).

### 2.3 Faisabilité empirique : `W` n'est calibrable sur aucune source disponible

`05_faisabilite_donnees.py` reproduit chaque chiffre. Les deux sources échouent pour des
raisons **opposées**, et c'est cette opposition qui fait la valeur du chapitre.

| Source | Pas temporel | Transitions | Verdict |
|---|---|---|---|
| Data Breach Chronology | trimestre | **89** | manque de volume et de taxonomie |
| SAS OpRisk (Bâle niv. 1) | année | **4 329** | volume suffisant, mais `z = -0,3` contre le placebo |

- La chronologie des brèches classe par **vecteur d'attaque**, pas par domaine de contrôle.
  `UNKN` pèse 53 %. La date de survenance manque de 2,6 % (`CARD`) à 89,4 % (`PHYS`), et le
  délai de déclaration va de 44 à 131 jours selon le type : la date piège des deux côtés.
- SAS OpRisk atteint enfin le volume requis (103 obs/cellule), mais l'asymétrie réelle (119)
  tombe **sous** le placebo par permutation (128 ± 27). Aucune des 18 paires n'est
  significative, la plus faible p-value valant 0,180. **Le pas annuel a lessivé la
  direction.** C'est la confirmation empirique, par l'échec, de l'argument d'identification.
- Ce que les données donnent : **`ξ ≈ 0,9`** sur 20 590 pertes en dollars, désormais utilisé
  par `02` et `04` à la place du `0,40` postulé. Fragile : retirer la seule erreur de saisie
  Citigroup 2024 (81 000 milliards, opération annulée) déplace `ξ` de 0,92 à 0,68 à `q99`.
- **Recommandation de conception :** un registre DORA doit horodater la **survenance** au mois
  ou à la semaine, et catégoriser par **domaine de contrôle**. Sinon la structure dirigée
  reste inidentifiable, quel que soit le volume collecté.

### 2.4 De l'ordinal à l'euro : SCR en unités normalisées (07-10)

`ossature_scr.tex` (« Ossature du SCR DORA ») pose les conventions de cette partie : de la
cascade qualitative à une charge de capital (severité, fréquence, agrégation, mesure de
risque).

| Fichier | Rôle |
|---|---|
| `severite_model.py` / `07_severite.py` | brique sévérité : corps lognormal + queue GPD par pilier ; le score GBASE fixe l'échelle, pas le montant ; figure S1_severite |
| `frequence_model.py` / `08_frequence.py` | brique fréquence : Poisson mélangé par un facteur systémique Y commun (surdispersion + co-occurrence) ; figure S2_frequence |
| `scr_engine.py` / `09_agregation_scr.py` | assemble fréquence x cascade x sévérité → perte annuelle → SCR (VaR 99,5 %, Solvabilité II art. 101) ; figure S3_agregation |
| `10_sensibilite_scr.py` | **le livrable** : le SCR n'est pas un nombre mais une surface SCR(g, xi) + tornado ; figure S4_sensibilite |

**Portée.** Unités normalisées (1 unité = perte médiane d'un incident sur le pilier le
moins grave), pas d'euros absolus à ce stade. Lecture d'honnêteté (10) : `g` (gain de
propagation) est calibrable **en principe** avec un registre horodaté, `xi` (indice de
queue) est importé de données externes et non calibrable sur l'entité, la VaR y étant
hypersensible au-delà de 0,9.

### 2.5 Copules et allocation d'Euler (11)

`11_copules_allocation.py`, figure S5_copules_allocation. Marges fixées par le modèle
mécaniste, seule la copule qui les relie varie (pas de double comptage avec le facteur
commun).

- SCR (VaR 99,5 %) par copule, marges identiques : indépendance 5070 (-12,9 % vs
  gaussienne), gaussienne 5822 (contrôle, ~ mécaniste), mécaniste réel 5606 (-3,7 % vs
  gaussienne), Student nu=4 6169 (+6,0 %, prime de dépendance de queue). Hiérarchie
  honnête : la structure de dépendance déplace le SCR dans une bande ~15-20 %, second
  ordre face à xi (x3).
- Allocation d'Euler du SCR mécaniste entre piliers (VaR-Euler et TVaR-Euler, sommes
  exactes) : au quantile réglementaire, le pilier le plus grave (P4) capte 47 % du
  capital (VaR-Euler) contre 43 % de la perte moyenne, la queue concentre le capital sur
  le pilier le plus lourd.

### 2.6 SCR en euros par la cascade : le chantier DORA (12-15)

`euro_cascade_model.py` est la source unique du moteur euro-cascade (importé par 12-15) :
il réutilise tels quels les modules du mémoire (sévérité GPD euro de
`src.aggregation.lda`, NegBin + multiplicateurs de scénario de `src.frequency.negbin`,
paramètres OpRisk/PRC de `src.utils.config`) et remplace uniquement l'agrégation par le
Vasicek dirigé de la cascade (noyau `e_j = g·s_j/max_s`).

| Fichier | Rôle |
|---|---|
| `12_scr_euro_cascade.py` | SCR en euros par la cascade, calibré comme le mémoire (OpRisk/PRC) ; figure S6_scr_euro_cascade |
| `13_delta_dora_cascade.py` | Delta_DORA (conforme vs non conforme) par bootstrap 2 niveaux, graine MC commune ; figure S7_delta_dora_cascade |
| `14_robustesse_delta_cascade.py` | robustesse du Delta_DORA + IC honnête à partir des exces réels (corrige l'IC trop large de 13) ; figure S8_robustesse_delta |
| `15_tornado_robustesse_cascade.py` | tornado de robustesse : sensibilité du Delta_DORA aux leviers non calibrés ; figure S9_tornado_robustesse |

Figures S1-S9 : préfixe dédié à ce chapitre (SCR chiffré, 07-15), numéroté sans trou et
distinct du préfixe G du chapitre 2.1 (G1_non_transitivite, seule figure en G de ce
chapitre-là).

**Résultats clés.**
- `g=0` (aucune propagation) retombe dans la bande du mémoire (contrôle : OpRisk 9275 M€
  vs 9260, PRC 2973 M€ vs 2773). La **prime de propagation** de la cascade (g=0,90) :
  +63 % (OpRisk), +86 % (PRC) sur une entité 15 000 M€.
- Delta_DORA bootstrap (entité 15 000 M€, canal fréquence g=0,90) : OpRisk médiane
  5552 M€ IC90 [1750 ; 42639] (mémoire : 3879 [1497 ; 22249]), PRC médiane 2865 M€ IC90
  [2436 ; 3558] (mémoire : 2015 [1607 ; 2366]). Même ordre et même structure d'IC que le
  mémoire, la propagation amplifie l'écart conforme/non conforme (~1,4x).
  Canal propre à la cascade (propagation contenue par la conformité) : +55 % de
  Delta_DORA en plus du canal fréquence.
- IC honnête (14) : bootstrapper `xi` sur les 91 excès réels (au lieu d'une normale non
  bornée) fait tomber le facteur IC90 de ~24 à 12,5 (comparable au mémoire, 14,9). L'IQR
  (écart typique) est resserré à un facteur 3,3 ; l'IC90 large est réel, pas un artefact.
  100 % des tirages donnent Delta_DORA > 0, robuste à `g_nc` dans [0,3 ; 1,0].
- Tornado (15) : le **seuil POT `u`** domine la sensibilité (fragilité EVT classique, du
  même ordre que la dominance de `xi` dans le mémoire) ; `lambda_ref` a un effet modéré ;
  le gain `g` et `phi` ont un effet faible. Toutes les variantes testées restent
  pluri-milliardaires et positives (min 4056, max 12944 M€).
- **Verdict robuste** : le niveau du capital n'est pas pinçable (queue lourde, 91 excès),
  mais le verdict (la non-conformité coûte, pluri-milliard, > 0) l'est sur tous les
  leviers testés, structurels et statistiques.

### 2.7 Conformité multi-états : SCR par état et Delta_DORA (16)

`16_scr_multi_etats_global.py`, figure S10_scr_multi_etats. Établit le SCR_DORA pour les
**trois états de conformité** de l'entité (Conforme, Partiellement conforme, Non conforme),
alignés sur les scénarios sources S0/S1/S2, au lieu des deux états de 13. État global
(tous piliers alignés), cas particulier du modèle par pilier à venir (16b). Décisions
validées : le Markov multi-états remplace la latente statique du mémoire ; l'état est par
pilier, mis en scène global d'abord.

Deux lectures, comme 13 : lecture A (fréquence seule, g constant, comparable au mémoire)
et lecture B (fréquence + propagation, g croît de C à NC). Résultats (entité type,
graine MC commune entre états) :
- échelle de SCR monotone C < PC < NC ; l'état intermédiaire PC est le nouvel apport.
- Delta_DORA bootstrap 2 niveaux **à méthode honnête** : la sévérité de queue OpRisk est
  ré-échantillonnée sur les 91 excès réels (méthode du 14), non tirée dans une approximation
  normale ; couvre les lectures A et B. Chiffres de tête (lecture B) : NC vs C OpRisk médiane
  7401 M€ IC90 [2830 ; 38793], PRC 3668 M€ IC90 [3201 ; 4094] ; PC vs C (chiffré pour la
  première fois) OpRisk 2556 M€ [963 ; 12768], PRC 1257 M€ [1077 ; 1466]. 100 % des tirages
  > 0 sur les 4 combinaisons. Même ordre que le mémoire (OpRisk 3879, PRC 2015), amplifié
  par la propagation de la cascade ; l'IC OpRisk reste large parce que la queue l'est.

`16b_scr_multi_etats_par_pilier.py`, figure S11_decomp_par_pilier. État de conformité
**par pilier** (chaque pilier dans son propre état), via `simulate_euro_pp` qui indexe les
trois canaux par pilier sans réécrire l'agrégation. Gain de propagation indexé sur le
pilier source. Deux résultats :
- cohérence : les configurations homogènes redonnent l'ordre du 16 (tous C 6085, tous NC
  17012 M€ OpRisk), contrôle du moteur par pilier.
- décomposition du Delta_DORA : basculer un seul pilier en Non conforme chiffre sa
  contribution. Classement OpRisk P1 (37 %) > P4 (28 %) > P2 (17 %) > P3 (11 %) > P5 (7 %),
  qui **reproduit le classement ROOT du modèle qualitatif** (validation croisée). Les
  contributions isolées ne somment pas au total (terme d'interaction) ; la mesure fiable de
  cette interaction et l'attribution principielle du surcoût sont l'objet des scripts 20/20b
  (le signe en VaR OpRisk est dans le bruit MC, la super-additivité est robuste en moyenne
  et sur PRC). Prépare la priorisation de remédiation (script 18) et l'allocation (20).

### 2.8 Markov et trajectoire SCR(t) : la dimension temps (17)

`17_markov_trajectoire_scr.py`, figure S12_trajectoire_scr. Empile une dynamique
markovienne sur le moteur du 16 (fast-slow) : une chaîne de Markov NC -> PC -> C (C
absorbant, séjours de type phase Erlang-2 pour une durée de projet réaliste, non
exponentielle) fait progresser l'état de conformité ; à chaque horizon t, la distribution
des états agrège les 3 SCR du 16 en SCR(t). Les taux de transition ne se calibrent pas
(DORA appliqué depuis 2025), ils sont ancrés sur des durées de projet types (~1,5 an par
transition) et présentés en sensibilité.

Le couplage se fait par le **même** facteur systémique Theta : un environnement dégradé
ralentit la remédiation (taux mu(Theta)) et durcit la cascade (SCR par état), ce qui
restaure la corrélation entre conformité et sinistralité et engendre la bande
d'incertitude. Résultat (OpRisk, départ marginale NC 35 / PC 35 / C 30) : SCR(t) décroît
de 10752 M€ (t=0) vers le SCR conforme 6925 M€, et le Delta_DORA(t) (surcoût résiduel de
non-conformité) tombe de 3827 à 116 M€ sur 5 ans. Bande 90 % large et persistante en haut :
dans un environnement dégradé, la remédiation traîne et le capital reste élevé plus
longtemps.

### 2.9 Priorisation de la remédiation (18)

`18_priorisation_remediation.py`, figure S13_priorisation. Sous budget contraint (un pilier
remédié à la fois), dans quel ordre remédier les 5 piliers pour minimiser le capital porté ?
Valeur d'accélération par pilier (différence finie, gain si remédié en premier : P1 2398,
P4 1637, P5 969, P3 699, P2 ~0 M€), puis énumération des 120 ordres pour l'ordre optimal.
Deux résultats forts :
- **l'ordre optimal coïncide avec l'ordre ROOT** du modèle qualitatif (P1 > P4 > P2 > P3 > P5) :
  la hiérarchie d'expert est la séquence de remédiation qui minimise le capital, retrouvée
  par une voie entièrement chiffrée.
- **l'ordre optimal diffère de l'ordre glouton** (par valeur immédiate) : à cause des
  interactions de cascade, remédier myopiquement le plus fort gain instantané n'est pas
  optimal. Écart pire/optimal : 21 % du capital intégré.
La cohérence est confirmée avec la décomposition Delta_k (16b) et l'allocation d'Euler (11,
qui remonte P4 en tête côté sévérité, vue complémentaire).

### 2.10 Robustesse du chantier multi-états (19)

`19_robustesse_multietats.py`, figure S14_robustesse_multietats. Teste si les verdicts
survivent à la perturbation des leviers non calibrés, en écho à la sensibilité globale du
modèle qualitatif. Tornado du Delta_DORA (base 8322 M€) : xi domine (3810 à 24474 M€,
facteur 6,4, comme le mémoire), les autres leviers sont modérés, et le Delta reste > 0
partout. La priorité P1 tient sur tous les réglages. Verdict, identique à celui du chantier
cascade : le classement est robuste, le niveau ne l'est pas (queue lourde). Point analytique :
l'ordre de remédiation optimal ne dépend que des SCR par configuration, donc il est
invariant aux taux de transition Markov (les moins calibrables) qui ne fixent que le
calendrier, pas la séquence recommandée.

### 2.11 Allocation du capital : Shapley et Euler en euros (20, 20b)

`20_allocation_shapley_euler.py`, figure S15_allocation_shapley_euler. Deux allocations
complémentaires sur le SCR_DORA multi-états (lecture C, protocole 16b, ~30 min).
- **Shapley du surcoût** : v(S) = SCR(S en NC, reste C) − SCR(tous C) sur les 2^5
  configurations (CRN), phi_j = moyenne des marginaux sur tous les ordres. Par efficience
  la somme des phi_j égale exactement le Delta total (10 927 M€ OpRisk, 4 957 PRC), là où
  les marginaux 16b ne somment pas (9 531). Parts OpRisk : P1 34 % > P4 26 % > P2 17 % >
  P3 14 % > P5 10 % ; classement == ROOT sur les deux périmètres. Anti-circularité : les
  amorces étant semées ∝ ROOT (30/27/18/15/9 %), le test non trivial est la déformation
  (P1 34 % > 30 % d'amorce, effet propre de la propagation), pas le classement brut.
- **Euler du niveau** (TVaR exacte, perte par pilier touché via `simulate_euro_pp(by_pillar)`) :
  PRC stable et presque plat (P2 23, P4 23, P1 20, P3 18, P5 17 %), capital ≈ moyenne car le
  cap tronque la queue (TVaR 6 795 ≈ VaR 6 573). OpRisk : parts moyennes stables, mais
  l'allocation de la queue extrême est non résoluble (xi ≈ 0,6 > 0,5 → variance de sévérité
  infinie, convergence en loi stable ; le classement conditionnel bascule entre 150k et
  240k années). Vue source (Shapley, P1) contre vue réceptacle (Euler, quasi uniforme).

`20b_robustesse_interaction.py` (un processus par graine, pas de figure). Tranche le signe
de l'interaction totale−somme des marginaux, en séparant VaR 99,5 % et perte moyenne sur les
mêmes simulations. Verdict : en VaR OpRisk le signe est dans le bruit MC (de −1,9 à
+2,1 Md€ selon la graine à 60k ; +117 M€ à 150k) ; la super-additivité est robuste en
perte moyenne (≈ +550 M€ OpRisk, +824 PRC, un cinquième du surcoût moyen, toutes graines)
et jusque dans la VaR du PRC plafonné (+800 M€ stable). Mécanisme : un pilier NC amplifie
aussi les cascades amorcées ailleurs qui le traversent. Conséquence : l'encadré du chapitre
résultats est formulé sur la moyenne et le PRC, pas sur la VaR OpRisk.

### 2.12 Résidu de la conversion Jacobs : l'IC PRC interrogé (21)

`21_prc_jacobs_residu.py`, figure S16_prc_jacobs_residu. La sévérité PRC est dérivée des
enregistrements compromis par la conversion log-log de Jacobs 2014 (ln L = 7,68 + 0,76 ln X),
un transport déterministe qui écrase la dispersion résiduelle de la régression d'origine
(RSE 0,523 en ln, R² 0,51, source primaire Data Driven Security : facteur de coût ~2,4 à
90 % autour de la droite). Le script réinjecte ce résidu par enregistrement dans le
bootstrap 2 niveaux, variantes ON/OFF à mêmes records rééchantillonnés et mêmes fréquences
(l'écart isole le résidu). Verdict contre-intuitif, rapporté tel quel : l'IC90 ne se rouvre
presque pas (facteur ~1,4 dans les deux variantes ; 15 053 enregistrements moyennent le
bruit dans le fit GPD, le cap 40 M€ borne la queue épaissie), mais le **niveau** monte de
7 % (médiane NC vs C 3600 → 3861 M€ ; xi dérivé 1,033 → 1,072 ; p_u 0,150 → 0,157).
L'étroitesse de l'IC PRC n'est donc pas un artefact de la conversion déterministe d'après
ce test. L'incertitude qui ne se moyenne pas est celle des coefficients (a, b), estimés sur
115 observations : à traiter en axe de sensibilité (à venir), pas en bruit par
enregistrement.

### 2.13 Sensibilités des hypothèses restantes (22)

`22_sensibilites_hypotheses.py`, figure S17_sensibilites_hypotheses. Complète le tornado
(19) et le résidu (21) par les trois entrées non calibrées restantes du chantier.
- **Coefficients Jacobs (a, b)** : b stressé à ±1,645 SE en pivotant la droite au centroïde
  de la régression, déduit des erreurs-types publiées (SE_a 0,7013, SE_b 0,0697, RSE 0,523,
  n 115 → x̄ = 10,04, ~23 000 enregistrements) ; stresser a et b indépendamment ignorerait
  leur corrélation négative. Recalibration complète en aval (u = P85, refit GPD) : xi dérivé
  0,846 → 1,214, Delta PRC 3125 → 3977 M€ autour du central 3577 (le cap borne l'effet).
  Axe d'hypothèse dominant du PRC ; la re-dérivation centrale retombe sur la calibration
  figée (écarts au 3e chiffre).
- **Gamma** (0,50 / 0,68 / 0,85) : SCR espéré normal invariant par construction (10 644 M€,
  la marginale redonne l'ancrage) ; gamma ne commande que la bascule en crise (P(NC|crise)
  84 → 100 %, SCR espéré crise 14 148 → 15 071 M€).
- **Ancrage NC/PC/C** (25/40/35 ; 35/35/30 ; 45/35/20) : déplace le capital espéré actuel
  (9951 → 11 485 M€) et le point de départ de la trajectoire (17), jamais le SCR par état
  ni le Delta NC vs C (conditionnels à l'état).
Verdict commun : les hypothèses bougent des niveaux, jamais la direction ni le classement.

### 2.14 Benchmark copule : la dépendance n'est pas le mécanisme (23)

`23_benchmark_copule.py`, figure S18_benchmark_copule. Referme la boucle avec le monde
copule que la cascade a remplacé, en confrontant la cascade à des jumeaux construits pour
lui ressembler (OpRisk, CRN, même U de copule entre configurations).
- **Photo** (marges par pilier identiques à la cascade, R calée Spearman → Pearson) : la
  gaussienne retombe sur le SCR de base (+0,1 %). En queue lourde (xi ~ 0,6) la queue
  annuelle est portée par la perte unique dominante : le niveau n'identifie pas la
  dépendance. La Student nu=4 le surestime de 17 % en forçant des co-extrêmes que le
  mécanisme ne produit pas (2,28 vs 1,12 piliers extrêmes par année de queue). Choix de
  copule non identifiable ET conséquent ; la cascade produit sa dépendance par mécanisme.
- **Intervention** (jumeau LDA-copule par pilier : canaux fréquence + détection dans les
  marges, copule figée) : trois manques structurels. Surcoût total 6760 M€ contre 10 927
  (−38 %, le canal propagation est inexprimable dans des marges) ; interaction moyenne
  exactement nulle par construction (+0 vs +560 M€ : l'interaction de la cascade est une
  signature falsifiable) ; priorité de remédiation inversée sur P2/P3, et la dépendance ne
  durcit pas avec la non-conformité, précisément le canal que DORA fait bouger.

## Deux pièges rencontrés, et gardés en mémoire

> **Le test du « temps inversé » est dégénéré** sur un comptage brut de transitions
> (`M_inv = Mᵀ` par construction, donc corrélation −1 toujours). Seul le **placebo par
> permutation** est valide. Le test garde son sens sur l'estimateur probit à effets fixes.

> **Une erreur d'indexation qui rendait le chiffre attendu.** Le panel est aplati *ligne par
> ligne* par `reshape(-1)`, donc les indicatrices de période s'assignent avec `np.tile`, pas
> `np.repeat`. Avec `repeat`, les effets fixes n'absorbaient **rien** : le systémique `s_j·Y`
> restait dans l'erreur, dont la variance passe de `1` à `1 + s²`, atténuant tous les
> coefficients probit du facteur `1/√(1+0,5²) = 0,894`. La pente rapportée valait 0,92 au lieu
> de 1 (un écart de 8 % vers le bas, **indiscernable d'un estimateur qui fonctionne**). Le bug
> n'a été démasqué que par la tâche suivante (extraire `Y_j` de ces mêmes effets fixes, qui
> rendait `corr(Y) = 0,05`). *Un estimateur qui rend le chiffre attendu n'est pas pour autant
> correct.*

## Portée commune du chantier 2.6

Même calibration euro et mêmes biais que le mémoire (OpRisk grandes entités ; PRC
sévérité Jacobs plafonnée 40 M€). Le canal propagation (`g_c`) est un choix de
modélisation non calibré, présenté en sensibilité. Rien n'est lu depuis `data/raw` sauf
mention contraire (14 relit les 91 excès locaux pour l'IC) ; aucun script de ce chantier
ne modifie `src/` ni `memoire/`.

## Compilation des PDF

Documents pdfLaTeX-standard, compilés avec Tectonic :
`tectonic -X compile <fichier>.tex --outdir <dossier>`. Le binaire vit dans `memoire/tectonic`
(non versionné). Les scripts Python demandent numpy, scipy, pandas, matplotlib, openpyxl,
scikit-learn et **statsmodels** (le probit). `ossature_scr.tex` n'a pas encore de PDF compilé
dans le dépôt.
