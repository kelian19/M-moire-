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

## L'état mesuré, au 18 septembre 2026

**`main_ensae.tex` EST LE MÉMOIRE DÉPOSÉ, ET LE SEUL QUI SE COMPILE DÉSORMAIS.** La v3 est
supprimée (décision de Kélian le 17 septembre) ; `main.tex` et `main_v2.tex` restent au dépôt,
partagent les chapitres, mais ne sont plus recompilés ni contrôlés : leurs PDF sont périmés.

**LE FICHIER DÉPOSÉ EXISTE** : `exploratory/memoire_cascade/KADDOURI_Kelian_3A25.pdf`, copie
exacte de `main_ensae.pdf`, **sans suffixe `_CONF`** (mémoire non confidentiel, décision du
16 septembre). Gitignoré. **Il se périme à la moindre recompilation** : recopier après chaque
compilation.

**SON FORMAT EST IMPOSÉ PAR L'ÉCOLE** : pas de limite de trente pages, **Times New Roman 12 et
interligne 1,5**, par l'interrupteur `\formatensae`. Couverture ENSAE complète.

| Document | Total | Folios | Débordements | Harnais |
|---|---|---|---|---|
| **`main_ensae.pdf`, le mémoire déposé** | **172 pages** | corps (parties I à V) 21 à 132, stage 133, annexes 139 | **5, ligne de base** | **1 490 sur 1 490** |
| `rapport_ensae.pdf` | 52 pages | 36 de corps | 0 | ne part plus |

**Ordre des pièces** : couverture, remerciements, résumé et sommaire, glossaire en 10, note de
synthèse en 12, executive summary en 16, Contexte en 21, Données en 37, Modélisation en 49,
Résultats en 88, Robustesse en 113, Le stage en 133, Annexes en 139, bibliographie en fin.

**Annexes depuis le 18 septembre, et les lettres ont toutes bougé** : une notice sans numéro
« Organisation des annexes et matériel complémentaire » ouvre la partie, puis **A** démonstrations
du modèle de cascade (`15b`), **B** adaptations par pilier (`12b`), **C** protocole d'élicitation
(`18`), **D** table des paramètres (`17b`, revenue du dossier déporté le 18 septembre au soir),
**E** table des notations (`16`). Les renvois passent tous par `\ref`, aucune lettre
n'est écrite en dur.

**TROIS ANNEXES SONT DÉPORTÉES** dans `exploratory/memoire_cascade/materiel_complementaire/`,
avec leur `README.md` : démonstrations du socle EVT (`15_demonstrations`), pièces justificatives
(`17_pieces_justificatives`) et compléments aux chapitres du corps (`21_complements_corps`).
Aucun fichier maître ne les appelle. Les 54 renvois qui y pointaient portent la macro
`\matcomp`, qui imprime « *(voir le Matériel Complémentaire en ligne)* » et ne contient aucun
`\ref`. **L'adresse du dépôt externe reste à renseigner**, le gabarit
`https://LIEN_VERS_LE_DEPOT.com` étant en clair dans les trois fichiers maîtres.

**Harnais : 2 357 nombres, 2 357 confirmés**, et **0 hors contrôle non déclaré** chapitre par
chapitre (publiés = sous contrôle + déclarés partout). Contrôles `controles_memoire.py` au vert :
0 `??`, 0 vbox, 0 annotation hors page, 0 page tournée, aucune figure seule ni trop haute.

**Les lignes « Sources : scripts… » vivent dans des commentaires `% SOURCES-SCRIPTS: NN`**, sur
leur propre ligne (un commentaire posé en fin de ligne de prose avale le texte qui suit).

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

### L'agent qui vérifie les figures, et comment le lancer depuis n'importe quel poste

**`.claude/agents/verificateur-figures.md` est versionné**, donc un `git pull` suffit pour
l'avoir sur l'autre machine : Claude Code lit ce dossier au démarrage, et une session déjà
ouverte quand le fichier arrive ne le connaît pas encore. Dans une session ouverte à la racine du
dépôt, il se lance en le nommant, par exemple « lance l'agent verificateur-figures sur les figures
Z20, Z22 et Z19 », et `/agents` le montre dans la liste. Plusieurs instances peuvent tourner en
parallèle sur des lots disjoints ; elles ne doivent pas se partager un script ni un bloc LaTeX.

Ce qu'il fait : il repère la page où tombe chaque figure, la rend en image, la **regarde**, juge
la figure et sa place sur la page, corrige le code de tracé et le bloc LaTeX, recompile dans un
dossier privé et regarde à nouveau. Sa grille et ses interdits sont dans sa définition ; les deux
règles qui protègent le reste du projet sont qu'il ne touche ni aux calculs ni aux `print`, dont
sortent les chiffres du mémoire, et qu'il ne compile **jamais** sans `--outdir`.

```powershell
# La carte : page, taille imprimée, taille réelle des polices, appel LaTeX, script producteur
& $py exploratory\memoire_cascade\carte_figures.py
& $py exploratory\memoire_cascade\carte_figures.py --image Z20_corpus_etendu_pij --rendu $env:TEMP\pages
# Juger une correction sans salir le dossier du mémoire (une compilation dure ~20 s)
cd exploratory\memoire_cascade
cmd /c "..\..\memoire\tectonic.exe -X compile main_ensae.tex --outdir %TEMP%\essai > %TEMP%\essai\log.txt 2>&1"
& $py carte_figures.py --pdf $env:TEMP\essai\main_ensae.pdf --image Z20_corpus_etendu_pij --rendu $env:TEMP\essai\pages
```

Le facteur `police` de la carte est ce qui manquait pour juger sans compiler : une police de
`s` points dans matplotlib s'imprime à `s` fois ce facteur. C'est lui qui a chiffré le reproche de
Kélian du 15 septembre, « l'image est trop grande » : la figure Z20 s'imprimait sur 15,4 × 21,9 cm,
soit presque la page entière.

---

## Ce qui reste ouvert, par propriétaire

### Kélian, et cela ne peut pas être fait à sa place

- **La seconde réponse au formulaire de relecture est RETROUVÉE et INTÉGRÉE le 17 septembre**
  (chapitre 09, annexe `sec:relecture-praticien`, chapitre 19), fichier déposé régénéré. **Reste la
  réponse de Hugo Rapior**, annoncée : la citer à part comme regard de l'encadrant, et vérifier qu'il
  remplit le formulaire le plus récent (phrases 8 à 10).
  Elle date du 10 septembre à 9 h 35 et vit dans la feuille créée le 3 août à 9 h 07
  (`1yltQ8ghx02xNsyRMjQEz5gO2tan7ZylPA6W7oa84aek`), le répondant ayant reçu un ancien lien.
  C'est la réponse de **Mehdi Cherkaoui** (jeudi 10 septembre), attribution confirmée par Kélian ; la ligne
  « xw » du 9 septembre dans la feuille du 8 est un test de Kélian, et Nathanaël n'a pas répondu. Les lignes
  qui suivent décrivent l'état du 16 au soir, avant qu'elle soit retrouvée. **Au 16 septembre, elle
  n'était pas encore récupérée**. Deux tentatives ont échoué ce soir-là : le connecteur Google Drive avait
  expiré puis a été retiré de la session, et le lien Teams transmis ne s'ouvre pas sans connexion
  Microsoft (la page ne renvoie que « Join conversation »). **Le plus simple est de coller la
  réponse, ou l'export CSV de l'onglet Réponses, dans la session.** Le formulaire en diffusion
  est sur le compte **keliankaddouripro@gmail.com**, identifiant
  `1uBKaP_3dj6blEsHqVHgJQp-Rf7rViu2PwYjxI8uIpyY`, inscrit en tête de
  `exploratory/vasicek_lab/notes/form_relecture_praticien.gs`. Sept formulaires homonymes vivent
  dans ce Drive : une feuille vide ne prouve rien.
- ~~Le courriel au service des stages~~ : **fait, confirmé par Kélian le 19 septembre 2026.** Ce
  point n'est plus ouvert. Historique : il portait sur les dispositions prises pour la voie
  actuariat, que
  les consignes qualifient d'impératif. Non attesté dans le dossier.
- **Le dépôt GitHub est public.** Rien de confidentiel n'y est poussé (`data/raw` est gitignoré),
  mais le mémoire, les sorties et les notes y sont lisibles. Le passer en privé est une décision de
  Kélian.
- **La page de garde de la version Institut** (`page_de_garde.tex`, partagée par `main`, `main_v2`
  et `main_v3`, pas par `main_ensae`) : date de soutenance, case de confidentialité et membres du
  jury restent à remplir pour le dépôt Institut.
- **L'erratum du rapport LUCY** (2,53 pour 3,53 en section 7.1) : décision des auteurs.
- **La date limite du Prix SCOR**, toujours inconnue.

### Hugo Rapior

- **Le second codage en aveugle** du corpus de post-mortems. La réception est prête, le script 54
  ne fabrique rien sans donnée.

### Faisable par l'assistant, si Kélian le demande

- **Intégrer la réponse de Mehdi** dès qu'elle est collée : voir la prochaine étape.
- **La passe de mise en page du script 97** (deux étiquettes se chevauchent sur L1, une passe sous
  la légende sur L2), à ne faire que si les figures redessinées doivent remplacer celles du rapport.
- **Réduire encore l'annexe** : la table des notations (5 pages, en partie redondante avec le
  glossaire), la relecture de praticien (2 pages), la table des proxys (2 pages, demandée par Hugo).
- **La construction du support de soutenance ENSAE**, le prompt étant prêt.

### Clos, à ne pas rouvrir

Le statut de citation de Hackmageddon, le processus auto-excité, la non-transitivité, le
périmètre, l'anonymisation, les decks des 7, 14 et 21 août, la convention de normalisation de la
matrice, le gel de la calibration, la convention sur les mesures de risque, le détecteur de
contradictions entre scripts, les séquences ordonnées, l'ancrage du gain de propagation sur des
sources prudentielles, l'élicitation, **la confidentialité (non confidentiel)**, **le placement des
notes de synthèse (en tête, sur le modèle du mémoire de F. Dountio)** et **la bibliographie en
français** et **la reproduction des figures LUCY (validée par Hugo le 17 septembre)**.

---

## La prochaine étape immédiate

**1. ~~Intégrer la réponse de Mehdi Cherkaoui~~ : FAIT le 17 septembre.** Reste la réponse
de Hugo Rapior, à citer à part comme regard de l'encadrant.

**2. ~~Envoyer le courriel au service des stages~~** : fait le 19 septembre 2026.

**3. ~~Obtenir l'accord de Hugo sur les figures LUCY~~ : ACCORDÉ le 17 septembre 2026.** Les
figures du rapport restent en place, rien à recompiler pour ce point.

**4. Le rapport de jury simulé est traité en entier (P0, P1, P2).** Ce qui reste possible si
Kélian le veut : rien. Le corps est à 112 pages, pour 110 visés.

