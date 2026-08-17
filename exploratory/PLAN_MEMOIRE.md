# Plan du mémoire : ce qu'il reste à faire

Document de travail. Objectif : Prix SCOR. **État au 17 août 2026.**

La version précédente de ce fichier datait du 16 juillet et listait comme « à faire » les
scripts 16, 17 et 18, la rédaction du `main.tex` cascade et la décision Markov contre latente.
Tout cela est fait depuis. Ce document repart de l'état mesuré, pas de l'état déclaré.

---

## Où on en est, en chiffres relevés aujourd'hui

| Grandeur | Valeur | Comment elle se relit |
| --- | --- | --- |
| Corps du mémoire | **118 p.** | première page d'annexe moins une, dans `main.toc` |
| Document complet | **163 p.** | comptage des pages du PDF, jamais un index |
| Chapitres rédigés | 19 | dont 6 annexes |
| Scripts de calcul | 97 | `vasicek_lab/*/*.py` |
| Sorties versionnées | 93 | `sorties_verif/NN.txt` |
| Scripts cités par le mémoire | **79** | le reste est du travail non publié, voir A1 |
| Nombres publiés sous contrôle | 1 950 | harnais, tous chapitres |
| Confirmation | 98,3 % | 1 916 confirmés |
| **Couverture** | **100 %** | 0 hors contrôle non déclaré, et c'est ce qui passe en premier |
| Contrôles du document | 0 / 0 / 0 / 0 | `??` dans le PDF, Overfull vbox, annotation hors page, page tournée |

Le modèle est construit, calibré, **gelé depuis le 7 août** et vérifié. **A1 et A3 sont fermés
depuis le 17 août au soir** ; A2 attend les réponses des collègues et rien d'autre ne le débloque.

---

## A. Les trois trous du mémoire, par ordre de rendement

> **A1 et A3 sont fermés depuis le 17 août 2026 au soir.** Ce qui suit décrit ce qu'ils étaient
> et ce qui a été fait. **A2 reste ouvert** et attend les réponses des collègues.

### A1. Du travail fait, mesuré, versionné, et invisible pour le jury — **FERMÉ**

**Ce qui a été porté au mémoire :**

- **le dispositif de vérification est désormais décrit**, section D.1 de l'annexe des pièces
  justificatives : le principe, la formule de tolérance, les trois lignes rendues, pourquoi la
  couverture passe avant le taux, les trois états, **ce que le harnais ne fait pas**, les quatre
  classes de résidu et les trois erreurs réelles qu'il a trouvées. Plus un paragraphe dans la
  conclusion, section « Ce qui est établi », qui le compte comme un acquis de méthode. La section
  est déclarée hors script avec le motif de **circularité** : la faire vérifier par le harnais
  reviendrait à lui faire confirmer le nombre qui compte ce qu'il confirme ;
- **le +0,1 % du benchmark copule est requalifié** (script 80) : c'est **une graine**, l'écart
  valant +4,8 % d'étendue 10 points sur quatre. L'énoncé publié devient le seul qui tienne, à
  savoir que l'écart ne dépasse pas son propre bruit. Et **la séparation en queue ne vaut que pour
  la Student**, seule structure à dépendance de queue asymptotique ;
- **l'équivalence observationnelle Hawkes / cascade est écrite** (script 85), chapitre 13 : une
  cascade sans auto-excitation prédit n = 0,482 analytiquement et l'ajustement en trouve 0,480 au
  jour, contre 0,551 mesuré. Le rejet se reformule en équivalence suivie d'un choix de parcimonie
  interprétative, avec la mise en garde sur le sens de l'effet de résolution ;
- **l'ablation en échelle est publiée** (script 81), chapitre 12 : la queue à −76 % contre la
  propagation à −20 %, facteur 3,7, même conclusion que le tornado par un chemin indépendant. Avec
  le résultat qui ne s'attendait pas, la **forme de queue est héritée de la sévérité et non
  produite par la cascade** (CTE/VaR passe de 2,075 à 2,061 quand on retire la propagation) ;
- **les deux horloges** (script 79) et **le plafond avec la saturation** (script 86) ont chacun
  leur section d'annexe : le capital **concave** en durée de non-conformité, un trimestre portant
  33 % du surcoût annuel et une remédiation à mi-exercice n'en rendant que 44 % ; et le plafond
  comme **amortisseur** et non contrepoids, sans aucune crête de compensation.

Reste hors mémoire, et sans dommage : les scripts 83 et 87, dont les résultats sont déjà portés
autrement (la formule du retour au chapitre 12, la part d'amorce à l'annexe C).

<details>
<summary>Ce que le trou était</summary>

**Le plus rentable de toute la liste, et de loin.** Vingt sorties versionnées ne sont citées par
aucun chapitre, dont **les sept plus récentes : 79, 80, 81, 83, 85, 86, 87**.

