# Plan du mémoire : ce qu'il reste à faire

Document de travail. Objectif : Prix SCOR. **État au 3 septembre 2026.**
**Remise : fin novembre 2026.**

La version précédente de ce fichier datait du 17 août et listait comme dues la lecture des
rapports SFCR, le passage du deck du 7 août sous harnais et quatorze grandeurs non imprimées.
Tout cela est fait. Ce document repart de l'état mesuré, pas de l'état déclaré.

---

## Où on en est, en chiffres relevés aujourd'hui

| Grandeur | Valeur | Comment elle se relit |
| --- | --- | --- |
| Corps du mémoire | **130 p.** (v1) / **136 p.** (v2) | première page d'annexe moins une |
| Document complet | **178 p.** (v1) / **185 p.** (v2) | comptage des pages du PDF, jamais un index |
| Chapitres rédigés | 19 | dont 6 annexes |
| Scripts de calcul | 106 | `vasicek_lab/*/*.py` |
| Sorties versionnées | 101 | `sorties_verif/NN.txt` |
| Scripts cités par le mémoire | **88** | le reste est du travail deja porte autrement |
| Nombres publiés | 2 172 | harnais, tous chapitres |
| Confirmation | **100 %** | 2 172 confirmés |
| **Couverture** | **100 %** | 0 hors contrôle non déclaré, et c'est ce qui passe en premier |
| Contrôles du document | 0 / 0 / 0 / 0 | `??` dans le PDF, Overfull vbox, annotation hors page, page tournée |

Le modèle est construit, calibré, **gelé depuis le 7 août** et vérifié. **A1, A3, B, C, D et E
sont fermés** ; **A2 est confié à Hugo Rapior**, qui l'annonce pour la fin de la semaine du
2 septembre, et la réception est prête et testée. Rien d'autre ne dépend de l'assistant.

**Avec trois mois devant, l'ordre de travail n'est plus celui du délai mais celui de la
dépendance externe.** Ce qui dépend des autres (le second codage, la relecture par praticiens)
se charge en septembre parce que son délai ne se comprime pas ; ce qui dépend de Kélian
(compression du corps, finition, deck de soutenance) tient en octobre et novembre.

---

## A. Les trois trous du mémoire, par ordre de rendement

> **A1 et A3 sont fermés depuis le 17 août 2026 au soir.** Ce qui suit décrit ce qu'ils étaient
> et ce qui a été fait. **A2 reste ouvert**, mais il est confié à Hugo Rapior et daté de la fin
> de la semaine du 2 septembre, et sa réception est prête et testée.

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

### A2. Le second codage en aveugle — **OUVERT, mais confié et daté**

Le seul endroit où le mémoire **annonce une mesure qui n'existe pas encore**. Le kit est prêt,
dix récits, une heure de travail. Le script 54 attend son CSV et ne fabrique rien sans.

**Hugo Rapior s'en charge et l'annonce pour la fin de la semaine du 2 septembre.** La réception
est prête et **testée** : `54b_reception_formulaire.py` convertit l'export du formulaire Google
vers le format long du script 54, et deux commandes suffisent. Deux défauts réels avaient été
trouvés en la préparant, et ils auraient bloqué le vendredi soir : les sept grilles partagent le
même intitulé, donc les soixante-dix colonnes de l'export ont des **en-têtes identiques** et la
correspondance doit être positionnelle ; et le formulaire répond par position (« le 1er a
entraîné le 2e ») quand le script 54 attend un nom de domaine. Le convertisseur **n'interprète
rien** : il écrit le nom désigné et laisse au 54 la sémantique de la relation.

Tant qu'il manque, la direction de W repose sur un codeur unique, ce qui est exactement
l'objection qu'un jury formulera en premier sur la partie la plus originale du mémoire.

**Deux choses à ne pas oublier à l'arrivée.** Déclarer que le second codeur est **le tuteur** et
non un praticien indépendant du projet, ce qui est une limite et se dit. Et porter le
coefficient **avec son intervalle**, jamais seul.

**Et si le codage n'arrive jamais, le mémoire tient quand même**, ce qui est mesuré et non
espéré : le script 64 borne déjà l'objection par l'adverse. Retirer les onze arêtes partant de
P1 laisse p = 0,0039 ; la pire configuration à quatre arêtes retournées atteint p = 0,084 ;
rendre P1 muette déplace le capital d'entité de 41,9 M€, soit **0,81 fois** la largeur de la
bande d'identification déjà publiée (51,7 M€). Accorder au critique la totalité de son objection
coûte donc **moins** cher que l'ignorance directionnelle que le mémoire assume et publie.

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
d'arête en tête, le nôtre l'indice de queue dix fois devant la propagation.

**La cause est identifiable dans leur propre texte** : leur sévérité est bornée, donc elle
n'a pas d'indice de queue, et leur ablation ne contient aucune brique de queue. Les deux
classements sont corrects chacun dans son modèle. Conséquence de citation : le préprint se
cite sur le **protocole**, jamais sur l'**ordre** d'un résultat en queue.

