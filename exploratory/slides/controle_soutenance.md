# Contrôle du support de soutenance

`soutenance_memoire_DORA.pptx`, généré par `build_soutenance_ppt.py`. **28 diapositives** :
couverture, sommaire, **14 de contenu**, clôture, intercalaire, **10 de sauvegarde**.

**Mise à la charte Nexialog le 11 septembre 2026.** Kélian a fourni le gabarit de présentation de
l'entreprise et demandé « le style exacte que je veux ». **Le contenu n'a pas bougé** : ce sont
les primitives de mise en page du script qui ont été réécrites, et c'est précisément ce que la
génération par script rendait bon marché. La liste des valeurs affichées ci-dessous est inchangée
par rapport à la version du 11 septembre au matin, et elle a été revérifiée ligne par ligne.

---

## Les diapositives, leur source et ce qu'elles affichent

| # | Titre | Source | Figure | Chiffres affichés |
|---|---|---|---|---|
| 1 | Couverture, au gabarit Nexialog | page de garde du mémoire | logos de charte | aucun |
| 2 | Sommaire, six entrées | plan de soutenance | — | aucun |
| 3 | DORA impose une maîtrise, aucun dispositif n'en fait du capital | ch. 1 et 2 | schéma construit | aucun |
| 4 | Une question en deux temps, et trois apports | ch. 1, contribution et plan | schéma construit | aucun |
| 5 | Cinq domaines de contrôle, pas cinq cases à cocher | ch. 1 et 2 ; matrice ch. 6 | schéma construit | aucun |
| 6 | La donnée montre la co-occurrence, jamais la direction | ch. 4 et 8 | tableau construit | aucun |
| 7 | D'un état de conformité à une décision, en quatre étages | ch. 5 à 10 | schéma construit | 99,5 % |
| 8 | L'ordre de propagation change la criticité | ch. 6 ; ch. 10 comparaison | `H1_reseau_W.png` | aucun hors figure |
| 9 | La direction n'est pas identifiable, et c'est un résultat | ch. 8 | `Z11_reversibilite_martingale.png` | aucun hors figure |
| 10 | Du point à la bande : borner plutôt que poser | ch. 9 | `Z_identification_partielle.png` | 1 024 |
| 11 | Quatre canaux déplacés, et leurs effets ne s'additionnent pas | ch. 10 | `S24_interaction_canaux.png` | 6 049 ; 20 188 ; 3,34 ; 9 138 ; 14 139 ; 5 001 ; 35 % |
| 12 | Le pilier des tiers concentre | annexe C | `Z9_p4_accumulation.png` | aucun hors figure |
| 13 | La donnée manquante devient une exigence de reporting | ch. 12 | `Z18_valeur_information.png` | aucun hors figure |
| 14 | Trois décisions, et une confusion à ne pas commettre | ch. 10 | schéma construit | aucun |
| 15 | Ce que ce travail n'établit pas | ch. 11, table des limites | tableau construit | aucun |
| 16 | Trois messages | ch. 13 | — | aucun |
| 17 | Merci pour votre attention, des questions | — | — | aucun |
| 18 | Intercalaire « Annexes » | — | — | aucun |

### Diapositives de sauvegarde

| # | Titre | Source | Figure | Chiffres |
|---|---|---|---|---|
| A1 | Sept sources, et chacune avec son statut de preuve | ch. 4 ; scripts 62, 63 | — | aucun |
| A2 | Les paramètres, et ce qui est estimé, posé ou gelé | annexe D ; scripts 07, 08b, 63, 66 | — | 0,5954 ; 20,03 ; 91 ; 0,45 ; 0,68 ; 0,90 |
| A3 | Pourquoi une loi de valeurs extrêmes | ch. 5 ; scripts 07, 47 | `J3_validation_adequation.png` | aucun hors figure |
| A4 | La cascade est un branchement sous-critique | ch. 6 ; script 03 | `K3_branchement_R0.png` | 0,506 ; 0,054 (notes) |
| A5 | Ce que le corpus corrobore, et ce qu'il ne lève pas | ch. 8 ; scripts 53, 59, 64 | `Z17_postmortem_direction.png` | aucun hors figure |
| A6 | La bande et ses trois étages d'incertitude | ch. 11 ; script 48 | `J4_bande_modele.png` | aucun hors figure |
| A7 | L'attribution par canal : trois lectures | ch. 10 ; scripts 68, 82 | `S15_allocation_shapley_euler.png` | aucun hors figure |
| A8 | Défaillances simultanées : une sortie, pas une lacune | annexe D ; script 74 | `S30_defaillances_simultanees.png` | 62,31 % ; 31,15 % (notes) |
| A9 | Les hypothèses, par ordre de ce qu'elles coûtent | annexe D ; scripts 76, 81 | `S32_tornado_normalise.png` | aucun hors figure |
| A10 | Glossaire | annexe F | — | 99,5 % |

