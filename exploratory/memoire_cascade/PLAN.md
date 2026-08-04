# Le mémoire : état réel et ce qui reste

Dernière mise à jour : 2026-08-04. **Le document est `main.tex`.** Corps 88 pages
(parties I à V), annexes A à E ensuite. Le corps a été ramené de 103 à 88 pages le 04/08 :
voir la section « Format » plus bas.

```powershell
cd exploratory\memoire_cascade
New-Item -ItemType Directory -Force -Path build | Out-Null
..\..\memoire\tectonic.exe -X compile main.tex --outdir build
```

## La thèse

Une défaillance de conformité ne reste pas dans son pilier DORA : elle se propage, **dans
un sens**, et ce sens change le capital. Le mémoire construit ce mécanisme, le traduit en
SCR, et démontre **jusqu'où la donnée permet d'aller** dans son estimation.

## Structure et statut

Document éclaté : `main.tex` (orchestre, 30 lignes) + `preambule.tex` + un fichier par
chapitre dans `chapitres/`.

| Fichier | Statut |
|---|---|
| `01_resume` | réécrit : mène sur la frontière d'identifiabilité et les bornes ; FR + abstract EN |
| `02_introduction` | réécrite : ouverture rédigée, le vide comblé, contribution en 3 points, encadré « ce que le mémoire ne prétend pas » |
| `03_etat_art_positionnement` | intégré ; reste à fusionner l'état de l'art de l'ancien mémoire |
| `04_cadre_reglementaire` | migré de l'ancien mémoire |
| `05_donnees_limites` | migré |
| `06_socle_mecaniste` | migré (EVT + calibration) |
| `07_cascade_dirigee` | rédigé 16/07 ; section faisabilité corrigée (temps inversé dégénéré) |
| ~~`08_proprietes_formelles`~~ | **supprimé le 04/08** : ses six propositions étaient déjà énoncées en `\S sec:formalisation` (ch. 6) et démontrées en annexe A. Ses vérifications numériques sont reprises en fin de `07_cascade_dirigee` |
| `09_identifiabilite` | neuf ; + event-study MOVEit (script 35) |
| `10_identification_partielle` | neuf, chapitre central ; + échelle u_ij (script 34) |
| `11_conformite_multietats` | rédigé 16/07, à relire |
| `12_resultats` | rédigé 16/07 ; cadrage corrigé ; chiffres vérifiés à 88 %, interaction corrigée |
| `13_inventaire_hypotheses` | intégré |
| `14_conclusion` | réécrite : établi / non mesurable / régulateur / limites / ouvertures |
| `15_demonstrations`, `16_notations` | migrés |

## Format : ce qui a été fait le 04/08

Le corps dépassait de 47 % la convention de l'Institut (~70 pages). Un mémoire qui
déborde contredit sa propre thèse, qui est une thèse de retenue. Corps ramené de **103 à
88 pages**, sans supprimer un seul résultat :

- **`08_proprietes_formelles` dissous.** Redondant à 100 % : ses six propositions sont
  énoncées en `\S sec:formalisation` (ch. 6) et démontrées en annexe A. Ses vérifications
  numériques (22/26 chaînes, rho = 0,506, écart 10,6-19,9 %, 1 173 M€) sont reprises en
  fin de `07_cascade_dirigee`. L'encadré qui admettait « le recouvrement est voulu »
  disparaît avec lui.
- **`12b_adaptations_pilier` passé en annexe C** (8 pages, 8 figures, zéro renvoi entrant).
  Un renvoi depuis le ch. Résultats dit ce qu'on y trouve et pourquoi c'est en annexe.
- **Annexe D `17_pieces_justificatives` créée** : réconciliation socle/conforme, résidu
  Jacobs, inventaire des paramètres, sensibilités hors tornado. Le corps garde le verdict
  d'une phrase et renvoie.
- **`titlespacing` du chapitre resserré** (l'espacement par défaut de `report` coûtait un
  quart de page par chapitre).

Reste ouvert si l'on veut descendre plus bas : le ch. Résultats pèse encore 16 pages et le
ch. Identifiabilité 12. Descendre à 70 imposerait de supprimer des résultats, pas de les
déplacer.

## Passe de prose : ce qui a été fait le 04/08

- **Tirets cadratins éliminés** (une soixantaine en prose, règle maison).
- **Gabarits d'encadrés cassés** : « ... et il faut le dire » (4 occurrences), « Ce que X
  établit » (4, dont 3 dans le seul ch. Résultats), « n'est pas un défaut » (2). Un même
  cadre rhétorique réemployé d'un chapitre à l'autre est le tic le plus visible du
  document.