Leurs chiffres sont enregistrés sous le statut de **citation externe, non recalculable** et
imprimés par le script 63, au même titre que Hackmageddon. Le fichier config.py n'a pas été
touché.

### B2. Le théorème du coin supérieur — FERMÉ, et il ne transporte qu'à moitié

Nouveau **script 88**. Trois résultats, et le deuxième n'était pas prévu.

1. **Le coin supérieur est démontré au sens du quantile.** Sur les 65 paires emboîtées des
   seize configurations, relâcher un canal de plus ne fait **jamais** baisser le capital,
   graine par graine. L'état non conforme est donc le maximum du pavé, et un test de
   résistance sur les quatre canaux se réduit à une seule évaluation. Contrôle exact aux deux
   coins : 6 049 et 20 188.
2. **La version trajectorielle du préprint ne transporte pas**, et le motif diffère selon le
   canal. À aléas communs, la perte d'une année baisse dans 16,2 % des cas quand on relâche la
   propagation et dans **30,7 %** quand on relâche la détection. Pour la propagation, la table
   des sous-ensembles n'est pas ordonnée par inclusion ; pour la détection, qui viole le plus,
   p_u entre dans la **transformation de sévérité** et non dans une table, ce qui n'a rien à
   voir avec la cascade. L'obtenir demanderait un couplage monotone, donc d'autres tirages :
   recalibration, le gel l'interdit, et le gain serait un renforcement d'énoncé sans
   déplacement de conclusion.
3. **Un coin peut être infaisable**, et c'est le garde-fou qui compte. Deux canaux sur quatre
   sont des bornes posées : rien ne garantit qu'une entité présente les quatre au maximum
   simultanément. Le coin est donc un **majorant sur un pavé déclaré**, pas la description
   d'une entité, ce qui est exactement le statut déjà donné à l'état non conforme.

Écrit à l'annexe C, après l'identité de Möbius.

### B3. Le contrôle « 0 référence indéfinie » — FERMÉ

