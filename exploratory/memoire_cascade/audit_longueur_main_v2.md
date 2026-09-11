# Audit de longueur de `main_v2`

Mesuré le 11 septembre 2026 sur `main_v2.pdf` recompilé le jour même, et sur `main_v2.toc`.
Aucun fichier source n'a été modifié pour produire cet audit.

**La norme opposée est celle de l'Institut, et elle est chiffrée dans son propre texte**, relevé
dans `GUIDE_REDACTION.md` du dépôt : *« Volume du corps : environ 70 pages, hors introduction,
conclusion et annexes »*, section 5.1 de la version validée le 20 janvier 2026 et **applicable
depuis le 1er avril 2026**, donc celle qui fait foi pour une soutenance de novembre 2026. La
version ISFA la formule autrement et dans le même sens : *« le jury estime que l'essentiel d'une
étude peut s'exprimer en 70 pages, en moyenne, hors annexes »*.

**Une précision de périmètre qui change le calcul, et il faut la poser avant tout.** La norme
exclut l'**introduction**, la **conclusion** et les **annexes**. Le compte pertinent n'est donc
pas les 140 pages que la passation appelle « corps », mais ce qui reste une fois l'introduction
et la conclusion retirées. C'est ce compte qui est comparé ci-dessous.

---

## Verdict

### **Trop long**

| Grandeur | Mesure |
|---|---:|
| Total du PDF | **192 pages** |
| Préliminaires (résumé, abstract, sommaire), p. 1 à 5 | 5 |
| Corps au sens du document, p. 6 à 140 | 135 |
| dont introduction (ch. 1) | 9 |
| dont conclusion (ch. 13) | 2 |
| **Corps au sens de la norme, hors introduction et conclusion** | **124** |
| Annexes, p. 141 à 189 | 49 |
| Bibliographie, p. 190 à 192 | 3 |

**124 pages contre 70 recommandées, soit 77 % au-dessus.** L'écart est de 54 pages. Même en
lisant « environ 70 » avec la plus grande latitude, disons 85 pages, il resterait 39 pages de
trop. Le verdict ne dépend donc pas de la générosité de la lecture.

**Le principal facteur de la longueur n'est pas le bavardage, et c'est ce qui rend l'arbitrage
difficile.** Le mémoire ne délaye pas : il **publie l'intégralité de son dispositif de
vérification dans le corps**. Chaque résultat y est accompagné de sa mesure de robustesse, de sa
validation, de sa sensibilité et de sa réserve, au même niveau de détail que le résultat
lui-même. Trois chapitres portent à eux seuls 56 pages, soit 45 % du corps : le socle mécaniste
(17), l'identifiabilité (16) et les résultats (27). Ce n'est pas du remplissage, c'est un défaut
de **hiérarchisation** : le corps traite au même rang ce qui établit la thèse et ce qui la
contrôle.

**Recommandation : restructurer**, et non condenser ligne à ligne. Le levier principal est le
déplacement de blocs entiers vers les annexes, que la norme exclut du compte, et non la
réécriture du texte. Cible réaliste : **un corps de 80 à 85 pages**, soit 40 pages déplacées.

### Trois réserves, à lire avec le verdict

1. **L'arbitrage de format a déjà été tranché, et pas par moi.** La passation le dit :
   *« Tranché en faveur de Kélian, Hugo ayant dit de ne pas se contraindre »*, et le guide de
   rédaction classe la compression vers 70 pages en **dernier** de ses cinq chantiers, comme
   *« une décision de Kélian et non une règle »*. Le présent audit ne rouvre pas cette décision,
   il la documente : `main_v3` est une **version éditoriale parallèle**, `main_v2` reste intact,
   et le choix entre les deux reste entier.
2. **Le dépôt est le 30 septembre, donc dans dix-neuf jours.** Une restructuration touche la
   table des matières, les renvois croisés, le harnais de vérification et la numérotation des
   figures. Le risque n'est pas nul, et il justifie que `main_v3` procède par **déplacement de
   sections entières** plutôt que par réécriture.
