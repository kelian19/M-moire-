# Audit final — mémoire d'actuariat DORA

Clôture du 21 septembre 2026. Document : `main_ensae.pdf`, **204 pages**, harnais 1 839 / 1 839,
zéro hors contrôle non déclaré, 5 débordements à la ligne de base, 0 `??`. Dépôt le 30 septembre :
**il reste neuf jours**.

Référentiel : Recommandations Jury de l'Institut des actuaires, applicables depuis le
1er avril 2026. C'est le seul référentiel opposable, aucune consigne d'école distincte n'existant
au dépôt.

---

## 1. Notes estimées

### Lecture Institut des actuaires

| Critère | Points | Note | Justification |
|---|---|---|---|
| Problématique, positionnement, originalité | 3 | **2,75** | La contribution tient en une phrase : établir la frontière d'identifiabilité d'une contagion que tout le monde postule. L'état de l'art est positionné, et le benchmark copule montre le trou que le modèle comble. L'originalité coche explicitement le critère « publiable » du § 5.3 : importer une méthode d'un autre domaine, ici l'identification partielle de l'économétrie. Retenue d'un quart de point : l'introduction est absorbée dans un chapitre 1 de 15 pages, là où le § 5.1.d attend 2 à 3 pages |
| Rigueur méthodologique | 5 | **4,5** | Une définition, cinq propositions démontrées et vérifiées numériquement. La stabilité est **garantie** par la normalisation de Leontief, pas espérée, et le piège est documenté : ρ(TRANS) = 1,461 > 1 a été détecté avant de brancher la matrice. Deux rayons spectraux distingués. La non-transitivité a été testée dans trois formulations et **réfutée par l'auteur**. La DiD MOVEit a été retirée parce qu'un placebo la reproduisait. Retenue d'un demi-point : l'hypothèse porteuse g_C < g_NC n'est adossée qu'au règlement, et la matrice du chiffre de tête vient d'un seul expert |
| Données, résultats, sensibilités, reproductibilité | 4 | **3,5** | 1 839 nombres publiés rattachés à la sortie du script qui les produit, 112 sorties versionnées, **0 chemin absolu sur 128 scripts**, biais quantifiés et compensation mesurée (0,861 × 1,147 = 0,987). Retenue d'un demi-point : Hackmageddon consulté et non conservé, 17 sources en ligne sans adresse, et le chiffre d'entité déclaré hors domaine par le mémoire lui-même |
| Esprit critique, limites, interprétation métier | 3 | **3** | C'est l'axe le plus fort. Le mémoire réfute son hypothèse de départ, requalifie son chiffre central en borne, mesure le biais de narration au lieu de le déclarer, chiffre la puissance du backtest (1 811 années), et convertit sa limite en recommandation de reporting opposable. La section « détenir ou transférer » est de l'interprétation métier au sens du § 5.3 |
| Qualité rédactionnelle, structure, exigences formelles | 3 | **2,25** | Rédaction propre : 11 tournures automatiques sur 57 230 mots, ton impersonnel tenu. Les deux annexes exigées et la déclaration d'IA **manquaient et sont désormais en place**. Restent ouverts : la page de garde non signée, la note de synthèse séparée non produite, les deux résumés à ~10 % au-dessus de la limite |
| Qualité typographique et technique LaTeX | 2 | **2** | 0 erreur, 0 référence non définie, 0 étiquette dupliquée, 56 citations toutes résolues, 5 débordements à la ligne de base, 0 `vbox` |
| **Total** | **20** | **≈ 18 / 20** | |

**Cette note suppose que les actions P0 ci-dessous sont faites.** Ce matin, le dossier ne portait
pas un risque de note mais un **risque d'ajournement** : le § 4.5 prévoit que tout manquement à la
transparence sur l'IA conduit à l'ajournement « sans besoin d'une autre motivation », et rien
n'était déclaré. Ce risque est levé.

**La mention « publiable » est atteignable.** Le § 5.3 la réserve aux travaux qui offrent « une
avancée de la science actuarielle comme par exemple l'application de méthodes issues de domaines
autres que l'assurance ». C'est exactement ce que fait ce mémoire. Mais elle est **conditionnée à
la signature** de la page de garde : sans elle, l'Institut ne peut pas publier.

### Lecture école

**Je n'ai pas de barème ENSAE.** Aucun fichier du dépôt n'en contient, et tu as indiqué qu'il n'y
en avait pas de distinct. Je ne l'invente pas.

Le seul indice est l'en-tête de `19_enseignements_stage.tex`, qui affirme que « le barème de
l'école note sur 6 ». **Si ce barème existe**, le chapitre de 4 pages sur 204 est le poste au plus
fort rendement du dossier et il faut l'étoffer. **S'il n'existe pas**, le chapitre n'est requis par
rien et son en-tête invoque un référentiel fantôme, à corriger. Ce point doit être tranché.

