# Contrôle du support de soutenance

`soutenance_memoire_DORA.pptx`, généré par `build_soutenance_ppt.py`. **30 diapositives** :
couverture, sommaire, **14 de contenu**, clôture, intercalaire, **12 de sauvegarde**.

**Deux reprises le 11 septembre 2026.** Le matin, la mise au gabarit de présentation Nexialog, à
la demande de Kélian. L'après-midi, le passage aux **graphiques vectoriels et aux tableaux
construits**, toujours à sa demande. Dans les deux cas le **contenu n'a pas bougé** : ce sont les
primitives de mise en page du script qui ont été réécrites, et c'est ce que la génération par
script rendait bon marché.

---

## La règle qui gouverne les graphiques construits

**Un graphique dessiné dans le support retaperait ses nombres**, alors qu'une figure importée les
tient du script qui l'a produite. C'est exactement la faute que le harnais du mémoire existe pour
empêcher. Les graphiques et les tableaux construits **lisent donc `sorties_verif/NN.txt`**, et
chaque lecture est **contrôlée contre la valeur que le mémoire publie** : si une sortie versionnée
dérive, la construction s'arrête au lieu de publier en silence un chiffre que le document ne porte
pas.

Le garde-fou est **testé**, par `test_garde_sorties.py`, sur huit cas : trois dérives dont une
d'une seule unité, un motif introuvable, un nombre de valeurs capturées incorrect, et trois
lectures légitimes qui doivent passer. **Les huit passent.** Un contrôle qui passe à vide est le
pire défaut possible parce qu'il rassure, et le projet en a déjà connu deux.

**Et le premier jet du garde-fou était faux**, ce qui valait la peine de le tester plutôt que de
le supposer. La tolérance avait été recopiée sous la forme `max(0,6 % ; 0,5)`, avec un plancher
absolu de 0,5 : elle acceptait un indice de queue lu à 0,5954 pour une valeur attendue de 0,62.
C'est le défaut que le harnais du mémoire avait déjà corrigé une fois, en août. Le demi-pas se
prend sur la **dernière décimale écrite**, jamais sur une constante.

---

## Les diapositives, leur source et ce qu'elles affichent

| # | Titre | Source | Visuel | Chiffres affichés |
|---|---|---|---|---|
| 1 | Couverture, au gabarit Nexialog | page de garde du mémoire | logos de charte | aucun |
| 2 | Sommaire, six entrées | plan de soutenance | — | aucun |
| 3 | DORA impose une maîtrise, aucun dispositif n'en fait du capital | ch. 1 et 2 | schéma construit | aucun |
| 4 | Une question en deux temps, et trois apports | ch. 1, contribution et plan | schéma construit | aucun |
| 5 | Cinq domaines de contrôle, pas cinq cases à cocher | ch. 1 et 2 ; matrice ch. 6 | schéma construit | aucun |
| 6 | La donnée montre la co-occurrence, jamais la direction | ch. 4 et 8 | tableau construit | aucun |
| 7 | D'un état de conformité à une décision, en quatre étages | ch. 5 à 10 | schéma construit | 99,5 % |
| 8 | L'ordre de propagation change la criticité | ch. 6 | `H1_reseau_W.png` | aucun hors figure |
| 9 | La direction n'est pas identifiable, et c'est un résultat | ch. 8 | `Z11_reversibilite_martingale.png` | aucun hors figure |
| 10 | Du point à la bande : borner plutôt que poser | ch. 9 | **graphique construit, script 30** | bornes, largeurs, socle, point d'expert, 1 024 |
| 11 | Quatre canaux déplacés, et leurs effets ne s'additionnent pas | ch. 10 | **graphique construit, script 68** | les douze valeurs et leur bruit ; 6 049 ; 20 188 ; 3,34 ; 9 138 ; 14 139 ; 5 001 ; 35 % |
| 12 | Le pilier des tiers concentre | annexe C | `Z9_p4_accumulation.png` | aucun hors figure |
| 13 | La donnée manquante devient une exigence de reporting | ch. 12 | `Z18_valeur_information.png` | aucun hors figure |
| 14 | Trois décisions, et une confusion à ne pas commettre | ch. 10 | schéma construit | aucun |
| 15 | Ce que ce travail n'établit pas | ch. 11, table des limites | tableau construit | aucun |
| 16 | Trois messages | ch. 13 | — | aucun |
| 17 | Merci pour votre attention, des questions | — | — | aucun |
| 18 | Intercalaire « Annexes » | — | — | aucun |