**5. Déposer** `KADDOURI_Kelian_3A25.pdf` avant le 30 septembre, après avoir vérifié qu'il est la
copie exacte du dernier `main_ensae.pdf` (`cmp` les deux fichiers).

**Le support de soutenance devant l'Institut est fait** (`exploratory/slides/`, généré par
`build_soutenance_ppt.py`) ; il reste la date de soutenance sur sa couverture. **Le support de la
soutenance ENSAE reste à construire**, le prompt est dans
`exploratory/slides/prompt_soutenance_ensae.md`.

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
14b. **Un commentaire `% SOURCES-SCRIPTS:` posé sur une ligne de prose avale la fin de cette
    ligne.** Deux phrases du PDF étaient coupées ainsi (« graines. justifiait l'attente »,
    « renforcement. borne adverse »). Le commentaire va **seul sur sa ligne** ; contrôle :
    rechercher `SOURCES-SCRIPTS:` suivi de lettres.
14c. **La v3 ne lit pas les chapitres partagés** pour sept d'entre eux (`chapitres_v3/`). Une
    correction de fond ne l'atteint pas, et un renvoi vers un label absent de ces copies y imprime
    « ?? » : compiler la v3 à chaque fois.

### Figures et données

15. **Une étiquette de figure partiellement masquée se zoome avant d'être transcrite.** Relever une
    **étiquette imprimée** est licite, mesurer une **hauteur de barre** ne l'est pas.
16. **Les légendes opaques masquent les données** : toute légende posée par lot se relit figure par
    figure.
17. **`[System.IO.File]::ReadAllText` avec un chemin relatif** résout contre le répertoire courant
    de .NET, pas celui de PowerShell. A déjà créé un fichier parasite committé.
18. **`.Replace()` PowerShell avec `\n` échoue sur des fichiers CRLF.** Utiliser `[regex]::Replace`
    avec `\r?\n`, ou l'outil d'édition.

### PowerPoint, depuis le 11 septembre 2026

19. **Un titre posé à corps fixe qui passe à la ligne recouvre ce qui est dessous.** Le gabarit
    Nexialog lui-même porte ce défaut deux fois. Le remède est de **mesurer** le texte avec la
    vraie police, par `PIL.ImageFont` sur `georgiab.ttf` ou `segoeui.ttf`, et de descendre le
    corps jusqu'à ce que le titre tienne sur une ligne. Un corps qui varie de 20 à 26 points ne se
    remarque pas d'une diapositive à l'autre ; un chevauchement, si.
20. **Une photographie agrandie jusqu'à couvrir son cadre en SORT.** Le débord ne se perd pas hors
    diapositive, il passe sous le texte. Utiliser `pic.crop_left` et ses voisins, qui recadrent
    sans déformer et respectent le cadre demandé.
21. **Une forme empilée sur une autre laisse passer ce qu'il y a dessous entre les deux.** Une
    coupe diagonale se fait par **deux polygones superposés**, le plus grand par-dessous, jamais
    par trois triangles voisins.
22. **Le contrôle de mise en page se fait sur le PDF rendu, deux à deux.** Exporter par PowerPoint,
    puis comparer les cadres de toutes les lignes de texte de chaque page avec `pymupdf`. Quatre
    titres chevauchés sur vingt-huit pages ne se voient pas à la relecture.
23. **Toute dimension qui dépend d'un texte se MESURE.** Le corps d'un titre, la largeur réservée
    à une étiquette de valeur, la hauteur d'une ligne de tableau : posées en dur, les trois ont
    produit un chevauchement. `PIL.ImageFont` sur la vraie police, puis la coupure aux espaces,
    et le défaut disparaît par construction au lieu d'être corrigé au cas par cas.
24. **UNE TOLÉRANCE NE PORTE JAMAIS DE PLANCHER ABSOLU.** Recopiée sous la forme
    `max(0,6 % ; 0,5)`, la tolérance de comparaison acceptait un indice de queue lu à 0,5954 pour
    une valeur attendue de 0,62 : le plancher écrase tout ce qui vaut moins que lui. C'est le
    défaut que le harnais du mémoire avait déjà corrigé en août, reproduit à l'identique. Le
    demi-pas se prend sur la **dernière décimale écrite**. Et il ne se suppose pas : le garde-fou
    a été **testé sur cinq cas**, dont deux dérives, et c'est le test qui a révélé le défaut.

---

# Journal

## 19 septembre 2026

**Décision de cadrage, posée par Kélian en cours de journée : on ne travaille plus que sur
`main_ensae`.** Les autres fichiers maîtres restent au dépôt mais ne sont plus ni compilés ni
tenus à jour. `main.tex` appelle donc toujours `02_introduction` là où `main_ensae` appelle le
nouveau chapitre 1 : la divergence est assumée, elle n'est plus un défaut à corriger.

### 1. Un chapitre 1 neuf, qui absorbe l'introduction

`chapitres/02b_cadre_cyber_dora.tex`, cinq sections et dix-sept sous-sections, sur le plan arrêté
par Kélian : risque cyber et propagation, assurabilité et capital, marché français, DORA, puis
l'enjeu prudentiel qui se referme sur la problématique et le plan. **Il remplace
`02_introduction.tex` dans `main_ensae`**, qu'il absorbe en entier, lecture de marché LUCY
comprise. `02_introduction.tex` ne définissait qu'un label, `sec:lucy`, que rien d'autre ne cite :
la bascule se défait en une ligne. `04_cadre_reglementaire` reste appelé parce que cinq chapitres
citent son label, mais son exposé des cinq piliers fait désormais doublon avec la section 4 du
chapitre 1, et il reste à réduire à la seule articulation avec Solvabilité II.

**Trois sources de contexte 2026 y entrent, au statut de citation externe non recalculable**, le
même que Hackmageddon et LUCY : la cartographie prospective France Assureurs, le baromètre CESIN,
et une carte des tentatives WannaCry bloquées. Leurs valeurs sont transcrites dans `config.py`
sous `CARTO_FA_2026` et `CESIN_2026`, et le **script 103** les imprime avec quatre contrôles
d'identité internes.

**Le résultat qui travaille pour la thèse** : l'attaque indirecte par un tiers est le troisième
vecteur à 35 %, et monte à **43 % chez les grandes entreprises**. C'est le pilier P4 mesuré de
l'extérieur, par une source sans lien avec le projet. La déconnexion par les tiers, citée dans
12 % des impacts, dit que la dépendance joue **dans les deux sens**, ce qu'une dépendance
symétrique ne peut pas distinguer.

**Le piège de lecture à ne pas perdre** : CESIN et France Assureurs voient la fréquence *reculer*
quand LUCY voit le nombre de sinistres *tripler*. Les deux sont compatibles, le nombre de LUCY
étant un total sur une base d'assurés élargie de 49 % ; confondre le total et la fréquence ferait
lire une aggravation là où il y a une extension de périmètre. Un encadré le pose.

### 2. Les figures externes, et où elles vivent

`figures_externes/` porte désormais **six** images et non trois : les trois figures LUCY, plus la
rétrospective France Assureurs, les vecteurs CESIN et la carte WannaCry. **Un sous-dossier
`sources_brutes/` archive les captures d'origine non recadrées**, ce dossier n'étant lu par aucun
`\includegraphics`.

**À savoir avant le dépôt, et cela n'appartient pas à l'assistant : l'autorisation de Hugo Rapior
du 17 septembre ne couvre que les trois figures LUCY**, dont il est co-auteur. Celles du CESIN, de
France Assureurs et d'Avast relèvent de leurs éditeurs et **restent à vérifier**. Le repli est
prêt et sans perte : les deux séries 2026 sont intégralement transcrites et imprimées par le
script 103, donc elles se reposent en tableau.

**Cinq captures avaient été déposées dans `vasicek_lab/figures/`**, dossier réservé aux figures
produites par script. Elles en ont été retirées : y laisser des images externes aurait cassé
l'invariant qui rend ce dossier rejouable.

### 3. Le style du document a changé, globalement

Deux décisions de Kélian, appliquées dans `preambule_v2.tex`, donc à tous les chapitres :

- **plus aucun filet horizontal** : ni sous le titre de chapitre, ni autour de l'encadré `cle`,
  qui tient désormais par son seul espacement et son amorce en gras. Les filets de `booktabs`
  dans les tableaux sont **conservés**, ce sont des séparateurs de données et non un ornement ;
- **paquet typographique « classique ENSAE »** : chiffre de chapitre en très grande taille, seul
  et centré au-dessus du titre ; sections en **petites capitales** numérotées ; sous-sections en
  italique, inchangées. Un titre de section sur deux lignes se coupait en plein mot : la césure
  est désormais interdite dans les titres, par `raggedright` et pénalité infinie.

**Et têtes et pieds de page portent le même contenu** : filet noir, nom du chapitre à gauche,
folio à droite, en tête comme en pied. Sur la première page d'un chapitre la tête reste vide, le
grand titre suffisant à identifier la page, mais le pied est là comme partout ailleurs.

### 4. Le profilage des variables, qui manquait au chapitre des données

Nouvelle section `sec:profilage-variables` au chapitre 4, en trois sous-sections : table des
variables avec leur taux de renseignement, tests d'association sur les qualitatives, tests de
forme et d'hétérogénéité sur les quantitatives. **Script 104**, trois figures neuves (D1 matrice
de présence croisée, D2 sources de notification en double axe, D3 types de brèche dans le plan
fréquence contre impact médian).

**Le piège de complétude de la PRC, et il est grossier.** Un champ non renseigné n'y vaut pas
vide, il vaut la chaîne `UNKN`. Un contrôle ordinaire rend donc **100 % de présence sur les
trente-sept colonnes**, y compris sur `total_affected` qui n'est documentée que dans **41,77 %**
des cas. Les taux publiés comptent `UNKN` comme un manquant, et le script imprime les deux
mesures côte à côte.

**Le contrôle qui compte** : ce script recharge la PRC par un chemin indépendant de celui des
scripts 21, 22 et 62, avec son propre traitement du manquant, et retombe sur **15 053 incidents**
au périmètre retenu, l'effectif exact des sorties déjà versionnées. Le contrôle est dans le
script et il échoue bruyamment s'il dérive.

**Le résultat de modélisation, et il est convergent sur trois instruments indépendants.** Le $V$
de Cramér reste sous **0,20** (maximum 0,176), l'$\varepsilon^2$ de Kruskal-Wallis sous **0,08**,
et les corrélations de rang entre la perte et la taille sous **0,16**. La catégorie d'un incident
et la taille de l'entité informent donc **faiblement** sa sévérité : segmenter la queue coûterait
des degrés de liberté sans gain explicatif. **Le choix d'une queue commune cesse d'être une
commodité de rédaction pour devenir une mesure.**

