# Reprise de session

## Comment lire ce fichier, et la convention qui le gouverne

**`CLAUDE.md` fait foi sur le fond.** Ce fichier ne le remplace pas. Il donne l'état daté du
projet, ce que dit le mémoire, comment le code est fait, les points ouverts, et un journal des
journées de travail.

**CONVENTION, POSÉE PAR KÉLIAN LE 9 SEPTEMBRE 2026 : ce fichier se met à jour À CHAQUE FIN DE
JOURNÉE DE TRAVAIL.** Une entrée datée s'ajoute **en tête du journal**, en bas du fichier, la
plus récente en premier. Les sections d'état, elles, se **réécrivent** plutôt que de s'empiler :
un compte de pages périmé est pire qu'un compte absent.

À joindre à une nouvelle session **avec `CLAUDE.md`** si cette session n'a pas accès au dépôt. Si
elle y a accès, `CLAUDE.md` se charge tout seul et ce fichier suffit comme complément.

**Les comptes de ce fichier se périment en deux jours.** En cas de doute, recompter sur le PDF et
relire `main.toc`, jamais se fier à une ligne écrite ici.

---

## Le projet en dix lignes

- **Kélian Kaddouri**, ENSAE Paris 3A, stage chez **Nexialog Consulting**, département R&D.
- Mémoire d'actuariat : *Quantification du SCR lié à la non-conformité au règlement DORA, une
  cascade dirigée entre les cinq piliers*. Objectif affiché : le **Prix SCOR**, donc le top
  national et pas la simple validation.
- **Hugo Rapior**, maître de stage. **Caroline Hillairet**, tutrice académique. Stage du
  **1er juin au 27 novembre 2026**. Point d'avancement hebdomadaire.
- **LE DÉPÔT EST LE 30 SEPTEMBRE 2026**, soutenance en novembre. Il reste **trois semaines**.
  Toute décision qui invoque le temps restant doit se relire à cette aune.
- **DEUX DOCUMENTS À RENDRE.** Le mémoire d'actuariat, dans `exploratory/memoire_cascade/`, en
  **deux versions de style qui partagent leurs chapitres**. Et le **rapport de stage ENSAE**, dans
  `exploratory/rapport_ensae/`, document **distinct** aux consignes propres.
- **Voie actuariat** : les consignes de l'école disent que le mémoire d'actuariat **tient lieu de
  rapport de stage** et que la soutenance est **organisée par l'Institut des Actuaires**, avec un
  jury à double validation ENSAE et Institut. Le rapport ENSAE est produit **en plus**, sur
  décision de Kélian, et les deux ne se confondent pas.
- Branche de travail : **`exploratory`**. `main` n'est pas la branche de travail.

---

## L'état mesuré, au 9 septembre 2026 au soir

| Document | Total | Corps | Débordements | Harnais |
|---|---|---|---|---|
| `main.pdf`, version 1 | 186 pages | 136, annexes en 137 | 15, ligne de base | voir ci-dessous |
| `main_v2.pdf`, version 2 | 192 pages | 140, annexes en 141 | 6, ligne de base | mêmes chapitres |
| `rapport_ensae.pdf` | 52 pages | 36, références comprises | 0 | 373 confirmés sur 373 |

**Harnais du mémoire : 2 346 nombres, 2 346 confirmés, 100 %**, et **0 hors contrôle non déclaré
sur les dix-neuf chapitres**. Chapitre 02 à 100 % sur 204 nombres, couverture 100 %.

**Harnais du rapport ENSAE : 373 nombres sous contrôle sur 399 publiés**, soit 93,5 % de
couverture, **373 confirmés sur 373**, et **26 déclarés hors script** avec leur motif, donc
**0 hors contrôle non déclaré**. C'est ce dernier chiffre qui est l'indicateur, pas la couverture
brute : un document qui déclare légitimement des nombres hors script affiche une couverture sous
100 % sans que rien n'aille mal.

**Contrôles au vert sur les trois PDF** : 0 `??`, 0 `Overfull \vbox`, 0 annotation hors page,
0 page tournée. Arbre git propre.

**Le corps du rapport ENSAE est à 36 pages pour une cible d'environ 30.** C'est 20 % au-dessus, et
c'est un arbitrage assumé : ce qui pouvait partir est déjà en annexe, et les annexes ne comptent
pas dans les 30 pages. Si Kélian veut descendre, les deux blocs les moins coûteux à déplacer sont
**la trajectoire et la durée de non-conformité**, et **la mise en regard des cadres existants**.

---

## Le mémoire : ce qu'il dit

### La question et le fil

**Comment traduire un niveau de non-conformité à DORA en une distribution de pertes puis en une
charge de capital ?** Le mémoire ne demande pas si une entité est conforme aujourd'hui, mais
**combien coûte en capital de ne pas se conformer**.

Le vide qu'il comble : aucun dispositif prudentiel ne traduit le niveau de maîtrise DORA en
capital. La Formule Standard charge le risque opérationnel au forfait, donc elle est **aveugle** à
la conformité. Une copule capture la co-occurrence des pertes mais **symétriquement** : elle ne
distingue pas une défaillance qui entraîne les autres d'une défaillance qui les subit. Or c'est
cette asymétrie, la **direction**, qui devrait commander la priorité de remédiation.

### Les trois apports