---

## 2. Top 10 des actions, par gain attendu

| # | Action | Gain | Effort |
|---|---|---|---|
| 1 | **Faire signer la page de garde** par toi et Hugo Rapior | Débloque la publication, donc la mention « publiable », donc le Prix SCOR | 30 min + délai externe |
| 2 | **Trancher la question du barème ENSAE**, puis étoffer le chapitre 19 s'il existe | Jusqu'à 6 points sur la lecture école | 30 min à 1 jour |
| 3 | Ajouter `url` et `urldate` aux **17 sources en ligne** | Le § 4.2 dit la bibliographie potentiellement **éliminatoire** | 1 h 30 |
| 4 | Produire la **note de synthèse séparée** FR + EN | Exigée au § 6.5, sert l'indexation de l'Institut | 1 h |
| 5 | Appeler les **13 flottants orphelins** restants | Argumentation, lisibilité | 1 h |
| 6 | Rédiger la **note de contexte** (§ 6.4, 2 pages, jury seul) | Prépare le jury à l'identification partielle **avant** la soutenance | 1 h |
| 7 | **Publier le dépôt Zenodo** (brouillon prêt, DOI posé) | Ferme la promesse faite p. 160 | 15 min |
| 8 | Ramener les deux résumés **sous 250 mots** | Prescription chiffrée, facile à vérifier | 30 min |
| 9 | Recréer le **maître Institut** (`page_de_garde.tex` orpheline) | Sans lui, pas de version Institut compilable | 1 à 2 h |
| 10 | Relire les **cinq phrases de plus de 80 mots** | Confort de lecture | 30 min |

---

## 3. Plan d'action

### P0 — bloquant pour le dépôt

| Action | Fichier | Coût |
|---|---|---|
| Signature page de garde, étudiant et responsable de stage | `page_de_garde_ensae.tex` | 30 min + délai |
| Publier le dépôt Zenodo | — | 15 min |
| Trancher le barème ENSAE et corriger l'en-tête | `19_enseignements_stage.tex` | 30 min |

### P1 — fort impact

| Action | Fichier | Coût |
|---|---|---|
| 17 `url` + `urldate` | `references.bib` | 1 h 30 |
| Note de synthèse séparée FR + EN | nouveau document | 1 h |
| Note de contexte | nouveau document | 1 h |
| 13 flottants orphelins | 6 chapitres | 1 h |
| Étoffer le chapitre 19 si le barème existe | `19_enseignements_stage.tex` | 1 jour |

### P2 — finition

| Action | Coût |
|---|---|
| Résumés sous 250 mots | 30 min |
| Cinq phrases longues | 30 min |
| Retirer les 19 entrées `.bib` non citées | 15 min |
| Maître Institut | 1 à 2 h, **après le 30** |

---

## 4. Planning du 21 au 30 septembre

| Jour | Ce qui se fait | Gel |
|---|---|---|
| **Lun 21** | *Fait* : audit complet, deux annexes exigées créées, déclaration d'IA, DOI posé, matériel complémentaire construit, exposition des bornes et de la valeur d'information | |
| **Mar 22** | **Relancer Hugo pour la signature, en premier.** Puis les 17 URL de bibliographie | |
| **Mer 23** | Trancher le barème ENSAE. Note de synthèse séparée FR + EN | |
| **Jeu 24** | Chapitre 19 si le barème existe. Sinon : 13 flottants + note de contexte | |
| **Ven 25** | Support de soutenance (25 min, § 6.6) et choix des figures | |
| **Sam 26** | Relecture intégrale du PDF, page par page, à l'œil | |
| **Dim 27** | Répétition orale devant un jury fictif (§ 6.7 le recommande) | |
| **Lun 28** | **Gel du contenu. Seuls les P0 après ce point.** | **J-2** |
| **Mar 29** | **Répétition de dépôt** : compilation propre, harnais vert, contrôles, PDF relu, nom de fichier, métadonnées, taille. Publier Zenodo | **J-1** |
| **Mer 30** | Dépôt | |

**Répétition de dépôt du 29, la liste :** compiler `main_ensae.tex` ; vérifier 0 erreur, débordements
à 5, 0 `vbox`, 0 `??` sur le PDF, 0 page tournée ; passer le harnais sur les 24 chapitres et
constater zéro hors contrôle non déclaré ; recopier en `KADDOURI_Kelian_3A25.pdf` ; vérifier les
métadonnées du PDF (titre, auteur) ; vérifier que le DOI de la p. 160 résout ; vérifier la présence
des signatures ; arbre git propre.

---

## 5. Contenu manquant à forte valeur

