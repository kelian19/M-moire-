# Rapport de modifications : `main_v3`

11 septembre 2026. Verdict de l'audit : **trop long**. Consigne de Kélian le même jour :
**écarter la norme de l'Institut et réduire quand même de 20 %.**

---

## Pages, avant et après

| Partie | `main_v2` | `main_v3` | Écart |
|---|---:|---:|---:|
| Préliminaires (résumé, abstract, sommaire) | 5 | 5 | 0 |
| **Corps** (p. 6 à la veille des annexes) | **135** | **104** | **−31, soit −23,0 %** |
| Annexes et bibliographie | 52 | 52 | 0 |
| **Total** | **192** | **161** | **−31, soit −16,1 %** |

**Les deux chiffres sont donnés parce qu'ils ne disent pas la même chose, et il ne faut pas
choisir le plus flatteur.** La réduction demandée est **atteinte et dépassée sur le corps**,
à −23 %. Elle **n'est pas atteinte sur le document entier**, à −16 %, parce que les annexes et
la bibliographie n'ont pas été touchées. Les leviers pour aller au-delà sont nommés en fin de
rapport ; aucun n'a été actionné sans instruction, parce qu'ils entament tous du contenu.

---

## Ce qui a changé, et comment

**Quatorze sections ont été retirées du document**, soit 1 784 lignes de source. Chacune est
remplacée par une section courte, le « pont », qui énonce ce qu'elle établissait et cite le ou
les scripts qui le portent.

**Le changement de méthode en cours de route doit être dit.** La première construction
*déplaçait* ces quatorze sections vers une annexe de compléments. C'était la bonne réponse tant
que la cible était la norme de l'Institut, qui compte « environ 70 pages **hors annexes** » :
déplacer suffisait à s'y conformer. La consigne ayant changé pour une réduction réelle, cette
annexe a été supprimée et les sections sortent du document. Un déplacement ne réduit rien, il
redistribue.

### Les quatorze sections retirées

| Chapitre | Section retirée | Ce que le pont conserve |
|---|---|---|
| Données | Pourquoi ne pas multiplier les sources | Le choix et son principe, sans le détail source par source |
| Socle | Les deux théorèmes qui autorisent l'extrapolation de queue | Que la forme de queue est **héritée d'un théorème** et non ajustée librement |
| Socle | Hill contre maximum de vraisemblance | Le verdict, et **la figure du Hill plot est conservée** |
| Cascade | Vérification numérique des trois propriétés | Que les trois propriétés sont vérifiées, avec renvoi aux démonstrations de l'annexe A |
| Multi-états | Les valeurs de $g$ sont posées | **L'argument de monotonie en entier** : seule l'amplitude est un scénario |
| Identifiabilité | Le biais de narration, mesuré | Le verdict : le biais est **borné et non levé** |
| Identifiabilité | Les séquences ordonnées, voie refermée | Que la voie est fermée, et qu'un critère de réouverture existe |
| Identifiabilité | La formalisation bayésienne | Qu'elle **ne déplace pas la frontière** |
| Résultats | La sensibilité aux probabilités de propagation | Le résultat contre-intuitif : la fragilité est dans la queue, pas dans la contagion |
| Résultats | Un ordre de grandeur à l'épreuve du réel | La borne inférieure de validité, et **la table des échelles est conservée** |
| Résultats | Quatre entités réelles | **La requalification en borne supérieure**, qui est le point |
| Résultats | Détenir ou transférer | L'identité de la valeur présente et le **sens de la borne** du retour |
| Robustesse | De l'incertitude au chiffre reporté | La posture retenue, son motif, et que la robuste **est** la borne haute déjà publiée |
| Robustesse | Un défaut de calibration, chiffré | **La réserve entière et ses deux sens**, sans son établissement |

### Ce qui n'a pas été modifié

- **`main_v2.tex`, `main.tex`, tous les fichiers de `chapitres/`, les figures, `references.bib`
  et `sorties_verif/`** : vérifié par `git diff`, aucune modification ;
- **les six annexes**, conservées intégralement. L'Institut demande explicitement que les
  développements usuels y figurent, et une annexe retirée ne serait pas condensée mais perdue ;