1. **Un mécanisme** de dépendance dirigée et sensible à l'ordre entre les cinq piliers, la
   cascade, dont trois propriétés sont **démontrées** : la criticité dépend de l'ordre de la
   chaîne et non du seul ensemble des piliers touchés, ce qu'aucune dépendance symétrique ne
   reproduit ; la normalisation de Leontief borne la propagation ; et **une matrice et sa
   transposée, indistinguables pour la donnée, donnent un capital et une décision différents**.
2. **Une frontière d'identifiabilité**, démontrée puis muée en méthode. La matrice se décompose en
   une partie symétrique et une partie antisymétrique, `W = S + A` : la donnée identifie `S`, la
   co-occurrence, et **pas** `A`, la direction. Plutôt que de poser la direction, le mémoire
   **borne** le capital sur l'ensemble des matrices admissibles, par énumération exhaustive des
   **1 024** sommets, et chiffre en euros ce que la donnée manquante coûte.
3. **Une lecture décisionnelle** : le surcoût, son attribution par pilier et par canal, et l'ordre
   de remédiation, présentés en **rapports et en bornes** plutôt qu'en niveaux.

### Le chiffre de tête, tranché le 17 août et non rouvrable

**Le besoin de capital passe de 6 049 à 20 188 M€ entre l'état conforme et l'état non conforme,
soit un facteur 3,34 et un écart de 14 139 M€.**

Quatre protocoles chiffraient « l'écart entre conforme et non conforme » et donnaient quatre
résultats, parce qu'ils ne relâchent pas le même nombre de canaux. Le motif du choix est que la
lecture à quatre canaux est la **seule où l'état conforme est conforme sur tous les canaux du
modèle**. Les trois autres restent publiées comme des remédiations partielles, et leur emboîtement
est un résultat. **Ne pas rouvrir, ne pas remplacer un de ces chiffres par un autre.**

**La non-conformité n'ajoute aucune pénalité au capital : elle déplace quatre paramètres de la loi
de perte.** Fréquence de 21,6 à 53,6 sinistres par an, taux de dépassement de 0,128 à 0,181, gain
de propagation de 0,45 à 0,90, charge de facteur commun tiers de 0 à 0,68.

**Les canaux ne s'additionnent pas.** Pris isolément ils somment à 9 138 M€ quand l'écart total
vaut 14 139 : il manque **5 001 M€, soit 35 %**, la cascade étant super-additive sur ses canaux.
Trois lectures d'un même canal existent et ne sont pas interchangeables, isolée, fermeture et
Shapley, et c'est **la colonne de fermeture** qu'un plan de remédiation doit citer, parce qu'un
canal ferme aussi les croisés qu'il portait.

### Ce qui est démontré, ce qui est mesuré, ce qui est posé

Cette distinction est le fil du document et il ne faut pas l'aplatir.

- **Démontré** : les trois propriétés de la cascade, la frontière d'identifiabilité, l'identité de
  la colonne de fermeture, la monotonie du capital en le gain de propagation, la borne basse du
  facteur d'agrégation.
- **Mesuré** : le facteur 3,34 et l'écart, l'interaction de 5 001 M€ et son signe, la
  quasi-additivité en fonction des piliers (R carré 0,9945), les élasticités, la dérive de
  sévérité, la loi exacte du nombre de piliers touchés par sinistre.
- **Posé, et déclaré comme tel** : les trois valeurs du gain de propagation, 0,45, 0,68 et 0,90.
  La thèse n'en dépend pas, le capital étant croissant en ce gain, donc **toute correspondance
  respectant l'ordre produit l'écart** quand le forfait reste plat. Seule l'amplitude est un
  scénario.
- **Hypothèse de construction non testée, et c'est la plus lourde** : l'**additivité des coûts**
  au sein d'un sinistre. Relâchée par un exposant, elle déplace l'écart de 9 706 à 20 487 M€, soit
  76 % de l'écart publié. Ce qui tient sur toute la plage : le **signe et l'ordre**. Ce qui ne se
  déclare pas : le **sens** de l'effet.

### Les limites déclarées, qui font la valeur du document

Le mémoire vaut environ 17 sur 20 en évaluation interne, et ce qui le tient est qu'**il publie ses
propres limites**. La non-transitivité qui lui donnait son titre a été **réfutée par son auteur**
et remplacée par la dépendance à l'ordre. Le chiffre central d'entité a été **requalifié en borne
supérieure** d'ordre de grandeur. La borne inférieure de validité de la descente d'échelle est
publiée. Le harnais signale ce qu'il ne peut pas confirmer.

**Ne pas défaire cela.** Toute reformulation qui rend une réserve moins visible dégrade le
travail, même si elle le fait paraître plus assuré. Les grandeurs simulées se publient **avec leur
bruit** : une posture citée à 1 247 plus ou moins 24 est plus utile qu'à 1 247, et retirer le plus
ou moins pour faire plus net est exactement la dégradation contre laquelle cette section met en
garde.

### Le plan, et la règle qui le gouverne

Cinq parties, conformes aux recommandations de l'Institut. **La règle : aucun niveau de capital
agrégé n'apparaît avant la partie IV.** Les parties II et III établissent la donnée, le modèle et
ce qui est identifiable, et n'énoncent que des écarts relatifs.