**Faisable en moins d'une journée avec l'existant :**

- **La note de contexte du § 6.4.** Deux pages, destinées au seul jury, qui exposent les difficultés
  réelles du stage. Ici : l'indisponibilité de la donnée de direction, qui est le cœur du mémoire.
  Elle prépare le jury à l'identification partielle **avant** qu'il n'ouvre le document. Fort
  rendement, coût faible.
- **Une figure de synthèse de la bande de capital**, si elle n'existe pas déjà : le socle, la bande
  d'ignorance directionnelle, et le resserrement qu'un registre apporterait. C'est le résultat du
  mémoire en une image.
- **Étoffer le chapitre 19** avec des situations concrètes, si le barème le justifie.

**Non faisable dans le temps restant, et c'est assumé :**

- Exécuter l'élicitation (annexe C) : il faudrait constituer un panel.
- Calibrer l'amplitude des liens : demande de la donnée d'entité.
- Corriger la dérive d'échelle de 4,00 %/an : c'est un sujet de mémoire à part entière, et il est
  déjà légué en annexe F.

---

## 6. Préparation de la soutenance

**Format réel, § 6.7** : la soutenance dure une heure, dont **25 minutes maximum** de présentation,
20 minutes de questions, 15 de délibération. Le président a autorité pour interrompre au-delà du
temps imparti, et le dépassement est pénalisant.

### Les quinze questions probables

| # | Question | Réponse, et page d'appui |
|---|---|---|
| 1 | « Quel est votre SCR ? » | Le niveau n'est pas une mesure et le mémoire le démontre : il bouge d'un facteur 41 selon la seule source. Ce qui est déterminé, c'est un intervalle : entre 6 858 et 8 697 M€ sur les 1 024 sommets de l'ensemble admissible. La largeur, 1 839 M€, est le coût de l'ignorance de la direction, connu d'avance. **p. 5, p. 108-113** |
| 2 | « Votre corpus sur-attribue à la gouvernance, et vous concluez qu'elle domine » | Le biais est mesuré, pas déclaré. En dégradant l'émission de P1, le classement tient jusqu'au quart et ne bascule qu'à la moitié : il faudrait supposer la moitié des arêtes artefactuelles. Le niveau, lui, ne perd que 24,8 % même à dégradation totale. **p. 95-106, p. 114-133** |
| 3 | « Vous dites ne pas connaître la direction et vous publiez un facteur 3,34 » | Deux objets distincts. Le 3,34 mesure l'effet des quatre canaux **à direction fixée** ; la bande mesure ce que l'ignorance de la direction coûte. Le chapitre 10 réconcilie explicitement le socle de 5 275 M€ et le SCR conforme de 5 900 M€. **p. 108-113, p. 114** |
| 4 | « Rien ne prouve que la conformité réduit la propagation » | Exact, et le mémoire le dit. Il ne mesure pas cet effet : il en exhibe la conséquence sous une hypothèse d'**ordre**. Le capital étant croissant en ce paramètre (monotonie stochastique démontrée), toute correspondance qui respecte l'ordre reproduit l'écart. La sensibilité est bornée par construction. **p. 88-94, p. 79-87** |
| 5 | « Pourquoi pas une copule ? » | Elle a été testée en benchmark adverse. Elle imite la photo d'un état mais ni le surcoût, ni l'interaction, ni le durcissement de la dépendance avec la non-conformité. La dépendance n'est pas le mécanisme, c'en est l'ombre. **p. 114-133** |
| 6 | « On ne peut pas valider un quantile à 99,5 % » | Chiffré dans le mémoire : détecter un taux de dépassement double du nominal avec 80 % de puissance demanderait **1 811 années** à 99,5 %. D'où le choix de valider la forme et la fréquence, et de déclarer le niveau non testable. **p. 69-78** |
| 7 | « ξ = 0,595, donc moyenne infinie ? » | Non. Pour 1/2 < ξ < 1, la variance est infinie et l'espérance finie. La proposition qui donne quantile et moyenne de queue pose explicitement ξ ∈ (0,1). **p. 69-78** |
| 8 | « Votre fréquence vient d'une base américaine sans seuil de matérialité » | λ_ref est une **clé de répartition**, pas le niveau du modèle. Le niveau vient d'ailleurs. **p. 47-67, p. 69-78** |
| 9 | « Hackmageddon n'est pas reproductible » | Déclaré comme citation et non comme sortie. Et c'est la source dont le modèle dépend le moins : trois instruments indépendants montrent que la catégorie d'un incident ne porte pas de segmentation. **p. 47-67** |
| 10 | « Que vaut votre modèle pour mon entité ? » | Le mémoire déclare lui-même l'entité notionnelle **hors domaine de validité** : la charge décroît beaucoup moins vite que la taille. Le 169 M€ est illustratif. Ce qui transfère, c'est le rapport et le classement. **p. 114-133** |
| 11 | « Votre backtest rejette le niveau » | Oui, et pour un motif nommé et chiffré : une dérive d'échelle de 4,00 % par an. La loi de fréquence couvre 91,7 % pour 90 % annoncé, la forme de queue passe. Le défaut est chiffré plutôt que corrigé, et légué en annexe F. **p. 135-146** |
| 12 | « Avez-vous utilisé l'IA ? » | Oui, et c'est déclaré en fin de résumé et détaillé à l'annexe G. Le dispositif de vérification rattache chaque nombre publié à la sortie du script qui le produit, et l'annexe dit aussi ce qu'il ne détecte pas. **p. 5, p. 197** |
| 13 | « Qu'apportez-vous à la science actuarielle ? » | Un mécanisme de dépendance dirigée dont trois propriétés sont démontrées, une frontière d'identification établie sur données réelles, et une recommandation de reporting **chiffrée** : documenter une seule dépendance lève 28,9 % de l'ambiguïté de capital. **p. 147-149, p. 150-153** |
| 14 | « Pourquoi avoir abandonné la non-transitivité, qui donnait son titre au mémoire ? » | Parce qu'elle a été testée dans trois formulations et qu'aucune ne tient. La réfuter était plus utile que la maintenir. **p. 79-87** |
| 15 | « Qu'auriez-vous fait avec plus de temps ? » | L'élicitation est prête et non exécutée, faute de panel ; le second codage en aveugle attend sa donnée ; l'amplitude des liens reste à calibrer. Les six pistes sont en annexe F. **p. 179-188, p. 194-196** |