---

## Vérification : aucun chiffre nouveau

**Les valeurs distinctes affichées ou prononcées** sont toutes publiées dans le mémoire et
imprimées par un script versionné. Aucune n'a été calculée pour ce support.

| Valeur | Objet | Où elle est publiée |
|---|---|---|
| 6 049 M€ | besoin de capital, état conforme, secteur | ch. 10 ; scripts 43, 68 |
| 20 188 M€ | besoin de capital, état non conforme, secteur | ch. 10 ; scripts 43, 68 |
| 3,34 | facteur entre les deux états | ch. 10 ; script 43 |
| 9 138 M€ | somme des quatre canaux isolés | ch. 10 ; script 68 |
| 14 139 M€ | écart total | ch. 10 ; scripts 43, 68 |
| 5 001 M€ | interaction entre canaux | ch. 10 ; script 68 |
| 35 % | l'interaction rapportée aux canaux isolés | ch. 10 ; script 68 |
| 1 024 | sommets du pavé d'identification partielle | ch. 9 ; script 40 |
| 99,5 % | niveau du quantile réglementaire | ch. 5, ch. 10 |
| 0,5954 | indice de queue de la sévérité | annexe D ; script 63 |
| 20,03 M€ | seuil de la calibration | annexe D ; script 63 |
| 91 | nombre d'excès au-dessus du seuil | annexe D ; script 63 |
| 0,45 / 0,68 / 0,90 | les trois valeurs posées du gain de propagation | ch. 7 ; script 66 |
| 0,506 et 0,054 | rayon spectral et taux de reproduction | ch. 6 ; script 03 |
| 62,31 % et 31,15 % | part des sinistres touchant plus d'un pilier | annexe D ; script 74 |
| 169 M€ | besoin à l'échelle d'une entité, **borne supérieure** | ch. 10 ; script 65 |
| 1 811 | années nécessaires pour tester le quantile | annexe D ; script 91 |

Les quatre dernières ne figurent que dans les **notes orales** et les diapositives de sauvegarde,
pour répondre aux questions. Elles ne sont pas affichées dans l'exposé principal.

**Contrôle complémentaire.** Les figures reprises portent leurs propres étiquettes chiffrées, qui
sont celles des scripts qui les ont produites. Elles n'ont été ni retouchées, ni recadrées, ni
recoloriées, donc aucun chiffre ne peut y avoir été déplacé. Le changement de charte n'a touché
aucune figure : les couleurs du gabarit sont celles des diapositives, jamais celles des tracés.

---

## Figures reprises

**Six figures dans l'exposé principal, sept dans les sauvegardes, toutes issues de
`exploratory/vasicek_lab/figures/` et produites par les scripts du projet.** Aucune capture de
page PDF, aucune figure redessinée, aucune figure inventée.

| Figure | Diapositive | Traitement |
|---|---|---|
| `H1_reseau_W.png` | 8 | aucune retouche, pleine largeur |
| `Z11_reversibilite_martingale.png` | 9 | aucune retouche, colonne gauche |
| `Z_identification_partielle.png` | 10 | aucune retouche, colonne gauche |
| `S24_interaction_canaux.png` | 11 | aucune retouche, pleine largeur |
| `Z9_p4_accumulation.png` | 12 | aucune retouche, pleine largeur |
| `Z18_valeur_information.png` | 13 | aucune retouche, colonne gauche |
| `J3`, `K3`, `Z17`, `J4`, `S15`, `S30`, `S32` | sauvegardes | aucune retouche |

**Trois figures sont presque carrées et ont reçu un gabarit à deux colonnes**, figure à gauche et
texte à droite, séparés par le filet vertical du gabarit Nexialog. Posées pleine largeur elles se
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
| Corps | Segoe UI 13 à 16 pt, `#122738` |
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
   cadratin dans ses livrables. Le libellé reste, en gras rouge, et le gras suffit à séparer : la
   lecture est la même, la règle est tenue.
2. **Le corps des titres varie de 20 à 26 points selon leur longueur.** Le gabarit fixe 26 pt, et
   c'est pour cette raison qu'il porte lui-même deux titres tronqués et un titre qui recouvre son
   sous-titre. Ici le titre tient sur **une** ligne et c'est le corps qui cède, ce qui ne se
   remarque pas d'une diapositive à l'autre alors qu'un chevauchement se remarque tout de suite.