| Partie | Chapitres |
|---|---|
| I. Contexte et problématique | `02_introduction`, `04_cadre_reglementaire`, `03_etat_art_positionnement` |
| II. Les données et leurs limites | `05_donnees_limites` |
| III. Modélisation | `06_socle_mecaniste`, `07_cascade_dirigee`, `11_conformite_multietats`, `09_identifiabilite` |
| IV. Résultats | `10_identification_partielle`, `12_resultats` |
| V. Robustesse, limites, perspectives | `13_inventaire_hypotheses`, `13b_donnee_manquante_livrable`, `14_conclusion` |
| Annexes | `15b_demonstrations_cascade`, `15_demonstrations`, `12b_adaptations_pilier`, `17_pieces_justificatives`, `18_elicitation_protocole`, `16_notations` |

**Le nom d'un fichier ne dit pas sa partie** : `12b_adaptations_pilier` est l'**annexe C**, pas un
chapitre du corps. Vérifier avant de conclure qu'un ajout grossit le corps.

**Les deux versions partagent leurs chapitres.** `main.tex` et `main_v2.tex` ne diffèrent que par
la ligne du préambule et, depuis le 9 septembre, par l'absence d'un `\addcontentsline` dans la v2.
**Ne jamais dupliquer un chapitre pour faire évoluer une version.**

---

## Le code : comment c'est fait

### L'arborescence

| Quoi | Où |
|---|---|
| **Source de vérité unique des constantes** | `src/utils/config.py` |
| Bibliothèque de modélisation | `src/` : `severity/`, `frequency/`, `aggregation/`, `compliance/`, `scenarios/`, `visualization/` |
| **Scripts de calcul numérotés** | `exploratory/vasicek_lab/<N>_<theme>/<num>_<nom>.py` |
| Modules partagés des scripts | `exploratory/vasicek_lab/*.py`, à la racine du dossier |
| Figures produites | `exploratory/vasicek_lab/figures/*.png` |
| **Sorties versionnées des scripts** | `sorties_verif/NN.txt` plus son `README.md` |
| Harnais de vérification | `exploratory/memoire_cascade/verif_chiffres.py` |
| Palette et style de figures | `exploratory/vasicek_lab/style_nexialog.py` |
| Données brutes | `data/raw/` : **gitignoré, sous licence, ne jamais committer** |

Les neuf dossiers de scripts, environ 105 scripts au total : `1_fondations` (18),
`2_donnees` (15), `3_marges` (3), `4_scr` (9), `5_etats` (23), `6_contagion` (24),
`7_elicitation` (2), `8_benchmarks` (3), `9_cas_usage` (9).

Le dossier `exploratory/memoire_cascade/a_integrer/` est **mort** : aucun `\input` ne le lit.

### Les modules partagés, et ce que chacun porte

- **`canaux_conformite.py`** : le moteur des quatre canaux, lu par les scripts 43, 50 et 68. **Le
  modifier déplace les 14 139 M€.**
- **`scr_engine.py`**, **`euro_cascade_model.py`** : le calcul du capital. Le second lit
  `config.py`, donc toucher `config.py` déplace tous les capitaux.
- **`severite_model.py`**, **`frequence_model.py`** : les deux marges.
- **`partial_id.py`** : l'identification partielle et l'évaluateur à nombres aléatoires communs.
- **`descente.py`** : le panel de risque opérationnel et les élasticités, lu par 60 et 65.
- **`postmortem_corpus.py`** : le corpus de post-mortems, lu par 59 et 64.
- **`derive_severite.py`** : l'estimation de la dérive d'échelle, lue par 89 et 90, **qui ne
  peuvent donc pas s'écarter d'une décimale**.
- **`resultats_partages.py`**, **`style_nexialog.py`**.

### Le patron à suivre quand un script doit faire tourner le moteur avec un paramètre changé

**Ne pas modifier `canaux_conformite.py`, et ne pas le contourner par une substitution de ses
variables de module.** Recopier la fonction de pertes annuelles dans le script, **dans le même
ordre de tirages**, avec le paramètre rendu variable, puis **contrôler** que l'appel aux valeurs
publiées reproduit la sortie du moteur **tirage pour tirage**. C'est ce que font les scripts 81 et
90, et ce contrôle est ce qui empêche de démontrer une propriété d'un autre modèle.

### Les couleurs ne se codent pas en dur

`style_nexialog.py` est la **source unique**. On importe des **rôles**, `ENCRE`, `FOND`,
`CATEGORIEL`, `ORDINAL_5`, `SEQUENTIEL_6`, `DIVERGENT`, `ETAT`, **jamais un hexadécimal**. Trois
choses à savoir :

- **la charte porte trois emplacements catégoriels, pas quatre**, et c'est mesuré : un quatrième
  échoue le plancher de vision normale. Une quatrième série se replie en « autres », se facette,
  ou tire son identité de la position. La fonction de rampe **lève une erreur au lieu de boucler** ;
- **les cinq piliers ne sont pas un cas catégoriel** : ils se présentent ordonnés par
  contribution, donc rampe à une seule teinte ;
- **la déclaration de police reste DejaVu Sans en premier**, et c'est un écart assumé à la charte :
  matplotlib la fournit, donc une figure rejouée est identique à l'octet sur les deux postes.

### Le harnais, et ce qu'il ne fait pas

Il cherche chaque nombre publié dans un bloc du document parmi les sorties des scripts que ce bloc
cite en `\texttt{NN}`. Tolérance : le maximum de 0,6 % et de la demi-unité du dernier chiffre
écrit, c'est-à-dire la borne de l'arrondi d'écriture.

Il rend **trois lignes et pas une** : vérifiés, exemptés par motif, non confirmés. Une exemption
n'est jamais silencieuse, sinon le taux se mesure lui-même. Et une exemption se juge sur le
**contexte**, jamais sur la valeur.

