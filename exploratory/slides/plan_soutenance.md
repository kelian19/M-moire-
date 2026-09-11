# Plan de soutenance, mémoire d'actuariat DORA

Établi le 11 septembre 2026, à partir de `main_v3.pdf` (161 pages, version courte), des chapitres
LaTeX, des cinquante figures de `exploratory/vasicek_lab/figures/` et des sorties versionnées de
`sorties_verif/`. **Aucun chiffre de ce plan n'est nouveau** : tous sont repris du mémoire ou
d'une sortie de script.

---

## Une réserve de cadrage, à lever avant de répéter

La demande fixe **20 minutes d'exposé puis 10 de questions**. Le texte de l'Institut, relevé dans
`GUIDE_REDACTION.md` du dépôt, donne **25 minutes de présentation et 20 minutes de questions**,
et précise que « le non-respect du délai imparti peut être pénalisant ». Le plan ci-dessous est
calibré sur **20 minutes**, donc il tient dans les deux enveloppes, mais il laisse cinq minutes
libres si l'enveloppe officielle s'applique. **À vérifier auprès des responsables de voie.**

Second point du même texte, qui commande la conception : le support « ne constitue pas une
photocopie du mémoire et ne doit pas nécessairement suivre l'ordre des parties », et le jury
« essaie de retrouver dans le texte du mémoire ce que l'étudiant présente à l'oral ». **L'oral ne
doit donc rien affirmer que le document ne porte pas.**

---

## Titre de soutenance recommandé

> **Quand la contagion n'est pas identifiable : borner le capital DORA plutôt que le poser**
>
> *Quantification du besoin de capital lié à la non-conformité au règlement DORA*

Court, orienté problème, et il annonce la contribution au lieu du sujet. Le titre complet du
mémoire reste sur la page de garde.

## Message principal, en une phrase

> Les données publiques ancrent une partie du risque DORA mais **n'identifient pas la direction
> de contagion** entre piliers. La réponse actuarielle n'est donc pas de forcer une calibration :
> elle consiste à **borner le capital, qualifier l'incertitude, et transformer la donnée manquante
> en recommandation de reporting**.

## Trois messages secondaires

1. **La non-conformité ne se paie pas en pénalité, elle déplace la loi de perte.** Quatre
   paramètres bougent, et leurs effets **ne s'additionnent pas**.
2. **Une dépendance symétrique ne représente pas le mécanisme.** L'ordre de propagation change la
   criticité, et une matrice et sa transposée, indistinguables pour la donnée, donnent un capital
   et une décision différents.
3. **Le niveau absolu est illustratif, le rapport et la hiérarchie sont le résultat.** C'est
   déclaré dans le mémoire, pas concédé en séance.

---

## Déroulé, slide par slide

Durées cumulées entre parenthèses. Total visé : **20 minutes**.

| # | Titre | Objectif | À retenir | Source | Figure | Durée |
|---|---|---|---|---|---|---:|
| 1 | Titre | Poser l'identité | — | page de garde | — | 0:20 (0:20) |
| 2 | Une exigence de maîtrise sans exigence de capital | Poser le problème métier | DORA impose cinq domaines de maîtrise ; aucun module prudentiel ne les traduit en capital | ch. 1, ch. 2 | schéma construit, pas de figure | 1:30 (1:50) |
| 3 | Question, et ce que ce travail apporte | Annoncer la contribution | Trois apports : un mécanisme, une frontière, une lecture décisionnelle | ch. 1 § contribution | — | 1:20 (3:10) |
| 4 | Cinq domaines de contrôle, pas cinq cases | Cadrer DORA | La défaillance de l'un dégrade la capacité à tenir les autres | ch. 1, ch. 2 | schéma cinq blocs | 1:00 (4:10) |
| 5 | Ce que la donnée montre, et ce qu'elle ne montre pas | Préparer la non-identifiabilité | La co-occurrence est observable, la direction non | ch. 4, ch. 8 | tableau deux colonnes | 1:30 (5:40) |
| 6 | L'architecture, d'un état de conformité à une décision | Donner la chaîne complète | Partiellement calibré, partiellement borné | ch. 5 à 10 | schéma en chaîne | 1:30 (7:10) |
| 7 | L'ordre de propagation change la criticité | Justifier la cascade | Une copule capture la co-occurrence, pas la direction | ch. 6, ch. 10 § comparaison | `H1_reseau_W.png` | 1:30 (8:40) |
| 8 | La direction n'est pas identifiable, et c'est un résultat | Le cœur | Matrice et transposée indistinguables pour la donnée | ch. 8 | `Z11_reversibilite_martingale.png` | 2:00 (10:40) |
| 9 | Du point à la bande | Le résultat de capital | La bande quantifie l'incertitude au lieu de la masquer | ch. 9, ch. 10 | `Z_identification_partielle.png` | 2:00 (12:40) |
| 10 | Quatre canaux, et ils ne s'additionnent pas | Hiérarchiser les leviers | Isolés 9 138, total 14 139 : 5 001 d'interaction | ch. 10 | `S24_interaction_canaux.png` | 1:40 (14:20) |
| 11 | Le pilier des tiers, nœud d'accumulation | Le point DORA le plus opérationnel | Chocs communs et concentration, ce que DORA demande de cartographier | annexe C | `Z9_p4_accumulation.png` | 1:00 (15:20) |
| 12 | La donnée manquante devient un livrable | La contribution réglementaire | Quel champ de registre resserre la bande, et de combien | ch. 12 | `Z18_valeur_information.png` | 1:40 (17:00) |
| 13 | Ce que l'entité peut en faire | L'implication managériale | Remédier, détenir, transférer, et ne pas confondre borne et budget | ch. 10 § détenir ou transférer | — | 1:20 (18:20) |
| 14 | Ce que ce travail n'établit pas | Les limites, assumées | Quatre limites en face de ce qui tient malgré elles | ch. 11 | tableau deux colonnes | 1:10 (19:30) |
| 15 | Conclusion | Trois messages | La fausse précision n'est pas une réponse actuarielle | ch. 13 | — | 0:30 (20:00) |
| 16 | Questions | Clore sobrement | — | — | rappel de l'architecture | — |