**Deux trouvailles à ne pas perdre.** L'**actif total est le plus faible des trois prédicteurs de
taille** (rho 0,068, derrière le chiffre d'affaires à 0,159 et l'effectif à 0,139), alors que
c'est le bilan qui porte la mise à l'échelle prudentielle. Et Shapiro-Wilk rejette la normalité
totalement à l'échelle brute ($W = 0{,}037$ sur la PRC) mais **seulement partiellement en
logarithme** ($W = 0{,}970$) : la queue est plus lourde qu'une log-normale, ce qui est
exactement l'argument d'une Pareto généralisée au-delà d'un seuil plutôt qu'un ajustement global.

**Une leçon de méthode, la huitième du même type.** Deux nombres des commentaires du script 104
avaient été écrits **avant** lecture de sa sortie : un taux de 41,80 % recopié d'une source
extérieure, et des corrélations annoncées « de l'ordre de 0,2 à 0,3 » quand elles valent 0,07 à
0,16. Les deux ont été corrigés, le premier en le calculant au lieu de l'écrire. Écrire le
commentaire APRÈS avoir lu la sortie, jamais en même temps que le code.

### 5. Trois décisions de fin de journée

- **`main.tex` et `main_v2.tex` sont SUPPRIMÉS du dépôt**, avec `main.pdf`. Il ne reste qu'un
  fichier maître, `main_ensae.tex`. Les deux fichiers restent dans l'historique git si besoin.
  **`preambule.tex` et `page_de_garde.tex` deviennent orphelins** : plus rien ne les appelle. Le
  second est la couverture officielle de l'Institut des Actuaires, il n'a pas été supprimé pour
  cette raison. `02_introduction.tex` est orphelin lui aussi depuis que le chapitre 1 l'absorbe.
- **L'autorisation de reproduction est ACQUISE POUR TOUTES LES FIGURES EXTERNES**, Hugo Rapior
  l'ayant étendue le 19 septembre à la cartographie France Assureurs, au baromètre CESIN et à la
  carte Avast, au-delà des trois figures LUCY du 17 septembre. Point clos.
- **Les doublons entre le chapitre 1 et le chapitre du cadre prudentiel sont supprimés.** Les
  cinq piliers et la date d'entrée en application de DORA ne vivent plus qu'à **un seul endroit**,
  le \S du chapitre 1, qui a **repris la précision juridique** du second : délais de notification
  de quatre, vingt-quatre et soixante-douze heures puis un mois, périodicité triennale des tests
  guidés par la menace, troisième rang de la chaîne de sous-traitance, et le registre
  d'informations avec sa portée de modélisation. Le chapitre du cadre réglementaire passe de 176
  à 115 lignes, se recentre sur Bâle, Solvabilité II et l'articulation avec l'évaluation interne,
  et se retitre en conséquence ; son label `chap:reglementaire` ne bouge pas, cinq chapitres le
  citent.

### 6. Trois ajouts inspirés du mémoire de F. Dountio, dans l'ordre de valeur

Comparaison faite sur les neuf pages de son chapitre 2 et de son début de chapitre 3. Trois
manques y étaient visibles, tous comblés le même jour, tous adossés au script 104.

**La table de statistiques descriptives** (`subsec:describe-impact`). Le mémoire publiait des
quantiles de sévérité dans plusieurs chapitres sans les avoir jamais rassemblés. Quatre colonnes,
douze lignes, plus trois rapports de forme. **Le contrôle qu'elle porte n'est pas celui qu'on
écrirait spontanément** : vérifier que le $q_{85}$ redonne le seuil publié serait faux, le seuil
étant gelé au percentile 84,4 quand le $q_{85}$ courant vaut 22,03. Le bon contrôle est le nombre
d'excès au-dessus du seuil publié, et il rend **91**, exactement le `n_excess` de `config.py`.
C'est un troisième chemin indépendant qui confirme la calibration.

**Les sous-figures (a)/(b)** (paquet `subcaption`). La figure de présence croisée devient à deux
panneaux, taux et effectifs, sur le modèle de sa figure 2.1. Ce n'est pas cosmétique : les
12,5 % du croisement le plus pauvre représentent encore plus de neuf mille incidents, ce qu'un
taux seul ne dit pas. **Règle posée : les panneaux servent aux variantes d'un même objet, jamais
à entasser deux figures sans rapport pour gagner une page.**

**Le top des sinistres nommés** (`subsec:top-incidents`). Douze incidents PRC avec organisation,
date et volume. Nommer est licite ici, ce sont des notifications publiques ; la base SAS reste
sous licence et n'est jamais nommée, et la règle d'anonymisation des quatre assureurs SFCR est
encore une autre question, inchangée.

**Et cette table a fait tomber un défaut de base, trouvé en la regardant.** La PRC n'agrège pas
les notifications : un même incident déclaré à plusieurs autorités y figure autant de fois, avec
le même volume. La table brute affichait un établissement de crédit **quatre fois**. Le
dédoublonnage retire **1 643 lignes, soit 10,9 %** de la période, et ce chiffre est une **borne
basse**, l'appariement exact ne rapprochant pas deux graphies d'une même raison sociale. **Le
mémoire n'est pas touché** parce qu'il n'additionne jamais ces volumes : chaque ligne y est une
observation de sévérité. Déclaré comme tel.

**Le chiffre qui rend la queue concrète** : la moitié du volume de sept années tient dans
**31 incidents sur 13 410**, soit 0,23 % de la base. C'est l'argument de queue lourde énoncé sur
des événements nommés plutôt que sur un paramètre.

### État à la fin de la journée

`main_ensae` à **191 pages**, seul fichier maître subsistant. Débordements **exactement à la ligne de base de 5**, 0 Overfull
`\vbox`, 0 annotation hors page, 0 page tournée, 0 `??` compté dans le PDF.
`KADDOURI_Kelian_3A25.pdf` régénéré. Harnais : chapitre 1 à **63 sur 63**, chapitre 4 à **266 sur
266**, hors contrôle non déclaré à zéro sur les deux. Deux sorties versionnées neuves, **103 et
104**, et trois figures neuves, D1 à D3.

---

## 18 septembre 2026

### Trois annexes déportées, et le chapitre du stage réécrit

**Le mémoire passe de 236 à 170 pages.** Les annexes B (démonstrations du socle EVT), D (pièces
justificatives) et E (compléments aux chapitres du corps) sont sorties du document et vivent dans
`exploratory/memoire_cascade/materiel_complementaire/`, destinées à un dépôt numérique pérenne.
Une notice sans numéro ouvre la partie Annexes et explique le déport au jury. **L'adresse du dépôt
reste à renseigner** : le gabarit `https://LIEN_VERS_LE_DEPOT.com` est en clair dans les trois
fichiers maîtres.

**Les annexes conservées se relettrent** : A démonstrations de la cascade, B adaptations par
pilier, C protocole d'élicitation, D table des notations.

**Les 54 renvois orphelins passent par une macro et non par un `\ref`.** `\matcomp` est définie
dans les deux préambules et imprime « *(voir le Matériel Complémentaire en ligne)* ». Les phrases
hôtes ont été réécrites une par une pour rester grammaticales. Zéro `??` dans le PDF.

**Trois choses partent avec ces annexes** : deux des trois figures LUCY, la table des paramètres
et la description du dispositif de vérification. Le `README.md` du dossier déporté les liste, avec
ce qu'il faut pour recompiler ces annexes à part.

**Le chapitre 14, sur le stage, est réécrit en entier.** Registre strictement factuel : le
paragraphe « sept fois j'ai rédigé… » et les anecdotes de vérification sont supprimés, la section
« Ce que j'en retiens » est refaite sur trois points de méthode (traduire un texte réglementaire
en paramètres, séparer estimé, posé et non identifié, rendre un résultat vérifiable).
**Aucune mention d'outils d'intelligence artificielle générative** : le paragraphe du 16 septembre
est supprimé et ne doit pas revenir. L'encadrement est nommé, Hugo Rapior en entreprise et
Caroline Hillairet à l'ENSAE ; les répondants au formulaire de relecture restent non nommés. Le
chapitre ne publie plus aucun nombre.

Contrôles : `main_ensae` 170 pages, **1 débordement** (nouvelle ligne de base, contre 5 avant le
déport), 0 vbox, 0 annotation hors page, 0 page tournée, 0 `??`, harnais 1 434 sur 1 434 et hors
contrôle non déclaré à zéro sur tous les chapitres. `main` et `main_v2` compilent (7 et 0
débordements). Pages 135 à 137 et la notice relues à l'œil. `KADDOURI_Kelian_3A25.pdf` régénéré et
identique à `main_ensae.pdf`.

**La table des paramètres est revenue le soir même**, demande de Kélian. Elle forme l'annexe D à
elle seule (`chapitres/17b_table_parametres.tex`), a été retirée du fichier déporté et non
recopiée, et le chapitre 13 la cite de nouveau par un vrai `\ref`. Le mémoire repasse à
**172 pages**, harnais **1 490 sur 1 490**, ligne de base des débordements de retour à **5**, les
quatre de la table étant antérieurs et valant 2,47 pt chacun.

**Reste à faire par Kélian** : renseigner l'adresse du dépôt externe et y publier les trois
fichiers, puis recompiler.

## 17 septembre 2026

### P2-11 mené jusqu'au bout : le corps passe de 142 à 112 pages

**Kélian a validé la descente vers 110 pages.** Le principe est le même que pour les premiers
déplacements : chaque section du corps garde son titre, son label et un résumé de ses résultats
chiffrés, avec un renvoi ; le détail part dans une **nouvelle annexe E**, « Compléments aux
chapitres du corps » (`chapitres/21_complements_corps.tex`, appelée par les trois fichiers maîtres
après les pièces justificatives), rangée dans l'ordre des chapitres. **Aucun résultat, aucune limite
déclarée ni aucun nombre n'a été retiré du mémoire.** Les annexes E et F deviennent F et G.