**Une section sans script cité est hors contrôle**, et c'est plus dangereux qu'un non confirmé
parce que cela ne se voit pas dans le taux. **La couverture passe avant le taux**, dans cet ordre :
un taux de confirmation se règle en retirant une citation, la couverture non.

**Il ne vérifie pas** qu'un nombre est au bon endroit ni qu'il veut dire ce que la phrase prétend.
Un nombre confirmé peut être mal commenté.

**Il tourne aussi sur un fichier de slides et sur le rapport ENSAE**, et il faut s'en servir : le
deck du 14 août était à 35 % de couverture au premier passage, le rapport ENSAE à 7,5 %.

**Ne pas essayer de lui faire détecter les contradictions entre scripts.** L'idée a été instruite
le 10 août et écartée pour une raison, pas par manque de temps. Ce qui la remplace est une
convention plus efficace : **toute grandeur simulée se publie avec son bruit**.

### Les scripts qu'il faut connaître

La table complète est dans `CLAUDE.md` et elle compte une cinquantaine d'entrées. Les quinze qui
reviennent le plus :

| N° | Rôle |
|---|---|
| 07, 08b | calibration de la sévérité et de la fréquence |
| 43 | les quatre canaux, leur attribution, l'interaction, le facteur 3,34 |
| 68 | la table complète des seize configurations, les trois lectures, la décomposition de Möbius |
| 63 | la calibration figée rendue citable, plus les citations externes non recalculables |
| 67 | les grandeurs citées et jamais imprimées, et le **pont entre quantile unitaire et capital agrégé** |
| 65 | le besoin ORSA sur quatre bilans réels, et la borne inférieure de validité |
| 59, 53 | le corpus de post-mortems et la direction de la matrice |
| 64 | le biais de narration, mesuré au lieu d'être déclaré |
| 69, 94 | l'additivité en fonction des piliers, et le quantile de la loi des configurations |
| 74 | la loi exacte du nombre de piliers touchés, et les trois énoncés d'additivité distingués |
| 76 | le tornado **renormalisé**, en élasticités |
| 81 | l'ablation en échelle : la brique la plus lourde est la **queue**, pas la propagation |
| 88, 92 | la monotonie sur le pavé des canaux, puis le test de résistance **inversé** |
| 89, 91 | les deux backtests, marginal puis agrégé |
| 90 | ce que la dérive de sévérité fait à l'écart entre états |

**Deux scripts sont lents ou dépendants d'une machine.** Le 93 demande un quart d'heure, seize
mille ajustements : ne pas le relancer sans nécessité. Et **les deux postes ne portent pas le même
format de la chronologie de brèches** : le script 35 et le 08h ne tournent que sur le PC, le
script 05 que sur le Mac. Ne pas fabriquer un fichier depuis l'autre.

### La parité des deux machines

Vérifiée le 6 août 2026 : sur Python 3.13.5, numpy 2.5.1, pandas 3.0.5, scipy 1.18.0, les scripts
rejouent leurs sorties versionnées **ligne pour ligne**, au chemin absolu près. Deux points
propres au Mac : **épingler matplotlib à 3.11.0**, la version du PC, parce que le numéro de
version est écrit dans les métadonnées du PNG ; et **une figure en recadrage serré ne se régénère
pas à l'octet** d'une machine à l'autre, les métriques de police différant.

---

## Les règles à ne pas enfreindre

Condensé opérationnel. Le détail et les motifs sont dans `CLAUDE.md`.

### Sur la donnée et la calibration

- **`data/raw/` est gitignoré, sous licence, et ne se committe jamais.**
- **LA CALIBRATION EST GELÉE DEPUIS LE 7 AOÛT 2026.** Plus aucune recalibration : ni `config.py`,
  ni les paramètres figés, ni le pipeline stochastique. **Les corrections d'erreur restent
  autorisées et attendues**, et la distinction est nette : une **erreur** est une valeur qu'aucun
  calcul du projet ne reproduit ; une **recalibration** est un changement d'entrée qui déplace des
  résultats corrects.
- **Tout rapport cité doit être imprimé par un script.** Un ratio calculé pendant la rédaction
  n'est vérifiable par personne.

### Sur le vocabulaire, et ces erreurs ont déjà coûté une séance

- **Ne jamais écrire « le SCR DORA de telle entité ».** Écrire **« besoin de capital ORSA au titre
  de DORA »**. Il n'existe aucun module DORA en Formule Standard, et le rapport à un SCR publié
  est une **mise à l'échelle, pas une part**.
- **`VaR` et `TVaR` sont réservées à la charge annuelle agrégée**, `qsev` et `qbarsev` à la
  sévérité d'un sinistre. Le 662,78 M€ est un quantile de sévérité, **pas un capital**. La
  confusion s'est produite en séance le 7 août 2026.
- **Ne jamais additionner les quatre canaux** pour chiffrer une remédiation partielle : deux des
  quatre sont des **bornes posées**, pas des budgets.
- **Ne jamais additionner l'interaction entre canaux et l'interaction entre piliers.** Deux
  partitions du même écart.
- **« Additivité » désigne trois choses à trois étages** : hypothèse sur les coûts au sein d'un
  sinistre (non testée), quasi-additivité en fonction des piliers (mesurée), super-additivité en
  fonction des canaux (mesurée). Répondre « le modèle est super-additif » sans préciser est
  **faux**.
