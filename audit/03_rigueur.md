# Phase 3 — Rigueur scientifique et actuarielle

Méthode : le modèle a été **reconstruit à partir des chapitres 5, 6, 7, 9, 10, 11, 12 et 13**, en
extrayant leurs sections, leurs énoncés formels et leurs encadrés. La description du prompt d'audit
n'a pas été utilisée, et elle est fausse sur plusieurs points (section 1).

**Portée de ce que j'ai lu.** J'ai lu la charpente argumentative de ces huit chapitres — titres,
définitions, propositions, théorèmes, encadrés de synthèse et d'avertissement — soit ce qui porte
les affirmations. Je n'ai pas relu ligne à ligne les 130 pages de corps, ni refait les calculs :
c'est la Phase 4 qui rapprochera les chiffres du code. Ce qui suit distingue donc **vérifié** (lu
dans le texte) de **supposé**.

---

## 1. Le modèle réel, et cinq écarts avec la description du prompt

| Ce que le prompt annonce | Ce que le mémoire fait | Vérifié |
|---|---|---|
| « agrégation par copule de Gumbel » | La copule n'est **pas** le mécanisme. Elle sert de **benchmark adverse** au chapitre 12, dont le verdict est : « La dépendance n'est pas le mécanisme : c'en est l'ombre. » La dépendance est produite par la cascade | ✔ |
| « modèle LDA en briques (remédiation, prestataire, sanction, aggravation) » | Les briques sont **quatre canaux** que la conformité déplace : nombre d'incidents, détection, propagation, accumulation par prestataire commun | ✔ |
| « variable latente de type Vasicek avec matrice de contagion » | Exact, mais en **deux couches et deux échelles de temps** : Vasicek multi-états rapide pour l'état de conformité, chaîne de Markov lente à séjours de type phase pour la remédiation, couplées par **un seul** facteur systémique Θ | ✔ |
| « si ξ > 1, la moyenne de la GPD est infinie » | ξ = 0,5954. La proposition qui donne quantile et moyenne de queue **pose explicitement ξ ∈ (0,1)**. Le texte écrit « la variance des pertes est infinie, leur espérance finie », ce qui est exact pour 1/2 < ξ < 1 | ✔ |
| « quantification du SCR » | Le mémoire **refuse ce mot** : « il n'existe aucun module DORA dans la Formule Standard ; la grandeur calculée est un besoin de capital ORSA, donc de pilier 2 » | ✔ |

**Le prompt sous-estime aussi le degré de formalisation.** Le chapitre 7 porte une définition, cinq
propositions et leur vérification numérique. Ce n'est pas un modèle posé puis illustré.

---

## 2. Audit étage par étage

