# Contrôle du support de soutenance

`soutenance_memoire_DORA.pptx`, généré le 11 septembre 2026 par
`build_soutenance_ppt.py`. 27 diapositives : **16 principales**, 1 séparateur, **10 de
sauvegarde**.

---

## Les diapositives, leur source et ce qu'elles affichent

| # | Titre | Source | Figure | Chiffres affichés |
|---|---|---|---|---|
| 1 | Titre | page de garde du mémoire | — | aucun |
| 2 | DORA impose une maîtrise, aucun dispositif n'en fait du capital | ch. 1 et 2 | schéma construit | aucun |
| 3 | Une question en deux temps, et trois apports | ch. 1, contribution et plan | schéma construit | aucun |
| 4 | Cinq domaines de contrôle, pas cinq cases à cocher | ch. 1 et 2 ; matrice ch. 6 | schéma construit | aucun |
| 5 | La donnée montre la co-occurrence, jamais la direction | ch. 4 et 8 | tableau construit | aucun |
| 6 | D'un état de conformité à une décision, en quatre étages | ch. 5 à 10 | schéma construit | 99,5 % |
| 7 | L'ordre de propagation change la criticité | ch. 6 ; ch. 10 comparaison | `H1_reseau_W.png` | aucun hors figure |
| 8 | La direction n'est pas identifiable, et c'est un résultat | ch. 8 | `Z11_reversibilite_martingale.png` | aucun hors figure |
| 9 | Du point à la bande | ch. 9 | `Z_identification_partielle.png` | 1 024 |
| 10 | Quatre canaux déplacés, et leurs effets ne s'additionnent pas | ch. 10 | `S24_interaction_canaux.png` | 6 049 ; 20 188 ; 3,34 ; 9 138 ; 14 139 ; 5 001 ; 35 % |
| 11 | Le pilier des tiers concentre | annexe C | `Z9_p4_accumulation.png` | aucun hors figure |
| 12 | La donnée manquante devient une exigence de reporting | ch. 12 | `Z18_valeur_information.png` | aucun hors figure |
| 13 | Trois décisions, et une confusion à ne pas commettre | ch. 10 | schéma construit | aucun |
| 14 | Ce que ce travail n'établit pas | ch. 11, table des limites | tableau construit | aucun |
| 15 | Conclusion | ch. 13 | — | aucun |
| 16 | Questions | — | rappel d'architecture | aucun |

### Diapositives de sauvegarde

| # | Titre | Source | Figure | Chiffres |
|---|---|---|---|---|
| B1 | Sept sources, et chacune avec son statut de preuve | ch. 4 ; scripts 62, 63 | — | aucun |
| B2 | Les paramètres, et ce qui est estimé, posé ou gelé | annexe D ; scripts 07, 08b, 63, 66 | — | 0,5954 ; 20,03 ; 91 ; 0,45 ; 0,68 ; 0,90 |
| B3 | Pourquoi une loi de valeurs extrêmes | ch. 5 ; scripts 07, 47 | `J3_validation_adequation.png` | aucun hors figure |
| B4 | La cascade est un branchement sous-critique | ch. 6 ; script 03 | `K3_branchement_R0.png` | 0,506 ; 0,054 (notes) |
| B5 | Ce que le corpus corrobore, et ce qu'il ne lève pas | ch. 8 ; scripts 53, 59, 64 | `Z17_postmortem_direction.png` | aucun hors figure |
| B6 | La bande et ses trois étages d'incertitude | ch. 11 ; script 48 | `J4_bande_modele.png` | aucun hors figure |
| B7 | L'attribution par canal : trois lectures | ch. 10 ; scripts 68, 82 | `S15_allocation_shapley_euler.png` | aucun hors figure |
| B8 | Défaillances simultanées : une sortie, pas une lacune | annexe D ; script 74 | `S30_defaillances_simultanees.png` | 62,31 % ; 31,15 % (notes) |
| B9 | Les hypothèses, par ordre de ce qu'elles coûtent | annexe D ; scripts 76, 81 | `S32_tornado_normalise.png` | aucun hors figure |
| B10 | Glossaire | annexe F | — | 99,5 % |

---

## Vérification : aucun chiffre nouveau

**Les quinze valeurs distinctes affichées ou prononcées** sont toutes publiées dans le mémoire et
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
recoloriées, donc aucun chiffre ne peut y avoir été déplacé.

---

## Figures reprises

**Six figures dans l'exposé principal, quatre dans les sauvegardes, toutes issues de
`exploratory/vasicek_lab/figures/` et produites par les scripts du projet.** Aucune capture de
page PDF, aucune figure redessinée, aucune figure inventée.

