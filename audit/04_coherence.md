# Phase 4 — Cohérence texte, code, données et reproductibilité

Relevé du 21 septembre 2026, sur `main_ensae.pdf` (202 pages) et le dépôt à l'état courant.

**Le rapprochement exhaustif texte ↔ code existe déjà et il est vert.** Le harnais du projet relit
le manuscrit, extrait chaque nombre publié et le cherche dans les sorties versionnées des scripts
que le bloc déclare. Exécuté deux fois pendant cette session, par un chemin indépendant de celui du
projet : **1 826 nombres vérifiables, 1 826 confirmés, sur 24 chapitres, zéro hors contrôle non
déclaré.**

Cette phase porte donc sur ce que le harnais **ne voit pas** : la cohérence d'une zone du document
à l'autre, et la reproductibilité de la chaîne.

---

## 1. Cohérence entre les zones du document

Le harnais contrôle chaque chapitre **indépendamment** contre les scripts. Deux zones peuvent donc
citer la même sortie à des arrondis différents et être toutes deux confirmées. J'ai extrait les
grandeurs de tête de six zones du PDF et les ai confrontées.

| Grandeur | Résumé FR | Abstract EN | Note de synthèse | Exec. summary | Ch. 12 | Conclusion |
|---|---|---|---|---|---|---|
| Capital conforme, 6 049 M€ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Capital non conforme, 20 188 M€ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Facteur 3,34 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Interaction 5 001 M€ (35 %) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Écart 14 139 M€ | ✔ | ✔ | ✔ | ✔ | ✔ | **absent** |
| **Bornes 6 858 – 8 697 M€** | **absent** | **absent** | ✔ | ✔ | **absent** | **absent** |
| Largeur de bande 1 839 M€ | absent | absent | ✔ | ✔ | ✔ | absent |
| **Valeur d'information 28,9 % / 66 %** | **absent** | **absent** | **absent** | **absent** | **absent** | **absent** |

**Aucune divergence d'arrondi, nulle part.** Les grandeurs de tête sont écrites à l'identique dans
les six zones. Sur un document qui a porté quatre versions pendant des mois, c'est un résultat
solide, et c'est ce que la Phase 4 cherchait en priorité.

Mais deux absences en ressortent, et elles ne sont pas des détails de rédaction.

### P4-1 — Les bornes de capital n'apparaissent que dans la note de synthèse · **majeure**

**Constat, vérifié page par page.** Les bornes 6 858 – 8 697 M€ figurent dans la note de synthèse et
l'executive summary, et **nulle part ailleurs** : ni dans le résumé français, ni dans l'abstract,
ni dans le chapitre 12, ni dans la conclusion. Le mot « borne » y est bien présent, mais pas les
nombres.

**Risque devant le jury.** Un juré qui lit le résumé puis la conclusion — c'est la lecture d'un
membre pressé, et le référentiel dit au § 5.1.f que la conclusion « donne la dernière impression au
lecteur, l'image finale qui influencera fortement le jury » — ne voit jamais la réponse que le
mémoire donne réellement à la question « quel est votre capital ? ». Il ne voit que le point 3,34.

C'est la confirmation, par un chemin indépendant, du constat F12 de la Phase 3 : **la thèse
centrale du mémoire est la moins visible de ses affirmations.**

**Correction.** Porter les bornes et leur largeur dans le résumé et dans la conclusion. Le texte
existe déjà dans la note de synthèse : c'est un déplacement, pas une rédaction. **Coût : 45 min.**

### P4-2 — La contribution réglementaire n'apparaît dans aucune zone de synthèse · **majeure**

**Constat, vérifié.** La valeur d'information — 66 % de resserrement de la bande, et 28,9 %
d'ambiguïté levée par la seule dépendance gouvernance-incidents — n'apparaît **dans aucune** des six
zones. Elle vit uniquement dans le chapitre 13b, pages 146 à 148.

Or c'est ce même chapitre qui écrit d'elle : « C'est la contribution réglementaire du travail »,
et « c'est le seul endroit du mémoire où une limite produit un livrable ».

**Risque devant le jury.** Le § 5.1.f demande que la conclusion « indique clairement ce que le
travail a amené à la science actuarielle ». Le mémoire a une réponse chiffrée et opposable —
documenter tel champ vaut tant en capital — et elle n'atteint ni le résumé, ni la note de synthèse,
ni la conclusion. Trois pages sur 202 portent ce que le mémoire désigne lui-même comme son apport
réglementaire.