| Étage | Point vérifié | Statut | Gravité | Correction | Coût |
|---|---|---|---|---|---|
| **Cadre** | SCR requalifié en besoin ORSA, absence de module DORA en FS énoncée deux fois | **OK** | — | — | — |
| **Cadre** | Articulation avec la Formule Standard traitée par l'agrégation réglementaire (« un euro économisé sur DORA vaut plus qu'un euro sur un risque qui se diversifie ») | **OK** | — | — | — |
| **Données** | Trois sources, rôles distincts et déclarés ; trois biais posés avant usage | **OK** | — | — | — |
| **Données** | Deux corrections de biais qui se compensent (0,861 × 1,147 = 0,987, effet net 1,3 %) | **OK**, résultat non prévisible et honnête | — | — | — |
| **Données** | Déduplication PRC : défaut trouvé en regardant la table des plus gros incidents | **OK** | — | — | — |
| **Données** | **Hackmageddon consulté puis non conservé**, déclaré comme citation non rejouable | **fragile** | majeure | Voir F11 | 1 h |
| **Données** | λ_ref = clé de répartition, périmètre américain, sans seuil de matérialité | **OK** mais exposé | mineure | Voir attaque n°8 | — |
| **Socle, fréquence** | Binomiale négative, surdispersion ; trois « fréquences » distinguées nommément | **OK** | — | — | — |
| **Socle, sévérité** | POT, seuil 20,03 M€ obtenu par règle de stabilité sur dix candidats, 91 excès, ξ = 0,5954 | **OK** | — | — | — |
| **Socle, sévérité** | Hill contre maximum de vraisemblance confrontés | **OK** | — | — | — |
| **Socle** | Quantiles de sévérité **jamais** comparés à un SCR, avertissement explicite | **OK** | — | — | — |
| **Socle** | Backtest à origine glissante ; **puissance chiffrée : 1 811 années** pour tester 99,5 % | **OK**, préempte l'attaque | — | — | — |
| **Socle** | **Dérive d'échelle de 4,00 %/an, mesurée et non corrigée** ; calibration stationnaire | **fragile assumé** | majeure | Voir attaque n°5 | — |
| **Cascade** | Convention d'indices W_jk encadrée et fixée une fois pour toutes | **OK** | — | — | — |
| **Cascade** | ρ(TRANS) = 1,461 > 1 détecté ; normalisation de Leontief donne ρ(W) ≤ g < 1, **stabilité garantie et non supposée** | **OK**, vérifié numériquement | — | — | — |
| **Cascade** | ρ(W) et R₀ = ρ(M) explicitement distingués | **OK** | — | — | — |
| **Cascade** | Loi exacte de l'ensemble atteint, monotonie stochastique, dépendance à l'ordre : démontrées | **OK** | — | — | — |
| **Cascade** | Non-transitivité **testée dans trois formulations et réfutée par l'auteur**, annoncée comme non revendiquée | **OK**, exemplaire | — | — | — |
| **Cascade** | ROOT et TRANS viennent **du même expert** ; la cohérence interne est déclarée comme telle, pas comme validation | **OK** sur la déclaration, **fragile** sur l'usage | **critique** | Voir F12 | — |
| **Multi-états** | Deux échelles de temps, seuils ordonnés, un seul Θ couple les deux couches | **OK** | — | — | — |
| **Multi-états** | Deux « Erlang » distincts explicitement démêlés | **OK** | — | — | — |
| **Multi-états** | **g_C < g_NC est la seule hypothèse restante**, qualitative, non calibrée | **fragile assumé** | **critique** | Voir F13 | — |
| **Identifiabilité** | Trois sources échouent pour trois raisons distinctes ; VERIS porte les champs et ne les renseigne qu'1 fois sur 10 591 | **OK**, le plus fort résultat du mémoire | — | — | — |
| **Identifiabilité** | Piège du « temps inversé » désamorcé (M_inv = Mᵀ par construction, corrélation −1 triviale) | **OK** | — | — | — |
| **Identifiabilité** | MOVEit : DiD brute significative **mais placebo la reproduit** ; conclusion retirée | **OK**, exemplaire | — | — | — |
| **Identifiabilité** | **Confondant du corpus non levé** : une enquête officielle est mandatée pour trouver une cause racine, donc sur-attribue à la gouvernance | **fragile** | **critique** | Voir F14 | — |
| **Identifiabilité** | Biais de narration mesuré et son coût en capital recalculé, pas seulement déclaré | **OK** | — | — | — |
| **Identifiabilité** | Bayésien conjugué : les quatre paires non documentées gardent un θ uniforme, l'identification partielle se reproduit d'elle-même | **OK**, élégant | — | — | — |
| **Ident. partielle** | Énumération des 1 024 sommets, **et vérification que les extrêmes y sont atteints** (l'argument usuel ne s'applique pas directement) | **OK**, piège évité | — | — | — |
| **Ident. partielle** | Niveau déclaré illustratif ; le résultat est le **rapport au socle**, la largeur de bande et le classement | **OK** | — | — | — |
| **Résultats** | Interaction super-additive établie « là où l'estimateur est fiable » | **OK** | — | — | — |
| **Résultats** | Shapley (vue source, P1 à 34 %) et Euler (vue réceptacle, presque uniforme) : deux lectures, et l'écart **est** le résultat | **OK** | — | — | — |
| **Résultats** | Ordre de remédiation **invariant aux taux de transition**, les paramètres les moins calibrables | **OK**, fort | — | — | — |
| **Résultats** | Copule en benchmark adverse : elle imite l'état, pas le surcoût ni l'interaction | **OK** | — | — | — |
| **Résultats** | Entité notionnelle à 19 231 M€ d'actifs **déclarée hors domaine de validité par le mémoire lui-même** | **OK** sur l'honnêteté, **coûteux** sur l'usage | majeure | Voir attaque n°4 | — |
| **Robustesse** | Moteur d'agrégation contrôlé par inversion de Fourier et trois chemins indépendants, avec la limite du contrôle déclarée | **OK** | — | — | — |
| **Robustesse** | VaR prédictive (centrale) et VaR robuste (prudente) toutes deux publiées, choix de posture argumenté | **OK** | — | — | — |
| **Robustesse** | Tests de sensibilité menés **à matrice W fixée**, périmètre explicitement déclaré | **OK** sur la déclaration | — | Voir F12 | — |