**Quinze slides d'exposé plus la slide de questions.** Le format demandé est de quatorze à seize
hors annexes : la présentation est à seize, dont une sans contenu.

### Détail de ce qu'il ne faut pas surcharger

- **slide 2** : un schéma linéaire en cinq blocs, aucun article de règlement ;
- **slide 5** : deux colonnes, six mots par cellule ;
- **slide 8** : une figure, trois lignes de texte. C'est la slide où le jury doit comprendre, pas
  lire ;
- **slide 10** : trois nombres au plus, le reste dans la figure ;
- **slide 14** : deux colonnes face à face, jamais une liste de limites seule.

---

## Les résultats qui doivent impérativement être montrés

1. **le chiffre de tête** : 6 049 vers 20 188 M€ entre état conforme et non conforme, facteur
   3,34, écart 14 139 M€, et le fait que **quatre paramètres bougent** sans qu'aucune pénalité
   soit ajoutée ;
2. **la non-additivité** : 9 138 M€ en canaux isolés contre 14 139 au total, soit **5 001 M€
   d'interaction**, et sa conséquence : c'est la colonne de fermeture qu'un plan de remédiation
   doit citer ;
3. **la frontière d'identifiabilité** : la décomposition en partie symétrique et antisymétrique,
   et l'indistinguabilité d'une matrice et de sa transposée ;
4. **l'identification partielle** : l'énumération des 1 024 sommets et la bande qui en résulte ;
5. **le coût de l'ignorance directionnelle**, gradué et non stressé : la largeur croît
   linéairement avec l'ignorance et son maximum est connu d'avance ;
6. **la valeur de l'information** : quelle dépendance documenter en priorité ;
7. **le statut des niveaux** : illustratif au secteur, borne supérieure à l'entité.

## Ce qui est réservé aux questions

- les deux théorèmes d'extrapolation de queue et le choix du seuil ;
- la confrontation Hill contre maximum de vraisemblance ;
- le backtest hors échantillon et sa puissance chiffrée en années ;
- la décomposition de Möbius et le détail des effets croisés ;
- le biais de narration du corpus et son jackknife ;
- la formalisation bayésienne de la direction ;
- les quatre bilans réels et la descente d'échelle ;
- le protocole d'élicitation préparé et non exécuté ;
- la comparaison au processus auto-excité ;
- le dispositif de vérification des chiffres publiés.

---

## Script oral synthétique

**Ouverture, slides 1 à 3.** « DORA impose depuis janvier 2025 la maîtrise de cinq domaines de
résilience opérationnelle. Aucun dispositif prudentiel ne traduit ce niveau de maîtrise en
capital : la Formule Standard charge le risque opérationnel au forfait, donc elle est aveugle à
la conformité. La question de ce mémoire est donc : combien coûte en capital de ne pas se
conformer, et jusqu'où ce chiffre peut-il être affirmé. La seconde moitié de la question est ce
qui fait le travail. »

**Le modèle, slides 4 à 7.** « Les cinq piliers ne sont pas des cases à cocher, ce sont des
domaines de contrôle : la défaillance de l'un dégrade la capacité à tenir les autres. Pour
représenter cela, une dépendance symétrique ne suffit pas. Une copule capture bien la
co-occurrence des pertes, mais elle ne distingue pas une défaillance qui entraîne les autres
d'une défaillance qui les subit. Or c'est cette asymétrie qui commande la priorité de
remédiation. »