**Correction.** Deux phrases dans la conclusion et une dans le résumé. **Coût : 30 min.**

### Point mineur

L'écart de 14 139 M€ est absent de la conclusion alors que ses deux composantes, 9 138 et 5 001, y
figurent. Incohérence de présentation, sans conséquence. *Coût : 5 min.*

---

## 2. Le chiffre qui manquait à F14, et il change la réponse à donner

La Phase 3 laissait ouvert : jusqu'à quel degré de dégradation du corpus le classement des piliers
tient-il ? Le chiffre existe, il est calculé, il est dans `sorties_verif/64.txt`.

Le script dégrade l'émission de P1 par $W_{1k} \to (1-a)W_{1k}$ et **recalcule l'ensemble
admissible** pour chaque degré, la dégradation modifiant la partie symétrique.

| $a$ | SCR entité | Bande | Largeur | Shapley P1 | Shapley P4 | 1er |
|---|---|---|---|---|---|---|
| 0,00 | 169,0 | [131,5 ; 183,3] | 51,7 | **41,9** | 28,6 | P1 |
| 0,25 | 159,3 | [126,5 ; 171,3] | 44,7 | **32,2** | 28,1 | P1 |
| **0,50** | 149,5 | [121,8 ; 159,3] | 37,4 | 22,4 | **27,6** | **P4** |
| 0,75 | 138,0 | [115,8 ; 148,5] | 32,6 | 10,8 | **24,8** | P4 |
| 1,00 | 127,1 | [111,4 ; 137,1] | 25,8 | 0,0 | **23,3** | P4 |

**Deux lectures opposées, et le mémoire n'en publie qu'une.**

- **Le niveau résiste.** Même en rendant P1 complètement muette, le SCR d'entité ne passe que de
  169,0 à 127,1 M€, soit −24,8 %, c'est-à-dire **0,81 fois la largeur de la bande d'identification
  déjà publiée**. Vérifié : `127,1`, `24,8` et `0,81` sont **bien imprimés dans le PDF**.
- **Le classement ne résiste pas.** Il bascule entre $a = 0{,}25$ et $a = 0{,}50$ : P4 passe devant
  P1. Vérifié : les valeurs `22,4` et `27,6` sont **absentes du PDF**, et l'expression « classement
  de remédiation » n'y figure nulle part.

La sortie du script conclut elle-même : « **Le NIVEAU résiste, le CLASSEMENT de remédiation non.** »

**Ce que le mémoire en dit.** Le chapitre 12 porte bien un avertissement qualitatif : les tests de
robustesse sont menés à matrice $W$ fixée, et ils établissent que « P1 arrive en tête **si l'on
admet cette direction** ». L'honnêteté est là. Mais le **seuil** ne l'est pas.

**Risque devant le jury.** C'est l'attaque n°2 de la Phase 3, la plus dangereuse du dossier. Telle
que le mémoire est écrit, la réponse disponible est qualitative. Or la réponse quantitative existe,
elle est calculée, et elle est plus solide qu'il n'y paraît :

> « Une dégradation de 25 % de l'émission de la gouvernance laisse le classement inchangé. Il faut
> dégrader de moitié pour que la priorité passe à la gestion des tiers. Et le niveau de capital,
> lui, ne bouge que de 0,81 fois la largeur de la bande d'ignorance que je publie déjà. »

C'est une réponse qui **désamorce** l'attaque au lieu de la subir, et elle ne demande aucun calcul
nouveau.

**Correction.** Publier la table de dégradation, ou au minimum la ligne $a = 0{,}50$, dans la
section de robustesse du chapitre 12, avec la phrase du script. **Coût : 1 h.** C'est la correction
au meilleur rendement de la Phase 4.

---

## 3. Reproductibilité

| Contrôle | Résultat | Statut |
|---|---|---|
| **Chemins absolus dans les scripts** | **0** sur 128 scripts | ✔ |
| Scripts fixant une graine | 82 sur 128 | ✔ |
| Sorties versionnées | 112 fichiers dans `sorties_verif/` | ✔ |
| Séparation données brutes / traitées | `data/raw/` gitignoré, `.gitkeep` conservé, `data/processed/` versionné | ✔ |
| README à la racine | présent | ✔ |
| Confidentialité | mémoire non confidentiel, rien de sensible poussé | ✔ |
| **Figures : provenance** | 43 référencées, **39 produites par script** | ✔ |
| Figures sans script | 4 : Avast WannaCry, cartographie France Assureurs, vecteurs CESIN, tailles de sinistres LUCY | ✔ **reproductions tierces, sourcées** |
| Droits d'usage des figures externes | autorisation étendue à toutes le 19 septembre ; 23 mentions de source dans les chapitres | ✔ |