Blocs déplacés, en quatre passes : détail de la lecture de marché LUCY et ses trois figures ; Bâle
III/IV, table comparative et limites de l'ORSA (cadre réglementaire) ; mesures des biais de taille
et de troncature ; règles du moteur et confrontation à ENISA ; énoncés développés des théorèmes des
valeurs extrêmes, lois asymptotiques et démonstration du quantile GPD ; détail de Hill contre MLE ;
règles de choix du seuil ; détail du backtest ; figures du corpus de post-mortems (les deux
relectures de praticiens sont résumées, l'annexe du protocole les porte) ; échelle de repli sur la
direction ; sensibilité aux probabilités de propagation (Sobol, tornado brut, gradation,
ablation, préprint) ; figure du benchmark réglementaire ; épreuve du réel (descente d'échelle,
mise à l'échelle proportionnelle écartée) ; contrefactuel et plafond de l'agrégation au capital
total ; dimensionnement du traité ; motif épistémique de l'étage de modèle et équivalence
Hawkes/cascade ; lecture ligne par ligne du registre des limites.

**Piège rencontré** : la seule formule mise en ligne dans un résumé (intervalle delta-méthode du
§5.2) a créé un débordement ; reformulée, retour à la ligne de base de 5. **Et une règle de
harnais tenue** : chaque résumé du corps garde la ligne `% SOURCES-SCRIPTS` des nombres qu'il
cite, chaque section d'annexe porte la sienne, et la section réglementaire de l'annexe est
déclarée hors script.

Contrôles : `main_ensae` 236 pages, corps 21 à 132, 5 débordements, 0 `??`, 0 vbox, aucune page
d'image seule ; harnais 2 357 nombres confirmés (les résumés reprennent des nombres de l'annexe),
aucun hors contrôle non déclaré ; deux pages rendues et relues ; fichier déposé régénéré.


### P1 et P2 du rapport de jury, traités en entier (commits f59d6e3 à la fin de journée)

**P1.** Interaction relue comme une composition presque multiplicative (script 100 : produit des
facteurs isolés 3,47 contre 3,34 publié) ; bibliographie complétée (58 entrées citées, Pineau et
Zuñiga retirés faute de vérification, entrées marquées TODO dans `references.bib` à compléter par
Kélian) ; note de synthèse avec une figure unique lisible (script 101, FR et EN) ; figures 9.1 et
8.1 reprises (scripts 30 et 40) ; **plaidoyer retiré** : vingt-quatre formules d'auto-justification
(« gage de rigueur », « il serait malhonnête », « Limites, sans détour »...) réécrites en énoncés
simples, aucun nombre déplacé.

**P2-11, le corps raccourci par déplacement en annexe D, à résultats constants.** Accord de Kélian.
Sept blocs sont passés du corps à l'annexe D, le corps gardant un résumé et un renvoi : la
dynamique du facteur systémique (`sec:dynamique-Y`), le quantile de la loi des configurations
(`sec:ann-quantile-configurations`), le détail du biais de narration (`sec:ann-biais-narration`),
les séquences ordonnées (le corps redisait `sec:ann-sequences`), les vérifications bayésiennes
(`sec:ann-bayes`), les graines du benchmark copule (`sec:ann-benchmark-graines`) et la précision
des postures (`sec:ann-postures`, avec la figure J2). **Corps 147 → 141 pages**, puis 142 avec les
ajouts de P2-12 à 14. **La cible de 110 n'est pas atteinte** : les blocs nommés par le rapport ne
pesaient que six pages. Candidats suivants si Kélian veut aller plus loin : la section de
sensibilité aux probabilités de propagation (§10.7), la mise en regard réglementaire (§10.9), le
défaut de calibration chiffré (§11.5), la lecture de marché LUCY de l'introduction.

**P2-12, les montants SAS sont NOMINAUX, et c'est mesuré (script 102).** La chaîne publiée lit
`Loss Amount ($M)` ; la base porte aussi `Current Value of Loss ($M)`, corrigée de l'inflation. Le
rapport des deux vaut 1,747 en 2004 et 1,025 en 2025 : **inflation implicite 2,19 % par an**. Rejouée
sur la valeur courante, la dérive de la médiane passe de 13,0 à 10,6 % par an (toujours
significative : l'inflation n'en explique que 17 %), et **la dérive de queue tombe de 4,00 à 2,00 %
par an et cesse d'être significative** (p = 0,211, 106 excès au seuil publié). La moitié de la
dérive de queue est donc monétaire. Le chapitre 4 **supposait** jusqu'ici les bases déjà
homogénéisées et déclarait l'hypothèse invérifiable : c'était la contradiction relevée entre les
pages 44 et 72. Réécrit au chapitre 4, paragraphe ajouté au backtest du chapitre 5, mention dans la
table de l'inventaire (chapitre 11). **Aucune recalibration** : le sens anti-conservateur de l'écart
déclaré ne change pas pour un capital en euros courants, seule sa lecture change.

**P2-13.** SCR(t) renommé en barre et nommé **moyenne de quantiles** pondérée par la loi d'état,
distincte du quantile du mélange (écart de 9,3 % mesuré sur les 32 configurations, script 77).

**P2-14, le « SCR » du titre : le titre est gardé**, il est inscrit sur les deux pages de garde et
porte le mot-clé du domaine. Le risque est traité à la première page de l'introduction, dans
l'encadré de la question centrale : quantile à 99,5 % de la charge annuelle, besoin de capital au
sens de l'ORSA, pas un SCR réglementaire. Le résumé le disait déjà.

Contrôles en fin de journée : `main_ensae` 230 pages, 5 débordements, 0 `??`, harnais 2 282 sur
2 282 sans hors contrôle non déclaré, fichier déposé régénéré.


### Rapport de jury simulé, puis corrections P0 (quatre commits, 0eb637b à 82026f3)

Kélian a demandé une évaluation de jury Prix SCOR, face au mémoire de Franck Dountio Zaboue. Note
rendue : 13/20 en l'état, 11,5 pour Franck, 16 à 17 atteignable après corrections. Les points P0,
tous traités ce jour :

- **La proposition 6.7 était fausse telle qu'écrite.** La co-occurrence ne dépend de W que par S
  **au premier ordre et sous amorce uniforme** ; la loi complète des ensembles touchés distingue W
  de sa transposée (fourche contre collisionneur, Verma et Pearl 1990, entrée ajoutée à la
  bibliographie). **Script 98** : lois exactes de la marche (moteur publié) et de la cascade
  indépendante, contrôlées contre `scr_engine` à 1e-16 ; sous W^T, la part des sinistres
  multi-piliers passe de 62,31 % à 50,77 %. Réécrits : proposition, preuve (annexe A), §6.9,
  §8.3 et encadré de thèse, résumé, notes de synthèse FR et EN, introduction, chapitre 9,
  annexe D.9, annexe E. **Le chapitre 12 gagne une quatrième exigence** : consigner l'ensemble des
  piliers touchés par incident.
- **Le moteur publié n'est pas la cascade de la définition 6.1** mais la marche auto-évitante ; la
  proposition 6.4 affirmait le contraire. Déclaré après la proposition (écart branchement −4 %,
  script 29).
- **Formule Standard** : le « forfait de 3 % des provisions » est requalifié en repère (branche
  provisions non-vie) ; l'écart au module publié (−8 % et +56 %) vient de l'approximation, pas du
  règlement. Équation du chapitre 2 labellisée `reg:eq:scrop`.
- **Multiplicateur de fréquence sourcé, script 99** : λ NC = 21,56 × 2,4875 = 53,62, parts
  Hackmageddon × centres des fourchettes S2 de `src/frequency/negbin.py`. Table au §7.3, qui passe
  à **quatre canaux** ; ligne ajoutée à la table D.4. **Conséquence** : les parts Hackmageddon
  entrent dans le moteur, contrairement à ce qu'écrivait le chapitre 4, corrigé.
- **ξ = 0,90 n'est pas le ξ du chiffre de tête** (0,5954) : corrigé dans D.4, la table 11.5 (ligne
  retirée des choix posés), la fin du chapitre 4 et l'ouverture du chapitre 10.
- **Contradictions levées** : ordre des chapitres (introduction 1.4, chapitre 7), −53 % contre 3,34,
  asymétrie « qui porte le résultat » contre co-occurrence, posture « ouverte » puis « retenue »,
  « six des dix » sens au §12.2, architecture des données du chapitre 4, populations 582 et 1 476,
  convergence avec ROOT dite indépendante, Change Healthcare, borne supérieure du gain de transfert.
- **Affirmations fausses corrigées** : facteur brownien et dispersion (§5.3.1), EVT et biais de
  survie (§4.2), écart ξ PRC / OpRisk (conversion en puissance, pas biais de taille), confusion
  entre registre d'information et notification d'incidents (§12.1), test OpRisk attribué au corpus
  de post-mortems (D.9).
- **Traces de versions retirées** : « ancien mémoire », colonne « mémoire (réf.) », table corrigée
  « migration pré-cascade », renvoi à `references.bib`, « la chapitre », titre courant du résumé.

Contrôles : **harnais 2 255 nombres, 2 255 confirmés**, aucun hors contrôle non déclaré ; quatre
versions aux lignes de base (5, 13, 4, 4), 0 « ?? », 0 vbox ; `main_ensae` à **227 pages**, notes
de synthèse toujours à quatre pages chacune ; `KADDOURI_Kelian_3A25.pdf` régénéré.

**Reste pour la suite, dans l'ordre du rapport** : P1 (réécrire l'interaction en multiplicativité,
facteur 3,34 contre produit des facteurs isolés 3,47 ; bibliographie ; note de synthèse lisible ;
figures 9.1(d) et 8.1(b)(c) ; plaidoyer), puis P2. **Et la v3 ne reçoit pas ces corrections** :
elle lit sept chapitres dans `chapitres_v3/`, des copies. Arbitrage à faire par Kélian : la
retirer, ou reporter les corrections.

### La seconde réponse de relecture, retrouvée et intégrée

**Hugo Rapior a validé la reproduction des trois figures LUCY** : le point est clos, le script 97
reste un repli sans usage prévu.

**La réponse de Mehdi Cherkaoui, du jeudi 10 septembre, vivait dans la feuille créée le 3 août**,
et non dans celle du formulaire en diffusion : il avait reçu un ancien lien. Le connecteur Google
Drive, reconnecté, a permis de lire les **douze** feuilles homonymes, dont la date de modification ne
suit pas les réponses. Trois lignes en tout : la première répondante (8 septembre), un test de
Kélian (9 septembre, champs « xw ») et Mehdi. Nathanaël n'a pas répondu.

**Ce qu'elle apporte.** Sur la phrase qui oppose la contagion à la cause commune, Mehdi avance de
lui-même l'explication concurrente (manque de ressources, transformation mal pilotée, architecture
vieillissante) et parle de dépendances plutôt que de causalité : c'est la corroboration la plus
nette de la frontière d'identifiabilité. Il **conteste deux phrases**, la gouvernance source pure et
la gestion des incidents puits, en décrivant des boucles de rétroaction. Lecture écrite au mémoire :
la plupart de ses exemples sont une rétroaction corrective, qui relève des états de conformité et non
de la propagation de pertes ; un seul est une dégradation en retour, de la gestion des incidents vers
le partage d'information ; et le capital publié n'est pas déplacé, l'ensemble admissible ne fixant
aucune direction. Il conditionne les indicateurs et le registre à des règles de qualification, et
signale la gestion des changements et des vulnérabilités comme déclencheurs transversaux absents du
modèle.

**Où c'est écrit** : encadré du chapitre 09, section `sec:relecture-praticien` de l'annexe E (cinq
paragraphes nouveaux et un statut réécrit), paragraphe du chapitre 19. Répondant non nommé, comptes
en lettres, aucune recalibration.

Contrôles : harnais sans nombre hors contrôle non déclaré sur les trois chapitres, quatre versions
aux lignes de base (5, 13, 4, 4), 0 vbox, 0 « ?? », `main_ensae` à 223 pages, pages relues à
l'œil, `KADDOURI_Kelian_3A25.pdf` régénéré et identique au dernier `main_ensae.pdf`.

### Deux comptes du corpus de post-mortems rendus lisibles