---

## Les distinctions de statut, maintenues sur les diapositives

Le support conserve les quatre statuts que le mémoire distingue, et il ne les aplatit nulle part.

| Statut | Où c'est dit sur les diapositives |
|---|---|
| **Calibré** | diapositive 7, colonne de gauche : « calibrés sur données » |
| **Borné** | diapositive 7, colonne de droite, et diapositive 15 |
| **Illustratif** | diapositive 10, ligne en rouge : « le niveau affiché reste illustratif » ; diapositive 15 |
| **Non identifiable** | diapositives 6, 9 et 15, en rouge, la couleur étant réservée à cet usage |

**La couleur d'accent ne sert qu'à cela.** Rouge pour la non-identifiabilité, pour les alertes et
pour les deux piliers qui émettent le plus. Jamais décorative, à l'exception des éléments de
gabarit, où elle est la couleur de la marque.

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

Le mémoire fait 161 pages en version courte ; l'exposé en couvre la ligne directrice. Sont
délibérément absents des quatorze diapositives de contenu et disponibles en sauvegarde ou dans les
notes :

les deux théorèmes d'extrapolation de queue et le choix du seuil ; la confrontation de deux
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
| Diapositives de sauvegarde | **10** |
| Format | **16:9**, fond blanc posé explicitement |
| Corps de texte | 12 à 16 pt ; titres 20 à 26 pt ; sources 9 pt |
| Chevauchements de texte, mesurés sur le PDF rendu | **0 sur 340 lignes** |
| Texte hors page, mesuré sur le PDF rendu | **0** |
| Figures illisibles | **aucune** après le gabarit à deux colonnes |
| Notes orales | **en français**, sur les 14 diapositives de contenu et les 10 sauvegardes |
| Sources du mémoire modifiées | **aucune** |

### Le contrôle qui a servi, et pourquoi il est écrit ainsi

**Les chevauchements et les débords se mesurent sur le PDF rendu, pas sur le code.** Le script
exporte en PDF par PowerPoint, puis compare deux à deux les cadres de toutes les lignes de texte
de chaque page. Il a trouvé quatre titres d'annexe qui recouvraient leur sous-titre, et c'est ce
qui a produit la règle d'ajustement du corps décrite plus haut. Le contrôle est reproductible et
il vaut mieux qu'une relecture : quatre défauts sur vingt-huit pages ne se voient pas à l'œil sur
une relecture rapide.

### Défauts trouvés en regardant les diapositives rendues

Ils n'auraient pas été vus en relisant le code, et c'est la règle du projet : on regarde la sortie.

1. **les flèches du schéma sortaient en carrés gris.** La numérotation des formes automatiques
   passée en nombre entier ne désigne pas ce qu'on croit ; l'énumération nommée corrige ;
2. **une figure presque carrée était illisible** posée pleine largeur : elle se dimensionnait sur
   la hauteur et n'occupait qu'un tiers de la diapositive. D'où le gabarit à deux colonnes ;
3. **deux blocs de texte passaient sous le bandeau de bas de page**, donc coupés à l'écran. Les
   hauteurs ont été recalculées ;
4. **les photographies du gabarit sortaient de leur cadre.** Agrandies jusqu'à couvrir, elles
   débordaient par la gauche et passaient sous le texte de la couverture. Elles sont désormais
   **recadrées** par `crop_left` et `crop_right`, ce que fait le gabarit lui-même ;
5. **la chaîne en cinq étapes coupait ses mots au milieu** dans une demi-diapositive : chaque
   étape n'avait qu'un pouce de large. Elle est devenue verticale ;
6. **l'intercalaire laissait passer la photographie entre ses trois triangles.** Il est refait
   avec deux polygones superposés, dont la différence est la bande diagonale.

### Un point de rédaction décidé à la mise à la charte

**La couverture porte désormais le titre du mémoire**, comme le gabarit Nexialog le prévoit, et
non le titre de soutenance recommandé par `plan_soutenance.md`. La thèse du travail n'est pas
perdue pour autant : elle est le titre de la diapositive 10, « borner plutôt que poser », qui est
le moment où on l'énonce. Si Kélian préfère l'inverse, la ligne se change en un endroit.

### Un ajout conservé depuis la version précédente

La diapositive des quatre canaux ne portait le chiffre de tête que dans les étiquettes de la
figure. La ligne de texte dit **« au secteur »** avant les montants, et le sous-titre le répète.
Sans ce mot, un jury lit vingt milliards pour une entité, et la question de l'échelle part avant
qu'on ait pu la cadrer.
