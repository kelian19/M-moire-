# Plan du mémoire : ce qu'il reste à faire

Document de travail. Objectif : Prix SCOR. **État au 17 août 2026.**

La version précédente de ce fichier datait du 16 juillet et listait comme « à faire » les
scripts 16, 17 et 18, la rédaction du `main.tex` cascade et la décision Markov contre latente.
Tout cela est fait depuis. Ce document repart de l'état mesuré, pas de l'état déclaré.

---

## Où on en est, en chiffres relevés aujourd'hui

| Grandeur | Valeur | Comment elle se relit |
| --- | --- | --- |
| Corps du mémoire | **121 p.** | première page d'annexe moins une, dans `main.toc` |
| Document complet | **167 p.** | comptage des pages du PDF, jamais un index |
| Chapitres rédigés | 19 | dont 6 annexes |
| Scripts de calcul | 98 | `vasicek_lab/*/*.py` |
| Sorties versionnées | 95 | `sorties_verif/NN.txt` |
| Scripts cités par le mémoire | **82** | le reste est du travail deja porte autrement |
| Nombres publiés sous contrôle | 1 964 | harnais, tous chapitres |
| Confirmation | 99,9 % | 1 963 confirmés |
| **Couverture** | **100 %** | 0 hors contrôle non déclaré, et c'est ce qui passe en premier |
| Contrôles du document | 0 / 0 / 0 / 0 | `??` dans le PDF, Overfull vbox, annotation hors page, page tournée |

Le modèle est construit, calibré, **gelé depuis le 7 août** et vérifié. **A1, A3, B, D et E sont fermés
depuis le 17 août au soir** ; A2 attend les réponses des collègues et rien d'autre ne le
débloque.

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

## B. Nouvelles tâches de la semaine — **TOUTES FERMÉES le 17 août 2026 au soir**

### B1. Le désaccord avec le préprint climatique — FERMÉ

Écrit au chapitre 12, dans la section de sensibilité, avec sa table de comparaison et son
explication. Leur brique la plus lourde est la propagation dirigée (VaR de 3,767 à 1,738
milliards, soit −53,9 %), la nôtre est la queue (−76 %) ; leur tornado met la probabilité
d\'arête en tête, le nôtre l\'indice de queue dix fois devant la propagation.

**La cause est identifiable dans leur propre texte** : leur sévérité est bornée, donc elle
n\'a pas d\'indice de queue, et leur ablation ne contient aucune brique de queue. Les deux
classements sont corrects chacun dans son modèle. Conséquence de citation : le préprint se
cite sur le **protocole**, jamais sur l\'**ordre** d\'un résultat en queue.

Leurs chiffres sont enregistrés sous le statut de **citation externe, non recalculable** et
imprimés par le script 63, au même titre que Hackmageddon. Le fichier config.py n\'a pas été
touché.

### B2. Le théorème du coin supérieur — FERMÉ, et il ne transporte qu\'à moitié

Nouveau **script 88**. Trois résultats, et le deuxième n\'était pas prévu.

1. **Le coin supérieur est démontré au sens du quantile.** Sur les 65 paires emboîtées des
   seize configurations, relâcher un canal de plus ne fait **jamais** baisser le capital,
   graine par graine. L\'état non conforme est donc le maximum du pavé, et un test de
   résistance sur les quatre canaux se réduit à une seule évaluation. Contrôle exact aux deux
   coins : 6 049 et 20 188.
2. **La version trajectorielle du préprint ne transporte pas**, et le motif diffère selon le
   canal. À aléas communs, la perte d\'une année baisse dans 16,2 % des cas quand on relâche la
   propagation et dans **30,7 %** quand on relâche la détection. Pour la propagation, la table
   des sous-ensembles n\'est pas ordonnée par inclusion ; pour la détection, qui viole le plus,
   p_u entre dans la **transformation de sévérité** et non dans une table, ce qui n\'a rien à
   voir avec la cascade. L\'obtenir demanderait un couplage monotone, donc d\'autres tirages :
   recalibration, le gel l\'interdit, et le gain serait un renforcement d\'énoncé sans
   déplacement de conclusion.