3. **Une partie de la longueur est exactement ce que le jury note.** Le texte de l'Institut
   attache *« une attention particulière à l'esprit critique »*, demande de mettre en avant
   *« les échecs ou risques d'erreurs »*, et déclare que *« ce n'est pas un échec que de ne pas
   aboutir »*. La thèse réfutée par son auteur, le chiffre requalifié en borne supérieure, le
   défaut de calibration chiffré plutôt que corrigé : tout cela pèse des pages et **doit rester
   visible**. La réduction ne doit donc jamais porter sur les réserves elles-mêmes, mais sur leur
   **répétition** et sur le **détail de leur établissement**.

---

## Diagnostic quantitatif

### Vue d'ensemble

| Élément | Pages | Diagnostic |
|---|---:|---|
| Préliminaires | 5 | Conforme. Résumé français, abstract anglais et sommaire, tous exigés par la norme |
| Corps principal (norme) | **124** | **Trop long, 77 % au-dessus des 70 recommandées** |
| Introduction | 9 | Hors norme de comptage. Longue mais **exclue** du plafond, donc sans coût |
| Conclusion | 2 | Conforme, peut-être courte au regard de ce qu'elle doit faire |
| Bibliographie | 3 | Conforme |
| Annexes | 49 | Conforme, et **encore extensible** : la norme ne les plafonne pas |
| **Total** | **192** | Le total n'est pas la grandeur jugée, mais il pèse à la lecture |

**Les annexes sont l'endroit où la norme autorise le volume**, et elles ne représentent
aujourd'hui que 26 % du document. Le texte de l'Institut est explicite dans le même sens : *« les
données volumineuses et les listings ne figurent pas dans le corps mais en annexe »*. Le
déséquilibre actuel, 124 pages de corps pour 49 d'annexes, est l'inverse de ce que la norme
suggère pour un travail de cette densité.

### Par chapitre

| Chapitre | Sujet | Pages | Diagnostic | Action proposée |
|---|---|---:|---|---|
| 1 | Introduction | 9 | **Hors plafond.** Porte la lecture de marché ajoutée le 9 septembre | **Conserver** |
| 2 | Cadre réglementaire | 5 | Contexte nécessaire, mais exposé plus long que ce que la suite exploite | Condenser vers 3 |
| 3 | État de l'art et positionnement | 4 | Nécessaire et éliminatoire si absent. Volume correct | Conserver |
| 4 | Données et limites | 12 | Cœur de la traçabilité. Deux sections tiennent du justificatif | Condenser vers 9 |
| 5 | Socle mécaniste | **17** | **Le plus classique du mémoire.** Théorèmes d'extrapolation et comparaison d'estimateurs sont du cours | Condenser vers 11 |
| 6 | La cascade dirigée | 8 | Porte le mécanisme. Sa vérification numérique double l'annexe A | Condenser vers 6 |
| 7 | La conformité multi-états | 7 | Correct. Une section de trois pages sur le statut de $g$ est répétitive | Condenser vers 5 |
| 8 | L'identifiabilité | **16** | **Porte la contribution centrale.** Mais deux sections sont des chemins refermés | Condenser vers 11 |
| 9 | Identification partielle | 6 | Porte la méthode issue de la contribution | Conserver |
| 10 | Résultats | **27** | **Le plus long, et de loin.** Mêle le chiffre de tête, les extensions d'échelle et la lecture économique | Condenser vers 16 |
| 11 | Robustesse et incertitude | 13 | Indispensable au barème. Trop détaillé dans l'établissement | Condenser vers 8 |
| 12 | La donnée manquante | 4 | Contribution réglementaire, courte et utile | Conserver |
| 13 | Conclusion | 2 | **Hors plafond.** Courte au regard de ce que la norme lui demande | Conserver, voire étoffer |

Les cinq pages de titre de partie s'ajoutent aux totaux ci-dessus.

### Par annexe

| Annexe | Sujet | Pages | Diagnostic |
|---|---|---:|---|
| A | Démonstrations de la cascade | 3 | Bien placée |
| B | Démonstrations du socle | 2 | Bien placée |
| C | Adaptations par pilier | 13 | Bien placée. Contient les cas d'usage, six pages |
| D | Pièces justificatives | 21 | Bien placée, et c'est le bon réceptacle pour les déplacements |
| E | Protocole d'élicitation non exécuté | 5 | Bien placée, et c'est un actif devant le jury |
| F | Table des notations | 4 | Exigée par la norme |