### Diapositives de sauvegarde

| # | Titre | Source | Visuel | Chiffres |
|---|---|---|---|---|
| A1 | Sept sources, et chacune avec son statut de preuve | ch. 4 ; scripts 62, 63 | **tableau construit** | aucun |
| A2 | Les paramètres, et ce qui est estimé, posé ou gelé | annexe D ; **lu dans le script 63** | **tableau construit** | 20,03 ; 91 ; 0,5954 ; [0,304 ; 0,831] ; 57,97 ; 21,56 ; 9,2 ; 0,45 / 0,68 / 0,90 ; 0,1509 ; +2,4 % |
| A3 | Pourquoi une loi de valeurs extrêmes | ch. 5 ; scripts 07, 47 | `J3_validation_adequation.png` | aucun hors figure |
| A4 | La cascade est un branchement sous-critique | ch. 6 ; script 03 | `K3_branchement_R0.png` | 0,506 ; 0,054 (notes) |
| A5 | Ce que le corpus corrobore, et ce qu'il ne lève pas | ch. 8 ; scripts 53, 59, 64 | `Z17_postmortem_direction.png` | aucun hors figure |
| A6 | La bande et ses trois étages d'incertitude | ch. 11 ; script 48 | `J4_bande_modele.png` | aucun hors figure |
| A7 | L'attribution par canal : trois lectures | ch. 10 ; scripts 68, 82 | `S15_allocation_shapley_euler.png` | aucun hors figure |
| A8 | Défaillances simultanées : une sortie, pas une lacune | annexe D ; script 74 | `S30_defaillances_simultanees.png` | 62,31 % ; 31,15 % (notes) |
| A9 | Les hypothèses, par ordre de ce qu'elles coûtent | annexe D ; scripts 76, 81 | `S32_tornado_normalise.png` | aucun hors figure |
| A10 | Glossaire | annexe F | — | 99,5 % |
| A11 | La table complète des quatre canaux, telle qu'elle est au mémoire | ch. 10 ; scripts 43, 68 | `S24_interaction_canaux.png` | aucun hors figure |
| A12 | L'ensemble d'identification partielle, tel qu'il est au mémoire | ch. 9 ; scripts 30, 40 | `Z_identification_partielle.png` | aucun hors figure |

**A11 et A12 portent les deux figures du mémoire que l'exposé redessine.** Le texte de l'Institut
dit que le jury « essaie de retrouver dans le texte du mémoire ce que l'étudiant présente à
l'oral » : la figure du document doit donc rester à portée de voix, même quand la diapositive en
donne une lecture plus lisible à la projection.

---

## Vérification : aucun chiffre nouveau

Toutes les valeurs affichées ou prononcées sont publiées dans le mémoire et imprimées par un
script versionné. Aucune n'a été calculée pour ce support.

### Valeurs affichées dans l'exposé