---

## 3. Les quatre fragilités à traiter

### F11 — Une source du chapitre de données n'est pas rejouable · **majeure**

**Où** : chapitre 5, section Hackmageddon.

**Constat, vérifié.** Le mémoire écrit lui-même : « Contrairement aux bases PRC et OpRisk,
versionnées dans le dépôt et rejouables par script, le jeu Hackmageddon a été consulté puis non
conservé. Les 1 041 incidents et les 840 à vecteur renseigné sont une citation, non un résultat du
dispositif. »

**Risque devant le jury.** Le § 4.4 du référentiel insiste sur la **traçabilité** des données et
demande « un avis circonstancié concernant les éventuelles conséquences de qualité des données sur
les résultats ». Le mémoire est irréprochable sur la déclaration, mais un juré peut demander :
qu'est-ce qui dépend de cette source, et que devient le résultat si elle est fausse ?

**Correction.** Une phrase suffit, et le matériau existe : Hackmageddon ne sert qu'à la
**structure par vecteur d'attaque**, jamais au niveau ; et le chapitre 5 établit par ailleurs, par
trois instruments indépendants (V de Cramér < 0,20, ε² < 0,08, rangs < 0,16), que la catégorie
d'un incident **n'est pas une variable de segmentation**. Autrement dit, la source la moins
traçable est aussi celle dont le modèle dépend le moins. **Le dire explicitement.** *Coût : 1 h.*

### F12 — Le chiffre de tête repose sur la matrice d'un seul expert, que le mémoire déclare ne pas savoir identifier · **critique**

**Où** : chapitre 12 (chiffre de tête), chapitre 7 (ROOT/TRANS), chapitre 9 (non-identifiabilité).

**Constat, vérifié.** Trois affirmations du mémoire, prises ensemble, créent une tension que le
jury verra :

1. Chapitre 9 : « la direction de la contagion n'est pas identifiable sur les données publiques
   agrégées ».
2. Chapitre 7 : « ROOT et TRANS sont issus du jugement du **même expert** ; retrouver ROOT à partir
   de TRANS n'est pas une validation externe mais un test de cohérence interne ».
3. Chapitre 12 : le chiffre publié, 6 049 → 20 188 M€, facteur 3,34, et les tests de robustesse
   sont menés « **à matrice W fixée, celle du classeur qualitatif** ».

Le mémoire déclare chacun de ces trois points. Mais l'abstract s'ouvre sur le facteur 3,34, tandis
que la thèse centrale est qu'on ne connaît pas la direction.

**Ce n'est pas une incohérence** — les deux chapitres mesurent des objets différents, et le
chapitre 12 porte une section de réconciliation explicite entre son SCR conforme de 5 900 M€ et le
socle de 5 275 M€ du chapitre 10. Mais l'articulation n'est pas assez visible en tête.

**Risque devant le jury.** « Vous dites ne pas connaître la direction, et vous publiez un facteur
3,34 calculé sur une direction. Laquelle est votre réponse ? » C'est la question qui sera posée.