**Il n'y avait pas d'erreur, mais une ambiguïté.** Le chapitre 09 porte deux corpus : l'initial
(script 53, sept rapports, dix-sept transitions, z = +3,93), qui trace la figure 8.3, et l'étendu
(script 59, dix rapports, vingt-deux transitions, z = +5,12), que cite la note de synthèse. La
légende de la figure citait le premier sans le nommer, et le tableau « La frontière, en trois
niveaux » ne retenait que lui alors que le signal se renforce sur le second. La légende nomme
désormais le corpus initial et renvoie à l'étendu, et le tableau donne les deux (section rattachée
au script 59 en plus de 55 et 64). Chapitre 09 à 180 nombres sur 180, quatre versions aux lignes de
base, fichier déposé régénéré.

## 16 septembre 2026

### Le soir, tard : le mémoire prêt au dépôt, et ce qui a changé depuis l'audit ENSAE

**Le fil de la soirée est parti d'une question, « est-ce qu'il passe ? », et de deux
comparaisons.** Le mémoire a été comparé à un mémoire cyber publié par l'Institut (A. Ranguin,
ISUP, 2024), puis au mémoire de **Franck Dountio** (ENSAE, soutenu le 18 mars 2026, même cabinet,
même tuteur, Caroline Hillairet au jury), seul précédent validé pour cette filière. Verdict : au
fond actuariel le mémoire est au-dessus des deux ; le format et les pièces d'accueil étaient en
dessous. Tout ce qui suit en découle.

**Trois défauts de fond trouvés en relisant les pages qu'un jury lit en premier.** Le résumé et la
conclusion ne citaient pas le chiffre de tête ; la conclusion écrivait la queue de sévérité à
« ξ ≈ 0,9 », valeur du pire cas posé, au lieu de 0,5954 ; et elle parlait de « rejet » du Hawkes
et d'un panel « à constituer ». Résumé, introduction (encadré « Le résultat en bref » et guide de
lecture) et conclusion portent désormais le chiffre, son statut non réglementaire, l'interaction
de 35 %, le seuil de la fréquence, le fait que g est posé mais que seul son ordre compte, et le
backtest.

**Trois travaux sur les mêmes sources n'étaient pas cités** : Ranguin (2024), Kher, Lopez et
Rapior (2023), l'article du tuteur, dont l'entrée bibliographique était un gabarit à auteur « ? »,
et Dountio (2026). Deux paragraphes de l'état de l'art les positionnent.

**Ce qui a été repris du mémoire de Franck, dans `main_ensae` :**

- **notes de synthèse en tête**, quatre pages en français et quatre en anglais au lieu de deux et
  deux en fin, sur son plan : contexte, objectif, démarche en six étapes, tableau des quatre
  canaux, figure S24, résultats, limites, recommandations, conclusion. Elles portaient une erreur
  corrigée au passage : la matrice y était dite « calibrée » au lieu de « posée à dire d'expert,
  corroborée par un corpus » ;
- **un glossaire de sigles** en tête (`00_glossaire.tex`) ;
- **une section « Le risque cyber en quelques cas »** en début d'introduction, NotPetya, MOVEit et
  CrowdStrike reliés aux piliers, sans chiffre, partagée par les quatre versions ;
- **un paragraphe d'usage de l'IA générative** au chapitre 19, seul chapitre à la première
  personne. Il engage Kélian personnellement : à relire ;
- **les trois figures du rapport LUCY 2026 remises dans l'introduction**, retirées le 15 lors de
  la coupe de la section marché, avec une lecture courte chacune, et la figure primes et sinistres
  en tête de la note de synthèse. Tous les chiffres ajoutés sont imprimés par le script 63.

**L'annexe est passée de 58 à 50 pages, à résultats constants**, sur demande de Kélian. Neuf
sections réécrites (détail dans `CLAUDE.md`). Rien n'a été retiré de ce qui est un résultat, une
limite déclarée ou un renvoi. Deux garde-fous rencontrés : la tolérance du harnais doit rester en
formule hors texte, sinon le paragraphe déborde de 32,7 pt ; et la section du test inversé doit
citer le script 84, faute de quoi cinq nombres sortent du contrôle.

**Dépôt ENSAE tranché** : mémoire **non confidentiel**, dates de stage confirmées, fichier
`KADDOURI_Kelian_3A25.pdf` généré.

**Script 97, en repli seulement.** Il redessine les trois figures LUCY depuis la transcription de
`config.py`, avec trois contrôles d'identité rejoués. Le mémoire ne l'appelle pas : Kélian garde
les figures du rapport, dont il est co-auteur. Deux défauts de mise en page connus, à corriger avant
tout usage.

**La réponse de Mehdi Cherkaoui au formulaire est arrivée et n'est pas récupérée**, faute d'accès :
connecteur Drive expiré puis retiré, lien Teams inaccessible sans connexion. C'est la première
chose à faire à la reprise.

**Note donnée au mémoire ce soir-là, à titre indicatif** : 16,5 sur 20. Ce qui coûte le plus : les
paramètres posés (matrice, niveaux de g), le niveau non utilisable à l'échelle d'une entité, la
densité. Ce qui fait monter : la traçabilité, l'honnêteté des limites, les résultats négatifs
publiés avec leur motif.

Contrôles en fin de soirée : quatre versions recompilées, débordements aux lignes de base
(5, 13, 4, 4), 0 vbox, 0 annotation hors page, 0 « ?? », harnais 2 208 sur 2 208, tout poussé.


### Le soir, en dernier : fondateur, « et », et ce qui reste avant le dépôt

**Le nom du fondateur est renseigné** : les remerciements impriment « Ali BEHBAHANI » et non plus
« Ali [NOM À COMPLÉTER] ». **La bibliographie passe en français** par un style local,
`plainnat-fr.bst`, copie de `plainnat` qui ne diffère que par la conjonction entre auteurs et par
l'absence de virgule anglaise avant elle : « Hillairet et Lopez », « David Pym et Julian
Williams ». Les quatre fichiers maîtres l'appellent. Les « and » restants sont dans des titres
anglais de revues et dans une catégorie bâloise, et doivent rester.

**La confidentialité est laissée à plus tard**, décision de Kélian : elle appartient à Nexialog
et fixe le nom du fichier déposé.

**Puis la bibliographie est corrigée entièrement**, sur relevé du PDF imprimé : accents absents dans
trois entrées jusque dans le nom des auteurs (« Autorites europeennes », « Reglement
d'execution »), noms propres mis en minuscules par le style (« hawkes », « pareto », « united
states », « lucy », « Solvabilité ii », « dora »), formules anglaises du style (« Technical
report », « In », « editors », « number 28 in »), mois imprimés en chiffres (« Marsh, 4 2025 »), et
espace française devant les deux-points des références anglaises (« arXiv :2311 », « doi :
10.1016 »), neutralisée par `\NoAutoSpacing` autour de la bibliographie. Vingt-cinq motifs de
défaut recherchés sur le nouveau PDF, tous à zéro ; les trois pages relues à l'œil. Aucune donnée
bibliographique n'est inventée, seules l'orthographe, la casse et la mise en forme changent.

**`CLAUDE.md` porte désormais en tête un bloc « À lire d'abord »** avec l'état de dépôt, le
registre d'écriture fixé par la révision et le style bibliographique, et ses chemins du PC ont
été corrigés : l'ancien en-tête présentait encore comme livrable ENSAE le rapport de trente
pages, qui ne part plus.

Contrôles : quatre versions recompilées, débordements à leurs lignes de base (5, 13, 4, 4),
0 vbox, 0 annotation hors page, 0 « ?? ».

### Le soir : la version ENSAE passe au format de l'école

**CE QUI A CHANGÉ DANS LA CONSIGNE.** Courriel de Fallou : la limite de trente pages ne vaut pas
pour le mémoire déposé à l'ENSAE, qui est « une version à peu près définitive du mémoire
Institut des actuaires ». La police et l'interligne restent imposés, Times New Roman 12 et 1,5.
La version déposée était en Palatino 11 et interligne 1,05, héritée du préambule de la v2.

**LE PRÉAMBULE ÉTANT PARTAGÉ, LE FORMAT PASSE PAR UN INTERRUPTEUR.** `main_ensae.tex` définit
`\formatensae` avant d'appeler `preambule_v2.tex`, qui charge alors Times et l'interligne 1,5.
Les trois autres versions ne définissent pas la commande : leurs pages et leurs polices sont
inchangées, ce qui a été contrôlé sur les PDF. Deux arrêts de compilation en chemin, tous deux
connus de `newtxmath`, qui exige `amsmath` et `amsthm` avant lui et refuse `amssymb`.

**UNE POLICE CHOISIE POUR UNE RAISON QUI NE SE VOIT PAS.** La Times retenue est `newtx`, et non la
Times New Roman du système : cette dernière n'a pas de vraies petites capitales, et les soixante
acronymes composés en `\textsc{}` à partir de minuscules (`scr`, `dora`, `tic`...) se seraient
imprimés en minuscules dans le texte. Le PDF embarque TeX Gyre Termes, Times métriquement.

**DEUX DÉBORDEMENTS ANCIENS, RENDUS VISIBLES PAR LE CORPS 12, SUPPRIMÉS À LA SOURCE.** Une équation
à trois membres du chapitre 09, passée sur deux lignes, et une définition en ligne insécable au
chapitre 17, passée en formule centrée. **La première tentative sur la seconde visait la mauvaise
formule** : le paragraphe en porte deux, et c'est le relevé des fins de ligne sur la page
imprimée, non la lecture du source, qui a désigné la bonne. Les deux corrections valent pour les
quatre versions et abaissent leurs lignes de base : **ENSAE 5, v1 13, v2 4, v3 4**.

**Contrôles.** `main_ensae` 219 pages dont 156 de corps ; les notes de synthèse tiennent en deux
pages chacune, une première lecture en annonçant trois pour la note anglaise, faute d'avoir tenu
compte du décalage d'une page entre les folios du sommaire et les pages du PDF. Harnais inchangé,
2 219 nombres confirmés. 0 vbox, 0 annotation hors page, 0 « ?? » dans les quatre PDF. Couverture,
page de texte courant, page à tableau et page de l'équation corrigée rendues et relues.

**Ce qui reste avant le dépôt, et qui appartient à Kélian** : la décision de confidentialité de
Nexialog, qui fixe le nom du fichier (`KADDOURI_Kelian_3A25.pdf` ou `_CONF`), et le courriel au
service des stages. Le nom du fondateur et le « et » de la bibliographie ont été traités le même
soir, voir l'entrée ci-dessus.

Kélian a déposé les deux fichiers de `data/raw` sur le PC, ce qui débloque seize scripts d'un
coup, et la journée s'est terminée sur un axe de validation que le mémoire annonçait sans
l'avoir tenu.

### La révision stylistique des vingt-deux chapitres

Demande de Kélian : réviser le mémoire entier sur le style, l'orthographe et la rédaction, à
l'étalon des mémoires de l'Institut ayant obtenu les meilleures distinctions. Consigne de
méthode en cours de route : cesser de demander validation et appliquer ce qu'un actuaire
certifié aurait fait, sur tous les fichiers.