| Valeur | Objet | Où elle est publiée |
|---|---|---|
| 6 049 M€ | besoin de capital, état conforme, secteur | ch. 10 ; scripts 43, 68 |
| 20 188 M€ | besoin de capital, état non conforme, secteur | ch. 10 ; scripts 43, 68 |
| 3,34 | facteur entre les deux états | ch. 10 ; script 43 |
| 9 138 M€ | somme des quatre canaux isolés | ch. 10 ; script 68 |
| 14 139 M€ | écart total | ch. 10 ; scripts 43, 68 |
| 5 001 M€ et 35 % | interaction entre canaux, et sa part | ch. 10 ; script 68 |
| 4 328 ± 463 / 8 775 ± 1 004 / 6 546 ± 457 | fréquence : isolé, fermeture, Shapley | ch. 10 ; **lus dans le script 68** |
| 1 448 ± 277 / 4 562 ± 819 / 2 928 ± 343 | détection : les trois lectures | ch. 10 ; **lus dans le script 68** |
| 1 633 ± 188 / 2 402 ± 442 / 2 088 ± 152 | propagation : les trois lectures | ch. 10 ; **lus dans le script 68** |
| 1 728 ± 210 / 3 402 ± 493 / 2 576 ± 222 | accumulation : les trois lectures | ch. 10 ; **lus dans le script 68** |
| [7 837 ; 8 174] · [7 605 ; 8 300] · [7 348 ; 8 431] · [6 858 ; 8 697] | bornes de capital pour t = 0,25 à 1 | ch. 9 ; **lues dans le script 30** |
| 336 / 695 / 1 083 / 1 839 M€ | largeur de la bande, par niveau d'ignorance | ch. 9 ; **lues dans le script 30** |
| 5 275 M€ | socle identifié, sans aucune contagion | ch. 9 ; **lu dans le script 30** |
| 8 110 M€ | point d'expert, **un point de l'ensemble** | ch. 9 ; **lu dans le script 30** |
| 1 024 | sommets du pavé d'identification partielle | ch. 9 ; script 40 |
| 99,5 % | niveau du quantile réglementaire | ch. 5, ch. 10 |

### Valeurs affichées dans les sauvegardes

| Valeur | Objet | Où elle est publiée |
|---|---|---|
| 20,03 M€ · 91 | seuil de la calibration, et ses excès | annexe D ; **lus dans le script 63** |
| 0,5954 · [0,304 ; 0,831] | indice de queue et son intervalle à 90 % | annexe D ; **lus dans le script 63** |
| 57,97 M€ | échelle de la loi de queue | annexe D ; **lu dans le script 63** |
| 21,56 par an | fréquence au secteur | annexe D ; **lu dans le script 63** |
| 9,2 | facteur de surdispersion, posé | annexe D ; **lu dans le script 63** |
| 0,45 / 0,68 / 0,90 | les trois valeurs posées du gain de propagation | ch. 7 ; **lu dans les scripts 63 et 66** |
| 0,1509 et +2,4 % | taux de dépassement gelé, et l'écart chiffré | ch. 13 ; scripts 47, 63 |
| 0,506 et 0,054 | rayon spectral et taux de reproduction | ch. 6 ; script 03 |
| 62,31 % et 31,15 % | part des sinistres touchant plus d'un pilier | annexe D ; script 74 |
| 169 M€ | besoin à l'échelle d'une entité, **borne supérieure** | ch. 10 ; script 65 |
| 1 811 | années nécessaires pour tester le quantile | annexe D ; script 91 |

Les trois dernières ne figurent que dans les **notes orales**, pour répondre aux questions.

**Contrôle complémentaire.** Les figures reprises portent leurs propres étiquettes chiffrées, qui
sont celles des scripts qui les ont produites. Elles n'ont été ni retouchées, ni recadrées, ni
recoloriées. Le changement de charte n'a touché aucune figure : les couleurs du gabarit sont
celles des diapositives, jamais celles des tracés.

---

## Les visuels, et d'où chacun vient

**Trois familles, et elles ne se confondent pas.**

| Famille | Ce que c'est | Où |
|---|---|---|
| Figure du mémoire | PNG produit par un script du dépôt, non retouché | 8, 9, 12, 13 ; A3 à A9, A11, A12 |
| Graphique construit | dessiné par le script de construction, valeurs **lues** dans `sorties_verif/` | 10, 11 |
| Schéma ou tableau construit | formes vectorielles, aucune donnée chiffrée | 3, 4, 5, 6, 7, 14, 15 ; A1, A2 |
| Visuel de charte | logos et photographies du gabarit Nexialog | couverture, sommaire, intercalaire, clôture |

**Pourquoi des formes plutôt qu'un objet graphique PowerPoint.** Un graphique natif d'Office porte
son classeur et son habillage par défaut : il faudrait le restyler pièce par pièce pour retrouver
la charte, et python-pptx n'expose aucune interface pour les **barres d'erreur**, qu'il faudrait
écrire en XML. Or la convention du projet veut que toute grandeur simulée se publie **avec son
bruit**. Des formes donnent le contrôle exact de la charte, la barre d'erreur en trois traits, et
un rendu identique sur tout poste.