Remplacé dans CLAUDE.md par le comptage des ?? dans le PDF produit, avec l'explication
(tectonic n'émet aucun avertissement, le grep passait à vide). Les cinq renvois cassés qu'il
avait laissés passer sont corrigés. Une note sur les **ligatures** est ajoutée au passage :
chercher « vérification » dans le texte du PDF échoue parce que le i sort en U+FB01.

### B4. La sortie du script 35 — FERMÉ

Relancée sur ce PC, où Data_Breach_Chronology.xlsx est présent, et versionnée. **Le chapitre
09 passe de 95,5 à 100 % de confirmation** : les huit nombres de l'étude d'événement MOVEit
étaient les seuls non confirmés. La phrase du mémoire qui annonçait que sa sortie n'était pas
versionnée est corrigée, et la section cite désormais le script.

### B5. La preuve d'efficience de Shapley — FERMÉ

Écrite à l'annexe des démonstrations de la cascade, par la réécriture du poids et l'argument
télescopique sur les permutations. Avec deux paragraphes de portée : ce que l'efficience
garantit (une partition exacte, quel que soit le signe de l'interaction) et ce qu'elle ne
garantit pas (une part de Shapley n'est pas une contribution marginale, et pas un budget de
remédiation puisque deux canaux sont bornés). Et pourquoi aucun échantillonnage n'est
nécessaire à cinq piliers.

## C. Envois et relances — **FAIT le 17 août 2026**

Les deux formulaires sont créés et diffusés, le mail est parti, le message Teams est posté.
**Le formulaire Cooke n'est pas parti**, conformément à la décision : l'élicitation est
abandonnée depuis le 12 août, la calibration est gelée, et des réponses ne pourraient pas être
exploitées. Il reste en annexe comme pièce justificative, ce qu'il est déjà.

**Défaut rattrapé juste avant l'envoi**, et il valait le détour : le formulaire des sept phrases
posait la question du consentement à citation **deux fois**, avec des jeux d'options différents,
quatre choix gradués en tête et trois en fin. Un répondant pouvait donc se contredire sur le seul
point où il doit être protégé, sans qu'aucune des deux réponses ne fasse foi. La seconde est
retirée.

### Ce que cet envoi change au calendrier

**L'horloge n'est plus la mienne.** Tout ce qui restait sous mon contrôle est fermé (A1, A3, B,
D, E) ; ce qui reste attend des gens. La conséquence pratique est qu'il faut prévoir la relance
plutôt que l'espérer : sur ce genre de sollicitation, une partie des destinataires ne répondra
pas, et **il ne faut qu'un seul second codeur** pour débloquer A2.

**Où cela en est au 3 septembre.** Le second codage est **confié à Hugo Rapior**, qui l'annonce
pour la fin de la semaine du 2 septembre, et la réception est prête et testée (voir A2). La
relecture par praticiens, elle, **n'a produit aucun retour** depuis l'envoi du 17 août : c'est
elle qu'il faut relancer, et c'est le seul point du calendrier de septembre qui traîne. Avec
trois mois devant, viser **trois codeurs** plutôt qu'un change la nature du résultat.

### Quand les réponses arrivent, la chaîne à dérouler

À écrire ici parce que c'est le moment où l'on oublie une étape.

1. **Codage en aveugle** : verser le CSV au format du gabarit gabarit_second_codeur.csv, lancer
   le script 54, qui ne fabrique rien sans donnée. Il rend le coefficient d'accord inter-juges.
2. Porter ce coefficient au chapitre d'identifiabilité, **avec son intervalle**, et rattacher la
   section au script 54. C'est ce qui ferme A2 : la direction de W cesse de reposer sur un
   codeur unique.
3. **Sept phrases** : les désaccords se citent en premier, sous la forme que chaque répondant a
   choisie. Si la phrase 3 ou la 4 est contredite par une expérience de terrain, c'est le modèle
   qui bouge, pas la citation qu'on aménage.
4. Repasser le harnais sur le chapitre touché, et vérifier la couverture avant le taux.

---

## D. Vérifications dues — **toutes faites, sauf une qui ne dépend pas de nous**

- ~~Les quatre jeux de chiffres SFCR contre les rapports~~ : **FAIT le 2 septembre 2026**, sur
  les rapports 2024 eux-mêmes. **Une erreur de champ trouvée** sur l'assureur non-vie B, dont le
  3 234 M€ était saisi comme total d'actif alors que le rapport le donne comme fonds propres
  éligibles (actifs réels 5 305, et 5 305 − 2 071 = 3 234 le confirme) : le SCR déduit valait 292
  quand le rapport en publie **812,5**, et la part attribuée à DORA passe de 41,3 à **16,7 %**.
  Trois gains, dont un qui **supprime une limite déclarée** : les quatre SCR sont publiés, donc
  la réserve « deux SCR sur quatre sont déduits » et sa borne sous stress de ±10 % n'ont plus
  d'objet. Le forfait de 3 % se compare désormais au module opérationnel publié et **se trompe
  dans les deux sens**, −8 % et +56 %, donc il n'est ni majorant ni minorant. Et le **test du
  levier a changé de sens** : la part de l'entité notionnelle passe de 13 à 9 %, soit sous le
  critère de 10 %, de sorte que la requalification du 169 M€ en borne supérieure repose
  désormais sur le **seul** argument de taille, qui tient par lui-même.
- ~~Le deck du 7 août à 0 % de couverture~~ : **FAIT le 17 août**, il est à 100 % sous contrôle
  ou déclaré, et la crainte de faire déborder des cadres était infondée. **Reste un chiffre à
  savoir** : le 8 553 M€ du contrôle croisé en marche aléatoire n'est reproduit par aucun des
  scripts cités, à vérifier avant réutilisation.
- ~~14 grandeurs dérivées non imprimées~~ : **traitées**, le harnais étant à 100 % de
  confirmation sur 2 034 nombres.
- **Registre de sous-traitance** : le seul point restant, et il ne dépend pas de nous.

---

## E. Les cinq décisions, tranchées le 17 août 2026

Prises en jugement de modélisation, chacune avec son motif écrit dans le mémoire et son critère
de réouverture. Aucune ne déplace une calibration.

### E1. Posture reportée : le **plug-in avec sa bande**

La robuste reste publiée comme axe prudentiel déclaré. Trois raisons, de natures différentes.

1. **Réglementaire, et elle vient en premier.** Le régime définit le SCR comme une VaR à 99,5 %
   de la variation des fonds propres. Une borne haute sur un ensemble d'ambiguïté est un
   *supremum sur une famille de lois*, pas un quantile de la loi de perte : la substituer répond
   à une autre question. Le risque d'estimation se traite par la validation et le récit ORSA,
   non en gonflant le quantile, sinon la même logique appliquée à chaque module empilerait des
   marges dont le niveau de confiance global ne serait plus énonçable.
2. **Une mesure, et c'est elle qui rend le choix confortable.** La prédictive, théoriquement
   préférable, vaut 645 contre 657 pour le plug-in, soit deux fois le bruit. **La bonne réponse
   ne déplace pas le point.** La reporter échangerait un nombre publié partout contre un nombre
   indiscernable, au prix de la piste d'audit. L'écart passe à +4 % à 99,9 % : c'est en
   profondeur de queue, non au niveau réglementaire, que la posture compterait.
3. **La précision, et elle va contre l'intuition.** Les postures robustes sont les moins
   reproductibles des six (± 13, ± 9, ± 24) quand les deux extrémités n'ont aucun bruit.
   Reporter la valeur la moins précise contredirait la convention du mémoire.

**Ce que la décision ne dit pas.** La robuste est le bon nombre pour un *autre* usage :
dimensionner une couverture est une décision sous ambiguïté, où l'on veut la borne haute.
**Réouverture** si l'écart prédictive / plug-in dépassait durablement quelques unités de bruit
au niveau réglementaire, ou si l'objet passait du capital reporté à une décision sous ambiguïté.

Écrit au chapitre 13, sous-section « La posture retenue ».

### E2. Niveau de l'intervalle : **90 % reste le niveau reporté**

Et c'est une correction, pas seulement une décision : l'annexe **se contredisait**. Son
ouverture annonçait « le choix retenu est désormais 95 % » quand sa conclusion, deux pages plus
bas, gardait 90 % avec trois motifs. L'ouverture est corrigée.

**L'argument décisif est mesuré et il tue l'idée de relever le nominal.** La couverture réelle
vaut 86,8 ± 0,8 % pour un niveau annoncé de 90, et 91,8 ± 0,6 % pour un niveau annoncé de 95 :
**le manque est le même, −3,2 points dans les deux cas.** Passer à 95 % ne répare rien, cela
déplace l'annonce sans corriger l'estimateur. Et la constance du déficit en points désigne la
cause, un écart-type asymptotique trop petit à 91 excès, propriété connue des intervalles GPD à
petit échantillon.

Le 95 % reste publié comme alternative chiffrée, avec le fait que l'élargissement du capital est
**très asymétrique** : la borne basse ne descend que de 315 M€ quand la haute monte de 7 790.

### E3. La CTE en diagnostic : **déjà fait**, la liste de Caroline est vidée

Le plan la donnait comme le seul point non traité. C'est faux : l'annexe D porte la table
complète (CTE à 95, 99 et 99,5 %) et surtout le nombre qui rend les deux conventions
comparables, **CTE_β = VaR 99,5 % pour β = 97,73 %**. Une CTE à 95 % vaut 5 734 M€ contre 8 374 :
rapportée comme capital elle serait **moins** prudente que l'exigence, dans un rapport de 1,46.
La réserve d'existence tient, la mesure n'étant pas définie sous PRC.

### E4. GBASE / G_BASE : **on ne renomme pas**, on rend la confusion impossible à commettre

Vingt-sept fichiers sur un pipeline gelé, pour un problème de nommage : mauvais rapport risque
sur gain. Et surtout **une substitution sémantiquement fausse mais numériquement valide ne serait
rattrapée par aucun contrôle**, le harnais vérifiant que les nombres sortent des scripts et non
qu'ils veulent dire ce qu'on croit.

Ce qui remplace le renommage, dans le script 63 : les deux constantes imprimées côte à côte avec
leur nature, leur unité et leur module, plus **deux assertions** garantissant que le gain reste un
scalaire, l'échelon une table par pilier, et que le premier ne prend aucune valeur de la seconde.
C'est le seul point où la substitution pouvait passer inaperçue. Même pattern que pour p_u :
déclarer et garder plutôt que déplacer.

### E5. Ancrage des valeurs de g sur ACPR ou EIOPA : **non, et c'est une décision**

Le motif n'est pas la disponibilité mais la **nature** de ce que ces sources publient : des
attentes prudentielles et des échelles de maturité, jamais des probabilités de propagation entre
domaines de contrôle. Passer des unes aux autres demanderait une **seconde correspondance posée**,
et le résultat serait pire que la valeur posée d'aujourd'hui : il aurait l'apparence d'un
calibrage sans en être un.

**Et l'invariance rend l'ancrage sans objet.** Le capital étant croissant en g, un ancrage
n'achèterait que l'amplitude, soit exactement la part déjà déclarée comme un scénario. Même
arbitrage que celui qui a écarté l'élicitation : une source faiblement calibrée introduit une
incertitude **non déclarable** en échange d'une ignorance mesurée.

**Les cinq arbitrages qui figuraient ici sont tranchés**, chacun dans sa sous-section E1 à E5
ci-dessus. Une table les redonnait comme ouverts, ce qui contredisait la section : elle est
retirée. Ce qui reste n'est pas un arbitrage mais une **validation** : le choix de posture est à
présenter à Caroline, pas à reprendre.

**Le format est tranché en faveur de Kélian.** Hugo a dit de ne pas se contraindre. Le corps est
à 130 pages en v1 et 136 en v2, contre les ~70 recommandés de l'Institut.

**Ce qui change avec la remise fin novembre, et c'est le seul point rouvert par le calendrier.**
Une compression du corps était écartée faute de temps ; trois mois la rendent possible, et c'est
le second levier sur la note après le second codage. Quatre blocs sont compressibles et ils sont
déjà ordonnés par ce qu'ils coûtent : la table graduée du chapitre 12, la sous-section du
chapitre 13 sur l'étage de modèle, la sous-section du chapitre 11 sur la dépendance des états,
et les deux paragraphes d'élasticité du chapitre 12. **La décision reste à Kélian**, et l'ordre
de grandeur de l'enjeu est qu'un jury note ce qu'il trouve en vingt minutes de lecture.

---

## Depuis le 17 août : ce qui a été fait les 2 et 3 septembre 2026

- **Les quatre rapports SFCR sont lus** : voir la section D, qui porte l'erreur trouvée et les
  trois gains.
- **La dynamique du facteur systémique entre au mémoire**, chapitre 06, section
  `sec:dynamique-Y`. C'était la question de Caroline, qui demandait quelle **trajectoire** suit
  `Y_j,t` puisque la PD de crédit sous Vasicek est portée par un brownien. La réponse tient en
  deux temps et elle est publiable : le `Y_j,t` publié **n'a pas de trajectoire**, il est iid en
  t, ce qui est *le même objet* qu'un incrément brownien normalisé au pas comptable ; mais un
  facteur purement brownien imposerait un indice de dispersion de 1, or il est mesuré à 1,19,
  2,24 et 9,20 selon l'échelle, ce qui **identifie une composante de saut**. La section publie
  donc la forme à sauts avec sa normalisation, et déclare l'hypothèse de renouvellement retenue.
  La brique ne déplace aucune probabilité marginale, donc **aucun capital publié**.
- **Le harnais atteint 100 % pour la première fois**, 1 979 sur 1 979 ce jour-là. Le dernier nombre non
  confirmé cachait un défaut réel : la conclusion écrivait que le rapport détention / transfert
  « résiste » **et** qu'il tombe « à moins de 11 % de sa valeur », ce qui se contredit, et le
  11 % n'était reproduit par aucun script. Remplacé par une **identité** imprimée par la
  nouvelle section 3ter du script 67, avec l'effet de forme borné à +36 % sur une plage de SCR
  d'un facteur quatre.
- **Le deck du 21 août est réécrit** : voir la note en section F.
- **Ce fichier et `CLAUDE.md` sont remis à l'état mesuré**, et 96 antislashs parasites devant
  des apostrophes ont été retirés d'ici, séquelles d'une écriture scriptée.

## Le 8 septembre : le premier backtest hors échantillon du projet (script 89)

Le mémoire validait l'adéquation **dans** l'échantillon (Anderson-Darling, Kolmogorov-Smirnov,
balayage de seuil, bootstrap de $\xi$) et ne demandait jamais au modèle de prédire une période
qu'il n'avait pas vue. C'était le trou le plus visible, et c'est la première question d'un jury
d'actuaires sur un modèle de capital. Protocole : origine glissante un pas en avant, fenêtre
2004-2025, douze années notées hors échantillon.

**Trois résultats, et ils ne vont pas dans le même sens.**

1. **La loi de fréquence est validée, et c'est un gain net.** La binomiale négative couvre
   **91,7 %** pour un intervalle annoncé à 90 %, quand Poisson ne couvre que **75 %**. Elle
   gagne aussi au log-score prédictif, donc son paramètre supplémentaire n'est pas payé par une
   largeur inutile. Le choix de surdispersion cesse d'être une précaution et devient une mesure.
2. **La forme de la queue survit au test PIT**, ce qui n'était pas acquis avec vingt à quatre-
   vingt-dix excès par ajustement. La GPD n'est donc pas la mauvaise famille.
3. **Les quantiles de sévérité sont dépassés trois fois trop souvent** et le test de Kupiec les
   rejette aux deux niveaux (huit dépassements contre 2,8 attendus à 99 %, p = 0,0078).

**Le motif du troisième est mesuré, et il n'est pas celui qu'on attendrait.** Ce n'est pas la
queue : c'est l'**échelle** de la loi de sévérité qui dérive. Le taux de dépassement du seuil
vaut 15,1 % en apprentissage contre **27,1 %** hors échantillon (rapport 1,80, p = 2,4·10⁻⁷), et
la médiane annuelle des pertes monte de **13 % par an** en log (p = 0,0003). Une fenêtre
d'apprentissage qui s'étend garde les petites pertes anciennes, donc elle retarde sur la dérive.
C'est un défaut de **stationnarité**, pas de famille.

**LA DÉRIVE N'EST PAS HOMOGÈNE, ET C'EST LE GARDE-FOU À CONNAÎTRE.** Le point ci-dessus invite à
une erreur d'un facteur trois, et la **section 1ter** du script, écrite le même jour, la corrige.
La dérive de 13,0 % par an est celle du **corps** (la médiane) ; dans la **queue** elle ne vaut
que **4,00 % par an** (écart-type 1,84, rapport de vraisemblance p = 0,0386), soit un facteur
**3,2**. L'effet à déclarer sur la grandeur publiée est donc de **+24,7 %**, ou **+162 M€** sur le
quantile de sévérité à 99,5 %, et c'est une **borne basse** puisque le taux de dépassement est
tenu commun aux deux branches.

**Deux résultats de la 1ter qui valent d'être connus.** Supposer que la queue dérive comme le
corps, en indexant toutes les pertes à la tendance de la médiane, donne un quantile de 4 291 M€,
soit 6,5 fois la référence, et un indice de queue de **1,27** à la borne haute de l'intervalle de
la tendance : **au-dessus de un, l'espérance de la sévérité cesse d'exister**. La variante se
rejette donc par un **argument d'existence**, du même type que celui qui écarte la source PRC
comme support d'une mesure de couverture. Et modéliser la dérive fait **tomber** ξ de 0,5979 à
0,5273, parce qu'un mélange de lois à échelles inégales paraît plus lourd de queue qu'aucune de
ses composantes : l'ajustement stationnaire attribue à la **forme** une part de ce qui relève de
la **dérive**. Les deux écarts du modèle publié sont donc de sens contraires.

**Décision prise le 8 septembre : déclarée, non corrigée**, du même type que celle du `p_u`.

- **Chapitre 06**, nouvelle section `soc:sec:backtest` : le résultat est présenté comme une
  **validation**, deux succès d'abord et la dérive ensuite. 49 nombres, tous confirmés.
- **Chapitre 13** : une ligne à la table à deux colonnes, du côté des écarts **involontaires**,
  et deux lignes à la table de synthèse de robustesse, une `\rob` et une `\ass`. Le texte de
  lecture passe de deux écarts involontaires à trois.
- **Aucune recalibration.** Corriger supposerait de déplacer tous les niveaux publiés à onze
  semaines du dépôt sans qu'aucun déplacement soit attribuable à la correction.
- **Slide J** du deck du 11 septembre, seule slide de travail neuf de ce deck.

### Et l'affirmation publiée le matin a été fermée l'après-midi, script 90

Les deux textes ci-dessus disaient qu'une dérive commune aux deux états de conformité se
simplifie dans un rapport, donc que la thèse était à l'abri. **C'était un argument, pas une
mesure.** Il n'était pas gratuit non plus : les quatre canaux ne transforment pas la sévérité de
la même façon selon l'état, la détection entrant dans la *transformation* de sévérité et la
propagation changeant le *nombre* de sévérités tirées par sinistre.

**Le résultat, et il corrige la formulation.** L'argument est juste pour l'**échelle** et pour
elle seule, où il est même remarquablement exact : une variation de la seule échelle multiplie
les deux états par le même facteur, 1,4556 et 1,4532, soit un rapport de **0,9984** alors que
les niveaux montent de 46 %. Il est **faux** pour un changement de **forme** de queue, et la
dérive mesurée en contient un, puisque la modéliser réattribue à l'échelle ce que l'ajustement
stationnaire lisait comme de la forme. Le facteur entre états passe donc de **3,344 à 3,124**,
soit −6,6 % résolu à 4,43 écarts-types, et le déplacement est **entièrement porté par la
composante de forme** (−6,1 %, 4,09 σ, contre −0,2 % non résolu pour l'échelle).

**L'écart en euros ne bouge que de −1,9 %, et il ne faut surtout pas y lire une robustesse.**
C'est une **compensation** : la composante de forme seule ramènerait l'écart à 9 393 M€ et celle
d'échelle seule le porterait à 20 041. L'écart est donc très sensible à la sévérité prise
composante par composante, et presque insensible à la seule combinaison que la dérive produit.

**Trois choses à retenir :** citer l'**invariance d'échelle**, jamais l'invariance à la dérive ;
ne jamais annoncer l'écart comme robuste à la sévérité ; et la direction est **favorable**, écart
et facteur étant plus petits sous la sévérité dérivée, donc le chiffre publié n'est pas gonflé.
Même structure à deux sens que le `p_u` gelé, le niveau devenant anti-conservateur et la thèse
légèrement prudente.

**Deux réserves imprimées par le script, à conserver :** il teste **une** sévérité alternative,
non toute la famille, et la séparation forme / échelle est une **reparamétrisation**, non deux
mécanismes physiques indépendants.

**Nouveau module partagé `derive_severite.py`**, lu par 89 et 90, pour que les deux ne puissent
pas s'écarter d'une décimale. Le refactor de la section 1ter du 89 reproduit sa sortie versionnée
**à l'octet**. Et le script 90 suit le patron du script 81 pour faire tourner le moteur des
canaux avec un paramètre changé : recopie de `pertes_annuelles` dans le même ordre de tirages,
puis **contrôle** que l'appel aux valeurs publiées reproduit le module tirage pour tirage (écart
maximal 0,00e+00) et que la branche publiée redonne 6 049 et 20 188.

### Et la charge agrégée, script 91 : l'agrégat est rejeté

**Le manque que les deux scripts précédents laissaient** : ils valident ou chiffrent des
**marginales**, quand le capital est le quantile de la **charge annuelle**. Un modèle composé peut
avoir deux marginales correctes et un agrégat faux.

**L'agrégat est rejeté** : transformée intégrale 0,734 pour 0,500 attendu, Kolmogorov-Smirnov
p = 0,0042, couverture 75,0 % pour 90 % annoncés, trois dépassements de la borne haute concentrés
dans les quatre dernières années notées.

**Mais le rejet n'est pas structurel**, et la signature de dérive est mesurée : PIT 0,611 sur les
six premières années notées contre 0,857 sur les six dernières (Mann-Whitney p = 0,0130), la charge
observée passant de 363 à 1 255 M€ en moyenne quand la médiane prédictive ne va que de 183 à 248.
C'est le retard d'une fenêtre qui s'étend sur une échelle qui dérive. **Aucune limite nouvelle
n'entre donc à l'inventaire** : un seul mécanisme est en défaut, l'échelle, et il produit
désormais trois symptômes.

**Trois autres résultats, dont deux favorables :**

- **la binomiale négative cesse d'être un déterminant du capital.** Décisive sur les comptes
  (3,054 nats, couverture 91,7 contre 75,0 %), elle ne gagne que **0,3 %** sur la charge, celle-ci
  étant portée par un sinistre unique. Elle reste le bon choix, mais ne pas la présenter comme ce
  qui porte le niveau ;
- **l'indépendance fréquence / sévérité TIENT**, et cette hypothèse de construction n'était testée
  nulle part dans le projet. Une pente négative significative apparaît sur toute la distribution
  (−0,02397, p = 0,0419 avec contrôle d'année), elle **disparaît sur les excès** (−0,00331,
  p = 0,84, soit 0,14 de sa valeur), qui sont la population que le modèle tire : c'est un artefact
  de profondeur de collecte, non une propriété du risque ;
- **la puissance du backtest est chiffrée en années, et c'est le paragraphe qui vaut le plus devant
  un jury.** Détecter un taux de dépassement double du nominal à 80 % de puissance demanderait
  **1 811 années** à 99,5 %, 905 à 99 %, 78 même à 90 %. Le quantile qui porte le capital n'est
  backtestable sur **aucun** historique de risque opérationnel existant. Ne jamais présenter ce
  backtest comme une validation du quantile.

**Deck** : slide K ajoutée, le deck du 11 septembre passe à douze pages.

### Puis les trois manques de test qui restaient, scripts 92, 93 et 94

La liste des manques identifiés le matin est **vide** au soir. Aucun des trois n'était une
recalibration : tous sont des diagnostics compatibles avec le gel.

**Le test de résistance INVERSÉ, script 92.** On fixe le capital et l'on cherche les états du
monde qui le produisent, ce qui est la forme sous laquelle un dispositif ORSA emploie un modèle.
La monotonie du script 88 rend l'exercice court : l'ensemble des configurations atteignant une
cible est **croissant**, donc décrit par ses seuls éléments **minimaux**, jamais plus de quatre
sur seize. Le résultat de gestion tient en deux seuils : la fréquence **seule** atteint
10 377 M€, quand les trois autres canaux **réunis** n'atteignent que 11 413. Toute cible sous le
premier se produit par un canal unique, toute cible au-dessus du second **exige** la fréquence, et
aucun autre canal seul n'atteint même 8 000. **La lecture inverse dit donc autre chose que la
lecture directe** : celle-là hiérarchise les canaux par leur contribution, celle-ci désigne celui
dont la maîtrise *interdit* les scénarios sévères. Et une découverte non cherchée : le canal
d'accumulation n'admet **pas** d'inversion continue, ses deux états étant deux structures de
table, et sa bascule à paramètre nul fait **baisser** le capital de 239 M€ parce qu'elle retire la
propagation propre de P4 ; son effet isolé publié de 1 728 est donc un **net**.

**La règle de sélection du seuil, script 93, et le résultat est favorable.** Trois règles sur dix
percentiles candidats. **La règle de stabilité sélectionne exactement le seuil publié**, 19,87
contre 20,03, à quantile identique : le seuil publié est précisément le plus bas au-dessus duquel
ξ cesse de dériver. Il est aussi **le mieux ajusté du balayage**, p d'Anderson-Darling 0,971
contre 0,954 pour le second candidat, donc deux critères indépendants désignent le même point.
Et surtout **la règle la plus permissive descendrait à 12,88 M€ et donnerait un quantile
supérieur de 16 %** : le seuil publié n'est pas celui qui maximise le chiffre du mémoire, ce qui
est l'argument le plus fort contre un soupçon de choix opportuniste. **Le compromis biais-variance
n'existe pas sur cette grandeur**, contre l'attente : l'écart-type du quantile est divisé par 3,5
en remontant le seuil alors que les excès sont divisés par six, parce que descendre gonfle ξ
jusqu'à 1,058 et que le quantile en dépend exponentiellement. Le double bootstrap d'erreur
quadratique asymptotique est **refusé avec son motif**, ses sous-échantillons vaudraient 118 puis
24 observations, même arbitrage que celui qui a écarté l'élicitation.

**Le quantile de la loi des configurations, script 94.** Le script 69 déclarait lui-même que son
invariance portait sur l'**espérance**. C'est chiffré : l'espérance bouge de −0,02 %, le quantile
à 75 % de +5,53 %, celui à 90 % de +2,76 %, la moyenne de queue à 90 % de +1,06 %. **La réserve
était justifiée**, l'argument d'additivité ne transporte pas à un quantile, mais l'ordre de
grandeur reste petit. Le mécanisme est la **polarisation**, mesurée : P(tous conformes) 29,06 →
33,03 % et P(tous non conformes) 6,83 → 8,78 % à espérance inchangée. **Et une limite de l'objet
lui-même** : au-delà de 93,17 % le quantile est saturé sur la configuration intégralement non
conforme, si bien qu'un « quantile à 99,5 % de la loi des configurations » n'a aucun contenu. Ce
n'est pas une mesure de capital et il ne reçoit ni `\VaR` ni `\TVaR`.

**Intégration** : deux paragraphes et un encadré au chapitre 06 pour le seuil, une nouvelle
sous-section de l'annexe C plus un paragraphe court au chapitre 12 pour le test inverse, et trois
paragraphes plus un encadré au chapitre 11 pour le quantile des configurations. Slide L au deck,
qui passe à treize pages. J, K et L sont les trois slides de travail neuf.

- Coût de la journée : corps 123 → **129 pages**, total 169 → **176**. Harnais 1 979 →
  **2 142**, à 100 %, hors contrôle non déclaré à zéro.

**Deux pièges évités en chemin, et le premier aurait invalidé le backtest.** Le périmètre couvre
1979-2026, mais avant 2004 la collecte porte un à neuf incidents par an contre treize à
trente-neuf ensuite, et 2026 n'en porte que cinq : ce ne sont pas des années calmes, c'est une
base qui ne les couvre pas. Retenir toute la période aurait produit un faux effondrement de
fréquence en fin de période. Et le seuil est **re-estimé** sur chaque échantillon
d'apprentissage par la règle du percentile 85, au lieu d'être lu dans `config.py` : un seuil
calculé sur toute la période ferait fuiter l'information de test dans l'apprentissage. Cette
différence avec la chaîne publiée est délibérée et écrite dans l'en-tête du script.

---

## F. Clos, à ne pas rouvrir

Le gel de la calibration (7 août), la convention de normalisation de W par l'émission maximale
(2,60), le statut de citation de Hackmageddon (la source **reste utilisée**, elle porte la
structure et jamais le niveau), le rejet du Hawkes, la non-transitivité (réfutée par son auteur,
remplacée par la dépendance à l'ordre), l'élicitation, l'anonymisation des entités, la convention
qui sépare la VaR de la charge annuelle du quantile de sévérité d'un sinistre, le détecteur de
contradictions entre scripts (instruit le 10 août puis écarté pour une raison), les séquences
ordonnées (refermées avec un critère de réouverture précis, script 75), et les decks des 7 et
14 août.

**Exception, et c'est la seule :** le deck du **21 août** a été **réécrit le 3 septembre**. Sa
version précédente datait du 5 août, donc d'avant les points du 7 et du 14, et présentait du
travail *antérieur* au deck du 14 tout en annonçant qu'elle le suivait ; elle portait en outre
deux valeurs devenues fausses (les champs SFCR de l'assureur non-vie B, et l'argument du levier).
La nouvelle version porte le travail des 17 et 19 août. Leçon d'archivage : **un deck daté
d'avance se périme sans que personne le relise.**

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

**Second piège : laisser du travail mesuré hors du document.** Un résultat qui n'est pas dans le
mémoire n'existe pas pour le jury. C'était le piège du 17 août, sept scripts et le dispositif de
vérification étant dans ce cas ; **il est refermé** et il faut le surveiller à chaque nouveau
script, parce qu'il se reforme tout seul.

---

## Le calendrier, maintenant que la remise est connue

**Remise fin novembre 2026.** Le mémoire est terminé au sens du travail interne : la contrainte
n'est plus le temps mais l'axe données, que seuls des tiers peuvent déplacer, et dont le délai
ne se comprime pas. D'où l'ordre.

- **Septembre : uniquement ce qui a un délai externe.** Le second codage, et pas seulement
  Hugo : à trois mois la bonne cible n'est plus « un répondant suffit à débloquer » mais
  **trois codeurs**, ce qui transforme la levée d'une objection en vraie étude de fiabilité
  inter-juges sur l'axe le plus attaquable. La relecture par praticiens sur les sept phrases,
  partie le 17 août et sans retour : à relancer, un désaccord argumenté valant plus qu'un
  accord. Le registre de sous-traitance. **Et vérifier l'échéance propre du Prix SCOR**, qui
  n'a aucune raison de coïncider avec fin novembre : si elle est antérieure, c'est elle qui
  commande tout ce qui précède.
- **Octobre : ce qui rapporte sur la note.** La compression du corps, enfin possible.
  L'intégration des codages reçus, une heure par codeur, la chaîne étant prête. La finition :
  les deux défauts de lisibilité restants, le balayage des légendes qui nomment une couleur,
  la dernière figure à l'ancienne palette (elle exige le Mac), et ce fichier.
- **Novembre : la soutenance.** Et ce n'est pas une remarque de politesse : la leçon la plus
  répétée du projet est que **la slide est le meilleur détecteur de défauts**, le κ⋆
  contradictoire, les six postures non définies et la prédictive à deux valeurs ayant tous été
  trouvés en regardant une slide. Préparer le deck de soutenance fera donc deux choses.
