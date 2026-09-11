# Notes orales, soutenance devant l'Institut

Support : `soutenance_memoire_DORA.pptx`, 16 diapositives principales et 10 de sauvegarde.
Les mêmes notes figurent dans le volet commentaires du fichier, diapositive par diapositive.

**Durée visée : 20 minutes.** Le texte de l'Institut prévoit 25 minutes de présentation et
20 de questions, et précise que le dépassement peut être pénalisant. Le support tient dans les
deux enveloppes. **À confirmer auprès des responsables de voie avant de répéter.**

**Deux règles d'élocution que le texte de l'Institut relève explicitement** : il est attentif aux
« expressions familières, apocopes et acronymes ». Donc dire « la valeur en risque » puis « la
VaR » une fois posée, et jamais un raccourci d'atelier comme « le harnais » ou « le 169 » sans
l'avoir introduit.

---

## 1. Titre — 20 s

**Message.** Se présenter, annoncer la durée, poser la question tout de suite.

**À dire.** « Combien coûte en capital de ne pas se conformer à DORA, et jusqu'où ce chiffre
peut-il être affirmé. »

**Précaution.** Ne pas lire la diapositive.

**Transition.** « Commençons par pourquoi cette question se pose. »

---

## 2. Le problème métier — 1 min 30

**Message.** Il existe un maillon manquant entre une exigence de maîtrise et une exigence de
capital.

**À dire.** DORA impose depuis janvier 2025 la maîtrise de cinq domaines de résilience
opérationnelle numérique. Aucun dispositif prudentiel ne traduit ce niveau de maîtrise en
capital : la Formule Standard charge le risque opérationnel par un pourcentage de primes ou de
provisions, donc elle donne le même chiffre à une entité exemplaire et à une entité défaillante.

**Chiffres à prononcer.** Aucun.

**Précaution.** Ne pas réciter le règlement. Le point est le maillon du milieu, pas le texte.

**Transition.** « La question de ce mémoire est donc celle de ce maillon. »

---

## 3. Question et contribution — 1 min 20

**Message.** Trois apports, et le second est celui qui distingue le travail.

**À dire.** Un mécanisme de dépendance dirigée, une frontière d'identifiabilité, et une lecture
décisionnelle. La seconde moitié de la question, « jusqu'où ce chiffre peut-il être affirmé »,
est celle qui produit la contribution.

**Précaution.** Ne pas annoncer de résultat chiffré à ce stade.

**Transition.** « Voyons d'abord ce que DORA demande de maîtriser. »

---

## 4. Les cinq piliers — 1 min

**Message.** Ce sont des domaines de contrôle, pas des cases à cocher, et ils interagissent.

**À dire.** La défaillance de l'un dégrade la capacité à tenir les autres : une gouvernance
défaillante retarde la détection des incidents, une dépendance non maîtrisée à un prestataire
ouvre une porte que les tests n'ont pas explorée.

**Précaution.** Les deux piliers en rouge, gouvernance et tiers, sont ceux qui émettent le plus
dans la matrice calibrée. Si on demande pourquoi, la figure est en sauvegarde.

**Transition.** « Reste à savoir ce que la donnée permet de voir de ces interactions. »

---

## 5. La donnée, observable et non observable — 1 min 30

**Message.** La colonne de droite n'est pas un manque à combler avec plus de données du même
type. Elle est structurelle.

**À dire.** Sept sources, chacune avec son statut de preuve déclaré. Elles donnent la fréquence,
la sévérité et la co-occurrence. Elles ne donnent pas la direction.

**Précaution.** Ne pas annoncer la démonstration ici : elle arrive trois diapositives plus loin.

**Transition.** « Avant d'y venir, voici comment le modèle est construit. »

---

## 6. L'architecture — 1 min 30

**Message.** Le modèle est partiellement calibré et partiellement borné, et le document dit
lequel est lequel.

**À dire.** Un état de conformité par pilier pilote quatre canaux ; ces canaux transforment la
loi de perte annuelle ; le quantile de cette loi donne le capital ; le capital éclaire une
décision. Deux canaux sont calibrables sur données, la fréquence et la détection. Deux sont des
bornes posées, la propagation et l'accumulation liée aux tiers.

**Précaution.** Pas de notation. La distinction calibrable contre borné revient à la fin sur les
limites, et c'est elle qui interdit d'additionner les quatre leviers.

**Transition.** « Pourquoi une cascade dirigée plutôt qu'une dépendance ordinaire. »

---

## 7. Pourquoi une cascade dirigée — 1 min 30

**Message.** L'ordre de propagation change la criticité, et une dépendance symétrique ne le voit
pas.

**À dire.** Une gouvernance défaillante retarde la détection des incidents ; l'inverse n'est pas
vrai au même degré. Une copule capture bien la co-occurrence des pertes, mais symétriquement :
elle donne le même nombre dans les deux sens, donc elle ne peut pas servir à prioriser une
remédiation.

**Précaution.** Ne pas entrer dans la normalisation de Leontief. Diapositive de sauvegarde.