---

## Diagnostic éditorial

### La question centrale

*Combien coûte en capital la non-conformité au règlement DORA, et jusqu'où ce chiffre peut-il
être affirmé ?* Elle est nette, tenue de bout en bout, et la seconde moitié de la question est ce
qui distingue ce mémoire d'un exercice de modélisation.

### La contribution, et il y en a une

**La frontière d'identifiabilité, puis sa transformation en méthode.** La matrice de contagion se
décompose en partie symétrique et antisymétrique ; la donnée identifie la co-occurrence et **pas**
la direction ; une matrice et sa transposée sont indistinguables pour la donnée et donnent un
capital et une décision différents. Plutôt que de poser la direction, le mémoire borne le capital
sur l'ensemble des matrices admissibles et chiffre en euros ce que la donnée manquante coûte.

C'est cela qui doit rester au premier plan, et c'est précisément ce que 124 pages rendent
difficile à voir.

### Les résultats indispensables au jury

1. l'écart entre états, 6 049 vers 20 188 M€, facteur 3,34, et le fait qu'il vienne du
   déplacement de **quatre paramètres** et non d'une pénalité ajoutée ;
2. la **non-additivité** des quatre canaux, 9 138 contre 14 139, soit 5 001 M€ d'interaction, et
   sa conséquence de gestion : c'est la colonne de fermeture qu'un plan de remédiation doit citer ;
3. la **frontière d'identifiabilité**, démontrée ;
4. l'**identification partielle** et le coût en euros de l'ignorance directionnelle ;
5. le **backtest hors échantillon**, avec ses deux succès et sa dérive ;
6. l'**inventaire des limites** en deux colonnes, écarts involontaires contre choix de prudence ;
7. la **donnée manquante comme livrable**, qui est la contribution réglementaire.

### Les résultats secondaires, et ils occupent un quart du corps

- la **descente d'échelle vers l'entité** et les quatre bilans réels, 7 pages, dont le mémoire
  déclare lui-même qu'elle produit une **borne supérieure d'ordre de grandeur et non une mesure** ;
- la **lecture économique**, détenir ou transférer, 6 pages, qui est une extension et non un
  résultat du modèle ;
- la **priorisation de la remédiation** et l'allocation Shapley et Euler, 4 pages, qui découlent
  du chiffre de tête sans le soutenir ;
- les **adaptations par pilier**, déjà en annexe, à bon droit.

### Ce qui est trop détaillé pour le corps

| Section | Pages | Nature |
|---|---:|---|
| 5.1 Les deux théorèmes qui autorisent l'extrapolation de queue | 2 | Résultats classiques de la théorie des valeurs extrêmes |
| 5.5 Hill contre maximum de vraisemblance | 2 | Comparaison d'estimateurs, établissement d'une validation |
| 6.9 Vérification numérique des trois propriétés | 2 | Contrôle, et l'annexe A porte déjà les démonstrations |
| 8.7 Le biais de narration, mesuré | 3 | Établissement d'un contrôle, dont seul le verdict compte au corps |
| 8.8 Les séquences ordonnées, voie refermée | 2 | **Chemin explicitement abandonné** |
| 10.7 La sensibilité aux probabilités de propagation | 4 | Sensibilité secondaire, dont la conclusion tient en trois nombres |
| 10.12 Détenir ou transférer | 6 | Lecture économique, hors du modèle |
| 11.4 Un défaut de calibration, chiffré | 4 | Réserve importante, mais son **établissement** est un détail |
| 4.9 Pourquoi ne pas multiplier les sources | 3 | Justificatif de choix de données |

### Les répétitions, comptées et non supposées

Comptage sur les treize fichiers du corps :

| Réserve | Occurrences |
|---|---:|
| « le niveau est illustratif » et ses variantes | **6** |
| « borne supérieure » | **7** |
| la direction n'est pas identifiable | **5** |
| la calibration est gelée | 3 |

Chacune de ces réserves est juste et doit figurer. Mais **une réserve énoncée sept fois cesse
d'être lue** : elle doit être posée une fois, à l'endroit où elle est établie, puis rappelée par
un renvoi. Le gain est diffus, de l'ordre de deux pages, mais le gain de lisibilité est supérieur
au gain de pages.