**Le cœur, slides 8 et 9.** « Et c'est ici que le travail rencontre sa limite, qui devient son
résultat. La matrice de contagion se décompose en une partie symétrique et une partie
antisymétrique. La donnée identifie la première, la co-occurrence. Elle n'identifie pas la
seconde, la direction. Une matrice et sa transposée sont indistinguables pour la donnée, et elles
donnent un capital et une décision différents. Plutôt que de poser la direction, ce mémoire borne
le capital sur l'ensemble des matrices admissibles, et chiffre en euros ce que la donnée manquante
coûte. »

**Les résultats, slides 10 à 13.** « La non-conformité n'ajoute aucune pénalité au capital : elle
déplace quatre paramètres de la loi de perte. Pris isolément ces quatre canaux somment à
9 138 millions quand l'écart total en vaut 14 139 : il manque 5 001 millions, soit 35 %, parce que
la cascade est super-additive sur ses canaux. La conséquence de gestion est directe : remédier un
canal rapporte davantage à une entité défaillante partout qu'à une entité déjà conforme. »

**La clôture, slides 14 et 15.** « Le niveau absolu est illustratif et le document le dit ; ce qui
est défendu est l'effet relatif et la hiérarchie. Quand la dépendance n'est pas identifiable, la
bonne réponse actuarielle n'est pas la fausse précision : c'est une borne, une hiérarchie de
données et une décision mieux informée. »

---

## Questions probables, et la première phrase de la réponse

Plusieurs sont des **pièges de prémisse** : la réponse commence alors par corriger la prémisse.

1. **« Vos chiffres sont en milliards, pour une seule entité ? »** Prémisse à corriger. Ces
   niveaux sont ceux du **secteur financier mondial**, la base de sévérité étant mondiale. Lue à
   la taille d'une entité, par la fréquence et par l'élasticité de sévérité, la méthode donne
   169 M€, et ce chiffre est publié comme **borne supérieure d'ordre de grandeur**, pas comme une
   mesure.
2. **« Votre matrice n'est pas calibrée. »** Exact, c'est démontré, et c'est pourquoi elle n'est
   pas posée mais bornée.
3. **« Pourquoi pas une copule ? »** Elle est implémentée comme jumeau numérique et comparée.
   Elle suit les marges et ne porte pas la direction.
4. **« Pourquoi pas un processus auto-excité ? »** Parce qu'il n'est **pas distinguable** de la
   cascade à la résolution disponible, et c'est mesuré, pas affirmé.
5. **« Pourquoi ne pas interroger des experts pour fixer la direction ? »** Un panel faiblement
   calibré introduirait une incertitude **non déclarable** en échange d'une ignorance mesurée. Le
   protocole est prêt et non exécuté, et l'annexe dit pourquoi.
6. **« Le modèle ne traite pas la défaillance simultanée de plusieurs piliers. »** Prémisse
   fausse : c'est une sortie du modèle, et à l'état non conforme elle est **majoritaire**.
7. **« Votre modèle est-il super-additif ? »** Il l'est sur les **canaux**, il est quasi additif
   sur les **piliers**, et l'additivité des **coûts** au sein d'un sinistre est une troisième
   chose, une hypothèse non testée. Les trois ne se confondent pas.
8. **« Le quantile à 99,5 % est-il testé ? »** Non, et la puissance est chiffrée : détecter un
   taux de dépassement double du nominal demanderait 1 811 années d'historique. Le backtest valide
   le centre et le corps, pas la queue.
9. **« Qu'est-ce qui est calibré, et qu'est-ce qui est posé ? »** Deux canaux sont calibrables,
   deux sont des bornes posées. Les trois valeurs du gain de propagation sont posées, et la thèse
   n'en dépend pas puisque le capital y est croissant.
10. **« À quoi cela sert-il concrètement ? »** À hiérarchiser une remédiation et à spécifier un
    registre d'incidents. Le chiffre à citer pour un plan est la colonne de **fermeture**, pas
    l'isolée.

---

## Ce que le support ne doit jamais écrire

Ces formulations ont déjà coûté une confusion en séance ou seraient fausses.

- **« le SCR DORA de telle entité »**. Écrire « besoin de capital ORSA au titre de DORA ». Il
  n'existe aucun module DORA en Formule Standard, et le rapport à un SCR publié est une **mise à
  l'échelle, pas une part** ;
- **additionner les quatre canaux** pour chiffrer une remédiation partielle : deux des quatre
  sont des bornes posées ;
- **additionner l'interaction entre canaux et l'interaction entre piliers** : deux partitions du
  même écart ;
- **confondre le quantile de sévérité d'un sinistre et la charge annuelle agrégée**. La confusion
  s'est produite en séance le 7 août 2026 ;
- **annoncer l'écart comme robuste à la sévérité**. L'invariance démontrée porte sur l'**échelle**
  et sur elle seule ;
- **nommer une entité réelle** ou une personne extérieure à l'encadrement ;
- **retirer une réserve pour faire plus net**. C'est ce que le jury note.