- **l'introduction, l'état de l'art, l'identification partielle, la donnée manquante et la
  conclusion**, qui portent la contribution ou sont déjà courts ;
- **le chapitre du cadre réglementaire.** Le plan prévoyait d'en dégager deux pages par
  relecture, avec une clause explicite : « si la relecture ne dégage pas ce gain sans perte, le
  chapitre reste inchangé ». Ce chapitre ne porte aucun découpage en sections, donc le gain
  n'était accessible que par réécriture d'une prose qui cite des articles, à dix-neuf jours du
  dépôt. **La clause joue, et c'est deux pages de moins que la cible.**

---

## Comment les chapitres de la v3 sont faits, et pourquoi cela compte

**Ils sont générés, pas écrits.** Le script `construire_v3.py` lit `chapitres/`, en retire les
quatorze sections et écrit `chapitres_v3/`. Corriger un chapitre de la v3 se fait **dans le
fichier partagé puis par relance du script**.

Ce n'est pas une préférence d'outillage. La règle du projet interdit de dupliquer un chapitre
pour faire évoluer une version, parce que deux textes à maintenir divergent en une semaine. La
v3 avait besoin de chapitres différents ; les dériver est la seule façon de tenir les deux
contraintes. **Ne jamais éditer `chapitres_v3/` à la main.**

---

## Comment la contribution a été préservée

**Aucune des quatre pièces qui portent le mémoire n'est touchée.**

1. **le mécanisme** : la cascade dirigée, ses trois propriétés et leurs démonstrations en
   annexe A, intégralement conservés. Seule leur vérification numérique part ;
2. **la frontière d'identifiabilité** : le chapitre la conserve en entier, les trois échecs, la
   lecture par la réversibilité, le choc MOVEit, le corpus, la matrice ordonnée et la frontière
   en trois niveaux. Ce qui part est ce qui **contrôle** la frontière, jamais ce qui l'établit ;
3. **l'identification partielle** : chapitre inchangé, appelé tel quel ;
4. **le résultat** : le chiffre de tête, les quatre canaux, leur non-additivité, l'attribution,
   la trajectoire, la priorisation et la mise en regard des cadres existants sont tous conservés.

**Et la distinction entre les quatre statuts est maintenue partout** : ce qui est démontré, ce
qui est mesuré, ce qui est posé, ce qui n'est pas identifiable. Les ponts la rappellent
explicitement là où la section retirée la portait, en particulier sur le statut posé des valeurs
du gain de propagation et sur la requalification du chiffre d'entité en borne supérieure.

**Une duplication disparaît au passage.** L'audit avait relevé que la section « Les séquences
ordonnées » du corps et la section D.16 de l'annexe traitaient le même objet sous deux titres,
cinq pages au total sur un chemin déclaré fermé. La v3 retire celle du corps et garde celle de
l'annexe : le sujet reste traité une fois, au bon endroit.

---

## Ce qu'il faut savoir avant de choisir la v3, et c'est le point le plus important

**Le retrait le plus lourd de conséquence est celui de « Un défaut de calibration, chiffré
plutôt que corrigé », quatre pages.** La réserve elle-même reste au corps, avec son ampleur et
ses deux sens opposés, mais son établissement part.

Or la note d'honnêteté du projet qualifie cette section d'« actif du mémoire, pas une dette », et
le texte de l'Institut va dans le même sens : il attache « une attention particulière à l'esprit
critique », demande de mettre en avant « les échecs ou risques d'erreurs », et déclare que « ce
n'est pas un échec que de ne pas aboutir ». **Ce sont les critères du jury, et cette section les
sert directement.**

Le même raisonnement vaut, à un degré moindre, pour le biais de narration et pour les quatre
entités réelles : ce sont trois endroits où le mémoire se critique lui-même avec des chiffres.
Les ponts disent le verdict, ils ne montrent plus le travail.

**C'est un arbitrage, pas un défaut de la v3, et il appartient à Kélian.** La version longue
existe, intacte, et le choix entre les deux reste entier.

---

## Contrôles passés

