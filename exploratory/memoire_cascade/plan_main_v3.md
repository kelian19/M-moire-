# Plan de restructuration : `main_v3`

Établi le 11 septembre 2026, après le verdict **trop long** de `audit_longueur_main_v2.md`
(corps de 124 pages au sens de la norme, contre 70 recommandées).

---

## Le principe, et il commande tout le reste

**`main_v3` déplace, il ne réécrit pas.** Quatorze sections entières quittent le corps pour une
annexe, avec leur texte, leurs nombres, leurs figures, leurs tables et leur ligne « Sources :
scripts… » du harnais. À leur place, le corps reçoit un **pont de deux à quatre phrases** qui dit
ce que la section établit et renvoie à l'annexe.

Trois raisons à ce choix plutôt qu'une condensation ligne à ligne :

1. **aucun nombre ne bouge**, donc le harnais reste valide et la traçabilité intacte ;
2. **l'opération est réversible** : remettre une section dans le corps est un déplacement inverse ;
3. **à dix-neuf jours du dépôt**, réécrire quatre-vingts pages de prose technique est le genre de
   chantier qui introduit des erreurs que plus personne n'a le temps de trouver.

## L'architecture, et ce qu'elle protège

| Fichier | Statut |
|---|---|
| `main_v2.tex`, `main.tex`, `preambule*.tex` | **NON MODIFIÉS** |
| `chapitres/*.tex` | **NON MODIFIÉS**, partagés par les deux versions existantes |
| `sorties_verif/`, `figures/`, `references.bib` | **NON MODIFIÉS** |
| `main_v3.tex` | **NOUVEAU**, autonome, appelle `preambule_v2.tex` |
| `chapitres_v3/*.tex` | **NOUVEAUX**, huit chapitres allégés plus une annexe de compléments |

Les chapitres que `main_v3` ne restructure pas sont appelés **tels quels** depuis `chapitres/`,
donc sans copie et sans risque de divergence. Seuls huit fichiers sur dix-neuf ont une variante.

---

## Corps conservé sans modification

Ces neuf pièces sont appelées depuis `chapitres/`, identiques à `main_v2` :

| Fichier | Chapitre | Motif |
|---|---|---|
| `01_resume.tex` | Résumé, abstract, sommaire | Exigés par la norme |
| `02_introduction.tex` | Introduction | **La norme exclut l'introduction du plafond.** La lecture de marché du 9 septembre ne coûte rien au verdict |
| `03_etat_art_positionnement.tex` | État de l'art | Quatre pages, et la recherche bibliographique peut être éliminatoire si jugée insuffisante |
| `10_identification_partielle.tex` | Identification partielle | **La méthode issue de la contribution** |
| `13b_donnee_manquante_livrable.tex` | La donnée manquante | **La contribution réglementaire**, quatre pages |
| `14_conclusion.tex` | Conclusion | Hors plafond, et déjà courte |
| `15b`, `15`, `12b`, `17`, `18`, `16` | Annexes A à F | Déjà à leur place |

---

## Chapitres restructurés, section par section

Quatorze déplacements. La colonne « pont » dit ce qui reste dans le corps.

### `05_donnees_limites.tex` → `chapitres_v3/05_donnees_limites_v3.tex`

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| Pourquoi ne pas multiplier les sources | Le choix de ne pas empiler les sources est un choix, son motif est en annexe | 3 |

### `06_socle_mecaniste.tex` → `chapitres_v3/06_socle_mecaniste_v3.tex`

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| Les deux théorèmes qui autorisent l'extrapolation de queue | L'énoncé des deux théorèmes et la condition d'application, sans les démonstrations | 2 |
| Hill contre maximum de vraisemblance | Le verdict : l'écart de 120,8 % est **exactement** ce qu'un $\xi$ de 0,595 produit, donc la donnée corrobore la calibration | 2 |

### `07_cascade_dirigee.tex` → `chapitres_v3/07_cascade_dirigee_v3.tex`

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| Vérification numérique des trois propriétés | Les trois propriétés sont vérifiées numériquement, l'annexe A porte déjà leurs démonstrations | 2 |

### `11_conformite_multietats.tex` → `chapitres_v3/11_conformite_multietats_v3.tex`

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| Les valeurs de $g$ sont posées, et la conclusion n'en dépend pas | **Le statut posé et l'argument de monotonie restent**, en un paragraphe. Le balayage part | 2 |

### `09_identifiabilite.tex` → `chapitres_v3/09_identifiabilite_v3.tex`

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| Le biais de narration, mesuré au lieu d'être déclaré | Le verdict et son ampleur : le biais est **borné et non levé** | 2 |
| Les séquences ordonnées : une voie explorée et refermée | Une phrase, et le renvoi. **Cette section faisait doublon avec l'annexe D.16** | 2 |
| La formalisation bayésienne, et sa prudence | Une phrase : la reformulation bayésienne ne déplace pas la frontière | 2 |

**Ce chapitre garde intégralement** ce qui porte la contribution : les trois échecs, la lecture
par la réversibilité, le choc MOVEit, le corpus, la matrice ordonnée et la frontière en trois
niveaux.

### `12_resultats.tex` → `chapitres_v3/12_resultats_v3.tex`

Le chapitre le plus long du mémoire, 27 pages. Quatre déplacements, aucun sur le chiffre de tête.

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| La sensibilité aux probabilités de propagation | **Le résultat contre-intuitif reste** : la fragilité est dans l'ajustement de queue, pas dans la contagion | 3 |
| Un ordre de grandeur à l'épreuve du réel | La descente d'échelle existe, sa borne inférieure de validité est publiée | 3 |
| Quatre entités réelles, et la borne inférieure de la méthode | **La requalification en borne supérieure reste au corps**, le détail des quatre bilans part | 2 |
| Détenir ou transférer | Le seuil de rentabilité et le sens de la borne restent en deux phrases | 5 |