3. **Un coin peut être infaisable**, et c\'est le garde-fou qui compte. Deux canaux sur quatre
   sont des bornes posées : rien ne garantit qu\'une entité présente les quatre au maximum
   simultanément. Le coin est donc un **majorant sur un pavé déclaré**, pas la description
   d\'une entité, ce qui est exactement le statut déjà donné à l\'état non conforme.

Écrit à l\'annexe C, après l\'identité de Möbius.

### B3. Le contrôle « 0 référence indéfinie » — FERMÉ

Remplacé dans CLAUDE.md par le comptage des ?? dans le PDF produit, avec l\'explication
(tectonic n\'émet aucun avertissement, le grep passait à vide). Les cinq renvois cassés qu\'il
avait laissés passer sont corrigés. Une note sur les **ligatures** est ajoutée au passage :
chercher « vérification » dans le texte du PDF échoue parce que le i sort en U+FB01.

### B4. La sortie du script 35 — FERMÉ

Relancée sur ce PC, où Data_Breach_Chronology.xlsx est présent, et versionnée. **Le chapitre
09 passe de 95,5 à 100 % de confirmation** : les huit nombres de l\'étude d\'événement MOVEit
étaient les seuls non confirmés. La phrase du mémoire qui annonçait que sa sortie n\'était pas
versionnée est corrigée, et la section cite désormais le script.

### B5. La preuve d\'efficience de Shapley — FERMÉ

Écrite à l\'annexe des démonstrations de la cascade, par la réécriture du poids et l\'argument
télescopique sur les permutations. Avec deux paragraphes de portée : ce que l\'efficience
garantit (une partition exacte, quel que soit le signe de l\'interaction) et ce qu\'elle ne
garantit pas (une part de Shapley n\'est pas une contribution marginale, et pas un budget de
remédiation puisque deux canaux sont bornés). Et pourquoi aucun échantillonnage n\'est
nécessaire à cinq piliers.

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

## E. Les cinq décisions, tranchées le 17 août 2026

Prises en jugement de modélisation, chacune avec son motif écrit dans le mémoire et son critère
de réouverture. Aucune ne déplace une calibration.

### E1. Posture reportée : le **plug-in avec sa bande**

La robuste reste publiée comme axe prudentiel déclaré. Trois raisons, de natures différentes.

1. **Réglementaire, et elle vient en premier.** Le régime définit le SCR comme une VaR à 99,5 %
   de la variation des fonds propres. Une borne haute sur un ensemble d\'ambiguïté est un
   *supremum sur une famille de lois*, pas un quantile de la loi de perte : la substituer répond
   à une autre question. Le risque d\'estimation se traite par la validation et le récit ORSA,
   non en gonflant le quantile, sinon la même logique appliquée à chaque module empilerait des
   marges dont le niveau de confiance global ne serait plus énonçable.
2. **Une mesure, et c\'est elle qui rend le choix confortable.** La prédictive, théoriquement
   préférable, vaut 645 contre 657 pour le plug-in, soit deux fois le bruit. **La bonne réponse
   ne déplace pas le point.** La reporter échangerait un nombre publié partout contre un nombre
   indiscernable, au prix de la piste d\'audit. L\'écart passe à +4 % à 99,9 % : c\'est en
   profondeur de queue, non au niveau réglementaire, que la posture compterait.
3. **La précision, et elle va contre l\'intuition.** Les postures robustes sont les moins
   reproductibles des six (± 13, ± 9, ± 24) quand les deux extrémités n\'ont aucun bruit.
   Reporter la valeur la moins précise contredirait la convention du mémoire.

**Ce que la décision ne dit pas.** La robuste est le bon nombre pour un *autre* usage :
dimensionner une couverture est une décision sous ambiguïté, où l\'on veut la borne haute.
**Réouverture** si l\'écart prédictive / plug-in dépassait durablement quelques unités de bruit
au niveau réglementaire, ou si l\'objet passait du capital reporté à une décision sous ambiguïté.

Écrit au chapitre 13, sous-section « La posture retenue ».

### E2. Niveau de l\'intervalle : **90 % reste le niveau reporté**

Et c\'est une correction, pas seulement une décision : l\'annexe **se contredisait**. Son
ouverture annonçait « le choix retenu est désormais 95 % » quand sa conclusion, deux pages plus
bas, gardait 90 % avec trois motifs. L\'ouverture est corrigée.

**L\'argument décisif est mesuré et il tue l\'idée de relever le nominal.** La couverture réelle
vaut 86,8 ± 0,8 % pour un niveau annoncé de 90, et 91,8 ± 0,6 % pour un niveau annoncé de 95 :
**le manque est le même, −3,2 points dans les deux cas.** Passer à 95 % ne répare rien, cela
déplace l\'annonce sans corriger l\'estimateur. Et la constance du déficit en points désigne la
cause, un écart-type asymptotique trop petit à 91 excès, propriété connue des intervalles GPD à
petit échantillon.

Le 95 % reste publié comme alternative chiffrée, avec le fait que l\'élargissement du capital est
**très asymétrique** : la borne basse ne descend que de 315 M€ quand la haute monte de 7 790.

### E3. La CTE en diagnostic : **déjà fait**, la liste de Caroline est vidée

Le plan la donnait comme le seul point non traité. C\'est faux : l\'annexe D porte la table
complète (CTE à 95, 99 et 99,5 %) et surtout le nombre qui rend les deux conventions
comparables, **CTE_β = VaR 99,5 % pour β = 97,73 %**. Une CTE à 95 % vaut 5 734 M€ contre 8 374 :
rapportée comme capital elle serait **moins** prudente que l\'exigence, dans un rapport de 1,46.
La réserve d\'existence tient, la mesure n\'étant pas définie sous PRC.

### E4. GBASE / G_BASE : **on ne renomme pas**, on rend la confusion impossible à commettre

Vingt-sept fichiers sur un pipeline gelé, pour un problème de nommage : mauvais rapport risque
sur gain. Et surtout **une substitution sémantiquement fausse mais numériquement valide ne serait
rattrapée par aucun contrôle**, le harnais vérifiant que les nombres sortent des scripts et non
qu\'ils veulent dire ce qu\'on croit.

Ce qui remplace le renommage, dans le script 63 : les deux constantes imprimées côte à côte avec
leur nature, leur unité et leur module, plus **deux assertions** garantissant que le gain reste un
scalaire, l\'échelon une table par pilier, et que le premier ne prend aucune valeur de la seconde.
C\'est le seul point où la substitution pouvait passer inaperçue. Même pattern que pour p_u :
déclarer et garder plutôt que déplacer.

### E5. Ancrage des valeurs de g sur ACPR ou EIOPA : **non, et c\'est une décision**

Le motif n\'est pas la disponibilité mais la **nature** de ce que ces sources publient : des
attentes prudentielles et des échelles de maturité, jamais des probabilités de propagation entre
domaines de contrôle. Passer des unes aux autres demanderait une **seconde correspondance posée**,
et le résultat serait pire que la valeur posée d\'aujourd\'hui : il aurait l\'apparence d\'un
calibrage sans en être un.

**Et l\'invariance rend l\'ancrage sans objet.** Le capital étant croissant en g, un ancrage
n\'achèterait que l\'amplitude, soit exactement la part déjà déclarée comme un scénario. Même
arbitrage que celui qui a écarté l\'élicitation : une source faiblement calibrée introduit une
incertitude **non déclarable** en échange d\'une ignorance mesurée.

**Le format est tranché en faveur de Kélian.** Hugo a dit de ne pas se contraindre.

--- | --- | --- |
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