**Trois figures du mémoire sont presque carrées et ont reçu un gabarit à deux colonnes**, figure à
gauche et texte à droite, séparés par le filet vertical du gabarit. Posées pleine largeur elles se
dimensionnaient sur la hauteur disponible et n'occupaient qu'un tiers de la diapositive,
étiquettes illisibles. C'est la transposition d'une règle du mémoire, où une figure portrait prend
une page entière et jamais un débord en largeur.

**Les visuels de charte sont les seules images non produites par un script**, et ils vivent dans
`charte_nexialog/` avec leur provenance écrite. Ce sont des logos et deux photographies de
gabarit : aucun ne porte de donnée.

---

## La charte, et d'où elle vient

Relevée dans le gabarit Nexialog fourni le 11 septembre, **mesurée et non devinée** : surface des
aplats vectoriels, et nombre de caractères par couple police-corps-couleur.

| Rôle | Valeur |
|---|---|
| Titre de diapositive | Georgia Bold, `#223E55` |
| Sous-titre | Georgia Bold, `#B10031` |
| Corps | Segoe UI 11 à 16 pt, `#122738` |
| Secondaire et légendes | Segoe UI, `#595959` |
| Aplats | `#223E55`, `#192E3F`, `#435B6E`, clair `#F2F2F2`, filets `#D9D9D9` |
| Accent | `#B10031` |
| Pied de page | 9 à 10 pt, `#A5A5A5` |

Éléments de gabarit repris : coin rouge en biseau, logo en haut à droite, titre navy et
sous-titre rouge, deux colonnes séparées d'un filet pointillé, têtes de bloc à numéro cerclé,
bandeau de bas de page, pagination à droite, couverture à photographie coupée en diagonale,
sommaire à carte blanche et barre rouge, intercalaire à chevron navy, clôture, et cartouche
« ANNEXE N » sur les diapositives de sauvegarde.

**Deux écarts assumés au gabarit, et leurs motifs.**

1. **Le gabarit écrit « Message clé — » avec un tiret cadratin.** Le projet proscrit le tiret
   cadratin dans ses livrables. Le libellé reste, en gras rouge, et le gras suffit à séparer.
2. **Le corps des titres varie de 20 à 26 points selon leur longueur.** Le gabarit fixe 26 pt, et
   c'est pour cette raison qu'il porte lui-même deux titres tronqués et un titre qui recouvre son
   sous-titre. Ici le titre tient sur **une** ligne et c'est le corps qui cède.

**Une seule teinte n'est pas décorative sur les graphiques.** Sur la diapositive des canaux, la
lecture de **fermeture** est en rouge parce que c'est celle qu'un plan de remédiation doit citer,
et les deux autres sont deux valeurs d'une même rampe navy. Sur la diapositive des bornes, le
rouge porte la **largeur** de la bande, qui est l'objet de la slide.

---

## Les distinctions de statut, maintenues sur les diapositives

| Statut | Où c'est dit sur les diapositives |
|---|---|
| **Calibré** | diapositive 7, colonne de gauche ; annexe 2, colonne « statut » |
| **Estimé** | annexe 2, colonne « statut », avec son intervalle |
| **Posé** | diapositive 7, colonne de droite ; annexe 2, en rouge |
| **Gelé** | annexe 2, avec l'écart chiffré plutôt que corrigé |
| **Illustratif** | diapositive 10, ligne en rouge ; diapositive 15 |
| **Non identifiable** | diapositives 6, 9 et 15, en rouge |
| **Citation externe** | annexe 1, colonne « statut de preuve », en rouge |

---

## Limites méthodologiques explicitement mentionnées

Sur la diapositive 15, en deux colonnes face à face, et rappelées dans les notes :

- la direction de contagion n'est pas identifiée ;
- le niveau absolu est illustratif, et il s'agit d'une borne supérieure à l'échelle d'une entité ;
- l'incertitude de queue est large ;
- deux canaux sur quatre sont des bornes posées, pas des calibrations ;
- le niveau de sévérité dérive dans le temps, et le backtest le mesure.

Et en face, ce que le travail établit malgré cela : le signe et l'ordre de l'écart, la hiérarchie
des piliers, le cadre de bornage et son coût, la recommandation de reporting, et les deux lois
validées hors échantillon.