### Une duplication franche, trouvée en vérifiant

**Le corps et l'annexe traitent le même objet sous deux titres différents.** La section 8.8,
« Les séquences ordonnées : une voie explorée et refermée », 2 pages de corps, et la section D.16,
« Les séquences ordonnées du corpus, et pourquoi elles n'identifient rien », 3 pages d'annexe,
portent sur la même exploration, avec la même conclusion négative. **Cinq pages au total sur un
chemin que le mémoire déclare lui-même fermé**, dont deux dans le corps. C'est le déplacement le
plus évident du document, et il ne coûte aucune information.

### Le risque principal

**Le message central est dilué par le volume de contrôle.** Un jury qui lit 124 pages où le
résultat et sa vérification ont le même rang typographique retient le sérieux du dispositif, pas
la contribution. Le mémoire a une thèse identifiable en une phrase, et cette phrase est noyée
dans quatre-vingts pages de matériel de validation qui, pris un par un, sont tous justifiés.

**Et le texte de l'Institut nomme ce risque.** Sa section 5.3 liste parmi les motifs de refus de
validation *« la simple présentation des résultats sans indication des méthodes mises en œuvre ou
sans commentaires pertinents »*. Le guide de rédaction du dépôt commente déjà ce point : *« un
mémoire riche en sorties de scripts peut glisser vers le catalogue de résultats »*. Le mémoire n'y
a pas glissé, chaque table portant ce qu'elle établit, mais le volume rapproche du bord.

---

## Plan de réduction

Toutes les actions ci-dessous sont des **déplacements de sections entières vers les annexes**,
sauf mention contraire. Aucune ne supprime un résultat, aucune ne touche un nombre.

| Partie concernée | Action | Justification | Gain |
|---|---|---|---:|
| 8.8 Séquences ordonnées | **Déplacer**, fusionner avec D.16 | Duplication franche entre corps et annexe sur un chemin refermé | 2 |
| 10.12 Détenir ou transférer | **Déplacer**, garder un paragraphe et un renvoi | Lecture économique hors modèle. Le seuil de rentabilité reste au corps | 5 |
| 10.10 et 10.11 Descente d'échelle et quatre entités | **Condenser** vers 2 pages, détail en annexe | Le mémoire déclare lui-même qu'il s'agit d'une borne supérieure, pas d'une mesure | 5 |
| 5.1 Deux théorèmes d'extrapolation | **Déplacer** vers l'annexe B | Résultats classiques. L'énoncé et la condition d'application suffisent au corps | 2 |
| 5.5 Hill contre maximum de vraisemblance | **Déplacer** vers l'annexe B | Établissement d'une validation. Le verdict tient en deux phrases | 2 |
| 11.4 Défaut de calibration chiffré | **Condenser** vers 1 page, détail en annexe D | La réserve reste au corps, son établissement part. **Ne pas la retirer** | 3 |
| 11.2 et 11.3 Étages d'incertitude et postures | **Condenser** vers 3 pages | Deux sections qui exposent la même incertitude sous deux angles | 3 |
| 4.9 Pourquoi ne pas multiplier les sources | **Déplacer** vers l'annexe D | Justificatif de choix, pas résultat | 3 |
| 8.7 Biais de narration | **Condenser** vers 1 page, détail en annexe | Seul le verdict et son ampleur comptent au corps | 2 |
| 10.7 Sensibilité à la propagation | **Condenser** vers 2 pages | Sa conclusion tient en trois nombres, et elle va contre l'intuition, donc elle reste | 2 |
| 2 Cadre réglementaire | **Condenser** vers 3 pages | Exposé plus long que ce que la suite exploite | 2 |
| 6.9 Vérification numérique des propriétés | **Déplacer** vers l'annexe A | L'annexe A porte déjà les démonstrations correspondantes | 2 |
| 7.4 Le statut des valeurs de $g$ | **Condenser** vers 1 page | Trois pages pour un argument que le chapitre 9 reprend | 2 |
| 10.3 et 10.5 Allocation et priorisation | **Condenser** vers 3 pages | Découlent du chiffre de tête, ne le soutiennent pas | 1 |
| Réserves répétées, tout le corps | **Condenser** par renvoi | Six « illustratif », sept « borne supérieure », cinq « non identifiable » | 2 |
| **Total** | | | **38** |

