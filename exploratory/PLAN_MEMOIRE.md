# Plan du mémoire : ce qu'il reste à faire

Document de travail. Objectif : Prix SCOR. **État au 17 août 2026.**

La version précédente de ce fichier datait du 16 juillet et listait comme « à faire » les
scripts 16, 17 et 18, la rédaction du `main.tex` cascade et la décision Markov contre latente.
Tout cela est fait depuis. Ce document repart de l'état mesuré, pas de l'état déclaré.

---

## Où on en est, en chiffres relevés aujourd'hui

| Grandeur | Valeur | Comment elle se relit |
| --- | --- | --- |
| Corps du mémoire | **117 p.** | première page d'annexe moins une, dans `main.toc` |
| Document complet | **159 p.** | comptage des pages du PDF, jamais un index |
| Chapitres rédigés | 19 | dont 6 annexes |
| Scripts de calcul | 97 | `vasicek_lab/*/*.py` |
| Sorties versionnées | 93 | `sorties_verif/NN.txt` |
| Scripts cités par le mémoire | **74** | le reste est du travail non publié, voir A1 |
| Nombres publiés sous contrôle | 1 865 | harnais, tous chapitres |
| Confirmation | 98,2 % | 1 831 confirmés |
| **Couverture** | **100 %** | 0 hors contrôle non déclaré, et c'est ce qui passe en premier |
| Contrôles du document | 0 / 0 / 0 / 0 | référence indéfinie, Overfull vbox, annotation hors page, page tournée |

Le modèle est construit, calibré, **gelé depuis le 7 août** et vérifié. Ce qui reste n'est plus
de produire mais de **rendre visible** ce qui est déjà mesuré, et de fermer trois trous.

---

## A. Les trois trous du mémoire, par ordre de rendement

### A1. Du travail fait, mesuré, versionné, et invisible pour le jury

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

### A2. Le second codage en aveugle

Le seul endroit où le mémoire **annonce une mesure qui n'existe pas encore**. Le kit est prêt,
dix récits, une heure de travail, et le formulaire est en état d'être envoyé depuis aujourd'hui.
Le script 54 attend son CSV et ne fabrique rien sans.

Tant qu'il manque, la direction de W repose sur un codeur unique, ce qui est exactement
l'objection qu'un jury formulera en premier sur la partie la plus originale du mémoire.

**Délai externe, donc à lancer avant tout le reste.**

### A3. Trancher le chiffre de tête

Trois valeurs circulent pour « l'écart entre conforme et non conforme » et elles ne mesurent pas
la même chose, parce qu'elles ne déplacent pas les mêmes paramètres :

| Valeur | Source | Ce qu'elle fait |
| --- | --- | --- |
| −53 % | script 25 | balaie q de 0 à 1 en gardant **g au niveau non conforme** |
| facteur 3,34 | script 43 | les quatre canaux, sévérité et échelle inchangées |
| −64 % (OpRisk), −75 % (PRC) | script 20 | par état, sur les 32 configurations |

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