Les cinq notions empruntées au préprint de cascade climatique ont été *mesurées* et leurs
résultats ne figurent dans aucun chapitre :

- la **concavité** du capital en durée de non-conformité : un trimestre porte déjà 33 % du
  surcoût annuel, remédier à mi-exercice ne rend que 44 % du bénéfice et non 50 % (script 79) ;
- l'échelle des quantiles : la séparation en queue **ne vaut que pour la Student**, et le
  +0,1 % publié est **une graine** parmi quatre (script 80) ;
- l'ablation en échelle : la brique la plus lourde est la **queue** à −76 %, pas la propagation
  à −20 %, par un chemin indépendant du tornado (script 81) ;
- l'**équivalence observationnelle** entre Hawkes et cascade : une cascade sans auto-excitation
  donne n = 0,480 au jour contre 0,551 mesuré (script 85) ;
- le plafond est un **amortisseur** et non un contrepoids de la saturation, l'interaction
  changeant de signe à thêta = 1 (script 86).

**Et le harnais lui-même n'est décrit nulle part.** Le mot n'apparaît qu'une fois dans le corps,
en passant, comme si le lecteur savait déjà de quoi il s'agit. Un dispositif qui vérifie 1 865
nombres publiés contre les sorties des scripts qui les produisent, avec une couverture de 100 %,
est un résultat de méthode et pas une coulisse. **Aucun jury ne peut le créditer s'il ne le lit
pas.** C'est le meilleur rapport valeur sur effort du projet : une section, aucun calcul.

</details>

### A2. Le second codage en aveugle — **OUVERT, en attente des collègues**

Le seul endroit où le mémoire **annonce une mesure qui n'existe pas encore**. Le kit est prêt,
dix récits, une heure de travail, et le formulaire est en état d'être envoyé depuis aujourd'hui.
Le script 54 attend son CSV et ne fabrique rien sans.

Tant qu'il manque, la direction de W repose sur un codeur unique, ce qui est exactement
l'objection qu'un jury formulera en premier sur la partie la plus originale du mémoire.

**Délai externe, donc à lancer avant tout le reste.**

### A3. Trancher le chiffre de tête — **FERMÉ**

**Le mémoire publie la lecture à quatre canaux : SCR 6 049 vers 20 188 M€, facteur 3,34, écart
14 139 M€.**

Il y avait non pas trois mais **quatre** protocoles en circulation, et ils diffèrent par le
**nombre de canaux relâchés** entre les deux états, par rien d'autre :

| Lecture | canaux | conforme | non conf. | facteur | source |
| --- | --- | --- | --- | --- | --- |
| score de conformité seul, g figé au niveau NC | 1 | 7 987 | 16 847 | 2,11 | script 25 |
| fréquence + propagation (lecture B) | 2 | 6 664 | 15 074 | 2,26 | script 16 |
| + détection (lecture C) | 3 | 5 932 | 16 595 | 2,80 | script 16 |
| **+ accumulation P4 (les quatre canaux)** | **4** | **6 049** | **20 188** | **3,34** | script 43 |

Le pire de la situation n'était pas la multiplicité : c'est que **le corps du mémoire publiait la
lecture B et que le chiffre à quatre canaux vivait en annexe**, sans qu'aucun texte ne dise qu'ils
diffèrent. Un encadré du chapitre 12 déclarait même la question « à trancher ».

**Motif du choix.** C'est la seule lecture où l'état conforme est conforme **sur tous les canaux
que le modèle possède**. Ailleurs, l'entité dite conforme propage encore comme une défaillante, ou
sa détection ou son accumulation tiers restent au niveau non conforme : ce n'est pas un état
conforme, c'est une remédiation partielle, et la nommer conforme sous-estime l'écart par
construction. Motif secondaire, tout l'aval en dépend déjà, la table des quatre canaux, Möbius,
les colonnes de fermeture et de Shapley, le portage.

**Ce qui a permis de trancher maintenant :** l'encadré excluait la détection tant que son ampleur
n'était pas validée. Elle l'est, le script 68 la chiffre à 2 928 ± 343 en Shapley, signe résolu
sur seize graines. La réserve a expiré.

**Les trois autres lectures ne sont pas retirées**, ce sont des remédiations partielles et leur
emboîtement chiffre ce que coûte de ne fermer qu'une partie des canaux. Deux précautions écrites :
le **facteur** se compare d'une lecture à l'autre mais l'**écart en euros non**, les bases
différant ; et la monotonie du facteur s'observe sans se tester ici, les protocoles ne partageant
ni graine ni base. Les rapports sont imprimés par la **section 3bis du script 67**.

Les trajectoires et la priorisation restent en lecture B, par choix d'objet (elles portent sur
l'ordre, invariant) et parce que les rejouer relèverait de la recalibration.