**Deux réserves supplémentaires vivent dans les notes orales** et doivent être exprimées si la
question vient : le retour sur investissement calculé sur le seul portage est un **majorant**, et
le backtest ne valide **pas** le quantile à 99,5 %, dont la puissance est chiffrée en années.

---

## Ce qui n'est pas dans l'exposé principal, et qui est réservé aux questions

Les deux théorèmes d'extrapolation de queue et le choix du seuil ; la confrontation de deux
estimateurs de l'indice de queue ; le backtest hors échantillon et sa puissance ; la décomposition
de Möbius et les effets croisés ; le biais de narration du corpus et son jackknife ; la
formalisation bayésienne de la direction ; la descente d'échelle et les quatre bilans réels ; le
protocole d'élicitation préparé et non exécuté ; la comparaison au processus auto-excité ; le
plafond de sévérité adossé à l'exposition ; le dispositif de vérification des chiffres publiés.

---

## Contrôles passés

| Contrôle | Résultat |
|---|---|
| Le fichier s'ouvre | **oui**, converti en PDF par PowerPoint sans erreur |
| Nombre de diapositives de contenu | **14**, dans la fourchette de 14 à 16 demandée |
| Diapositives de gabarit | couverture, sommaire, clôture, intercalaire |
| Diapositives de sauvegarde | **12** |
| Format | **16:9**, fond blanc posé explicitement |
| Corps de texte | 11 à 16 pt ; titres 20 à 26 pt ; sources 9 pt |
| Garde-fou de lecture des sorties versionnées | **8 cas sur 8**, `test_garde_sorties.py` |
| Chevauchements de texte, mesurés sur le PDF rendu | **0 sur 455 lignes** |
| Texte hors page, mesuré sur le PDF rendu | **0** |
| Pages tournées | **0** |
| Figures illisibles | **aucune** |
| Notes orales | **en français**, sur les 14 diapositives de contenu et les 12 sauvegardes |
| Sources du mémoire modifiées | **aucune** |

### Le contrôle qui a servi, et pourquoi il est écrit ainsi

**Les chevauchements et les débords se mesurent sur le PDF rendu, pas sur le code.** Le script
exporte en PDF par PowerPoint, puis compare deux à deux les cadres de toutes les lignes de texte
de chaque page. Il a trouvé quatre titres d'annexe qui recouvraient leur sous-titre, puis huit
cellules de tableau qui débordaient sur la ligne suivante. Ni les uns ni les autres ne se voient à
la relecture d'une source.

### Défauts trouvés en regardant les diapositives rendues

Ils n'auraient pas été vus en relisant le code, et c'est la règle du projet : on regarde la sortie.

1. **les flèches du schéma sortaient en carrés gris.** La numérotation des formes automatiques
   passée en nombre entier ne désigne pas ce qu'on croit ; l'énumération nommée corrige ;
2. **une figure presque carrée était illisible** posée pleine largeur. D'où le gabarit à deux
   colonnes ;
3. **deux blocs de texte passaient sous le bandeau de bas de page** ;
4. **les photographies du gabarit sortaient de leur cadre.** Agrandies jusqu'à couvrir, elles
   débordaient par la gauche et passaient sous le texte de la couverture. Elles sont désormais
   **recadrées** par `crop_left` et `crop_right` ;
5. **la chaîne en cinq étapes coupait ses mots au milieu.** Elle est devenue verticale ;
6. **l'intercalaire laissait passer la photographie entre ses trois triangles.** Deux polygones
   superposés à la place ;
7. **une étiquette de valeur passait à la ligne sous la barre suivante.** La réserve de droite est
   désormais **mesurée** sur la plus longue étiquette, comme les titres ;
8. **les cellules de tableau qui passaient à la ligne débordaient sur la ligne suivante.** La
   hauteur de ligne est **mesurée**, elle n'est plus posée.

### Un point de rédaction ouvert

**La couverture porte le titre du mémoire**, comme le gabarit le prévoit, et non le titre de
soutenance recommandé par `plan_soutenance.md`. La thèse n'est pas perdue : « borner plutôt que
poser » est le titre de la diapositive 10, qui est le moment où on l'énonce. Si Kélian préfère
l'inverse, la ligne se change en un endroit.