**Transition.** « Et c'est ici que le travail rencontre sa limite, qui devient son résultat. »

---

## 8. La non-identifiabilité — 2 min

**C'est la diapositive du mémoire. Prendre le temps, ralentir le débit.**

**Message.** La donnée identifie la co-occurrence et pas la direction, et ce n'est pas un échec.

**À dire, en trois temps.** La matrice se décompose en une partie symétrique et une partie
antisymétrique. La donnée identifie la première. Elle n'identifie pas la seconde. Une matrice et
sa transposée sont indistinguables pour la donnée, et elles donnent pourtant un capital et une
décision différents.

**Précaution à exprimer.** Dire explicitement : ce n'est pas un échec du modèle, c'est un
résultat d'identification. C'est ce qui interdit de publier une direction comme si elle avait
été observée.

**Transition.** « La question devient donc : que publie-t-on quand on ne peut pas identifier. »

---

## 9. Du point à la bande — 2 min

**Message.** Borner plutôt que poser, et chiffrer ce que l'ignorance coûte.

**À dire.** Plutôt que de poser la direction, le capital est borné sur l'ensemble des matrices
compatibles avec ce que la donnée identifie. L'énumération est exhaustive, pas un échantillonnage.
Le coût de l'ignorance est linéaire et son maximum est connu d'avance, ce qui est plus favorable
qu'un intervalle de confiance ordinaire.

**Chiffres à prononcer exactement.** 1 024 sommets.

**Précaution à exprimer.** Le niveau affiché est illustratif ; ce qui est défendu est le rapport
et la hiérarchie.

**Transition.** « Voyons maintenant ce qui, dans la non-conformité, déplace réellement le
capital. »

---

## 10. Les quatre canaux — 1 min 40

**Message.** La non-conformité ne se paie pas en pénalité, et les canaux ne s'additionnent pas.

**À dire.** Au secteur, le besoin de capital passe de 6 049 à 20 188 millions d'euros entre l'état
conforme et l'état non conforme, soit un facteur 3,34. Aucune pénalité n'est ajoutée : quatre
paramètres de la loi de perte se déplacent. Pris isolément, ces quatre canaux somment à 9 138
millions quand l'écart total en vaut 14 139 : il manque 5 001 millions, soit 35 %, parce que la
cascade est super-additive sur ses canaux.

**Chiffres à prononcer exactement.** 6 049 ; 20 188 ; 3,34 ; 9 138 ; 14 139 ; 5 001 ; 35 %.

**Précautions, et elles comptent.**
- dire **« au secteur »** dès la première phrase. Sans ce mot, le jury entend vingt milliards pour
  une entité et la question part avant qu'on ait pu la cadrer ;
- ajouter aussitôt la nuance qui évite une erreur : le modèle est super-additif **sur les
  canaux**, quasi additif **sur les piliers**, et l'additivité des **coûts** au sein d'un sinistre
  est une troisième chose, une hypothèse non testée ;
- **ne jamais additionner les quatre leviers** pour chiffrer une remédiation partielle : deux des
  quatre sont des bornes posées, pas des budgets.

**Transition.** « Un de ces canaux mérite qu'on s'y arrête, parce que DORA le vise nommément. »

---

## 11. Le pilier des tiers — 1 min

**Message.** Contagion et accumulation sont deux mécanismes différents, et le modèle porte les
deux.

**À dire.** La contagion va d'un pilier à l'autre au sein d'une même entité. L'accumulation vient
d'un prestataire commun à plusieurs entités : ce n'est plus de la propagation, c'est un choc
partagé. C'est exactement ce que DORA demande de cartographier.

**Précaution.** Si on insiste, dire que le canal d'accumulation est une borne posée, pas une
calibration.

**Transition.** « Et c'est ce qui conduit à la contribution la plus directement actionnable. »

---

## 12. La donnée manquante devient un livrable — 1 min 40

**L'une des deux diapositives les plus importantes, avec la huitième.**

**Message.** Le modèle ne dit pas seulement qu'il manque une donnée : il dit laquelle et ce
qu'elle rapporte.

**À dire.** Chaque champ de registre renseigné resserre la bande de capital, et les champs sont
hiérarchisés par ce resserrement. Horodatage des incidents, domaine de contrôle touché, cause
commune consolidée, champs obligatoires.

**Précaution.** C'est la recommandation la moins mathématique du travail, et c'est celle qu'une
relecture de praticien a confirmée comme déjà pratiquée sous une autre forme. Le dire si la
question de l'applicabilité vient.

**Transition.** « Reste ce qu'une direction des risques peut en faire. »

---

## 13. Décision pour l'entité — 1 min 20

**Message.** Trois décisions, et une confusion à ne pas commettre.

**À dire.** Remédier en priorisant les canaux calibrables ; détenir, en sachant que le capital
immobilisé coûte chaque année et non une seule fois ; ou transférer, en comparant au prix de
marché du même risque. Et une borne de capital n'est pas un budget de remédiation.