**Correction.** Ajouter, dans le résumé et en ouverture du chapitre 12, **une phrase qui hiérarchise
les deux chiffres** : le facteur 3,34 mesure l'effet des quatre canaux **à direction fixée**, la
bande 6 858–8 697 M€ mesure ce que l'ignorance de la direction coûte, et les deux répondent à des
questions différentes. Le matériau est déjà écrit au chapitre 10 ; il manque en tête.
*Coût : 1 h 30.* **C'est la correction au meilleur rendement de toute la Phase 3.**

### F13 — L'hypothèse porteuse, g_C < g_NC, n'est adossée qu'au règlement · **critique, mais probablement irréductible**

**Où** : chapitre 11, encadré « Ce qui reste une hypothèse, et c'est tout ce qui reste ».

**Constat, vérifié.** Toute la mécanique du surcoût repose sur : se conformer à DORA réduit la
propagation entre piliers. Le mémoire la qualifie lui-même d'« affirmation qualitative,
discutable », et s'appuie sur le fait que « le règlement lui-même prend parti » puisqu'il impose
ces exigences.

Le mémoire se protège de deux façons, et elles sont bonnes : le capital est **croissant** en ce
paramètre (proposition de monotonie stochastique, démontrée), donc toute correspondance qui
respecte l'**ordre** reproduit l'écart ; et la sensibilité est « bornée par construction et non
estimée ».

**Risque devant le jury.** Un juré peut objecter que le règlement énonce une intention, pas une
mesure, et qu'aucune donnée du mémoire n'établit que la conformité réduit la propagation.

**Correction.** Aucune, avec les données disponibles — et c'est défendable. Ce qu'il faut, c'est
**préparer la réponse** : le mémoire ne prétend pas mesurer cet effet, il en exhibe la conséquence
en capital sous l'hypothèse d'ordre, et il chiffre ce que l'hypothèse porte. C'est exactement la
posture que le § 4.6 du référentiel valorise. *Coût : préparation orale, pas d'écriture.*

### F14 — Le confondant du corpus documentaire pointe vers le pilier classé premier · **critique**

**Où** : chapitre 9, encadré « Le confondant, qu'aucun de ces chiffres ne lève ».

**Constat, vérifié.** Le mémoire écrit : « Le placebo teste la cohérence du codage, non
l'exogénéité de la direction. Or une enquête officielle est **mandatée** pour établir une cause
racine et des responsabilités, et conclut très souvent à une [défaillance de gouvernance]. »

Or le résultat de classement du mémoire est que **P1, la gouvernance, arrive en tête** (34 % du
surcoût en vue Shapley).

**Risque devant le jury.** C'est l'attaque la plus dangereuse du dossier, parce qu'elle est
construite à partir des propres aveux du mémoire : « votre corpus sur-attribue à la gouvernance par
construction, et votre conclusion est que la gouvernance domine. »

**Ce qui existe déjà en défense**, et il faut le savoir : le biais de narration **est mesuré**, et
son coût en capital est recalculé en dégradant l'émission de P1 (W_1k → (1−a)·W_1k) avec
recalcul de la bande pour chaque degré. Le mémoire ne se contente donc pas de déclarer le biais.

**Correction.** Vérifier en Phase 4 **jusqu'à quel degré de dégradation a le classement tient**, et
faire remonter ce nombre en tête du chapitre 12. Si P1 reste premier jusqu'à une dégradation
substantielle, c'est la réponse à l'attaque, et elle est déjà calculée. *Coût : 1 h si le chiffre
existe dans les sorties, une demi-journée sinon.*

---

## 4. Les dix attaques les plus probables, et l'état de la défense