En tenant compte des pages de titre de partie et des effets de recomposition, le gain attendu est
de **38 à 42 pages**.

### Ce qui ne doit pas être touché, et pourquoi

- **la frontière d'identifiabilité et sa démonstration** : c'est la contribution ;
- **l'identification partielle et les bornes** : c'est la méthode qui en découle ;
- **le chiffre de tête, les quatre canaux, l'interaction** : c'est le résultat ;
- **le backtest hors échantillon** : c'est le seul test hors échantillon du travail, et la
  première question d'un jury d'actuaires ;
- **l'inventaire des limites en deux colonnes** : c'est ce que la section 4.6 du texte de
  l'Institut note ;
- **la donnée manquante comme livrable** : c'est la contribution réglementaire, et elle est déjà
  courte ;
- **l'introduction et sa lecture de marché** : la norme **exclut l'introduction** du plafond, donc
  ces neuf pages ne coûtent rien au verdict. Y toucher serait défaire sans gain une demande du
  9 septembre ;
- **le protocole d'élicitation non exécuté** : déjà en annexe, et c'est un actif.

---

## Cible recommandée

| Grandeur | Actuel | Cible |
|---|---:|---:|
| Corps au sens de la norme | 124 | **82 à 86** |
| Introduction | 9 | 9, inchangée |
| Conclusion | 2 | 2 à 3 |
| Annexes | 49 | **85 à 90** |
| Préliminaires et bibliographie | 8 | 8 |
| **Total** | **192** | **188 à 194** |

**Le total ne baisse pas, et c'est voulu.** L'objet de la restructuration n'est pas de raccourcir
le travail, c'est de le **hiérarchiser** : le corps redevient lisible d'un trait, et le matériel
de validation reste intégralement disponible là où la norme le place. Rien n'est perdu, tout est
déplacé. C'est aussi ce qui rend l'opération réversible et peu risquée à dix-neuf jours du dépôt.

### Structure recommandée du corps

1. **Problème professionnel, actuariel et réglementaire** : le vide prudentiel, le marché, DORA.
2. **Question et contribution** : ce qui est établi, ce qui est borné, ce qui est posé.
3. **Données, limites d'observation et stratégie d'identification**.
4. **Modèle et hypothèses indispensables** : fréquence, sévérité, cascade, états.
5. **La frontière d'identifiabilité et l'identification partielle**.
6. **Résultats principaux** : l'écart, les quatre canaux, l'interaction.
7. **Limites et robustesse essentielles** : backtest, inventaire, bande reportée.
8. **Implications** : pour l'entité, pour le régulateur, pour la collecte.
9. **Conclusion**.

### Les sept éléments qui doivent rester dans le corps

1. la **table des quatre canaux** et ses trois lectures, isolée, fermeture, Shapley ;
2. la **figure de l'identification partielle**, désignée dans le document comme le résultat
   central ;
3. la **figure de la frontière**, le courant dirigé et l'énergie de fluctuation ;
4. le **chiffre de tête** par état de conformité ;
5. la **table des limites en deux colonnes**, écarts involontaires contre choix de prudence ;
6. le **backtest hors échantillon** et sa puissance chiffrée en années ;
7. la **mise en regard des cadres existants**, qui montre ce que la Formule Standard et une
   copule expriment de l'effet DORA.

---

## Décision découlant du verdict

Le verdict étant **Trop long**, la règle posée impose la création de `main_v3`. La suite du
travail est décrite dans `plan_main_v3.md`.

**Trois garanties de méthode, et elles sont contraignantes :**

1. `main_v2.tex`, ses chapitres partagés, les figures, les sorties de scripts et
   `sorties_verif/` ne sont **pas modifiés**. `main_v3` vit à côté ;
2. les chapitres que `main_v3` ne modifie pas sont **appelés tels quels** depuis
   `chapitres/`, donc sans aucun risque de divergence ;
3. les chapitres restructurés sont **de nouveaux fichiers** sous `chapitres_v3/`, obtenus par
   déplacement de sections et non par réécriture. Les nombres, les figures et les lignes de
   sources du harnais partent avec leur section.