**LES DEUX CHAPITRES MIGRÉS DE L'ANCIEN MÉMOIRE ÉTAIENT LES SEULS À TRAHIR LEUR ORIGINE.** Un
relevé de la première personne le montre sans discussion : $8$ occurrences pour $2\,312$ mots au
chapitre 04 et $9$ pour $1\,722$ au chapitre 03, contre $0{,}1$ à $0{,}7$ pour mille dans les
vingt autres fichiers. Le reste du document était déjà à la voix impersonnelle des mémoires
publiés ; il s'agissait d'y aligner ces deux-là, plus une vingtaine d'occurrences résiduelles
ailleurs. **Le chapitre 19 n'est pas touché** : il n'est appelé que par `main_ensae`, et le
barème de l'école exige explicitement le recul personnel.

**LE DÉFAUT DE REGISTRE LE PLUS VOYANT ÉTAIT UN ENCADRÉ AU \og{} JE \fg{}.** Le chapitre 03
portait, entre guillemets, un paragraphe de défense orale : \og{} Je n'invente pas une nouvelle
loi de sévérité... Ma contribution est le mécanisme... que je traduis en capital \fg{}. Un
mémoire de l'Institut n'argumente pas à la première personne du singulier, et le titre de
l'encadré, \og{} La revendication de nouveauté, défendable \fg{}, se donnait en outre un
satisfecit. Le fond est conservé, la voix change. Deux passages du même type au chapitre 13,
dont un \og{} je sais précisément de quoi mon SCR dépend \fg{}, ont reçu le même traitement.

**SIX DÉFAUTS DE FOND, QUE LE HARNAIS NE POUVAIT PAS VOIR.**

- **L'abstract anglais contredisait le résumé français.** Le français donne un facteur $22$ pour
  la seule source de sévérité et $41$ en y ajoutant l'échelle de fréquence ; l'anglais donnait
  \og{} a factor of forty with the severity source \fg{}, soit le mauvais facteur attribué à la
  mauvaise cause. Le harnais ne lit pas un nombre écrit en lettres. Un jury bilingue, si.
- **\og{} La base sera exhaustive \fg{}** annonçait le chapitre 05 à propos du futur registre
  DORA. C'est faux : la notification ne porte que sur les incidents \emph{majeurs}, donc
  au-dessus d'un seuil de matérialité. Le biais de déclaration change de nature, il ne disparaît
  pas. Le passage le dit maintenant.
- **Deux passages de survente**, au même endroit : \og{} prend toute sa valeur \fg{}, \og{} le
  moteur de calcul absorbera ces entrées qualifiées \fg{}, \og{} un SCR cyber d'une précision
  inédite \fg{}. La note d'honnêteté du dossier dit exactement l'inverse.
- **\og{} élicitée \fg{}** qualifiait la matrice de contagion aux chapitres 02 et 03, alors que
  l'annexe du protocole de Cooke dit elle-même que l'élicitation a été \emph{préparée et non
  exécutée}. La matrice est posée à dire d'expert, puis bornée.
- **Une hypothèse lourde posée en passant** au chapitre 05 : \og{} nous assumons que les bases
  commerciales intègrent une homogénéisation monétaire \fg{}, sans son sens d'erreur. Elle est
  désormais déclarée avec sa direction : si elle est fausse, elle minore la queue et le capital.
- **Le compte des cinq mouvements ne tombait pas** au chapitre 02 : le quatrième empaquetait la
  trajectoire et les résultats, si bien que \og{} les deux derniers mouvements, la trajectoire et
  les résultats \fg{} ne désignait pas les deux derniers. Découpage rétabli.

**TROIS DÉFAUTS DE SYNTAXE OU DE STRUCTURE.** Deux pronoms sans antécédent au résumé, dont un
\og{} il \fg{} qui renvoyait grammaticalement au schéma \textsc{veris} là où c'est le mémoire qui
caractérise l'ensemble des matrices. Une référence rompue au chapitre 04, où une phrase sur le
mémoire s'était intercalée entre la description des modèles AMA et le \og{} S'ils offraient \fg{}
qui y renvoie. Et un `\textbf` **coupé en deux par un commentaire** `SOURCES-SCRIPTS` inséré en
milieu de macro au chapitre 06 : cela compilait, mais toute édition ultérieure de ce bloc aurait
cassé la commande.

**LE GRAS DANS LE CORPS, ET POURQUOI LES PREMIERS RELEVÉS ÉTAIENT FAUX.** Le document porte $564$
occurrences de `\textbf`, dont $219$ en cellules de tableau et $64$ en tête de paragraphe, toutes
légitimes. Les premiers comptages annonçaient cinq gras en pleine prose ; il y en avait $84$. Le
motif de l'erreur est instructif : un gras qui **ouvre une ligne du source** n'ouvre pas pour
autant un paragraphe, le retour à la ligne de la source n'ayant aucune valeur typographique.
Règle appliquée, sur l'étalon des mémoires primés où le gras ne sert qu'aux têtes : un syntagme
d'un ou deux mots devient de l'italique, marque des termes techniques ; une clause de trois mots
ou plus perd son balisage, la structure de la phrase la portant déjà ; un nombre se dégraisse
sans prendre l'italique, qui ne marque pas une quantité. Soit **$44$ passages en italique et
$36$ dégraissés**, plus huit `\mathbf` qui mettaient un chiffre en gras au milieu d'une phrase.

**DIVERS DE TYPOGRAPHIE ET DE NOMENCLATURE.** Le sigle `ROI` désignait le \emph{Registre
d'Informations} au chapitre 04 et le retour sur investissement au chapitre 12b : le premier
usage, unique, est retiré. `ICT` subsistait trois fois contre treize `TIC`, la forme du règlement
en français. Six nombres du chapitre 03 étaient hors mode mathématique, seuls du document à
l'être. Dix espaces de fin de ligne retirées. Et la frontière Pilier~1 / Pilier~2 est tenue là où
elle ne l'était pas : \og{} une trajectoire de SCR \fg{} devient \og{} une trajectoire de besoin
de capital \fg{}, aucun module DORA n'existant en Formule Standard.

**L'OUTIL, ET LE GARDE-FOU QUI COMPTE.** Les corrections passent par `revision.py`, qui vérifie
chaque ancre **unique** avant de l'appliquer et compare, avant et après, le compte des commandes
de structure (`\section`, `\begin`, `\end`, `\label`, `\ref`, `\caption`, `\item`, `\figover`...).
Si l'une bouge sans avoir été déclarée, **rien n'est écrit**. Un compte de mots ne sait pas
distinguer un resserrage d'une troncature ; celui-ci le sait, et il a d'ailleurs refusé deux
écritures, dont une qui n'ajoutait qu'un renvoi de chapitre légitime.

**Contrôles.** Harnais **$2\,219$ nombres, $2\,219$ confirmés, $100\,\%$**, hors contrôle non
déclaré à zéro sur les dix-neuf chapitres. `main_ensae` $189$ pages dont $135$ de corps, `main`
$172$, `main_v2` $178$, `main_v3` $151$ : la révision rend **une page à chaque version**, sans
qu'aucun contenu soit retiré. Débordements exactement aux quatre lignes de base ($6$, $15$, $6$,
$5$), $0$ vbox, $0$ annotation hors page, $0$ page tournée, $0$ \og{} ?? \fg{}. Une page a été
rendue en image et relue pour juger le rendu après la purge du gras.

### `data/raw` arrive, et la première chose à faire est de ne rien croire

**LES DEUX FICHIERS NE SONT PAS CEUX QU'ON ATTENDAIT, ET L'UN A CHANGÉ DE FORMAT.**
`SAS_OpRisk_Global_Data_June_2026.xlsx` est bien là, mais la chronologie PRC arrive en `.csv`,
le format que `CLAUDE.md` attribuait au Mac, quand tous les scripts codaient en dur le `.xlsx`.
La règle du dossier interdit de fabriquer un format depuis l'autre, et elle a raison ; mais elle
n'interdit pas de **lire celui qui est là**, à condition de le prouver. La preuve est venue en
deux temps : le `.csv` donne **exactement 15 053 incidents** à `total_affected > 0` sur
2019-2025, le compte que publient les sorties versionnées 21, 22 et 62 ; et les scripts 21, 22,
35 et 62 relancés dessus reproduisent leur sortie **ligne pour ligne**. Un résolveur de chemin
partagé, `chemin_prc()` dans `src/severity/prc_analysis.py`, prend désormais le format présent,
`.xlsx` d'abord parce que c'est lui qui a produit les sorties versionnées.

**LE PREMIER CONTRÔLE À PASSER N'EST PAS LA FIGURE, C'EST LA SORTIE.** Onze scripts ont été
relancés avant toute modification, et **neuf reproduisent leur fichier versionné au caractère
près** : 16, 21, 22, 41, 44, 47, 48, 51, 57, 60, 78. C'est ce contrôle, et lui seul, qui
autorisait à toucher ensuite à leurs figures. Les deux autres ont révélé des **sorties
versionnées périmées**, et aucune n'était une dérive de calcul :

- `46.txt` ne portait pas les trois lignes que le script imprime depuis le 10 août sur le bruit
  de la VaR prédictive. Ajout pur, aucun nombre publié ne bouge ;
- `62.txt` portait des séparateurs de milliers que le commit `780cd0d` avait retirés du script
  **pour le harnais**, sans régénérer la sortie. Même valeur, `2 150,4` contre `2150.4`.

**Et un troisième écart, celui-là réel, sur le script 35.** Son bootstrap tirait avec
`RNG.choice` dans l'ordre du tableau : deux exports de la même base rangés autrement donnaient
deux intervalles, `[+1,067 ; +1,268]` contre `[+1,072 ; +1,268]`, pour un estimateur ponctuel
identique au millième. Un bootstrap porte sur un **multi-ensemble**, pas sur un ordre : le
tableau est trié avant tirage, la sortie devient la même sur les deux postes, et l'intervalle
publié au chapitre 09, arrondi à `[+1,07 ; +1,27]`, ne bouge pas.

### Les figures que `data/raw` débloque

Treize figures étaient gelées faute de données. **Dix sont reprises** : les cinq titres à code
interne restants sont retirés (J2, J4, J7, S34, Z14), plus Z6 et S16 ; S10 perd un titre général
qui portait le **nom de la variable du code**, `SCR_DORA`, et repasse en français accentué ;
J3 descend de 10,3 à 8,2 cm, la dernière figure au-dessus de la limite de 9. Les chevauchements
trouvés en les regardant une par une ont été corrigés sur J2, J4, N2, S20, S21, S34 et Z14.