| # | Attaque | Défense actuelle | État |
|---|---|---|---|
| 1 | « Vous ne connaissez pas la direction mais vous publiez un facteur 3,34. Quel est votre chiffre ? » | Existe (ch. 10 et réconciliation ch. 12) mais **pas assez visible en tête** | ⚠ F12 |
| 2 | « Votre corpus sur-attribue à la gouvernance, et vous concluez que la gouvernance domine » | Biais de narration mesuré et son coût recalculé | ⚠ F14 |
| 3 | « Rien ne prouve que la conformité réduit la propagation » | Monotonie démontrée, seul l'ordre est utilisé, sensibilité bornée par construction | ✔ à réciter |
| 4 | « Que vaut votre modèle pour mon entité ? » | Le mémoire **déclare lui-même** l'entité notionnelle hors domaine de validité | ✔ honnête, mais sans réponse chiffrée |
| 5 | « Votre backtest rejette le niveau » | Défaut nommé, chiffré (4,00 %/an), et non caché ; la fréquence et la forme passent | ✔ |
| 6 | « On ne peut pas valider un quantile à 99,5 % » | 1 811 années chiffrées, dans le texte | ✔ préempté |
| 7 | « Pourquoi pas une copule ? » | Benchmark adverse mené : la copule imite l'état, pas le surcoût ni l'interaction | ✔ fort |
| 8 | « Votre fréquence vient d'une base américaine sans seuil de matérialité » | λ_ref déclaré clé de répartition, pas niveau | ✔ à réciter |
| 9 | « Hackmageddon n'est pas rejouable » | Déclaré, mais le lien avec sa faible influence n'est pas fait | ⚠ F11 |
| 10 | « ξ = 0,595 : votre variance est infinie » | Énoncé exactement, condition ξ ∈ (0,1) posée dans la proposition | ✔ |

**Deux attaques que le mémoire a déjà désamorcées, et qu'il faut savoir raconter** : la
non-transitivité réfutée par l'auteur lui-même, et la DiD MOVEit retirée parce que le placebo la
reproduisait. Ce sont des arguments de crédibilité, pas des aveux.

---

## 5. « Quel est donc votre SCR ? » — la réponse à tenir

Le prompt a raison : cette question sera posée. Voici la réponse que le mémoire autorise, en trois
temps, chacun appuyé sur une page.

1. **« Le niveau n'est pas une mesure, et le mémoire le démontre. »** En ne faisant varier que la
   source de sévérité, le niveau bouge d'un facteur 22 ; d'un facteur 41 en y ajoutant l'échelle de
   fréquence. Publier un point serait publier un artefact de source.

2. **« Ce que le modèle détermine, et qui résiste, ce sont trois grandeurs. »** Le rapport du
   capital au socle ; la largeur de la bande d'ignorance directionnelle ; et le classement des
   piliers. Les trois sont stables quand le niveau ne l'est pas.

3. **« Et la question que vous posez a une réponse chiffrée, mais ce n'est pas un nombre : c'est
   un intervalle et son prix. »** Sur l'ensemble admissible, le capital se situe entre 6 858 et
   8 697 M€ ; la largeur, 1 839 M€, **est le coût de l'ignorance de la direction, connu d'avance**.
   Et ce coût se réduit : documenter la seule dépendance gouvernance-incidents en lèverait 28,9 %.

C'est la réponse d'un travail d'identification partielle, et le § 4.6 du référentiel la protège
explicitement : « Ce n'est pas un échec que de ne pas aboutir à des résultats pour peu que
l'étudiant fasse preuve d'esprit critique. »

---

## 6. Récapitulatif

| # | Action | Gravité | Coût |
|---|---|---|---|
| F12 | Hiérarchiser en tête le facteur 3,34 et la bande 6 858–8 697 | critique | 1 h 30 |
| F14 | Faire remonter le degré de dégradation jusqu'auquel le classement tient | critique | 1 h à 4 h |
| F11 | Relier Hackmageddon à sa faible influence sur le modèle | majeure | 1 h |
| F13 | Préparer la réponse orale sur g_C < g_NC | critique | oral |

**Aucun défaut de construction n'a été trouvé.** Les quatre points ci-dessus sont des défauts
d'**exposition** ou des limites que le mémoire déclare déjà : ce qui manque est leur mise en avant,
pas leur traitement. C'est une situation rare et il faut en tirer parti plutôt que de réécrire.
