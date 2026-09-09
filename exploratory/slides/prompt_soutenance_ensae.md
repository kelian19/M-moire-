# Prompt pour la construction du support de soutenance

Rédigé le 9 septembre 2026. À coller dans Claude avec les deux PDF joints,
`main_v2.pdf` (le mémoire d'actuariat) et `rapport_ensae.pdf` (le rapport de stage).

Tout ce qui suit est le texte du prompt. Il est autonome : l'agent qui le reçoit n'a
accès ni au dépôt ni à la passation, donc les contraintes, les chiffres et les interdits
y sont écrits en clair.

---

## LE PROMPT

Tu construis le support de soutenance d'un stage de fin d'études de l'ENSAE Paris, voie
actuariat. Deux documents sont joints : `main_v2.pdf`, le mémoire d'actuariat, et
`rapport_ensae.pdf`, le rapport de stage. Livrable attendu : un fichier PowerPoint au format
16:9, en français, avec des notes d'orateur sous chaque diapositive.

### 1. Le cadre officiel, et il est chiffré

Ces valeurs viennent des consignes de l'école. Elles ne se négocient pas.

- **La soutenance dure 45 minutes au total.**
- **L'exposé de l'élève dure 15 minutes**, pas plus. Il doit dégager les points les plus
  importants du travail et être **centré sur le travail réalisé pendant le stage**.
- **Les questions du jury durent 25 à 30 minutes**, donc **deux fois l'exposé**. C'est la
  partie la plus lourde de l'épreuve et le support doit la servir autant que l'exposé.
- La soutenance se tient **en visio, sur Teams**. Le support sera partagé en écran.
- Le jury comprend **un président extérieur à l'école et un enseignant de l'équipe
  pédagogique**. Pour la voie actuariat, la soutenance est organisée par l'**Institut des
  Actuaires** et le jury porte une **double validation, ENSAE et Institut**. Il faut donc
  supposer un jury mixte : un actuaire praticien, qui vérifiera la rigueur technique et la
  pertinence professionnelle, et un enseignant, qui vérifiera la démarche scientifique et le
  recul.
- Pour la voie actuariat, **le mémoire d'actuariat tient lieu de rapport de stage**. Les deux
  documents joints décrivent donc le même stage sous deux angles, et le support doit couvrir
  les deux.

**Conséquence de dimensionnement : quinze minutes valent treize à quinze diapositives, titre
compris.** Au-delà, l'exposé déborde et le débordement est visible du jury. Le plan ci-dessous
est calibré pour cela et il faut respecter son budget de temps, minute par minute.

### 2. Ce que le jury note, et comment chaque ligne se gagne

Le barème officiel est sur 20 points, en quatre lignes :

| Ligne | Points |
|---|---|
| Rapport et note de synthèse | 6 |
| Oral, présentation et réponses aux questions | 6 |
| Analyse et réflexion sur le contexte et les outils utilisés, qualité scientifique et technique | 6 |
| Évaluation du stagiaire par l'entreprise | 2 |

Le support agit sur les lignes deux et trois, soit **12 points sur 20**. Trois exigences
explicites des consignes sont mal servies par la plupart des supports et il faut les traiter
frontalement :

1. **faire apparaître quels enseignements de l'ENSAE ont été mobilisés**, et lesquels ;
2. **préciser la part de l'influence du maître de stage et de tierces personnes** dans la
   solution apportée ;
3. **attester d'une forme de recul sur l'expérience du stage**, y compris sur ce qui n'a pas
   marché.

Ces trois points ont leur propre diapositive dans le plan ci-dessous. Le rapport de stage les
porte dans sa section « Enseignements du stage », avec quatre sous-sections : le cadre de la
mission et ses contraintes, les enseignements de l'ENSAE mobilisés, la part de l'encadrement
et des tiers, ce que j'en retiens, ce que je ferais autrement. **Puise là et nulle part
ailleurs pour cette partie.**

Le jury doit aussi pouvoir apprécier l'esprit d'initiative et la façon dont la réflexion
personnelle a été menée. Donc partout où une décision a été prise, **dis qui l'a prise et
pourquoi**, plutôt que de présenter le résultat comme allant de soi.

### 3. Le plan imposé, avec son budget de temps

Une diapositive par ligne. Le titre de chaque diapositive doit être une **affirmation**, pas
une étiquette : « La direction de la contagion n'est pas identifiable » et non
« Identifiabilité ».

| # | Diapositive | Durée | Contenu |
|---|---|---|---|
| 1 | Titre | 20 s | Titre du mémoire, nom, ENSAE 3A, Nexialog Consulting, maître de stage Hugo Rapior, tutrice académique Caroline Hillairet, dates du 1er juin au 27 novembre 2026 |
| 2 | Le stage et la mission | 1 min | Nexialog Consulting, cabinet de conseil banque et assurance, département R&D. Deux destinataires du travail : un livrable client et un mémoire de recherche, qui ne demandent pas la même chose. Ce que le stage devait produire |
| 3 | Le problème, en une image | 1 min 30 | DORA impose la maîtrise de cinq domaines de résilience depuis janvier 2025. Aucun module de capital ne traduit ce niveau de maîtrise. La Formule Standard charge le risque opérationnel au forfait, donc elle est aveugle à la conformité. Une copule capture la co-occurrence mais pas la direction. La question retenue : combien coûte en capital de ne pas se conformer |
| 4 | Le marché qui justifie la question | 1 min | Une seule diapositive, pas plus. L'exposition cyber croît et se dégrade techniquement, sans traduction en exigence de capital. La queue française est vide : un seul sinistre au-delà de 10 M€ sur l'exercice 2025, et deux exercices sur sept sans aucun sinistre de la classe la plus haute. C'est ce qui commande de calibrer la sévérité sur une base internationale |
| 5 | Les données et leur statut de preuve | 1 min | Sept sources, chacune avec un statut de preuve explicite, de la source versionnée et rejouable à la citation externe non recalculable. La calibration est gelée depuis le 7 août, et c'est une décision de conduite de projet, pas de statistique |
| 6 | Le modèle en quatre équations | 1 min 30 | La charge annuelle composée et le capital comme son quantile à 99,5 %. La loi de comptage et sa surdispersion. La queue de Pareto généralisée. La cascade dirigée entre piliers. Écris les quatre équations, elles sont dans la section « Le modèle en quatre équations » du rapport de stage |
| 7 | La contribution : ce qui n'est pas identifiable | 1 min 30 | **C'est le cœur de l'exposé.** La matrice de contagion se décompose en une partie symétrique et une partie antisymétrique. La donnée identifie la première, la co-occurrence, et pas la seconde, la direction. Une matrice et sa transposée sont indistinguables pour la donnée et donnent un capital et une décision différents |
| 8 | Ce qu'on fait d'une limite : l'identification partielle | 1 min | Plutôt que de poser la direction, on borne le capital sur l'ensemble des matrices admissibles, par énumération exhaustive des 1 024 sommets. On publie un encadrement et le coût en euros de la donnée manquante |
| 9 | Le chiffre central | 1 min 30 | Le besoin de capital passe de 6 049 à 20 188 M€ entre l'état conforme et l'état non conforme, soit un facteur 3,34 et un écart de 14 139 M€. La non-conformité n'ajoute aucune pénalité : elle déplace quatre paramètres de la loi de perte |
| 10 | L'interaction, et ce qu'un plan de remédiation doit citer | 1 min | Les quatre canaux pris isolément somment à 9 138 M€ quand l'écart total vaut 14 139 : il manque 5 001 M€, soit 35 %, la cascade étant super-additive sur ses canaux. Conséquence de gestion : c'est la colonne de fermeture, et non l'isolée, qu'un plan de remédiation doit citer |
| 11 | Ce qui tient et ce qui ne tient pas | 1 min 30 | La validation hors échantillon, premier backtest du travail. La loi de comptage est validée, la forme de la queue survit, le niveau de sévérité dérive. Le niveau absolu du capital est illustratif ; ce qui est défendu est l'effet relatif et la hiérarchie des piliers |
| 12 | Ce que le stage a mobilisé, et le recul | 1 min 15 | Les enseignements de l'ENSAE effectivement appliqués, nommés un par un. La part de l'encadrement : ce que le maître de stage a tranché, ce que la tutrice académique a fait changer, ce qu'une relecture extérieure a produit. Ce que je ferais autrement |
| 13 | Conclusion et suites | 45 s | Ce qui a été réalisé, ce qui n'a pas pu l'être, et ce que la continuation demanderait |

**Total : 15 minutes.** Si une diapositive dépasse son budget, retire du contenu, ne réduis
pas le budget des suivantes.

### 4. Les diapositives de repli, et elles sont aussi importantes que l'exposé

Les questions durent 25 à 30 minutes. Prépare **douze à quinze diapositives de repli**, placées
après la conclusion, **numérotées de B1 à B15** de façon à pouvoir être appelées à la voix
(« j'ai une diapositive sur ce point, la B7 »). Une question par diapositive, une réponse
chiffrée par diapositive. Sujets, dans cet ordre :

- **B1** la table complète des quatre canaux, avec ses trois lectures : isolée, fermeture,
  Shapley ;
- **B2** l'attribution par pilier et l'ordre de remédiation ;
- **B3** l'analyse de sensibilité, en élasticités et non en plages ;
- **B4** la trajectoire du capital et la durée de non-conformité, dont la concavité ;
- **B5** le backtest en détail, avec sa puissance chiffrée en années ;
- **B6** la règle de sélection du seuil de la loi de queue ;
- **B7** la descente d'échelle du secteur vers l'entité, et sa borne de validité ;
- **B8** l'application à quatre bilans réels, entités anonymisées ;
- **B9** l'inventaire des limites, en deux colonnes, écarts involontaires et choix de
  prudence ;
- **B10** la mise en regard des cadres existants, dont la Formule Standard et une copule ;
- **B11** la lecture économique, portage et sinistralité évitée ;
- **B12** la comparaison au risque de contagion documenté dans la littérature ;
- **B13** les défaillances simultanées de plusieurs piliers, qui sont une sortie du modèle et
  non un cas non traité ;
- **B14** les trois énoncés d'additivité, à ne pas confondre ;
- **B15** le dispositif de vérification des chiffres publiés.

### 5. La fiche des chiffres, et ils ne doivent pas bouger

Reprends ces valeurs telles quelles. **Tout autre chiffre doit être repris mot pour mot des
deux PDF joints. N'invente aucun chiffre, n'en arrondis aucun autrement qu'il ne l'est dans
les documents, ne calcule aucun ratio nouveau.**

**Où trouver quoi.** Le mémoire porte l'essentiel de ces valeurs, mais **trois d'entre elles ne
figurent que dans le rapport de stage** : les deux niveaux du canal de détection, 0,128 et 0,181,
et l'ablation de la queue, 76,2 %. Ne les signale pas comme introuvables, elles sont dans le
second PDF.

**Le chiffre de tête**
- état conforme 6 049 M€, état non conforme 20 188 M€
- facteur 3,34, écart 14 139 M€
- ce sont les niveaux de la **lecture à quatre canaux**, seule où l'état conforme est conforme
  sur tous les canaux du modèle. Le mémoire publie **trois autres lectures**, comme des
  remédiations partielles, dont les écarts sont plus petits parce qu'elles relâchent moins de
  canaux. **Ne pas les mélanger et ne jamais remplacer un de ces chiffres par un autre.** Si tu
  as besoin d'un de ces trois écarts, reprends-le du mémoire et vérifie de quelle ligne il
  vient ; ne le déduis pas

**Les quatre canaux que la conformité déplace**
- fréquence : de 21,6 à 53,6 sinistres par an
- détection : taux de dépassement de 0,128 à 0,181
- propagation : gain de 0,45 à 0,90
- accumulation tiers : charge de facteur commun de 0 à 0,68

**Les trois lectures d'un canal, en M€**

| Canal | isolé | fermeture | Shapley |
|---|---|---|---|
| Fréquence | 4 328 | 8 775 | 6 546 |
| Détection | 1 448 | 4 562 | 2 928 |
| Accumulation | 1 728 | 3 402 | 2 576 |
| Propagation | 1 633 | 2 402 | 2 088 |
| Somme | 9 138 | 19 141 | 14 139 |

- interaction 5 001 M€, soit 35 %
- encadrement : 9 138 inférieur ou égal à 14 139 inférieur ou égal à 19 141

**La cascade**
- rayon spectral de la matrice de propagation 0,506, sous-critique
- taux de reproduction 0,054, gain critique 1,78
- identification partielle : énumération exhaustive de 1 024 sommets

**La sévérité, calibration gelée**
- seuil 20,03 M€, 91 excès, indice de queue 0,5954, échelle 57,97
- quantile de sévérité à 99,5 % pour un sinistre : 662,78 M€, intervalle à 90 % de 411,5 à 1 037

**La validation hors échantillon**
- loi de comptage validée : couverture 91,7 % contre 75 % pour la loi de Poisson
- forme de la queue : le test passe
- niveau de sévérité : dépassements trois fois trop fréquents, et le motif est une dérive
- la dérive n'est pas homogène : 13,0 % par an sur le corps de la distribution contre 4,00 %
  dans la queue, soit un facteur 3,2
- la puissance est chiffrée : détecter un taux de dépassement double du nominal à 99,5 %
  demanderait 1 811 années d'historique

**Ce que la dérive fait à la thèse**
- le facteur entre états passe de 3,344 à 3,124, soit une baisse de 6,6 %
- l'écart en euros ne bouge que de 1,9 %, mais **par compensation** entre deux composantes de
  sens contraire

### 6. Les interdits, et ils sont absolus

Ces formulations ont déjà coûté une confusion en séance ou seraient fausses. **Aucune ne doit
apparaître, ni sur une diapositive, ni dans une note d'orateur.**

1. **Ne jamais écrire « le SCR DORA de telle entité ».** La grandeur calculée n'est pas un SCR
   réglementaire, il n'existe aucun module DORA en Formule Standard. Écrire **« besoin de
   capital ORSA au titre de DORA »**. Le rapport à un SCR publié est une mise à l'échelle, pas
   une part.
2. **Ne jamais additionner les quatre leviers** pour chiffrer une remédiation partielle. Deux
   des quatre canaux sont des bornes posées, pas des budgets.
3. **Ne pas confondre le quantile de sévérité et la charge annuelle agrégée.** Le 662,78 M€ est
   un quantile de sévérité pour **un sinistre**, ce n'est pas un capital. Le niveau 99,5 % n'a
   de sens réglementaire que sur un horizon annuel. Cette confusion s'est produite en séance le
   7 août 2026.
4. **Ne pas dire qu'une source de comptage d'incidents est rejetée.** Elle est utilisée : elle
   porte la **structure** du risque par vecteur d'attaque, jamais son **niveau**. Ce qui est
   tranché est son statut de preuve, citation externe non recalculable.
5. **Ne pas dire que le processus auto-excité est rejeté.** L'énoncé juste est une
   **équivalence observationnelle** à la résolution disponible, suivie d'un choix de parcimonie
   interprétative.
6. **Ne pas dire « le modèle est super-additif » sans préciser sur quoi.** Il l'est sur les
   quatre **canaux**, il est quasi additif sur les cinq **piliers**, et l'additivité des
   **coûts** au sein d'un sinistre est une troisième chose, une hypothèse de construction non
   testée. Les trois se confondent facilement et donnent des réponses opposées.
7. **Ne pas annoncer l'écart comme robuste à la sévérité.** L'invariance démontrée porte sur
   l'**échelle** et sur elle seule.
8. **Ne pas présenter le besoin de capital d'une entité notionnelle comme une mesure.** C'est
   une **borne supérieure d'ordre de grandeur**, et le motif est écrit.
9. **Ne pas présenter le backtest comme validant le quantile à 99,5 %.** Il valide le centre et
   le corps de la distribution, et sa puissance sur la queue est nulle sur tout historique
   existant.
10. **Ne nommer aucune entité réelle.** Les quatre bilans sont anonymisés en classes de taille.
11. **Ne nommer aucune personne extérieure à l'encadrement.** La relecture de praticien se cite
    sous la forme « une consultante de Nexialog ».
12. **Ne jamais additionner l'interaction entre canaux et l'interaction entre piliers.** Ce sont
    deux partitions différentes du même écart, et les additionner double le même euro. Voir aussi
    les deux pièges de figure de la section 9.
13. **Ne retirer aucune réserve pour faire plus net.** Ce travail vaut par ce qu'il déclare de
    ses propres limites : une hypothèse réfutée par son auteur, un chiffre central requalifié en
    borne, une borne de validité publiée. Toute reformulation qui rend une réserve moins visible
    dégrade le travail, même si elle le fait paraître plus assuré.

### 7. Les questions que le jury posera, et la première phrase de la réponse

Prépare une **banque de questions** en fin de fichier, hors diapositives, avec pour chaque
question la première phrase de la réponse et le numéro de la diapositive de repli à appeler.
Ces neuf questions sont celles qui reviendront, et plusieurs sont des **pièges de prémisse** :
la réponse commence alors par corriger la prémisse, pas par s'excuser.

1. « Votre matrice de contagion n'est pas calibrée. » Réponse : c'est exact et c'est démontré,
   et c'est pourquoi elle n'est pas posée mais bornée.
2. « Le modèle ne traite pas la défaillance simultanée de plusieurs piliers. » **Prémisse
   fausse** : c'est une sortie du modèle, et à l'état non conforme elle est majoritaire, 62,31 %
   des sinistres touchant plus d'un pilier contre 31,15 % à l'état conforme.
3. « Pourquoi ne pas avoir utilisé un processus auto-excité, qui est la référence sur le
   cyber ? » Réponse : parce qu'il n'est pas distinguable de la cascade à cette résolution, et
   c'est mesuré.
4. « Pourquoi ne pas avoir interrogé des experts pour fixer la direction ? » Réponse : parce
   qu'un panel faiblement calibré introduirait une incertitude non déclarable, chiffrée, en
   échange d'une ignorance mesurée.
5. « Votre niveau de capital est-il crédible ? » Réponse : le niveau est illustratif et le
   document le dit ; ce qui est défendu est l'effet relatif et la hiérarchie.
6. « Le quantile à 99,5 % est-il testé ? » Réponse : non, et la puissance du test est chiffrée
   en années, ce qui vaut mieux qu'une absence de rejet.
7. « Qu'est-ce qui est de vous, et qu'est-ce qui vient de votre encadrement ? » Réponse
   attendue par le barème, donc préparée et honnête.
8. « Quelle est l'hypothèse la plus lourde du modèle ? » Réponse : l'additivité des coûts au
   sein d'un sinistre, non testée, dont le coût est borné par une analyse de sensibilité.
9. « À quoi cela sert-il à un assureur ? » Réponse : à hiérarchiser une remédiation, et le
   chiffre à citer est la colonne de fermeture.

### 8. Le style et le format

- **16:9**, français, **corps de texte au minimum 20 points** : le support sera lu en visio, sur
  des écrans de taille inconnue, et un tableau à petits caractères est illisible dans ces
  conditions.
- **Un message par diapositive.** Le titre porte l'affirmation, le corps l'étaie en trois points
  au maximum. Pas de paragraphe : le jury lit avant d'écouter, et une diapositive dense fait
  perdre l'attention pendant qu'il la déchiffre.
- **Cinq lignes de tableau au maximum** par diapositive. Au-delà, la table part en repli.
- **Aucune animation, aucune transition.** Le partage d'écran en visio les rend illisibles.
- **Numérote les diapositives**, y compris les replis, en B1 à B15.
- Palette sobre, deux couleurs et un neutre, celles de la charte du cabinet :
  encre `#1B1E30`, encre secondaire `#223E55`, accent `#a6002e`, second accent `#009a94`,
  fond `#FCFCFB`, gris de grille `#DCDCDC`. **Pas de dégradé, pas d'ombre, pas d'icône
  décorative.**
- **Pas de tirets cadratins.** Pas de tournures qui trahissent une rédaction automatique : pas
  de « il est important de noter que », pas de « dans un monde où », pas de triades
  décoratives, pas de conclusion qui recommence l'exposé.

### 9. Les figures, et comment les insérer

Les figures existent dans les deux PDF et sont produites par les scripts du projet. **Ne les
redessine pas et n'en invente aucune.** Pour chaque diapositive qui en demande une, insère un
**cadre de réservation** portant en clair le numéro de la figure et le début de sa légende, de
façon à ce que l'image soit collée ensuite. Les numéros sont ceux du mémoire.

| Diapositive | Figure | Légende, début |
|---|---|---|
| 3 | 10.8 | Ce que chaque cadre exprime de l'effet DORA : 0 % pour la Formule Standard, 62 % pour la copule, 100 % pour la cascade |
| 4 | 1.3 | Montant indemnisé par classe de taille de sinistre |
| 5 | 4.1 | Les deux biais, enfin chiffrés |
| 6 | 6.1 | Structure dirigée de la matrice sur les cinq piliers |
| 7 | 8.2 | La direction comme courant irréversible, et pourquoi la donnée ne peut pas la voir |
| 8 | 9.1 | Identification partielle de la contagion dirigée : le résultat central du mémoire |
| 9 | **aucune** | table des deux états et des quatre canaux, depuis la fiche de la section 5 |
| 10 | **aucune** | table des trois lectures d'un canal, depuis la fiche de la section 5 |
| 11 | 5.4 | Validation du socle |
| B1 | **aucune** | table complète des quatre canaux et de leurs trois lectures, depuis la fiche |
| B2 | 10.2, 10.3, 10.5 | décomposition par pilier, allocation Shapley contre marginaux, puis valeur d'accélération et ordre de remédiation. Trois diapositives B2a, B2b, B2c si nécessaire |
| B4 | 10.4 | Trajectoire du capital et évolution des états |
| B7 | 10.9 | La descente d'échelle, rendue cohérente |
| B8 | 10.11 | Le besoin de capital sur quatre bilans réels |
| B9 | 11.1 | La bande de modèle, troisième étage d'incertitude |

**Une figure par diapositive au maximum.** Si une figure porte plusieurs panneaux, dis dans la
note d'orateur lequel commenter, et ne commente que celui-là. En particulier, sur la figure 10.8,
ne commente que la comparaison des trois cadres et **pas** le panneau de mise en regard avec les
primes de marché, qui porte une entité notionnelle et une borne supérieure.

**DEUX PIÈGES DE FIGURE, ET ILS SONT LA RAISON POUR LAQUELLE LES DIAPOSITIVES 9 ET 10 N'EN
PORTENT AUCUNE.** Ne les contourne pas en allant chercher une figure qui « ressemble ».

- **La figure 10.1 montre le besoin de capital par état de conformité sur une lecture à TROIS
  canaux emboîtés**, pas sur les quatre. Ses niveaux ne sont donc pas ceux de la diapositive 9 :
  l'illustrer avec cette figure ferait apparaître deux chiffres différents pour la même phrase, et
  un jury le verrait. Quatre protocoles distincts chiffrent « l'écart entre conforme et non
  conforme » dans ce travail, et ils donnent quatre résultats parce qu'ils ne relâchent pas le
  même nombre de canaux. Le chiffre de tête est la lecture à quatre canaux, seule où l'état
  conforme est conforme sur tous les canaux du modèle. **Une table est la bonne réponse ici.**
- **Les figures 10.2 et 10.3 portent l'interaction entre les cinq PILIERS**, pas celle entre les
  quatre canaux. Ce sont **deux partitions différentes du même écart** et elles ne se
  additionnent jamais. La diapositive 10 parle de l'interaction entre canaux, 5 001 M€ : elle ne
  peut pas être illustrée par une figure d'attribution par pilier. Ces deux figures vont en repli,
  sur la question de l'attribution par pilier, où elles sont à leur place.

### 10. Ce que je veux en sortie

1. **Le fichier PowerPoint**, treize diapositives d'exposé plus les replis B1 à B15.
2. **Une note d'orateur sous chaque diapositive d'exposé**, rédigée pour être dite et non lue :
   phrases courtes, verbe conjugué, et **la durée cible en tête de la note**. La somme des
   durées doit faire 15 minutes.
3. **La banque des neuf questions** de la section 7, en fin de fichier, hors diapositives.
4. **Une liste de ce que tu n'as pas pu établir depuis les deux PDF**, s'il y a lieu, plutôt
   qu'une valeur inventée pour combler.

### 11. Ce qu'il ne faut pas faire

- **Ne fais pas un cours.** Ni sur le règlement, ni sur la théorie des valeurs extrêmes, ni sur
  les processus ponctuels. Les consignes demandent un exposé centré sur le travail réalisé, et
  un inventaire de méthodes est explicitement signalé comme un défaut du rapport.
- **Ne résume pas les 192 pages du mémoire.** Choisis. Ce qui n'entre pas dans les treize diapositives va
  en repli, et ce qui n'entre pas en repli n'est pas dit.
- **N'ouvre pas sur le modèle.** Ouvre sur le problème, sinon le jury ne sait pas pourquoi le
  modèle existe.
- **Ne termine pas sur une limite.** Les limites vont à la diapositive 11, la conclusion dit ce
  qui a été fait et ce qui suit.
- **Ne mets aucun chiffre qui ne soit pas dans les deux PDF ou dans la fiche de la section 5.**

---

## Notes pour Kélian, hors prompt

- **La mention de confidentialité.** Si Nexialog l'exige, la diapositive de titre doit la
  porter et la soutenance cesse d'être publique. Décision non prise au 9 septembre.
- **Le courriel au service des stages** sur les dispositions prises pour la voie actuariat
  reste à envoyer, les consignes le qualifient d'impératif.
- **Les figures à exporter** avant de coller : elles sont dans
  `exploratory/vasicek_lab/figures/`, en PNG, à la charte. Les numéros de figure du tableau de
  la section 9 sont ceux du mémoire, identiques dans les deux versions ; seule la pagination
  diffère entre `main.pdf` et `main_v2.pdf`.
- **Ce que le prompt ne demande pas exprès et qu'il faudra vérifier sur le résultat** : que
  les treize durées somment bien à quinze minutes, et que la diapositive 12 nomme des
  enseignements précis plutôt que des intitulés de cours. C'est cette diapositive qui porte le
  plus de points de barème pour le moins de contenu disponible.