À une question de soutenance sur le résultat principal, il faut **une** réponse et sa
définition. **Ne pas remplacer un de ces chiffres par un autre sans avoir tranché** : ce serait
échanger un chiffre mal défini contre un autre.

---

## B. Nouvelles tâches, sorties de cette semaine

### B1. Le désaccord avec le préprint climatique, non écrit

Le mémoire cite ce préprint **quatre fois, toujours comme convergent**, et jamais sur le point
où les deux travaux s'opposent. Leur ablation donne la propagation dirigée comme brique la plus
lourde (VaR de 3,767 à 1,738 milliards) ; la nôtre donne la queue à −76 % et la propagation à
−20 %. Leur tornado met la probabilité d'arête en tête ; le nôtre met l'indice de queue dix fois
devant la propagation.

**La cause est identifiable et elle joue en notre faveur** : leur sévérité est bornée (réponse
bornée, perte plafonnée, multiplicateurs lognormaux d'écart-type logarithmique 0,10 et 0,15),
la nôtre est une GPD à variance infinie. Une queue bornée ne peut pas dominer. Donc le préprint
se cite sur le **protocole**, jamais sur l'**ordre du résultat**, qui est gouverné par l'indice
de queue. C'est déjà écrit pour l'échelle des quantiles, il faut l'étendre aux leviers.

Un lecteur qui trouve la divergence tout seul en conclut qu'on a retenu ce qui arrangeait.

### B2. Le théorème du coin supérieur, non repris (optionnel)

C'est la moitié analytique de leur papier et elle est absente : sous statique comparative
monotone et à aléas communs, le maximum sur un **pavé** de stress est atteint **au coin
supérieur**, trajectoire par trajectoire. Nous avons déjà l'ingrédient, le script 66 démontrant
que le capital est croissant en g. Cela transformerait l'état non conforme d'un scénario posé en
un coin supérieur démontré. Leurs remarques 2.7 et 2.8 fournissent les garde-fous, dont un
contre-exemple où le coin est infaisable.

Chantier plus lourd que les autres, à décider séparément. Aucun conflit avec le gel.

### B3. Le contrôle « 0 référence indéfinie » ne teste rien

**Découvert le 17 août, et ce n'est pas anecdotique.** Le contrôle se lit en cherchant le mot
dans la sortie de tectonic, or **tectonic n'émet aucun avertissement** pour une référence non
résolue avec cette invocation. Le contrôle passait à vide, probablement depuis le début.

Il avait laissé passer cinq `\ref{chap:etat-art}` pointant vers un label inexistant, soit
« cité au chapitre ?? » cinq fois dans le PDF, pages 50, 73, 88, 104 et 110. Corrigé.

**À faire : remplacer le contrôle par le comptage des `??` dans le PDF produit**, et l'inscrire
dans `CLAUDE.md` à la place de l'ancien.

### B4. Versionner la sortie du script 35

Le mémoire cite le script 35 (étude d'événement MOVEit, chapitre identifiabilité) et **sa sortie
n'est pas versionnée** : c'est le seul script cité sans sortie. Ses huit nombres sont donc non
confirmés.

Le fichier qu'il exige, `Data_Breach_Chronology.xlsx`, **est présent sur ce PC** (107 Mo, dans
`data/raw`, gitignoré). C'est donc faisable tout de suite, contrairement à ce que note encore
`CLAUDE.md`, qui décrit la situation du Mac.

### B5. La preuve d'efficience de Shapley en annexe (optionnel)

Le mémoire **affirme** la propriété d'efficience sans la démontrer. Elle tient en deux pages à
partir de la réécriture du poids `(1/n) x C(n-1,s)^(-1) = (n-s-1)! s! / n!`. Les six références
sont désormais dans la bibliographie. L'arbitrage de format étant tranché en notre faveur, rien
ne s'y oppose.

---

## C. Envois et relances, à lancer maintenant

Rien de ceci ne dépend de moi une fois parti, donc tout passe avant les chantiers de rédaction.

| Quoi | État | Reste |
| --- | --- | --- |
| Formulaire **codage en aveugle** | prêt, corrigé le 17 août | créer dans Apps Script, habillage 3 clics |
| Formulaire **sept phrases** | prêt, corrigé le 17 août | idem, réglages identiques |
| Formulaire **Cooke** | prêt, **NE PAS ENVOYER** | rien, voir ci-dessous |
| Mail Benoît Bénéteau et Samuel Cywie | rédigé | vérifier l'orthographe des noms, coller les liens, décider les copies |
| Message Teams squad cyber | rédigé | poster |

**Le formulaire Cooke ne part pas.** L'élicitation est abandonnée depuis le 12 août, le mémoire
porte une annexe qui explique pourquoi elle n'a pas été lancée, et la calibration est gelée : des
réponses ne pourraient pas être exploitées. Faire travailler des actuaires une demi-heure pour
rien coûte plus cher que ça ne rapporte. Il reste en annexe comme pièce justificative, ce qu'il
est déjà.

**Défaut corrigé avant envoi.** Le formulaire des sept phrases posait la question du consentement
à citation **deux fois**, avec des jeux d'options différents (quatre choix gradués en tête, trois
en fin). Un répondant pouvait se contredire sur le seul point où il doit être protégé. La seconde
est retirée.