- **La source de comptage d'incidents n'est pas rejetée** : elle porte la **structure** du risque
  par vecteur, jamais son **niveau**.
- **Le processus auto-excité n'est pas rejeté** : l'énoncé juste est une **équivalence
  observationnelle** à la résolution disponible, suivie d'un choix de parcimonie interprétative.
- **L'écart n'est pas robuste à la sévérité.** L'invariance démontrée porte sur l'**échelle** et
  sur elle seule.
- **La défaillance simultanée de plusieurs piliers n'est pas un cas non traité**, c'est une sortie
  du modèle, et à l'état non conforme elle est **majoritaire**. La question suppose une lacune qui
  n'existe pas, et la réponse commence par corriger la prémisse.
- **Les entités réelles sont anonymisées.** Noms et provenance uniquement dans le script 65.
- **Aucune personne extérieure à l'encadrement n'est nommée.** La relecture se cite « une
  consultante de Nexialog ».
- **Le mémoire ne signale aucun défaut du rapport LUCY**, décision de Kélian du 9 septembre. Les
  valeurs justes sont publiées sans commentaire, l'audit interne garde la trace.

### Sur la façon de travailler

- **Step by step.** Ne pas élargir le périmètre au-delà de ce qui est demandé.
- **Écrire le commentaire APRÈS avoir lu la sortie**, jamais en même temps que le code qui la
  produit. Leçon apprise sept fois : la figure et la table sont le détecteur, la prose écrite
  d'avance est le défaut.
- **Pas de tirets cadratins, pas de tournures qui trahissent une rédaction automatique** dans les
  livrables. Vérifier **sur le PDF**, jamais sur la source.
- **Écrire les formules en texte brut dans le chat** : le LaTeX math ne s'affiche pas chez Kélian.
- **Toute figure modifiée s'ouvre et se regarde.**
- **Un deck figé ne se recharge jamais** avec du travail nouveau, et **aucune figure déjà utilisée
  dans un deck ne resserve** dans un nouveau. Exception unique : corriger une valeur fausse.
- **Ne pas envoyer le formulaire de Cooke** : l'élicitation est abandonnée depuis le 12 août.
- **Ne défaire aucune réserve pour faire plus net.**
- **Mettre ce fichier à jour à chaque fin de journée.**

### Sur la construction

- **Recompiler `main.tex` ET `main_v2.tex`** après toute modification de chapitre, et passer les
  contrôles sur les deux. Lignes de base : **15 débordements pour la v1, 6 pour la v2**.
- **Supprimer** `main.aux`, `.bbl`, `.blg`, `.out`, `.toc` et leurs équivalents `main_v2.*` après
  compilation. **`main.pdf` est versionné**, `main_v2.pdf` est gitignoré. Le PDF du rapport ENSAE
  est **versionné** : une compilation de simple vérification le salit, il faut le restaurer par
  `git checkout`.
- **Contrôles de fin de tâche**, dans cet ordre : **couverture égale 100 %**, ou zéro hors
  contrôle non déclaré, puis confirmation supérieure ou égale à 97 %, puis 0 `??` compté dans le
  PDF produit, 0 `Overfull \vbox`, 0 annotation hors page, 0 page tournée, git propre.
- **Vérifier le diff de suppression après toute édition scriptée** : `git diff --numstat`. Un
  script d'insertion a déjà écrasé six lignes de texte au lieu de les préfixer.

---

## Les commandes

```powershell
# Python et LaTeX
$py  = "C:\Users\KélianKADDOURI\Projects\M-moire-\.venv\Scripts\python.exe"
$tec = "C:\Users\KélianKADDOURI\Projects\M-moire-\memoire\tectonic.exe"

# Un script de calcul, lancé depuis la racine du dépôt
& $py exploratory\vasicek_lab\5_etats\66_invariance_ordre_conformite.py

# Régénérer une sortie versionnée. Sur le Mac, rediriger stderr séparément :
# matplotlib émet des avertissements de police qui s'intercalent au milieu d'une
# ligne de résultats et corrompent le fichier. Donc « 2>$null », jamais « 2>&1 ».
& $py exploratory\vasicek_lab\1_fondations\63_calibration_figee.py > sorties_verif\63.txt 2>$null

# Compiler les deux versions. TECTONIC ÉCRIT SES AVERTISSEMENTS SUR STDERR :
# un « > log.txt » ne capture RIEN des débordements, et deux contrôles ont été
# annoncés faux le 9 septembre pour cette raison. Rediriger les DEUX flux, par
# cmd pour éviter le NativeCommandError de PowerShell 5.1 :
cd exploratory\memoire_cascade
cmd /c "..\..\memoire\tectonic.exe -X compile main.tex    --keep-intermediates > %TEMP%\v1.txt 2>&1"
cmd /c "..\..\memoire\tectonic.exe -X compile main_v2.tex --keep-intermediates > %TEMP%\v2.txt 2>&1"

# Compter les débordements PAR EMPLACEMENT, jamais sur la ligne complète :
# les deux passes de tectonic ne donnent pas toujours la même largeur au
# dernier chiffre, et le même paragraphe ressort alors deux fois.
Get-Content "$env:TEMP\v1.txt" | Select-String 'Overfull \\hbox' |
  ForEach-Object { ($_.Line -replace ': Overfull.*','') } | Sort-Object -Unique

# Compter les ?? SUR LE PDF PRODUIT. Le contrôle « 0 référence indéfinie » ne se
# lit PAS dans la sortie de tectonic, qui n'émet aucun avertissement pour une
# référence non résolue : ce contrôle a passé à vide pendant des semaines et a
# laissé « cité au chapitre ?? » cinq fois dans un PDF publié.
& $py -c "import fitz,re; d=fitz.open('main.pdf'); print(sum(len(re.findall(r'\?\?', p.get_text())) for p in d))"

# Harnais, tous les chapitres puis un seul avec le détail des non confirmés
powershell -ExecutionPolicy Bypass -File verif_tous_chapitres.ps1
& $py verif_chiffres.py ..\..\sorties_verif chapitres\12_resultats.tex

# Le harnais prend n'importe quel chemin .tex : deck ou rapport ENSAE
& $py verif_chiffres.py ..\..\sorties_verif ..\rapport_ensae\rapport_ensae.tex
```