### Plan d'exposé, 25 minutes

| Durée | Contenu |
|---|---|
| 2 min | Le problème : DORA impose de la gestion, Solvabilité II impose du capital, rien n'articule les deux. La Formule Standard est aveugle à la conformité |
| 4 min | Le mécanisme : cascade dirigée plutôt que copule, et pourquoi la direction compte (une matrice et sa transposée donnent un capital et une décision différents) |
| 3 min | Les données, et ce qu'elles ne permettent pas |
| 6 min | **Le cœur : la direction n'est pas identifiable.** Trois échecs, dont VERIS qui porte les champs sans les remplir. La réponse : borner plutôt que poser |
| 5 min | Les résultats : le facteur 3,34 à direction fixée, la bande à direction inconnue, le classement des piliers et sa robustesse |
| 3 min | La limite devenue livrable : ce que vaut l'information manquante, et laquelle demander en premier |
| 2 min | Limites assumées et ouvertures |

**Ne pas lire les fiches, garder le contact visuel** (§ 6.7). Et s'entraîner devant un jury fictif,
que le référentiel recommande explicitement.

### Les cinq figures à projeter

1. **La structure dirigée de W** et la propagation d'un choc — le mécanisme en une image
   (`fig:reseau-W`, p. 79-87).
2. **Les deux rayons spectraux sur le domaine admissible** — la stabilité garantie, pas espérée
   (`fig:branchement-R0`).
3. **La bande de capital sur l'ensemble admissible** — la réponse à la question n°1.
4. **La valeur de l'information, hiérarchisée** — la contribution réglementaire (`fig:voi`,
   p. 147-149).
5. **Le benchmark contre la copule** — ce que chaque cadre sait exprimer (`tab:benchmark-sf`).

---

## 7. Ce qui a été fait aujourd'hui

| Livrable | État |
|---|---|
| Annexe F, pistes pour de futurs mémoires (exigée § 5.1.h) | créée, p. 194 |
| Annexe G, inventaire de l'usage de l'IA (exigée § 5.1.h) | créée, p. 197 |
| Déclaration d'usage de l'IA en fin de résumé (exigée § 5.1.c) | créée, p. 5 |
| Matériel complémentaire | 71 pages, 0 renvoi cassé, DOI `10.5281/zenodo.22874525` posé et cliquable |
| Bornes de capital et valeur d'information | portées dans le résumé et la conclusion |
| Seuil de bascule du classement | publié au chapitre 12 |
| Résumés | 547 → 287 mots, 367 → 274 mots |
| Deux renvois cassés du matériel complémentaire | réparés |
| Quatre flottants orphelins, dont les deux tables de résultats | appelés |
| `pymupdf` déclaré | `requirements.txt` |
| Comptes contradictoires du README | recalculés : 45 `\matcomp`, pas 51 ni 54 |

**Contrôles finaux** : 204 pages, exit 0, 0 erreur, 5 débordements, 0 `vbox`, 0 `??`, harnais
**1 839 / 1 839**, zéro hors contrôle non déclaré, arbre git propre et rien de commité.