**Zéro chemin absolu sur 128 scripts est un résultat remarquable**, et il répond directement à
l'exigence de traçabilité du § 4.4 du référentiel.

### Deux réserves mineures

**Le contrôle documenté des `??` dépend d'un paquet non déclaré.** La commande de contrôle du
projet utilise `fitz` (PyMuPDF), absent de `requirements.txt`. Un poste reconstruit depuis le dépôt
ne peut donc pas exécuter le contrôle documenté. Constaté en pratique : j'ai dû l'installer à la
main ce matin. *Correction : une ligne. Coût : 2 min.*

**Deux figures viennent d'en dehors du pipeline numéroté.** `mean_excess_oprisk.png` et
`diagnostic_gpd_oprisk.png` sont produites par `notebooks/01_oprisk_gpd_calibration.py`, hors de
`vasicek_lab/`, donc leur sortie n'est pas dans `sorties_verif/`. Ce sont précisément les deux
figures qui justifient le **choix du seuil POT** — celles qu'un juré regarde pour contester ξ.

**Ce n'est pas un trou de contrôle** : la couverture du chapitre 6 est de 93,9 %, et les 8 nombres
manquants sont dans la section des énoncés de théorèmes, déclarés hors script par motif. Les
nombres du seuil, eux, citent bien des scripts du pipeline. Mais les **figures** qui les illustrent
ne sont pas rejouées par le même mécanisme. *À mentionner si on te demande de régénérer la chaîne ;
sans effet sur le dépôt.*

---

## 4. Échantillon du rapprochement chiffre par chiffre

Le rapprochement exhaustif est fait par le harnais, sur 1 826 nombres. Extrait vérifiable à la main :

| Chiffre | Page | Valeur dans le texte | Source | Statut |
|---|---|---|---|---|
| Capital conforme | 5, 16, 116 | 6 049 M€ | scripts cités ch. 12 | ✔ confirmé, identique dans 6 zones |
| Capital non conforme | 5, 16, 116 | 20 188 M€ | idem | ✔ confirmé, 6 zones |
| Facteur | 5, 16, 116 | 3,34 | idem | ✔ confirmé, 6 zones |
| Indice de queue | 15 | 0,5954 | pipeline ch. 6 | ✔ confirmé |
| Seuil POT | 15 | 20,03 M€ | pipeline ch. 6 | ✔ confirmé |
| Bornes de capital | 16 | [6 858 ; 8 697] M€ | ch. 10 | ✔ confirmé, **mais 1 zone sur 6** |
| Largeur de bande | 16, 12x | 1 839 M€ | ch. 10 | ✔ confirmé, 3 zones sur 6 |
| SCR entité | 12x | 169,0 M€ | sortie 64 | ✔ confirmé |
| Dégradation totale de P1 | 12x | 127,1 M€, −24,8 % | sortie 64 | ✔ confirmé |
| **Bascule du classement** | — | **22,4 contre 27,6** | **sortie 64** | ✘ **calculé, non publié** |
| Valeur d'information | 147 | 28,9 % / 66 % | sorties 55 et 66 | ✔ confirmé, **0 zone de synthèse** |

---

## 5. Récapitulatif

| # | Action | Gravité | Coût |
|---|---|---|---|
| P4-3 | Publier la bascule du classement à $a = 0{,}50$ dans la robustesse du ch. 12 | **critique** | 1 h |
| P4-1 | Porter les bornes 6 858 – 8 697 dans le résumé et la conclusion | majeure | 45 min |
| P4-2 | Porter la valeur d'information dans le résumé et la conclusion | majeure | 30 min |
| — | Ajouter `pymupdf` à `requirements.txt` | mineure | 2 min |
| — | Rétablir l'écart 14 139 dans la conclusion | mineure | 5 min |

**Le dispositif de vérification est sain.** Aucune incohérence de chiffre n'a été trouvée entre les
zones, aucun chemin absolu, aucune figure non sourcée. Les cinq actions ci-dessus portent toutes sur
la **visibilité** de résultats déjà calculés et déjà corrects — comme en Phase 3. Le mémoire souffre
de sous-exposer ses meilleurs résultats, pas de les avoir mal produits.