**Deux défauts qui ne sont pas de mise en page, et qui comptent davantage.** Le titre du panneau
(a) de Z14 nommait **« le registre DORA de Mehdi »** : un prénom dans une figure d'un mémoire que
l'Institut met en ligne. Et deux figures portaient encore un renvoi de script dans l'image même,
`(script 46)` sur J4 et `(08g)` sur Z14, alors que le PDF n'en porte plus nulle part depuis le
15. Les trois sont retirés. Même famille pour la légende LaTeX de S34, qui annonçait des barres
« en orange » quand elles sont cramoisies depuis le passage à la charte : le script avait corrigé
son propre titre pour ce motif, la légende était restée en arrière ; elle renvoie désormais à la
légende de la figure, qui ne peut pas se périmer avec la palette.

**S17 a été annoncée à tort comme restée à moitié.** Son titre général était en fait retiré
dans le même commit que ceux de Z6 et S16 (`fba5bd7`), ce qu'un contrôle du fichier versionné
aurait montré avant de l'écrire. La figure gardait en revanche les défauts qu'avait S10 avant sa
reprise, et ils sont corrigés le même jour : texte entièrement désaccentué alors que la légende
LaTeX est accentuée, nom de variable `Delta_DORA` sur un axe, étiquettes d'abscisse illisibles
dans deux panneaux (« gamma = 0.50gamma = 0.68 »), valeurs coupées par le cadre, et une légende
qui traversait les barres. Sortie du script inchangée, 5,4 cm imprimés.

### `96` : le moteur d'agrégation cesse d'être le seul étage non contrôlé

Kélian a demandé ce qu'il y avait à prendre dans `memoire/main.pdf`, la version abandonnée
pré-cascade, pour comparer des méthodes. Il y avait trois choses ; il en a retenu une, et c'est
celle qui ferme un trou.

**LE TROU ÉTAIT DÉCLARÉ DANS LE MÉMOIRE LUI-MÊME.** L'encadré « Oui, chaque brique a des
alternatives » du chapitre 13 liste les concurrents par axe, dont « agrégation (formule standard,
**Panjer**) », puis affirme « on a testé les concurrents les plus sérieux ». Sur cet axe-là
c'était une promesse : tout ce que le mémoire valide, il le valide **contre la donnée**, et rien
ne regardait la machine qui transforme une loi de fréquence et une loi de sévérité en un quantile
annuel. Un diagnostic de convergence n'y supplée pas, il dit **stable** et non **juste**.

**L'ancien mémoire documente la méthode complètement** : dérivation de l'approximation par perte
unique en annexe A.3, récursion de Panjer et le motif de ne pas l'employer en A.4, algorithme
FFT en quatre lignes en annexe C. Et surtout, son annexe D montre que **sa calibration de
sévérité OpRisk est exactement celle qui est gelée aujourd'hui** (ξ = 0,595, σ = 57,97,
u = 20,03, 91 excès, VaR mono-perte 663) : la transposition ne touche donc pas au gel.

**L'adaptation rend le résultat plus fort que l'original.** L'ancienne version devait restreindre
sa comparaison à sa brique dominante, parce que sa surcharge systémique multiplicative faisait
sortir la charge de la classe composée. Le modèle actuel n'a pas ce défaut : la charge annuelle
est **exactement** une somme composée, dont la génératrice du nombre de pertes non nulles s'écrit
en forme fermée en composant la binomiale négative des amorces, la loi exacte des piliers touchés
et l'amincissement par le seuil. La triangulation porte donc sur **les 6 049 et 20 188 M€
publiés eux-mêmes**.

**Le résultat, et sa lecture.** Inversion de Fourier 5 945 et 19 890, perte unique au second
ordre 5 448 et 18 632, au premier 4 989 et 14 933. L'écart de l'inversion vaut −1,7 et −1,5 % en
relatif, **mais 0,75 et 0,59 erreur type de la référence**, donc **il n'est pas résolu** : deux
chemins qui ne partagent ni code ni aléa ne se séparent pas à la résolution disponible, ce qui
est le meilleur résultat que ce contrôle pouvait rendre. Ne jamais citer le −1,7 % sans le bruit
qui l'encadre, il se lirait comme un désaccord.

**Un contrôle croisé gratuit est tombé en chemin.** La fonction qui reconstruit la loi du nombre
de piliers touchés retombe **au dix-millième** sur les nombres du script 74 : 1,3799 pour 1,380
et 31,15 % à l'état conforme, 1,9311 pour 1,931 et 62,31 % à propagation seule. Elle a aussi
démenti un commentaire écrit d'avance, qui comparait le 1,931 à l'état non conforme **complet** :
celui-ci vaut 2,436, l'écart venant du canal d'accumulation et non de la propagation. Septième
fois que la sortie corrige une prose écrite avant elle.

**Les deux pièges numériques sont mesurés, pas supposés.** Le repliement de la transformée
circulaire, qui sur une queue en ξ = 0,60 renverrait la masse du bout de grille dans les petits
montants et gonflerait le quantile : masse résiduelle 1,65·10⁻⁸, quatre ordres de grandeur sous
le niveau de dépassement. Et la discrétisation par les masses et non par la densité, contrôlée
contre la moyenne analytique à 0,063 % près.

**Contrôles.** `main_ensae` 190 pages dont 136 de corps, `main` 173, `main_v2` 179, `main_v3`
152 ; débordements exactement aux quatre lignes de base (6, 15, 6, 5), 0 vbox, 0 annotation hors
page, 0 page tournée, 0 « ?? » dans les quatre PDF. Harnais **2 217 nombres, 2 217 confirmés,
100 %**, 0 hors contrôle non déclaré sur les dix-neuf chapitres.

## 15 septembre 2026

Journée sur `main_ensae`, qui devient le document déposé. Trois demandes de Kélian, et la
deuxième a cassé la compilation avant d'être réparée. Le soir, la passe des figures, reprise
depuis le PC après l'échec en 429 de la veille.

### Le soir : les figures, et le mémoire perd huit pages sans perdre une phrase

**LE DÉFAUT DE FOND ÉTAIT `\figcle`.** Huit figures étaient posées par cette macro, qui les
isole seules sur une page et les agrandit jusqu'à 0,88 fois la hauteur du texte. D'où les pages
que Kélian a signalées : une image de 22 cm, un grand blanc, et une petite matrice perdue au
milieu. **`\figcle` ne sert plus nulle part dans le mémoire**, et l'agent `verificateur-figures`
l'interdit désormais par sa première directive.

**Ce que les figures sont devenues.** Z11 passe de 21,9 à 7,3 cm, Z17 de 21,9 à 6,4, S19 de
21,9 à 6,0, Z18 de 21,0 à 6,2, Z\_identification\_partielle de 16,2 à 8,8, Z2 de 16,2 à 8,6 ;
Z20 et Z22 quittent leur page flottante. Les colonnes de panneaux sont retracées en lignes.
**Une seule figure du document dépasse encore 9 cm, J3 à 10,3**, et son script exige le fichier
OpRisk absent de ce poste.

**22 TITRES CODÉS RETIRÉS dans 21 scripts.** Un mémoire publié par l'Institut ne porte pas
« Z19 : » ni « S24 : » en tête d'une image : c'est un code de laboratoire, et la légende LaTeX
porte déjà le titre. Chaque figure a été régénérée et **sa sortie standard comparée à
`sorties_verif` : identique au caractère près**, sur les 21 scripts.

**S24 portait un défaut invisible dans son code, et il valait la peine d'être cherché** : le
script enregistrait **sans `bbox_inches="tight"`**, si bien que tout texte dépassant du cadre
était coupé. Le titre du panneau (c) et son intitulé d'axe l'étaient. La règle du projet dit
« toujours `bbox_inches="tight"` » ; ce script y échappait.

**TROIS FIGURES SUPPRIMÉES**, sur demande de Kélian d'écarter ce qui pose trop de problèmes pour
ce que cela apporte. `M_faisabilite` (jamais citée, ne se régénère que sur le Mac, seule figure
restée à l'ancienne palette), `S32_tornado_normalise` (jamais citée, tableau voisin donnant les
mêmes élasticités) et `S22_entites_reelles` (jamais citée, 22 cm, script bloqué par l'absence de
`data/raw`, et la section porte déjà le tableau des quatre entités). **`Z14` a été épargnée
parce qu'elle est citée** : le script de suppression refuse toute figure dont un `\ref` dépend.

**LE POSTE N'A PAS `data/raw`, ET CELA DÉCIDE DE CE QUI EST FAISABLE ICI.** Deux fonctions
seulement lisent la donnée brute, `oprisk_losses` et `oprisk_excesses` ; les scripts qui les
appellent ne peuvent pas régénérer leur figure. **Restent donc à reprendre sur un poste qui a
les données** : Z6, J2, J4, J7, S10, Z14, S16, S17, S20, N2 et J3, qui portent encore un titre
ou un code en dur. Ne pas modifier leur script ici : ce serait le désynchroniser de son image,
exactement l'état qu'a laissé la session interrompue.

**Deux défauts de mise en page corrigés au passage** : les espaces parasites « ( figure 8.2) »
et « ( figure 10.3) », laissées par les commentaires `SOURCES-SCRIPTS` insérés en milieu de
phrase (un `%` en fin de ligne les supprime), et un renvoi vers l'équation de Hill qui restait
non résolu dans la v3, où la section qui la définit est retirée.

**Contrôles.** `main_ensae` 187 pages, `main` 171, `main_v2` 177, `main_v3` 150 ; 0 erreur,
0 vbox, 0 annotation hors page, 0 page tournée, 0 « ?? » dans les quatre PDF, débordements à la
ligne de base partout. Harnais 2 157 nombres, tous confirmés.

**Piège d'environnement, à savoir avant de relancer un script sur ce poste.** Le `.venv` ne
trouvait pas `ffi.dll`, d'où « scipy install broken » et l'échec de `pip`. Un fichier
`zz_dll_ffi.pth` dans `.venv/Lib/site-packages` ajoute le dossier de DLL au démarrage et règle
les deux. PyMuPDF y est installé, ce qu'exige `carte_figures.py`. Et `memoire\tectonic.exe`
n'existe pas ici : le binaire est `C:\Users\kelia\miniconda3\Library\bin\tectonic.exe`.

### `6517607` : les renvois de script sortent du PDF

Demande : « enlève tous les scripts + chiffres du mémoire, ce n'est pas commun ». C'est juste, un
mémoire publié par l'Institut ne porte pas de lignes « Sources : scripts 43 et 68 » ; imprimées,
elles ont l'air de notes de laboratoire.

**Le problème était que ces lignes font tenir le harnais.** C'est par elles qu'une section est
rattachée à ses scripts, et sans rattachement la couverture tombe de 100 % à zéro : plus aucun
nombre publié n'est contrôlé. Le retrait a donc été précédé d'un ajout à `verif_chiffres.py`, qui
lit désormais un **second canal**, le commentaire `% SOURCES-SCRIPTS: NN`. 165 citations
déplacées, 141 en ligne autonome et 24 en fin de légende. Harnais inchangé après coup, **2 132
nombres, 2 132 confirmés, 100 %**.