---

## D. Vérifications dues

- **Les quatre jeux de chiffres SFCR contre les rapports.** Deux SCR sur quatre sont *déduits*
  d'un taux de couverture, et ce sont justement ceux dont la part attribuée à DORA est la plus
  frappante (26,3 et 41,3 %). La borne sous stress de plus ou moins 10 % existe déjà et **ne
  remplace pas la lecture des PDF**.
- **Le deck du 7 août est à 0 % de couverture**, vérifié aujourd'hui : 103 nombres, aucun sous
  contrôle, parce qu'il ne cite aucun script. C'est la faille qui avait laissé passer le
  `[0,32 ; 0,84]`. Le retrofit demande une ligne « Sources : scripts… » par slide et peut faire
  déborder des cadres d'un deck déjà présenté.
- **14 grandeurs dérivées** encore non imprimées par un script : le z = −0,33 du test de
  réversibilité (40), cinq quantités du corpus étendu (59), le multiple de capital 8,3 (58), le
  xi de Hill 1,42 (47).
- **Registre de sous-traitance.**

---

## E. Décisions en attente

| Décision | Qui tranche | Note |
| --- | --- | --- |
| Posture reportée : plug-in, prédictive ou robuste | Kélian avec Caroline | la grille existe, table des six postures avec leur bruit. Le robuste 95 % multiplierait le capital par 1,6 |
| Niveau de l'intervalle reporté, 90 ou 95 % | Kélian | ne déplacerait aucune calibration, seulement les bornes publiées et le facteur 2,5. À chiffrer avant de décider |
| CTE à 95 % en diagnostic à côté de la VaR | Kélian | **seul point de la liste de Caroline non traité** |
| Renommage `GBASE` / `G_BASE` | Kélian | 27 fichiers, pipeline gelé. La distinction est verrouillée dans la table des notations en attendant |
| Ancrage des valeurs de g sur ACPR ou EIOPA | Hugo | devenu optionnel depuis l'invariance (script 66) |

**Le format est tranché en faveur de Kélian.** Hugo a dit de ne pas se contraindre. Le corps est
à 117 pages contre les ~70 recommandés, et il n'y a plus de travail de compression à prévoir.

---

## F. Clos, à ne pas rouvrir

Le gel de la calibration (7 août), la convention de normalisation de W par l'émission maximale
(2,60), le statut de citation de Hackmageddon (la source **reste utilisée**, elle porte la
structure et jamais le niveau), le rejet du Hawkes, la non-transitivité (réfutée par son auteur,
remplacée par la dépendance à l'ordre), l'élicitation, l'anonymisation des entités, la convention
qui sépare la VaR de la charge annuelle du quantile de sévérité d'un sinistre, le détecteur de
contradictions entre scripts (instruit le 10 août puis écarté pour une raison), les séquences
ordonnées (refermées avec un critère de réouverture précis, script 75), et les decks des 7, 14 et
21 août.

---

## Ce qui fait un mémoire primé, et les deux pièges du moment

Un jury d'actuaires récompense l'originalité **maîtrisée** et l'honnêteté méthodologique. Les
trois atouts tiennent : un mécanisme neuf (la dépendance à l'ordre), une démonstration que la
contagion cyber n'est pas identifiable sur données publiques, et une pertinence réglementaire
directe. Le piège de juillet, survendre W comme calibré, a été évité et au-delà, puisque la
frontière d'identifiabilité est devenue une contribution à part entière.

**Premier piège restant : diluer le registre d'honnêteté.** Ce qui tient ce mémoire est qu'il
publie ses propres limites. Retirer un plus ou moins pour faire net, effacer que la posture la
plus prudente est la moins précise, taire un désaccord avec une source citée par ailleurs comme
convergente : trois façons de perdre ce qui distingue le travail.

**Second piège, et c'est celui d'aujourd'hui : laisser du travail mesuré hors du document.** Un
résultat qui n'est pas dans le mémoire n'existe pas pour le jury. Sept scripts et un dispositif
de vérification complet sont dans ce cas.

---

*Aucune date de remise ni de soutenance ne figure dans le dépôt : ce document est ordonné par
rendement, pas par échéance. La section C est à lancer aujourd'hui parce que son délai n'est pas
le nôtre ; A1 est le meilleur rapport valeur sur effort ; A3 est une décision d'une heure.*