**Le récapitulatif `verif_tous_chapitres.ps1` n'imprime PAS la couverture**, seulement le taux de
confirmation, alors que c'est la couverture qui passe en premier. Elle se relève chapitre par
chapitre.

**Le compte de pages ne se lit pas avec un index système**, qui se périme sans prévenir : compter
sur le PDF, ou lire `main.toc` après une compilation avec `--keep-intermediates`.

**Et le texte du PDF porte des ligatures.** Chercher « vérification » échoue parce que le `fi`
sort en un seul caractère. Normaliser en NFKD avant toute recherche.

---

## Ce qui reste ouvert, par propriétaire

### Kélian, et cela ne peut pas être fait à sa place

- **Les trois champs de la page de garde du mémoire** : la date de soutenance, qui s'imprime
  `[jj/mm/2026]` en gras tant qu'elle est vide, la **case de confidentialité**, obligatoire au
  dépôt et qui relève de Nexialog, et les membres du jury, que le gabarit laisse vides.
- **Les champs équivalents du rapport ENSAE**, dont la mention de confidentialité.
- **Le courriel au service des stages** sur les dispositions prises pour la voie actuariat, que
  les consignes qualifient d'**impératif**.
- **L'autorisation de reproduire trois figures du rapport LUCY** dans un mémoire mis en ligne par
  l'Institut. À poser à Hugo.
- **L'erratum du rapport LUCY** : la section 7.1 publie un multiplicateur de charge à 2,53 là où
  les deux montants qui l'encadrent donnent 3,55 et où la section 7.6 donne 3,53. Le rapport est
  co-signé, donc la décision est à ses auteurs.
- **Relire trois passages du rapport ENSAE**, parce qu'une erreur de fait y serait défendue
  oralement devant les deux encadrants : le cadre de la mission, la table des enseignements de
  l'ENSAE, et surtout **la table qui répartit les demandes entre Hugo Rapior et Caroline
  Hillairet**.
- **La passe d'orthographe** sur les 52 pages du rapport ENSAE, jamais faite, alors que les
  consignes notent le style et l'orthographe.
- **La bibliographie en `plainnat`**, style anglais : seize citations à deux auteurs impriment
  « and » et non « et ». Corriger touche toutes les citations, donc c'est une décision.
- **Le formulaire de relecture** : lancer la fonction qui greffe les trois questions ajoutées sur
  le formulaire du 8 septembre, **vérifier que Mehdi et Nathanaël détiennent le même lien** que la
  première répondante, et recoller le fichier du dépôt dans le projet Apps Script avant toute
  nouvelle diffusion, la version en ligne étant antérieure. **Sept exemplaires du formulaire
  vivent dans le Drive**, donc une feuille de réponses vide ne prouve rien.
- **La date limite du Prix SCOR**, signalée six fois et toujours inconnue.
- **Le retrait de la version 1**, si la v2 devient la référence de style : échange d'une ligne de
  préambule.

### Hugo Rapior

- **Le second codage en aveugle** du corpus de post-mortems, annoncé pour la fin de la semaine du
  2 septembre. La réception est prête et testée, le script 54 ne fabrique rien sans donnée.

### Faisable par l'assistant, si Kélian le demande

- **La construction du support de soutenance**, le prompt étant prêt.
- **La banque de questions et la préparation de l'oral** : 6 points de barème, rien de fait.
- **La réduction du corps du rapport ENSAE** de 36 à 30 pages.
- **L'agrégation avec les autres modules de SCR**, jamais traitée.
- **Les 7 % de blanc résiduels** sous trois titres de figures : cosmétique, refusé deux fois.

### Clos, à ne pas rouvrir

Le statut de citation de la source de comptage d'incidents, le processus auto-excité, la
non-transitivité, le périmètre, l'anonymisation, les decks des 7, 14 et 21 août, la convention de
normalisation de la matrice, le gel de la calibration, la convention sur les mesures de risque,
le détecteur de contradictions entre scripts, les séquences ordonnées, l'ancrage du gain de
propagation sur des sources prudentielles, et l'élicitation.

---

## La prochaine étape immédiate

**Construire le support de soutenance.** Le prompt est dans
`exploratory/slides/prompt_soutenance_ensae.md`, prêt à coller avec les deux PDF joints. Trois
choses à savoir avant de lancer :

- **la soutenance dure 45 minutes, dont 15 d'exposé et 25 à 30 de questions.** La partie questions
  vaut donc deux fois l'exposé, d'où quinze diapositives de repli en plus des treize de l'exposé ;