| Contrôle | `main_v2` | `main_v3` |
|---|---|---|
| Compilation, deux passes | sans erreur | **sans erreur** |
| `??` comptés dans le PDF | 0 | **0** |
| Renvois sans cible, diff `.aux` contre `\ref` | 0 | **0** |
| `Overfull \hbox` distincts | 6 | **5** |
| `Overfull \vbox` | 0 | **0** |
| Annotations hors page | 0 | **0** |
| Pages tournées | 0 | **0** |
| Bibliographie | compile | **compile** |

**Le harnais de vérification, chapitre par chapitre.** Aucun nombre n'ayant bougé, le taux devait
rester identique, et il l'est :

| Chapitre | v2 | v3 |
|---|---|---|
| Données et limites | 119 sur 119 | 113 sur 113 |
| Socle mécaniste | 291 sur 291 | 232 sur 232 |
| Cascade dirigée | 67 sur 67 | 44 sur 44 |
| Conformité multi-états | 104 sur 104 | 49 sur 49 |
| Identifiabilité | 179 sur 179 | 116 sur 116 |
| Résultats | 521 sur 521 | 257 sur 257 |
| Robustesse | 209 sur 209 | 88 sur 88 |

**100 % de couverture et 100 % de confirmation partout, zéro hors contrôle non déclaré.** Les
effectifs baissent parce que des sections sont parties, pas parce qu'un contrôle a été relâché.

### Deux défauts trouvés et corrigés pendant la construction

1. **Vingt `??` à la première compilation.** Retirer une section casse tous les renvois qui la
   visent, y compris depuis des chapitres non modifiés. Sept cibles manquaient. Les cinq labels
   de **section** sont désormais repris par les ponts, de sorte que le renvoi pointe vers
   l'endroit où le sujet vit désormais. Les deux labels de **flottant** ne pouvaient pas être
   redirigés vers une section sans mentir sur la nature de l'objet : **la figure du Hill plot et
   la table des échelles repartent donc avec leur pont**, dont elles illustrent exactement le
   propos. La table des échelles est un cas à connaître : elle vit au chapitre des résultats et
   le chapitre des données la cite **deux fois**.
2. **Une faute de syntaxe dans les ponts générés**, « sont **à** la version longue » au lieu de
   « sont **dans** la version longue », et un motif de substitution qui ne franchissait pas un
   retour à la ligne, ce qui laissait trois ponts sur quatorze non traités. Les deux ont été
   trouvés **en relisant la sortie générée**, pas le code.

---

## Comparaison des conclusions, v2 contre v3

- **la question de recherche est identique**, mot pour mot : le chapitre d'introduction n'est pas
  modifié ;
- **les résultats principaux sont identiques** : aucun nombre n'a été touché, ajouté ni
  recalculé. Le chiffre de tête, le facteur entre états, l'écart et l'interaction entre canaux
  sont les mêmes ;
- **les limites restent explicites** : la table des limites en deux colonnes est conservée, la
  requalification en borne supérieure est conservée, le statut posé du gain de propagation est
  conservé, le défaut de calibration est conservé comme réserve ;
- **aucune conclusion n'est renforcée.** Les ponts ne concluent rien que la section retirée ne
  concluait pas, et plusieurs disent explicitement ce qui n'est **pas** établi : le biais de
  narration « borné et non levé », la reformulation bayésienne qui « ne déplace pas la
  frontière », le retour sur investissement qui est un « majorant ».

---

## Les leviers restants, si les 20 % doivent être atteints sur le document entier

Il manque sept pages. Aucun de ces leviers n'a été actionné, parce que tous entament du contenu
plutôt que de le réorganiser.

| Levier | Gain | Ce qu'il coûte |
|---|---:|---|
| Cas d'usage de l'annexe C | 6 | La partie la plus concrète pour un lecteur opérationnel |
| Condensation du cadre réglementaire | 2 | Réécriture d'une prose qui cite des articles |
| Réserves répétées, six « illustratif », sept « borne supérieure », cinq « non identifiable » | 2 | Rien de scientifique, mais une vraie réécriture dans treize fichiers partagés |
| Allocation et priorisation, chapitre des résultats | 1 | Deux sorties de gestion parmi les plus lisibles |

**Le troisième est le seul gratuit sur le fond**, et c'est aussi celui qui améliorerait le plus la
lecture. Il suppose en revanche de modifier les chapitres **partagés**, donc de toucher aussi la
v1 et la v2, ce que la consigne de préservation interdit en l'état.