**Précaution.** Si on demande un retour sur investissement : le retour calculé sur le seul portage
de capital est un **majorant**, pas un plancher, parce que la seconde composante du bénéfice, la
sinistralité évitée, n'y est pas monétisée. Ne jamais donner le nombre d'années sans dire le sens
de la borne.

**Transition.** « Il faut maintenant dire ce que ce travail n'établit pas. »

---

## 14. Limites — 1 min 10

**Message.** Quatre limites, et en face ce qui tient malgré elles.

**À dire.** La direction n'est pas identifiée. Le niveau absolu est illustratif, et c'est une
borne supérieure à l'échelle d'une entité. L'incertitude de queue est large. Deux canaux sont
bornés et non calibrés. Ce qui tient malgré cela : le signe et l'ordre de l'écart, la hiérarchie
des piliers, le cadre de bornage et son coût, et la recommandation de reporting.

**Précaution.** Présenter les **deux colonnes ensemble**, jamais la gauche seule. Et dire que la
thèse de départ, la non-transitivité, a été **réfutée par son auteur**, et que le chiffre d'entité
a été **requalifié en borne supérieure**. Le texte de l'Institut récompense explicitement cela.

**Transition.** « En trois messages. »

---

## 15. Conclusion — 30 s

**À dire.** Les trois messages, puis la phrase finale, lentement et sans la lire mot à mot :
« Quand la dépendance n'est pas identifiable, la bonne réponse actuarielle n'est pas la fausse
précision : c'est une borne, une hiérarchie de données et une décision mieux informée. »

---

## 16. Questions

Garder l'architecture visible : elle sert de point d'appui pour situer chaque question. Les dix
diapositives de sauvegarde s'appellent à la voix.

---

# Les dix questions attendues, et la première phrase de la réponse

Plusieurs sont des **pièges de prémisse** : la réponse commence par corriger la prémisse, pas par
s'excuser.

| # | Question | Première phrase | Sauvegarde |
|---|---|---|---|
| 1 | « Vos chiffres sont en milliards, pour une entité ? » | **Prémisse à corriger.** Ces niveaux sont ceux du secteur financier mondial, la base de sévérité étant mondiale. Lu à la taille d'une entité, le besoin vaut 169 M€, publié comme borne supérieure d'ordre de grandeur | B2, et la figure de descente d'échelle |
| 2 | « Votre matrice n'est pas calibrée » | Exact, et c'est démontré. C'est pourquoi elle n'est pas posée mais bornée | B5 |
| 3 | « Pourquoi pas une copule ? » | Elle est implémentée comme jumeau numérique et comparée : elle suit les marges et ne porte pas la direction | B7 |
| 4 | « Pourquoi pas un processus auto-excité ? » | Parce qu'il n'est **pas distinguable** de la cascade à la résolution disponible, et c'est mesuré | B4 |
| 5 | « Pourquoi ne pas interroger des experts ? » | Un panel faiblement calibré introduirait une incertitude **non déclarable** en échange d'une ignorance mesurée. Le protocole est prêt et non exécuté | B5 |
| 6 | « Les défaillances simultanées ne sont pas traitées » | **Prémisse fausse** : c'est une sortie du modèle, et à l'état non conforme elle est majoritaire, 62,31 % contre 31,15 % | B8 |
| 7 | « Votre modèle est-il super-additif ? » | Sur les **canaux** oui, sur les **piliers** il est quasi additif, et l'additivité des **coûts** est une troisième chose, non testée | B7, B9 |
| 8 | « Le quantile à 99,5 % est-il testé ? » | Non, et la puissance est chiffrée : 1 811 années seraient nécessaires. Le backtest valide le centre et le corps, pas la queue | B3 |
| 9 | « Qu'est-ce qui est calibré, qu'est-ce qui est posé ? » | Deux canaux calibrables, deux bornes posées. Les trois valeurs du gain de propagation sont posées, et la thèse n'en dépend pas puisque le capital y est croissant | B2 |
| 10 | « À quoi cela sert-il concrètement ? » | À hiérarchiser une remédiation et à spécifier un registre d'incidents. Le chiffre à citer pour un plan est la colonne de **fermeture** | B7, et la diapositive 12 |

---

# Ce qu'il ne faut jamais dire

- **« le SCR DORA de telle entité »** : dire « besoin de capital ORSA au titre de DORA ». Il
  n'existe aucun module DORA en Formule Standard, et le rapport à un SCR publié est une mise à
  l'échelle, pas une part ;
- **additionner les quatre canaux**, ni l'interaction entre canaux et celle entre piliers ;
- **confondre le quantile de sévérité d'un sinistre et la charge annuelle agrégée**. Cette
  confusion s'est produite en séance le 7 août 2026 : un quantile de sévérité n'est pas un
  capital ;
- **« l'écart est robuste à la sévérité »** : l'invariance démontrée porte sur l'**échelle** et
  sur elle seule ;
- **nommer une entité réelle** ou une personne extérieure à l'encadrement ;
- **retirer une réserve pour faire plus net** : c'est exactement ce que le jury note.