| Figure | Diapositive | Traitement |
|---|---|---|
| `H1_reseau_W.png` | 7 | aucune retouche, pleine largeur |
| `Z11_reversibilite_martingale.png` | 8 | aucune retouche, colonne gauche |
| `Z_identification_partielle.png` | 9 | aucune retouche, colonne gauche |
| `S24_interaction_canaux.png` | 10 | aucune retouche, pleine largeur |
| `Z9_p4_accumulation.png` | 11 | aucune retouche, pleine largeur |
| `Z18_valeur_information.png` | 12 | aucune retouche, colonne gauche |
| `J3`, `K3`, `Z17`, `J4`, `S15`, `S30`, `S32` | sauvegardes | aucune retouche |

**Trois figures sont presque carrées et ont reçu un gabarit à deux colonnes**, figure à gauche et
texte à droite. Posées pleine largeur elles se dimensionnaient sur la hauteur disponible et
n'occupaient qu'un tiers de la diapositive, étiquettes illisibles. C'est la transposition d'une
règle du mémoire, où une figure portrait prend une page entière et jamais un débord en largeur.

---

## Les distinctions de statut, maintenues sur les diapositives

Le support conserve les quatre statuts que le mémoire distingue, et il ne les aplatit nulle part.

| Statut | Où c'est dit sur les diapositives |
|---|---|
| **Calibré** | diapositive 6 : « deux canaux calibrables, la fréquence et la détection » |
| **Borné** | diapositive 6 et 14 : « deux canaux bornés, non calibrés » |
| **Illustratif** | diapositive 9, ligne en rouge : « le niveau affiché reste illustratif » ; diapositive 14 |
| **Non identifiable** | diapositives 5, 8 et 14, en rouge, la couleur étant réservée à cet usage |

**La couleur d'accent ne sert qu'à cela.** Rouge pour la non-identifiabilité, pour les alertes et
pour les deux piliers qui émettent le plus. Jamais décorative.

---

## Limites méthodologiques explicitement mentionnées

Sur la diapositive 14, en deux colonnes face à face, et rappelées dans les notes :

- la direction de contagion n'est pas identifiée ;
- le niveau absolu est illustratif, et il s'agit d'une borne supérieure à l'échelle d'une entité ;
- l'incertitude de queue est large ;
- deux canaux sur quatre sont des bornes posées, pas des calibrations.

Et en face, ce que le travail établit malgré cela : le signe et l'ordre de l'écart, la hiérarchie
des piliers, le cadre de bornage et son coût, la recommandation de reporting, la priorité de
collecte.

**Deux réserves supplémentaires vivent dans les notes orales** et doivent être exprimées si la
question vient : le retour sur investissement calculé sur le seul portage est un **majorant**, et
le backtest ne valide **pas** le quantile à 99,5 %, dont la puissance est chiffrée en années.

---

## Ce qui n'est pas dans l'exposé principal, et qui est réservé aux questions

Le mémoire fait 161 pages en version courte ; l'exposé en couvre la ligne directrice. Sont
délibérément absents des seize diapositives principales et disponibles en sauvegarde ou dans les
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
| Nombre de diapositives principales | **16**, dans la fourchette de 14 à 16 demandée |
| Diapositives de sauvegarde | **10**, plus un séparateur |
| Format | **16:9**, fond blanc cassé posé explicitement |
| Corps de texte | 19 à 24 pt ; titres 32 pt ; sources 12 pt |
| Diapositives surchargées | **aucune** après correction, voir ci-dessous |
| Figures illisibles | **aucune** après correction |
| Notes orales | **en français**, sur les 16 diapositives et les 10 sauvegardes |
| Sources du mémoire modifiées | **aucune** |

### Trois défauts trouvés en regardant les diapositives rendues

Ils n'auraient pas été vus en relisant le code, et c'est la règle du projet : on regarde la sortie.

1. **les flèches du schéma sortaient en carrés gris.** La numérotation des formes automatiques
   passée en nombre entier ne désigne pas ce qu'on croit ; l'énumération nommée corrige ;
2. **une figure presque carrée était illisible** posée pleine largeur : elle se dimensionnait sur
   la hauteur et n'occupait qu'un tiers de la diapositive. D'où le gabarit à deux colonnes ;
3. **deux blocs de texte passaient sous la bande « À retenir »**, donc coupés à l'écran. Les
   hauteurs ont été recalculées.

### Un ajout décidé après relecture

La diapositive 10 ne portait le chiffre de tête que dans les étiquettes de la figure. La ligne de
texte a été complétée pour dire **« au secteur »** avant les montants. Sans ce mot, un jury lit
vingt milliards pour une entité, et la question de l'échelle part avant qu'on ait pu la cadrer.
