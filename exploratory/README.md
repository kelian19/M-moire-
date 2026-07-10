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
| `note_vasicek_dirige.tex/.pdf` | note pédagogique complète : concept → modèle → preuve → limites |
| `01_non_transitivite.py` | figure G1 : TRANS asymétrique à 81 % → pas une corrélation |
| `build_network_figure.py` | figure H1 : réseau dirigé `W` + sous-réseau d'exemple |
| `02_seuil_Ki_horserace.py` | figure J : banc d'essai `Phi^-1(PD)` vs EVT sur le capital |
| `03_calibration_W.py` | figures K1, K2, K3 : estimation probit de `W`, `R0`, progéniture |
| `04_seuil_Kj.py` | figure L : d'où vient le biais de `K_j`, et ce que l'EVT ne fait pas |
| `05_faisabilite_donnees.py` | figure M : **verdict de faisabilité** sur les deux sources réelles |
| `06_facteur_systemique.py` | figure N : calibration de `Y_j`, `s_j`, `Sigma_Y` (routes A et B) |
| `synthese_methode_systemique.tex/.pdf` | synthèse : ancienne vs nouvelle méthode (5 p.) |
| `figures/` | G1, H1, J, K1, K2, K3, L, M, N (PNG) |

**Le modèle retenu.** La contagion est **retardée sur incidents**, pas simultanée sur
latentes. Et `W` est une **matrice de parts**, normalisée comme la matrice technique de
Leontief :

```
W = g · TRANS / max_j(somme de la ligne j),     g ∈ (0, 1]
```

`g` est la part de contagion du pilier le plus exposé, bornée par la décomposition de
variance de Vasicek (contagion + systémique + idiosyncratique = 1). Alors `rho(W) ≤ g < 1` :
**la stabilité est garantie, pas supposée**, exactement comme la valeur ajoutée positive
garantit `rho(A) < 1` chez Leontief. Sans cette normalisation, `rho(TRANS) = 1,461 > 1` et
`(I-W)^-1` a 21 entrées négatives sur 25 — une erreur de catégorie, pas de calibration.

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
- Sur le seuil : `K_j = F^-1(1 - p_j)` — on inverse **toujours** une répartition. C'est
  exactement ce que fait CreditMetrics (Morgan et coll., 1997), dont le seuil de migration
  vaut `L = Phi^-1(fréquence cumulée observée)`. Le biais de `K_j` vaut exactement le taux de
  sous-déclaration à la barre, `E[q(S) | S >= u_j]`, et s'effondre quand la barre monte
  (+0,369 à `u=0,5` ; +0,001 à `u=40`). **La barre DORA est défendable parce qu'elle est
  haute, pas parce qu'elle est réglementaire.** Tension à gérer : trop haut, `p_j → 0` et le
  seuil diverge — d'où l'écrêtage de la littérature (Engelmann, 2021).
- Résultat négatif assumé : extrapoler le *taux* par EVT depuis un seuil haut vers la barre
  **n'est pas pilotable**. Le biais se décompose en un plancher de déclaration `E[q|S>v]`
  (qui tend vers 1) et une erreur de ratio (qui diverge). Un `v` optimal existe mais n'est
  pas localisable sans connaître la vérité. Le rôle de l'EVT reste la **sévérité** au-dessus
  de la barre, donc le capital : `-0,8 %` de biais contre `-63,9 %` pour la lognormale.
- La lognormale est **précise et fausse** (IQR 0,09, biais −64 %) ; l'EVT est **juste et
  imprécise** (IQR 0,62, biais −0,8 %). Avec `ξ = 0,9 > 0,5` la variance de la sévérité est
  infinie, donc le RMSE n'a plus de contenu : lire le biais médian et l'IQR.

## Calibrer le systémique : `Y_j`, `s_j`, `Sigma_Y`

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
  avec `Y[t-1]`). Le fractionnement d'échantillon ne corrigeait rien — le biais était
  structurel, pas aléatoire.
- **Le verrou est plus étroit qu'annoncé.** `W` exige un panel individuel horodaté au mois
  (introuvable). `Y_j`, `s_j`, `Sigma_Y` s'obtiennent sur des **statistiques agrégées
  publiques** — exactement ce que publient les registres DORA, l'ENISA et les CERT. La
  généralisation A est calibrable dès aujourd'hui ; seule la généralisation B attend sa donnée.
- Réserves : tout est établi sur données simulées ; la route B suppose `W` connue ; et
  `Sigma_Y` est le maillon faible (corrélation vrai/estimé de seulement 0,67 sur les dix
  coefficients hors-diagonale — on retrouve le *niveau* des dépendances, pas leur *structure*).

## Faisabilité empirique : `W` n'est calibrable sur aucune source disponible

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

## Deux pièges rencontrés, et gardés en mémoire

> **Le test du « temps inversé » est dégénéré** sur un comptage brut de transitions
> (`M_inv = Mᵀ` par construction, donc corrélation −1 toujours). Seul le **placebo par
> permutation** est valide. Le test garde son sens sur l'estimateur probit à effets fixes.

> **Une erreur d'indexation qui rendait le chiffre attendu.** Le panel est aplati *ligne par
> ligne* par `reshape(-1)`, donc les indicatrices de période s'assignent avec `np.tile`, pas
> `np.repeat`. Avec `repeat`, les effets fixes n'absorbaient **rien** : le systémique `s_j·Y`
> restait dans l'erreur, dont la variance passe de `1` à `1 + s²`, atténuant tous les
> coefficients probit du facteur `1/√(1+0,5²) = 0,894`. La pente rapportée valait 0,92 au lieu
> de 1 — un écart de 8 % vers le bas, **indiscernable d'un estimateur qui fonctionne**. Le bug
> n'a été démasqué que par la tâche suivante (extraire `Y_j` de ces mêmes effets fixes, qui
> rendait `corr(Y) = 0,05`). *Un estimateur qui rend le chiffre attendu n'est pas pour autant
> correct.*

## Compilation des PDF

Documents pdfLaTeX-standard, compilés avec Tectonic :
`tectonic -X compile <fichier>.tex --outdir <dossier>`. Le binaire vit dans `memoire/tectonic`
(non versionné). Les scripts Python demandent numpy, scipy, pandas, matplotlib, openpyxl,
scikit-learn et **statsmodels** (le probit).