- **le barème donne 12 points sur 20 à ce que le support porte**, et la diapositive qui rapporte le
  plus pour le moins de contenu disponible est celle des enseignements de l'ENSAE, de la part de
  l'encadrement et du recul. Le mémoire ne porte rien de tout cela, le rapport ENSAE oui ;
- **deux pièges de figure sont écrits dans le prompt et ne doivent pas être contournés.** La figure
  10.1 porte la lecture à **trois** canaux emboîtés, donc ses niveaux ne sont pas ceux du chiffre
  de tête à quatre canaux. Les figures 10.2 et 10.3 portent l'interaction entre les cinq
  **piliers**, pas celle entre les quatre **canaux**. Les diapositives du chiffre central et de
  l'interaction se font donc **en table, sans figure**.

---

## Les pièges d'instrument, cumulés

Chacun a coûté du temps au moins une fois.

### LaTeX et compilation

1. **Tectonic écrit ses avertissements sur stderr.** Un `> log.txt` ne capture rien, et le contrôle
   rend zéro partout **en ne regardant rien**.
2. **Les débordements se comptent par emplacement**, pas par ligne d'avertissement : les deux
   passes ne donnent pas toujours la même largeur au dernier chiffre.
3. **`titlesec` écrit lui-même l'entrée de sommaire d'un `\part*`** en style `[display]`, d'où un
   doublon si une ligne explicite s'y ajoute.
4. **Un `tabular` ne peut pas se couper entre deux pages** : hyperref émet alors des annotations à
   coordonnées négatives. Utiliser `longtable`.
5. **Une figure portrait prend la macro pleine page, jamais celle du débord**, qui ne contraint pas
   la hauteur.
6. **Un here-string PowerShell à guillemets doubles mange les accents graves du LaTeX**, le
   backtick y étant le caractère d'échappement. Guillemets **simples** pour écrire du LaTeX.
7. **`\newcolumntype` prend une lettre, pas un nom de macro**, sinon « Illegal pream-token ».
8. **La police Times du rapport ENSAE ne porte pas le caractère œ** : écrire `\oe{}`.

### Harnais

9. **Une ligne « Sources : scripts… » ne couvre que le bloc où elle se trouve.** Le harnais découpe
   sur `\section`, `\section*`, `\subsection` **et** `\subsection*` : il en faut **une par bloc**.
10. **Une déclaration hors section est ignorée si le bloc cite aussi un script**, le code exigeant
    les deux conditions.
11. **Le nom de fichier d'une figure verse son nombre dans le pool.** L'argument optionnel d'un
    `\includegraphics` est neutralisé, l'argument obligatoire non. Nommer les fichiers **sans
    chiffre**.
12. **Un type de colonne maison n'est pas neutralisé.** Écrire les colonnes en clair.
13. **Un séparateur de milliers dans une sortie de script casse l'extraction** : `20,996` se lit
    comme un décimal en convention française. Imprimer les grands entiers **sans séparateur**.
14. **Les nombres ronds d'un pool de plusieurs milliers se confirment mutuellement par hasard.**
    Ne jamais conclure d'une correspondance numérique seule.

### Figures et données

15. **Une étiquette de figure partiellement masquée se zoome avant d'être transcrite.** Relever une
    **étiquette imprimée** est licite, mesurer une **hauteur de barre** ne l'est pas.
16. **Les légendes opaques masquent les données** : toute légende posée par lot se relit figure par
    figure.
17. **`[System.IO.File]::ReadAllText` avec un chemin relatif** résout contre le répertoire courant
    de .NET, pas celui de PowerShell. A déjà créé un fichier parasite committé.
18. **`.Replace()` PowerShell avec `\n` échoue sur des fichiers CRLF.** Utiliser `[regex]::Replace`
    avec `\r?\n`, ou l'outil d'édition.

---

# Journal

## 9 septembre 2026

Journée en trois temps : le rapport ENSAE, puis la relecture de praticien, puis la page de garde
et la lecture de marché. Onze commits, du plus ancien au plus récent.

### `857ef39`, `e83cd31`, `5c9e2e8` : le rapport de stage ENSAE

Créé comme **document distinct** du mémoire, à la demande explicite de Kélian, aux consignes du
PDF de l'école. Il porte **6 figures, 13 tableaux et 3 propositions démontrées**, et **sept
annexes A à G**, parce que les annexes ne comptent pas dans les 30 pages : c'est là qu'est allé
tout le matériel ajouté. Trois « lectures » d'annexe **refusent une conclusion flatteuse**, et
c'est ce qui les rend utiles : l'accord parfait entre progéniture et amorce n'est pas une
validation externe mais une conséquence de la construction, la monotonie du capital s'appuie sur
l'hypothèse d'additivité des coûts, et l'encadrement de l'écart est **mesuré et non démontré**.

### `f2dded1` : un fichier parasite retiré

Créé par une commande à chemin relatif, voir le piège 17.

### `4cd2318` : le registre d'écriture et le cadre de la mission

Registre calé sur un **vrai mémoire de l'Institut**, téléchargé et dépouillé : voix impersonnelle,
titres nominaux, gras quasi absent. Le rapport ENSAE s'en écarte sur **un** point et c'est
délibéré : première personne là où une décision est assumée ou une erreur reconnue, parce que le
barème ENSAE exige le recul personnel, ce qu'un mémoire d'actuariat n'a pas à porter.

Nouvelle sous-section « Le cadre de la mission et ses contraintes », qui manquait au barème.