**LE DÉGÂT, ET IL FAUT LE CONNAÎTRE.** La première version du script avalait les lignes suivantes
jusqu'au point final, sans regarder ce qu'elle avalait. Une ligne de sources posée **à
l'intérieur** d'une légende lui a fait manger `\label`, `\end{figure}`, `\begin{cle}` et un
paragraphe entier, sur quatre blocs de `12_resultats` et `12b`. La compilation s'est arrêtée sur
`File ended while scanning use of \caption@xdblarg`, et le message ne désigne pas le fichier
fautif : il pointe la ligne d'`\input` du fichier maître. Ce qui a permis de trouver l'endroit est
le **diff de suppression**, `git diff -U0 | Select-String '^-[^-]'`, exactement le piège que
`CLAUDE.md` documente depuis août et qui a mordu une cinquième fois.

**Le garde-fou qui remplace la prudence.** Le script refuse maintenant de franchir une commande
structurelle, exige que le bloc consommé ait ses **accolades équilibrées**, et compare les comptes
de `\begin`, `\end`, `\label` et `\caption` avant et après : si la structure bouge, **rien n'est
écrit** et le fichier est signalé. Il a alors refusé de lui-même les quatre blocs qui avaient
cassé, et la branche légende les a traités correctement.

### La lecture de marché revient, en 1,84 page

Elle avait été coupée entièrement le 14 septembre (435 lignes, 3 640 mots, 7 sous-sections).
Kélian en a redemandé « une ptite partie, 2 pages max ». Ce qui est revenu est ce qui **travaille
pour le mémoire**, et le reste est resté dehors : le vide constaté de l'extérieur par ceux qui
observent le marché, la décomposition d'une charge en nombre et coût moyen que le chapitre 12
applique ensuite à ses quatre canaux, et la **queue française vide** qui commande de calibrer la
sévérité hors de France. Mesurée sur le PDF, pas sur le source : **1,84 page**, 29 nombres, 29
confirmés, couverture 100 %, tous imprimés par le script 63.

**Chaque terme technique y est défini à sa première apparition**, demande de Kélian le même jour :
ratio sinistres sur primes, fréquence contre nombre de sinistres, exposition, quantile à 99,5 %,
méthode par dépassement de seuil, franchise, capacité, perte brute contre perte indemnisée. Le
critère posé est qu'un lecteur non actuaire suive.

### Le contrôle du registre d'écriture, et ce qu'il donne

Kélian demandait de vérifier que le texte ne trahit pas une rédaction automatique. Deux mesures,
et les deux sont rassurantes :

- **aucun tiret cadratin en incise.** Le source en porte 1 036, mais **tous** sont dans des lignes
  de commentaire `% ------`, qui ne s'impriment jamais. Sur le PDF produit il en reste 24, et ce
  sont des **puces de liste à tirets** (pages 19, 24, 25, 36, 151, 158, 159) et des **cases vides
  de tableau** (92, 110, 122). Compter les tirets du source donne donc un nombre spectaculaire et
  faux : le seul comptage qui vaut se fait sur le PDF ;
- les 36 demi-cadratins sont de la typographie ordinaire, plages d'années `2019–2025`, pages de
  bibliographie `14–39`, noms propres composés Fisher–Tippett–Gnedenko et Pickands–Balkema–de
  Haan. Ne pas les « corriger » ;
- `audit_style.py` compte **73 marqueurs sur 66 811 mots, soit 1,09 pour mille**. Le plus fréquent
  est l'antithèse « ce n'est pas X, c'est Y », qui fait un vrai travail dans ce mémoire, celui de
  corriger une lecture fautive. Une purge à plat l'aplatirait.

### `ed73131` : huit figures retaillées, six sortent de l'illisible

`Z5_echelle_repli` 7,6 pt effectifs, `Z14_p4_sousprocess_open` 7,1, `J2_var_predictive` 7,1,
`S24_interaction_canaux` 7,5, `W_benchmark_sf` 7,2, `S20_biais_taille_troncature` 7,4. **Six
restent sous le plancher de 6,5 pt** : `J3_validation_adequation` 4,7 (six panneaux),
`M_faisabilite` 4,8 (script 05, Mac uniquement), `K3_branchement_R0` 5,7, `J6_roi_conformite` 6,1,
`Z19_bayes_direction` 6,3, `Z16_p4_temps_arret` 6,4.

### Contrôles de fin de journée

`main_ensae` : **195 pages, 0 `??` dans le PDF, 6 Overfull `\hbox` soit exactement la ligne de
base, 0 Overfull `\vbox`, 0 annotation hors page, 0 page tournée.** Harnais **2 132 sur 2 132,
100 %**, hors contrôle non déclaré à zéro. Arbre git propre, branche `exploratory` poussée.

## 11 septembre 2026

Deux demandes, et la seconde a fait tomber six défauts de mise en page.

### Le support de soutenance passe au gabarit Nexialog

Kélian a fourni un PDF de 53 pages en disant « voici le style exacte que je veux ». Le fichier
n'est pas un rapport : ce sont **deux supports de présentation concaténés**, le gabarit de
l'entreprise et un second support couvrant la même matière. C'est le **gabarit** qui a été suivi.

**La charte est mesurée dans le fichier, pas devinée.** Aplats vectoriels pondérés par leur
surface, polices pondérées par le nombre de caractères. Titre Georgia gras `#223E55`, sous-titre
Georgia gras `#B10031`, corps Segoe UI `#122738`, secondaire `#595959`, aplats `#223E55`,
`#192E3F`, `#435B6E`, clair `#F2F2F2`, accent `#B10031`, pied `#A5A5A5`. Tout est recopié en tête
de `build_soutenance_ppt.py`, qui en est le seul consommateur, et repris dans
`exploratory/slides/charte_nexialog/README.md`.

**ATTENTION À NE PAS CONFONDRE DEUX PALETTES.** Celle du gabarit vaut pour les **diapositives** ;
`style_nexialog.py` reste la source unique des couleurs des **figures**. Les deux se ressemblent
sans être identiques, et aucune figure n'a été recoloriée.

**Le contenu n'a pas bougé d'une ligne**, et c'est ce que la génération par script rendait bon
marché : seules les primitives de mise en page ont été réécrites. Un support fait à la main aurait
imposé de refaire vingt-huit diapositives une par une. Le décompte passe de 16 principales à
**couverture, sommaire, 14 de contenu, clôture, intercalaire et 10 de sauvegarde**, soit 28 pages,
le sommaire et la clôture étant des pièces de gabarit.

**Six visuels de charte entrent au dépôt**, dans `exploratory/slides/charte_nexialog/`, extraits
du gabarit sans retouche. Ce sont des logos et deux photographies : aucun ne porte de donnée, et
leur provenance est écrite. **Un gain à signaler** : `nexialog.png` est un PNG à fond
**transparent**, ce qui lève la réserve inscrite dans `CLAUDE.md` depuis le 9 septembre, selon
laquelle le logo d'entreprise ne pouvait pas figurer sur la page de garde du mémoire faute d'un
fichier détourable. La ligne à décommenter est déjà dans `page_de_garde.tex` ; **le geste n'est
pas fait**, il touche le mémoire et il appartient à Kélian.

### Ce que la relecture des diapositives rendues a trouvé

Six défauts, tous invisibles en relisant le code et tous vus en regardant la sortie. Ils sont
listés dans `controle_soutenance.md` et les quatre qui se généralisent sont passés aux pièges
d'instrument ci-dessus. Le plus instructif : **quatre titres d'annexe recouvraient leur
sous-titre**, et ils ont été trouvés non pas à l'œil mais par un contrôle qui compare deux à deux
les cadres de toutes les lignes de texte du PDF rendu. Après correction, **0 chevauchement et
0 débord sur 340 lignes de texte et 28 pages**.

Deux écarts au gabarit sont assumés et écrits : le bandeau de bas de page n'écrit pas le tiret
cadratin que le gabarit emploie, le gras du libellé suffisant ; et le corps des titres varie
entre 20 et 26 points au lieu des 26 fixes du gabarit, ce qui est précisément le remède au défaut
que le gabarit porte lui-même.

### Puis les graphiques et les tableaux passent en vectoriel, et ils LISENT leurs nombres

Seconde demande du jour, et c'est celle qui change le statut du support. Deux diapositives de
l'exposé et deux annexes ne portent plus une image importée mais un **graphique ou un tableau
dessiné par le script**, en formes vectorielles à la charte.

**LA RÈGLE QUI GOUVERNE CES GRAPHIQUES, ET ELLE N'EST PAS COSMÉTIQUE.** Une figure importée tient
ses nombres du script qui l'a produite : elle ne peut pas mentir. Un graphique dessiné dans le
support, lui, **retaperait** les valeurs, et c'est exactement la faute que le harnais du mémoire
existe pour empêcher. Les graphiques construits **lisent donc `sorties_verif/NN.txt`**, et chaque
lecture est **contrôlée contre la valeur que le mémoire publie** : si une sortie versionnée dérive,
la construction s'arrête au lieu de publier en silence un chiffre que le document ne porte pas.
Le support devient ainsi **plus sûr** qu'avec ses images, qui, elles, se périment sans rien dire.

Ce qui est passé en construit, et pourquoi : la diapositive des **quatre canaux**, qui portait une
figure à trois panneaux illisible à la projection et qui montre désormais les **douze valeurs avec
leur bruit** en barres groupées, lues dans le script 68 ; la diapositive des **bornes**, qui montre
la bande s'élargir linéairement avec l'ignorance, lue dans le script 30 ; l'**annexe des sources**
et l'**annexe des paramètres**, devenues de vraies tables, la seconde lue dans le script 63. Les
deux figures du mémoire remplacées sont **conservées en sauvegarde**, parce que le texte de
l'Institut dit que le jury cherche à retrouver dans le mémoire ce qui est présenté à l'oral.

**Ce qui n'a PAS été redessiné, et c'est une règle :** les figures qui portent autre chose qu'une
petite table de nombres, réseau, matrice, ajustement, courbe. Redessiner une figure de résultat en
approchant des positions à l'œil serait inventer.

**Un objet graphique PowerPoint natif a été écarté avec son motif.** Il porte son classeur et son
habillage Office, il faudrait le restyler pièce par pièce, et python-pptx n'expose aucune interface
pour les **barres d'erreur**, qu'il faudrait écrire en XML. Or toute grandeur simulée se publie
avec son bruit dans ce projet.

**Le garde-fou était faux au premier jet, et c'est le test qui l'a dit.** Voir le piège 24
ci-dessus : un plancher de tolérance absolu recopié sans réfléchir. Le contrôle tourne désormais
sur cinq cas, deux dérives comprises, et les cinq passent.

### Un point de rédaction ouvert, laissé à Kélian

**La couverture porte le titre du mémoire**, comme le gabarit le prévoit, et non le titre de
soutenance recommandé dans `plan_soutenance.md`. La thèse n'est pas perdue : « borner plutôt que
poser » est le titre de la diapositive qui l'énonce. L'arbitrage se change en un endroit.

---

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