- **Paragraphe fleuve du ch. 5** (NLP, 900 caractères d'une traite) scindé en deux.
- Faute corrigée : « l'ensemble de le chapitre ».

## Descente d'échelle : ce qui a été corrigé le 04/08

La table à trois échelles du chapitre Résultats avait deux défauts, corrigés par le
script `60_descente_echelle_entite`.

1. **Incohérence de taille.** Le SCR d'entité était calculé à lambda = 0,21, le taux des
   firmes à au moins dix événements, dont les actifs médians valent **19 fois** ceux de
   l'entité notionnelle. Ce seau est de surcroît défini par un filtre sur la grandeur même
   qu'on estime, donc biaisé vers le haut par construction. Lambda est désormais estimé
   comme une **fonction de la taille** (binomiale négative, log-lien, b_lambda = 0,074,
   z = 7,6) et lu à la taille cible : **0,092**.
2. **Correction mesurée mais non appliquée.** L'élasticité sévérité/taille du script 57
   n'était pas composée avec la descente de fréquence. Elle l'est : multiplicateur 0,854,
   homothétie exacte puisque la GPD est une famille d'échelle et qu'OpRisk n'est pas
   plafonnée.

**Conséquence à assumer : la coïncidence avec la Formule Standard ne survit pas.**
L'entité ressortait à 488 M€ contre une charge forfaitaire de 450 M€, et le mémoire y
lisait un écart refermé. La lecture cohérente donne **169 M€**, soit 0,38 fois le
forfait. La convergence venait du choix du seuil. Ce qui reste, et qui est le vrai
argument, c'est que le forfait vaut 450 M€ pour les trois états de conformité quand le
modèle les écarte de 116 à 169 M€.

Résultat d'entité publiable : socle 78,1 M€, bande **[131,5 ; 183,3]** M€ sur les 1 024
sommets, point d'expert 169 M€. La bande d'identification (51,7 M€) et la bande de
paramètre sur xi (51,5 M€) sont **du même ordre**.

Répercuté dans le corps : `05_donnees_limites` (table des trois fréquences),
`12_resultats` (table d'échelle, section ancrage, section détenir/transférer entièrement
rechiffrée), `14_conclusion`. Scripts 58 et 60 alignés sur la même graine et le même
nombre d'années.

## Ce qui reste, par ordre de rentabilité

1. **Relire les ~1100 lignes migrées.** Deux audits automatiques (mots-clés de l'ancien
   modèle, puis numérotation de l'ancien document), pas une lecture. Une phrase périmée
   sans aucun de ces motifs passerait au travers.
2. **Compléter le chapitre Résultats** avec le benchmark Formule Standard (0/62/100 % de
   l'effet DORA) et le test VCDB des sous-piliers. Les tableaux actuels restent valides.
3. **Basculer les références du chapitre positionnement dans `references.bib`.** La
   bibliographie ne compte que 4 entrées (les seules en `\citep`, venues de l'EVT) ; les
   ~14 références cyber y sont en liste texte.
4. **Retirer les 4 encadrés `[À migrer]` restants** (renvois « voir aussi » vers les notes
   de travail) avant toute diffusion : bénins mais visibles en orange dans le PDF.
5. **Mener les séances d'élicitation.** Le chapitre 10 démontre qu'elles ne servent qu'à
   départager P1 et P4 et à resserrer la bande ; tant qu'elles ne sont pas faites, la
   couche bayésienne tourne sur le classeur qualitatif.

## Contrôle qualité

`verif_chiffres.py` confronte chaque nombre publié dans un chapitre aux sorties des
scripts que la section cite, et signale ceux qu'il ne retrouve pas.

**Il n'avait jamais été exécuté** avant le 4 août 2026, faute d'un dossier de sorties.
Mode d'emploi, à faire avant toute diffusion :

```powershell
# 1. produire les sorties des scripts cités par le chapitre, une par fichier NN.txt
$out = "..\..\sorties" ; New-Item -ItemType Directory -Force $out | Out-Null
cd ..\vasicek_lab
..\..\.venv\Scripts\python.exe 9_cas_usage\58_detenir_ou_transferer.py  *> "$out\58.txt"
..\..\.venv\Scripts\python.exe 2_donnees\60_descente_echelle_entite.py *> "$out\60.txt"
# ... un par script cité
# 2. confronter
cd ..\memoire_cascade
..\..\.venv\Scripts\python.exe verif_chiffres.py $out chapitres\12_resultats.tex
```

**Premier passage, 4 août 2026, chapitre Résultats : 129 nombres vérifiables,
111 confirmés (86 %).** Les non confirmés sont des arrondis de rédaction, des nombres
appartenant à une autre section, et des **ratios dérivés à la main**. Cette dernière
catégorie est la seule dangereuse : elle a été supprimée en faisant imprimer les ratios
par le script 60 lui-même. Règle à tenir : **tout rapport cité dans le texte doit être
imprimé par un script**, jamais calculé pendant la rédaction.

Neuf sections du chapitre ne citent aucun script et ne sont donc pas vérifiables
automatiquement (Shapley et Euler, trajectoire, priorisation, robustesse, benchmark
copule, mise en regard réglementaire). C'est le trou restant du dispositif.

## Règles de rédaction

Pas de littéraux `«` `»` `§` (glyphes faux sous Tectonic) : `\og … \fg{}` et `\S`. L'euro
s'écrit `\euro{}`. Pas de tirets cadratins. **`W` n'est jamais présenté comme calibré**, et
le niveau absolu du SCR est toujours cadré comme illustratif (démontré au chapitre 10).