**Ce chapitre garde** le SCR par état, la décomposition par pilier, l'allocation, la trajectoire,
la priorisation, la robustesse, la comparaison au jumeau copule et la mise en regard
réglementaire.

### `13_inventaire_hypotheses.tex` → `chapitres_v3/13_inventaire_hypotheses_v3.tex`

| Section déplacée | Pont conservé au corps | Gain |
|---|---|---:|
| De l'incertitude au chiffre reporté : VaR prédictive et VaR robuste | La posture reportée et son motif, plus le fait que la robuste à 95 % **est** la borne haute de l'intervalle déjà publié | 2 |
| Un défaut de calibration, chiffré plutôt que corrigé | **La réserve reste au corps en une page**, avec son ampleur et son sens. Seul son établissement part | 3 |

**Ce chapitre garde** la table de robustesse, les trois étages d'incertitude et les défaillances
simultanées.

### `04_cadre_reglementaire.tex` → `chapitres_v3/04_cadre_reglementaire_v3.tex`

Fichier sans découpe en sections. Traitement différent : **aucun déplacement**, une relecture
resserrée qui retire les redites de l'exposé réglementaire sans toucher aux articles cités.
Gain visé : 2 pages. **Si la relecture ne dégage pas ce gain sans perte, le chapitre reste
inchangé** et le plan l'assume.

---

## L'annexe qui reçoit

**Nouveau fichier `chapitres_v3/19_complements_corps.tex`, annexe G**, intitulée
« Compléments méthodologiques ». Elle reçoit les quatorze sections **verbatim**, regroupées en
six blocs thématiques dans l'ordre du corps :

1. le choix de ne pas multiplier les sources ;
2. les fondements d'extrapolation de queue et la confrontation des estimateurs ;
3. la vérification numérique des propriétés de la cascade et le statut des valeurs de $g$ ;
4. le biais de narration, les séquences ordonnées et la formalisation bayésienne ;
5. la sensibilité à la propagation, la descente d'échelle, les quatre entités et la lecture
   économique ;
6. les postures de report et l'établissement du défaut de calibration.

Elle se place **après l'annexe E** et avant la table des notations, qui reste en dernier.

---

## Les renvois internes à créer

Chaque pont porte un `\ref` vers la section déplacée. Les sections qui n'ont pas de `\label` en
reçoivent un dans le fichier d'annexe, de la forme `\label{ann:g:<sujet>}`. **Aucun `\label`
existant n'est renommé** : les renvois des chapitres non modifiés continuent de résoudre, la
cible ayant seulement changé de place dans le document.

---

## Ce qui n'est pas supprimé

**Rien.** Aucune section, aucun tableau, aucune figure, aucun nombre, aucune réserve ne disparaît
du document. Le total de pages reste stable, autour de 190 : la restructuration change la
**place** du matériel, pas son existence. C'est la condition pour que l'opération soit sans perte
scientifique et réversible.

La seule exception envisagée est la **duplication mesurée** entre la section 8.8 du corps et la
section D.16 de l'annexe, qui traitent le même objet sous deux titres. Le plan la traite par
déplacement et non par suppression : les deux textes se retrouvent dans le même document, et leur
fusion éventuelle est laissée à Kélian.

---

## Longueur cible par partie

| Partie | `main_v2` | Cible `main_v3` |
|---|---:|---:|
| Préliminaires | 5 | 5 |
| Introduction | 9 | 9 |
| Corps hors introduction et conclusion | **124** | **86 à 91** |
| Conclusion | 2 | 2 |
| Annexes | 49 | 84 à 89 |
| Bibliographie | 3 | 3 |
| **Total** | **192** | **190 à 195** |

**Gain attendu sur le corps : 33 à 38 pages.** Cela ramène l'écart à la norme de **+77 % à
environ +25 %**.

**Et il faut le dire sans l'enjoliver : la cible de 70 pages n'est pas atteinte.** Y parvenir
demanderait d'entamer le chapitre de l'identifiabilité ou celui des résultats, c'est-à-dire la
contribution et le résultat central. Le plan s'y refuse. Un corps de 88 pages pour un mémoire qui
publie un mécanisme démontré, une frontière d'identifiabilité, une méthode de bornes et un
backtest est défendable devant un jury ; un corps de 70 pages obtenu en retirant l'un des quatre
ne le serait pas.

---

## Ordre d'exécution et contrôles

1. créer `chapitres_v3/` et l'annexe de compléments, en déplaçant les sections **par extraction
   de lignes**, sans retaper le texte ;
2. écrire les quatorze ponts ;
3. créer `main_v3.tex` ;
4. compiler deux fois, résoudre table des matières et renvois ;
5. **contrôles** : zéro `??` compté dans le PDF produit, zéro `Overfull \vbox`, zéro annotation
   hors page, zéro page tournée, débordements comparés à la ligne de base de la v2 ;
6. **harnais** sur les huit fichiers `_v3` et sur l'annexe de compléments : la couverture et le
   taux de confirmation doivent être **identiques** à ceux des fichiers d'origine, puisque aucun
   nombre n'a bougé. Toute différence est un défaut de découpe, pas un défaut de contenu ;
7. vérifier que `main_v2.pdf` et `main.pdf` sont inchangés.