### `b4acb5a` : la couverture du rapport ENSAE

Champs renseignés au modèle de l'annexe 1 des consignes.

### `ce5a9e3` : la relecture de praticien entre au mémoire

**Une consultante de Nexialog** a répondu aux sept phrases et n'en a contredit **aucune**. Elle
n'est **jamais nommée**, décision de Kélian, alors même qu'elle avait accepté de l'être.

**Le résultat qui compte.** Sur la phrase qui oppose la contagion à la cause extérieure commune,
son exemple est **compatible avec les deux explications** : une direction informatique sous-dotée
teste mal ET gère mal, sans que l'un cause l'autre. Le jugement de terrain nomme donc un ordre
qu'il ne distingue pas d'une cause commune. **Corroboration de la frontière d'identifiabilité,
jamais de la matrice**, et c'est un résultat plus fort qu'un acquiescement.

Une qualification substantielle est **déclarée et non traitée** : elle distingue l'occurrence d'un
incident chez un prestataire, qu'une bonne gouvernance ne change pas selon elle, de la maîtrise de
ses conséquences, qu'elle change. La traiter déplacerait un arc de la matrice vers le canal de
détection, donc **ce serait une recalibration et le gel l'interdit**.

### `38a7cec` : pourquoi la relecture est nécessaire, et les quatre équations

**L'argument de nécessité**, qui manquait : la direction n'est pas identifiable, donc la matrice
**n'est pas calibrée** au sens où le sont la fréquence et la sévérité. Sa structure est déduite
d'un corpus de post-mortems qui porte son propre biais de narration. Sur une structure ainsi posée
il ne reste qu'un seul contrôle externe, le jugement de praticiens, et ce jugement peut
**corroborer ou contredire, jamais calibrer**. C'est la différence entre une relecture et une
élicitation, et c'est elle qui commande la forme de l'instrument.

**Le modèle en quatre équations** entre dans le rapport ENSAE, qui décrivait un modèle sans jamais
l'écrire. Deux d'entre elles rendent visible ce qui était tacite : l'**hypothèse d'additivité des
coûts**, et la latente de conformité, qui montre que la corrélation publiée de 0,462 est le
**carré** de la charge de facteur commun de 0,68.

**Et la règle de la v2** : toute modification de chapitre vaut pour les deux versions, donc la v2
se recompile **à chaque fois**. Dès la première application, le PDF de la v1 était déjà périmé.

### `f3158b6` : la page de garde de l'Institut, et la lecture de marché

**La page de garde officielle** est posée dans `exploratory/memoire_cascade/page_de_garde.tex`,
avec ses logos dans `logos/`. Elle **remplace** le `\maketitle` et elle est **partagée par les deux
versions**. La structure et les mentions légales du gabarit ne sont pas touchées. Trois pièges de
mise en page mesurés et corrigés, voir le piège 10.

**La lecture de marché passe de deux pages à sept sous-sections**, avec trois figures du rapport
LUCY, cinq tableaux et l'équation de rétention. Deux ponts de méthode sont explicites, et c'est ce
qui fait travailler cette section pour le mémoire : la formule de rétention demande la donnée ligne
à ligne, donc **une baisse de franchise et une aggravation réelle de la menace produisent le même
signal** sur des agrégats, ce qui est la situation du chapitre 09 à l'échelle du marché ; et un
multiplicateur **hiérarchise des dynamiques, pas des enjeux**, les micro-entreprises portant tous
les multiplicateurs spectaculaires et 1,6 % de la charge.

Toute la transcription est dans `LUCY_2026` de `config.py` et imprimée par le **script 63**, sous
le statut inchangé de **citation externe non recalculable**. Le gel n'est pas touché. Le script en
tire **quatre contrôles d'identité** qui valident la transcription et non le rapport, et ils ont
fait tomber une coquille du rapport publié, une imprécision de la même source et une valeur que
j'avais relevée de travers.

### `0286b65` : le mémoire ne signale plus les défauts du rapport LUCY

**Décision de Kélian.** Le rapport est co-signé par lui et son maître de stage, et un mémoire n'est
pas le lieu où l'on relève les coquilles de son propre employeur. Les passages qui nommaient les
écarts sont retirés, les **valeurs justes restent publiées** sans commentaire, et l'encadré du mot
« fréquence » est réécrit en **distinction définitionnelle**, argument analytique intégralement
conservé. **Ne pas réintroduire ces passages.** L'audit interne, lui, garde tout : la sortie du
script 63 continue d'imprimer la vérification qui justifie la valeur publiée.

### `3b434ee` : le prompt de construction du support de soutenance

Dans `exploratory/slides/prompt_soutenance_ensae.md`, autonome, à coller avec les deux PDF joints.
Consignes chiffrées, barème, plan de treize diapositives avec budget minute par minute, quinze
diapositives de repli, fiche des chiffres à ne pas déplacer, treize interdits, neuf questions
attendues. Les trente-cinq valeurs de la fiche ont été **cherchées dans les deux PDF** : trois ne
sont que dans le rapport de stage, et une quatrième dans aucun des deux, donc retirée.

### Ce que la journée a coûté et rapporté

Corps du mémoire de 130 à **136 pages** en v1, de 136 à **140** en v2. Harnais de 2 172 à
**2 346 nombres, 100 %**. Trois défauts trouvés dans une source co-signée, un doublon de sommaire
antérieur dans la v2, et deux de mes propres contrôles reconnus faux puis refaits.
