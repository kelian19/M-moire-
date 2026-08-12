# Mémoire SCR DORA — contexte de reprise

Document de passation. À lire en entier avant de toucher quoi que ce soit.

## Le projet

Mémoire d'actuariat de Kélian Kaddouri (ENSAE / Nexialog Consulting) :
**« Quantification du SCR lié à la non-conformité au règlement DORA — une cascade dirigée entre
les cinq piliers »**. Objectif affiché : le Prix SCOR, donc le top 1-3 national, pas la simple
validation. Tuteur : Hugo. Point d'avancement hebdomadaire.

État au 12 août 2026 : **corps de 104 pages, annexes à partir de la 105, 127 pages au total**,
branche `exploratory`.

**Le compte de pages ne se lit pas avec `mdls`**, dont l'index Spotlight se périme sans
prévenir : il a annoncé 121 pages sur un PDF qui en faisait 123, y compris sur un fichier
déjà commité. Compter en décompressant les flux d'objets, ou lire `main.toc` après une
compilation avec `--keep-intermediates`. Le harnais est à **97,5 % de confirmation sur 1 398
nombres, pour une couverture de 100 %**.

**Et vérifier dans quelle partie tombe un ajout avant de conclure qu'il grossit le corps.** Le
chapitre `12b_adaptations_pilier.tex` est l'**annexe C**, pas un chapitre du corps : la page
gagnée le 12 août y est allée, le corps restant à 104. Le nom du fichier ne dit pas la partie.

**Le corps a gagné trois pages les 9 et 10 août** (101 → 104), au titre de la table des
postures, des deux limites déclarées du chapitre 13 et du cadrage de la CTE. L'arbitrage de
format reste ouvert et ces ajouts vont contre lui : à trancher par Kélian, pas par l'assistant,
puisque ce qui a été ajouté est exactement ce qui fait la valeur du mémoire selon la note
d'honnêteté en bas de ce fichier.

**Lire les deux chiffres ensemble, jamais l'un sans l'autre.** Le mémoire a commencé la
journée à 99,6 % sur 904 nombres, mais ces 904 ne représentaient que **74,7 %** des nombres
publiés : 332 vivaient dans des sections qui ne citaient aucun script, donc sans être ni
confirmés ni infirmés. Un taux de confirmation se règle en retirant une citation ; la
couverture, non. Les cinq chiffres périmés trouvés cette semaine venaient tous de la zone
non couverte ou d'une exemption silencieuse, **jamais d'un non confirmé**. Le contrôle de
fin de tâche est donc désormais **couverture = 100 % et confirmation ≥ 97 %**, dans cet
ordre.

Le harnais était à 96,1 % sur 915 nombres la veille. Les 36 non confirmés ont été dépouillés
un par un : aucun chiffre faux. Sept n'étaient pas des nombres du mémoire mais des artefacts de
lecture (`\tfrac12` lu comme 12, `p{4.3cm}` lu comme 4,3), corrigés dans le harnais ; six
rapports dérivés et les parts d'amorce sont désormais imprimés par les scripts 20 et 67 ;
quatre écarts d'unité ou de séparateur sont corrigés dans les scripts 36, 44, 48 et 60 ; trois
valeurs étaient imprimées par un script que leur section ne citait pas.

La tolérance a ensuite été resserrée, ce qui a sorti 35 nombres de plus, puis tout a été
traité. **Trois erreurs réelles**, toutes corrigées : l'intervalle de $\xi$ écrit
`[0,31 ; 0,83]` alors que la borne basse 0,3044 s'arrondit à 0,30, aux chapitres 05 et 06 ;
l'estimateur de Hill publié à 1,42 avec un écart de 138,7 % au MLE, qu'aucune population du
pipeline ne reproduit (la fonction `hill_estimator` du projet donne **1,32** et **+120,8 %**
sur la population calibrée) ; et le seuil d'inefficacité $\kappa^\star$, publié à 76 % sur un
taux marginal de prime de 0,0116 calculé à la main, alors que le script 58 l'imprime
désormais à **0,0103**, soit $\kappa^\star = 78\,\%$.

Cinq nouveaux artefacts de lecture ont aussi été corrigés dans le harnais : le `±` des
sorties lu comme un signe négatif, le renvoi de section `§5.5` lu comme un nombre, le moins
d'une soustraction lu comme un signe, le tiret demi-cadratin des plages d'années, et les
virgules décimales françaises dans les sorties des scripts 40, 53, 59 et 67.

## Où sont les choses

| Quoi | Où |
|---|---|
| **Mémoire vivant** | `exploratory/memoire_cascade/main.tex` |
| Version abandonnée, pré-cascade | `memoire/main.tex` — **ne jamais y toucher** |
| Chapitres | `exploratory/memoire_cascade/chapitres/*.tex` |
| Harnais de vérification | `exploratory/memoire_cascade/verif_chiffres.py` |
| Scripts de calcul | `exploratory/vasicek_lab/<N>_<theme>/<num>_<nom>.py` |
| Modules partagés | `exploratory/vasicek_lab/*.py` (racine) |
| Figures | `exploratory/vasicek_lab/figures/*.png` |
| Sorties de scripts versionnées | `sorties_verif/NN.txt` + son `README.md` |
| Decks tuteur | `exploratory/slides/AAAA-MM-JJ_point_tuteur.tex` |
| Deck tutrice de stage | `exploratory/slides/2026-08-10_point_caroline.tex` |
| Aide-mémoire de call | `exploratory/slides/aide_memoire_call_AAAA-MM-JJ.tex` |
| Données brutes | `data/raw/` — **gitignoré, sous licence, ne jamais committer** |

Le dossier `exploratory/memoire_cascade/a_integrer/` est **mort** : aucun `\input` ne le
lit, et son `STATUT.md` le dit. Ne pas y puiser.

## Comment construire

Le projet se construit sur les deux machines. Les commandes diffèrent, les résultats non :
la parité a été vérifiée le 6 août 2026 (voir plus bas).

**Sur le PC (Windows, PowerShell)**

```powershell
# Python
$py = "C:\Users\KélianKADDOURI\Projects\M-moire-\.venv\Scripts\python.exe"

# LaTeX (tectonic, pas dans le PATH)
$tec = "C:\Users\KélianKADDOURI\Projects\M-moire-\memoire\tectonic.exe"
cd exploratory\memoire_cascade
& $tec -X compile main.tex --keep-intermediates
# NB : --synctex=none n'existe pas sur cette version. Pas de main.log : tout va sur stdout.

# Harnais, tous les chapitres
cd exploratory\memoire_cascade
powershell -ExecutionPolicy Bypass -File verif_tous_chapitres.ps1

# Harnais, un chapitre avec le détail des non confirmés
& $py verif_chiffres.py ..\..\sorties_verif chapitres\12_resultats.tex
```

**Sur le Mac (macOS, zsh ou bash)**

```bash
# Python, depuis la racine du dépôt
.venv/bin/python exploratory/vasicek_lab/5_etats/66_invariance_ordre_conformite.py

# LaTeX (le binaire tectonic macOS est dans memoire/, sans extension, non versionné)
cd exploratory/memoire_cascade
../../memoire/tectonic -X compile main.tex --keep-intermediates

# Harnais, tous les chapitres
bash exploratory/memoire_cascade/verif_tous_chapitres.sh

# Harnais, un chapitre avec le détail des non confirmés
.venv/bin/python exploratory/memoire_cascade/verif_chiffres.py \
    sorties_verif exploratory/memoire_cascade/chapitres/12_resultats.tex
```

Si le `.venv` du Mac est absent, le reconstruire depuis la racine :

```bash
/Users/larbi/miniconda3/bin/python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install 'matplotlib==3.11.0'   # voir la note figures ci-dessous
```

Après compilation, **supprimer** `main.aux`, `main.bbl`, `main.out`, `main.toc` : ils ne sont
pas versionnés. `main.pdf`, lui, **l'est** : une compilation de simple vérification le salit
sans qu'aucune source ait changé, il faut alors le restaurer par `git checkout`.

**Parité des deux machines, vérifiée le 6 août 2026.** Sur Python 3.13.5, numpy 2.5.1,
pandas 3.0.5, scipy 1.18.0, le script 66 reproduit `sorties_verif/66.txt` à l'identique,
seul le chemin absolu de la figure diffère. Le harnais complet, lancé **avant** les corrections
de la journée, redonnait exactement le chiffre du PC : 915 nombres, 879 confirmés, 96,1 %.
C'est ce qui atteste la parité ; les corrections du jour et le resserrage de la tolérance
sont venus après, et ne viennent pas de la
machine. Le mémoire compile sans erreur, 0 référence indéfinie, 0 annotation hors page,
0 Overfull \vbox, 0 `/Rotate`. Les scripts 20, 36, 44, 46, 48, 60, 66 et 67 ont été relancés
sur le Mac et reproduisent leur sortie versionnée ligne pour ligne, au chemin absolu près.

**Deux points propres au Mac :**

- **Épingler matplotlib à 3.11.0**, la version du PC. Le numéro de version est écrit dans les
  métadonnées du PNG : en 3.11.1 les pixels sont rigoureusement identiques mais le fichier
  diffère de cinq octets, et `git status` signale alors comme modifiée une figure qui ne l'est
  pas. Avec 3.11.0, une figure rejouée est identique à l'octet.
- **Une figure en `bbox_inches="tight"` ne se régénère pas à l'octet d'une machine à l'autre.**
  Le recadrage dépend des métriques de police, qui diffèrent entre freetype Windows et macOS :
  `S15_allocation_shapley_euler.png` passe de 1057x2653 à 1059x2659 pixels pour un contenu
  identique. Les figures sans recadrage serré, elles, sont identiques à l'octet. Donc une
  figure qui apparaît modifiée après une simple relance n'est pas forcément une régression :
  comparer les dimensions et regarder l'image avant de conclure, et restaurer par
  `git checkout` si seul le cadrage a bougé.
- **Rediriger stderr séparément** quand on régénère un `sorties_verif/NN.txt`. matplotlib
  émet sur stderr des `findfont: Font family 'Segoe UI' not found.` qui s'intercalent au milieu
  d'une ligne de résultats et corrompent le fichier. Ces avertissements sont sans effet sur le
  tracé : la famille effective est `DejaVu Sans`, que matplotlib fournit lui-même et qui est
  placée en premier dans les 73 scripts concernés, sans exception ; `Segoe UI` n'est qu'un repli
  jamais atteint. Donc `> NN.txt 2>/dev/null`, jamais `> NN.txt 2>&1`.

## Contraintes de Kélian, à respecter littéralement

- **Step by step.** Ne pas élargir le périmètre au-delà de ce qui est demandé.
- **Un deck égale une semaine de travail.** Un deck figé ne se recharge JAMAIS avec du travail
  nouveau : le nouveau va dans le deck suivant. Exception : corriger une valeur qu'on sait
  fausse.
- **Aucune figure déjà utilisée dans un deck précédent** ne peut resservir dans un nouveau.
  Vérifier avec un grep sur `exploratory/slides/*.tex`.
- **Pas de tirets cadratins, pas de tournures qui trahissent l'IA** dans les livrables.
- **Écrire les formules en texte brut dans le chat** : le LaTeX math ne s'affiche pas chez lui.
- **L'élicitation est encore attendue.** Ne pas réécrire les passages qui la mentionnent comme
  si elle était abandonnée.
- **Hackmageddon n'est PAS rejetée**, et c'est un piège de lecture. Elle est utilisée : elle
  porte la *structure* du risque (les parts par vecteur d'attaque qui décomposent λ_ref) et
  jamais son niveau. Ce qui est tranché, c'est son **statut de preuve** : le jeu a été consulté
  puis non conservé, donc les 1 041 incidents et les 840 à vecteur identifié ne sont
  reproductibles par aucun script. Kélian a choisi d'assumer la citation datée plutôt que de
  versionner la source. Le mémoire le dit dans un encadré, le script 63 l'imprime sous
  l'étiquette « citation externe, non recalculable ». Ne pas rouvrir ce choix, et surtout **ne
  pas retirer la source** : elle est utilisée aux chapitres 5 et 6.

## Conventions du modèle, à ne pas confondre

- `W_jk` va de la **source j** vers la **cible k**. La ligne émet, la colonne reçoit. Les
  scripts 59 et 64 vérifient cette convention avant de calculer.
- `W(g) = g · TRANS / max_j(s_j)` où **`s_j` est l'ÉMISSION du pilier j**, donc le diviseur
  est 2,60 et non 2,3. Rayon spectral 0,506, sous-critique, `R_0 = 0,054`. La règle qui
  tranche : la normalisation garantit que le pilier le plus prolifique engendre au plus `g`
  descendants directs, et avec le diviseur de réception il en engendrait 1,02 pour `g = 0,9`.
  Le script 03 divisait par la réception jusqu'au 7 août ; il est aligné, et son en-tête,
  ses impressions et sa figure K3 avec lui. **Ne pas rouvrir ce point.**
- Décomposition `W = S + A` : la donnée identifie S (co-occurrence), pas A (direction). D'où
  l'identification partielle, énumération exhaustive des 2^10 = 1024 sommets.
- **La grandeur calculée n'est PAS un SCR réglementaire.** Il n'existe aucun module DORA en
  Formule Standard. On écrit « besoin de capital ORSA au titre de DORA », jamais « le SCR DORA
  de telle entité ». Le rapport au SCR publié est une **mise à l'échelle, pas une part**.
- **Les entités réelles sont anonymisées dans le mémoire** (assureur non-vie A/B, assureur vie
  C/D). Noms, sources SFCR et provenance de chaque champ : uniquement dans le script 65, qui
  imprime la table de correspondance. Raison : le modèle n'utilise que le bilan, jamais
  l'identité, et l'état de conformité est supposé.
- **Le 169 M€ est une borne supérieure d'ordre de grandeur, pas une mesure.** L'entité
  notionnelle tombe sous la borne inférieure de validité de la descente d'échelle (script 65).
- **Les trois valeurs de g (0,45 / 0,68 / 0,90) sont posées, non calibrées.** La thèse n'en
  dépend pas : le capital est croissant en g (lemme vérifié, script 66), donc toute
  correspondance respectant l'**ordre** produit l'écart, quand le forfait reste plat. Seule
  l'amplitude est un scénario.
- **`\VaR` et `\TVaR` sont réservées à la charge annuelle AGRÉGÉE, `\qsev` et `\qbarsev` à la
  sévérité d'un sinistre.** Ce n'est pas une coquetterie : le niveau 99,5 % n'a de sens
  réglementaire que sur un horizon annuel, et une perte isolée n'en porte aucun. Le 663 M€ est un
  quantile de sévérité, **pas un SCR**, et le confondre avec les 8 123 M€ du secteur fait lire une
  différence d'échelle comme une contradiction. C'est arrivé en séance le 7 août. Le pont entre
  les deux est imprimé par le script 67, section 1bis.
- **Les quatre canaux que la conformité déplace, et ils ne s'additionnent pas.** La
  non-conformité n'ajoute aucune pénalité au SCR : elle déplace quatre paramètres de la loi de
  perte, $\lambda$ de 21,6 à 53,6, $p_u$ de 0,128 à 0,181, $g$ de 0,45 à 0,90, $\varphi_{cs}$ de
  0 à 0,68. Les canaux isolés somment à 9 138 M€ quand l'écart total vaut 14 139 :
  **+5 001 M€ d'interaction, soit +35 %**, la cascade étant super-additive. Deux canaux sont
  calibrables (fréquence, détection), deux sont bornés (propagation, accumulation) : ne pas
  promettre une remédiation là où l'on n'a qu'une borne, et **ne jamais additionner les quatre
  leviers** pour chiffrer une remédiation partielle.

## Les scripts qu'il faut connaître

| N° | Rôle |
|---|---|
| 07, 08b | calibration sévérité et fréquence, dispersion de Pearson |
| 47, 57 | validation d'adéquation, biais de taille et de troncature |
| 53, 59 | corpus de post-mortems, direction de W, matrice ordonnée p_jk |
| 54 | fiabilité inter-juges — **attend un second codage, ne fabrique rien sans** |
| 60 | descente d'échelle secteur vers entité, seul dépositaire de λ et du multiplicateur |
| 62, 63 | comptages du chapitre données, calibration figée rendue citable |
| 64 | biais de narration : loi nulle exacte, jackknife, point de rupture |
| 65 | besoin ORSA sur quatre bilans SFCR réels, borne inférieure de validité |
| 66 | invariance de la thèse aux valeurs de g |
| 46, 51 | VaR prédictive et échelle des six postures — **51 est le dépositaire du bruit de simulation de chaque posture** ; 46 recalcule la prédictive à `B = 2000`, 51 à `B = 3000`, d'où deux valeurs du même nombre |
| 43 | KPI DORA en leviers de capital : les quatre canaux, leur attribution, l'interaction, le facteur 3,34 entre états |
| 68 | la table COMPLÈTE des quatre canaux : seize configurations, trois lectures d'un canal (isolé, fermeture, Shapley), décomposition de Möbius par ordre, six croisés de paires avec leur bruit. **C'est lui qui décompose le résidu de +5 001 M€ du script 43**, et les deux partagent `canaux_conformite.py` |
| 50 | ROI de la conformité : portage, sinistralité évitée, sens de la borne, et l'écart entre 6 % et 4,75 % |
| 08h | le rejet du Hawkes contre les variantes de Bessy-Roland/Boumezoued/Hillairet — **exige `Data_Breach_Chronology.xlsx`, absent du Mac, et sa sortie n'est pas versionnée** |
| 67 | grandeurs citées et jamais imprimées (formes fermées, rapports dérivés) et, section 1bis, **le pont entre quantile unitaire et capital agrégé** |

Modules partagés : `partial_id.py` (identification partielle et évaluateur à nombres communs),
`descente.py` (panel OpRisk et élasticités, lu par 60 et 65), `postmortem_corpus.py` (lu par 59
et 64), `canaux_conformite.py` (moteur des quatre canaux, lu par 43, 50 et 68 : **le modifier
déplace les 14 139 M€**), `scr_engine.py`, `euro_cascade_model.py`.

Règle : **tout rapport cité dans le mémoire doit être imprimé par un script.** Un ratio calculé
pendant la rédaction n'est vérifiable par personne. Trois des chiffres périmés trouvés cette
semaine étaient de cette nature.

## Le harnais, et ce qu'il ne fait pas

Il cherche chaque nombre publié dans une section du mémoire parmi les sorties des scripts que
cette section cite en `\texttt{NN}`. Tolérance d'arrondi : `max(0,6 % ; demi-unité du dernier
chiffre écrit)`.

Il rend trois lignes, et pas une : **vérifiés, exemptés par motif, non confirmés**. Une
exemption n'est jamais silencieuse, sinon le taux se mesure lui-même. Et une exemption se
juge sur le **contexte**, jamais sur la valeur : c'est en indexant sur la valeur que le
facteur 2,5 est passé entre les mailles pendant des semaines.

**Une section sans script cité est hors contrôle.** C'est la faille structurelle du dispositif,
et elle est plus dangereuse qu'un non confirmé, parce qu'elle ne se voit pas dans le taux. Le
harnais les liste sous « Sections SANS script cité » : cette liste est à relire, pas à
parcourir. La table des paramètres de l'annexe y a dormi jusqu'au 6 août.

Il **ne vérifie pas** qu'un nombre est au bon endroit ni qu'il veut dire ce que la phrase
prétend. Un nombre confirmé peut être mal commenté.

Le résidu se répartit en quatre classes, une seule est un défaut :

1. **séparateur de milliers** — corrigé dans le harnais ;
2. **unité** — le mémoire cite en pourcentage ce que le script imprime en fraction ;
3. **valeur légitimement hors script** — seuil statistique posé, point de lecture sur un
   graphique, exposant ;
4. **grandeur citée mais jamais imprimée** — la seule fautive, objet du script 67.

**La classification automatique du résidu ne fonctionne pas** : les correspondances trouvées à
un facteur 100 près sur des nombres ronds sont fortuites, un pool de plusieurs milliers de
valeurs en produit toujours une. Les nombres restants se lisent un par un.

**Le harnais tourne aussi sur un fichier de slides**, et il faut s'en servir. Il prend n'importe
quel chemin `.tex` en second argument :

```bash
.venv/bin/python exploratory/memoire_cascade/verif_chiffres.py \
    sorties_verif exploratory/slides/2026-08-14_point_tuteur.tex
```

Le deck du 14 août était à **35 % de couverture** quand on l'y a passé la première fois, avec
douze non confirmés : il ne citait que deux scripts. C'est la même faille que pour les chapitres,
et elle avait laissé passer dans ce fichier le $\kappa^\star$ à 76 % et un compte de pages
périmé. Les decks se rattachent donc à leurs scripts par une ligne « Sources : scripts… » en bas
de slide, discrète, et les slides de métadonnées (état du document, comptes de pages) se
déclarent par `% HARNAIS-HORS-SECTION:`. **Un deck sans `\section*` est vu comme un seul bloc**,
donc une déclaration posée en tête avale tout le fichier : découper avant de déclarer.

**N'essayez pas de faire détecter au harnais les contradictions entre scripts.** L'idée paraît
bonne et elle a été instruite le 10 août : elle ne tient pas. Le cas qui l'avait suggérée, la
VaR prédictive à 648 dans un script et 645 dans un autre, **n'est pas un angle mort** — la
tolérance d'arrondi (3,89 sur 648) dépasse l'écart (3), donc les deux valeurs se confirment
mutuellement et le harnais fait exactement ce qu'il annonce. Un détecteur de quasi-collision sur
les valeurs retomberait dans le travers déjà documenté juste au-dessus. Ce qui remplace ce
contrôle est une **convention**, et elle est plus efficace : toute grandeur simulée se publie
avec son bruit. Un lecteur qui voit ± 7 ne pose plus la question du troisième chiffre.

## Pièges qui ont déjà coûté du temps

- **`.Replace()` PowerShell avec `\n` échoue sur des fichiers CRLF.** Utiliser
  `[regex]::Replace` avec `\r?\n`, ou l'outil Edit. A mordu quatre fois.
- **Vérifier le diff de suppression après toute édition scriptée** :
  `git diff -U0 | Select-String '^-[^-]'`. Un script d'insertion a déjà écrasé six lignes de
  texte au lieu de les préfixer.
- **Les légendes opaques masquent les données.** Toute légende posée par lot doit être relue
  figure par figure : la place libre n'est pas au même endroit d'un panneau à l'autre.
- **Une figure portrait ne se dimensionne qu'en HAUTEUR sur une slide 4:3.** Posée en largeur,
  elle fait déborder son cadre (jusqu'à 7 cm constatés). `height=0.80\textheight`, et elle a sa
  propre slide.
- **`\figover` ne contraint pas la hauteur.** Une figure portrait dans le mémoire prend
  `\figcle` (page entière), jamais `\figover`.
- **Les PDF de `exploratory/slides/` peuvent être périmés** par rapport à `build/`. Recopier
  après compilation.
- **Un job d'arrière-plan peut écraser une figure après un commit.** Comparer les horodatages.
- **`tabular` ne peut pas se couper entre deux pages** : hyperref émet alors des annotations à
  coordonnées négatives (« Annotation out of page boundary »). Utiliser `longtable`.
- **Les nombres ronds d'un pool de plusieurs milliers se confirment mutuellement par hasard.**
  Ne jamais conclure d'une correspondance numérique seule.

## Contrôles à passer avant de dire que c'est fini

```
0 référence indéfinie · 0 « Annotation out of page boundary » · 0 Overfull \vbox
0 page tournée (/Rotate absent) · git status propre
COUVERTURE = 100 % (aucun nombre hors contrôle non déclaré) · confirmation ≥ 97 %
```

La couverture passe **avant** le taux, et dans cet ordre. Un taux de confirmation se règle en
retirant une citation ; la couverture, non. Le harnais imprime les deux, et distingue trois
états : sous contrôle, déclaré hors script (`% HARNAIS-HORS-SCRIPT:` ou `% HARNAIS-HORS-SECTION:`
dans le chapitre, avec son motif), hors contrôle. **Seul le dernier doit valoir zéro.**

Et, pour toute figure modifiée : **l'ouvrir et la regarder**. L'outil Read affiche les PNG. Le
contrôle des proportions ne remplace pas la lecture : quatre défauts de lisibilité réels ont
été trouvés cette semaine sur des figures dont le ratio était correct. Un cinquième le 10 août,
sur la figure J7 : l'étiquette « prédictive 645 » était coupée par la ligne du point à 657, les
deux lignes n'étant qu'à 12 M€ l'une de l'autre. Renvoyée à gauche (`ha="right"`).

**Et, pour tout deck : passer le harnais dessus aussi.** Voir la section sur le harnais.

## Ce qui a été tranché le 10 août 2026

Cette section est le compte rendu d'une journée dont le fil est parti d'une **confusion
d'échelles** au call du 7 août, et qui a fini par toucher le vocabulaire du mémoire, deux
limites déclarées et trois valeurs périmées.

### 1. Le quantile unitaire et le capital agrégé sont deux objets, et le mémoire les confondait

Le call du 7 août a buté là-dessus : le 663 M€ présenté comme une « VaR 99,5 % » est un
**quantile de sévérité d'un sinistre**, alors que le SCR est le quantile de la **charge annuelle
agrégée**. Un lecteur voit « VaR 99,5 % = 663 » à quelques pages de « SCR = 8 123 » et conclut à
une incohérence. C'est ce qui s'est passé en séance, et un jury le referait.

**Convention, désormais appliquée partout.** `\VaR` et `\TVaR` sont **réservées à la charge
annuelle agrégée $L$**, donc à la mesure de capital. Le quantile de sévérité d'un sinistre porte
`\qsev` ($\mathrm{q}$) et sa moyenne de queue `\qbarsev`, deux macros définies dans
`preambule.tex` avec le commentaire qui l'explique. La table des notations porte les deux entrées
et l'avertissement. Traité dans 05, 06, 12, 13, 15 et 16.

**Le pont entre les deux échelles est calculé et imprimé** par le script 67, section 1bis, au
lieu d'être fait à la main. À $\lambda = 21{,}56$ sinistres par an, atteindre le quantile annuel
à 99,5 % demande un quantile **par sinistre** à 99,977 %, soit 4 530 M€ ; le facteur résiduel de
1,8 est l'empreinte de la surdispersion et de la contagion. Deux mises en garde y sont imprimées
et il ne faut pas les perdre : $\lambda^\xi$ est une **borne basse** du facteur d'agrégation et
non son approximation centrée, parce que le terme additif $u - \sigma/\xi$ de la forme fermée est
négatif ; et le résidu vaut 1,79 au secteur contre 1,96 à l'entité, soit le même **ordre** à 9 %
près et non la même valeur, l'écart mesurant la qualité du pont.

**Le résultat qui ferme la question** : au secteur le capital vaut 12,3 fois le quantile
unitaire, à l'entité 0,30 fois, donc **il passe en dessous**. Le sens de l'inégalité s'inverse
avec l'échelle, donc aucun rapport fixe ne relie les deux objets et les comparer ne conclut
jamais, dans un sens comme dans l'autre.

### 2. La CTE mesure, elle ne couvre pas, et l'argument qui tranche est l'existence

Demande d'Hugo au call. Le mémoire y était déjà conforme sans le dire : le capital est partout un
$\VaR_{99,5\%}(L)$ centré (`scr_engine.py:213`), aucune grandeur de couverture n'est une TVaR.
C'est écrit maintenant, au chapitre 12, avec les deux titres de **diagnostic** sous lesquels la
mesure de queue intervient : noyau d'allocation d'Euler, qui répartit un niveau déjà fixé, et
indicateur de forme de queue par le rapport $\TVaR/\VaR = 2{,}1$ contre l'asymptote
$1/(1-\xi) = 2{,}5$.

**L'argument décisif n'est pas la proportion mais l'existence** : sous la calibration PRC,
$\hat\xi = 1{,}033 > 1$, donc l'espérance est infinie et **la mesure n'existe pas**. Une
couverture qui cesse d'être définie selon la source de sévérité ne peut pas porter un capital.
À utiliser plutôt que « la TVaR est excessive », qui est un argument de degré.

### 3. Les six postures sont définies, et leur bruit est publié

La figure J7 affichait **six** postures et le mémoire n'en expliquait que quatre : les niveaux
$\beta = 90\,\%$ (939) et $\beta = 99\,\%$ (1 247) n'étaient cités nulle part dans le texte, sur
une figure qu'un jury lit avant la prose. Table de définitions au chapitre 13, et le script 51
imprime les définitions avec les valeurs.

**Le bruit de simulation de chaque posture est mesuré** (quatre rééchantillonnages, `B = 3000`)
et publié : prédictive $\pm 7$, $\beta = 90\,\%$ $\pm 13$, $\beta = 95\,\%$ $\pm 9$,
$\beta = 99\,\%$ $\pm 24$. Deux constats, et le second n'était pas attendu :

- **les deux extrémités de l'échelle sont exactes**, le point étant le quantile d'un ajustement
  unique et le pire-cas celui d'un $\xi$ **posé** à 0,90. Tout le bruit est au milieu, donc dans
  les postures qui intègrent l'incertitude : une posture plus riche est moins reproductible ;
- **la posture la plus prudente est la moins précise.** À ne pas surinterpréter : sur quatre
  graines un écart-type est lui-même connu à 40 % près, donc l'ordre entre $\beta = 90$ et
  $95\,\%$ n'est **pas** résolu et n'a pas à l'être. Seul le saut vers $\beta = 99\,\%$ est net.

La figure J7 porte désormais ses **barres d'erreur**, sans lesquelles six barres étiquetées à
trois chiffres suggèrent six mesures également précises.

### 4. La VaR prédictive : 648 et 645 sont le même nombre

Le mémoire publiait 648 (script 46) et la figure affichait 645 (script 51), sans que rien ne
signalât laquelle lire. **Aucun des deux n'a tort** : même estimateur, ensembles bootstrap de
tailles différentes (`B = 2000` contre `3000`), et l'écart de 3 M€ vaut moins d'un écart-type de
simulation (7). L'étiquette du script 51 disait « melange, script 46 » alors qu'il **recalcule** :
corrigée. Le script 46 imprime la précision de sa propre valeur et renvoie au 51.

**Conséquence de rédaction, à tenir** : toute grandeur simulée se publie **avec son bruit**, ce
qui rend la question sans objet et donne la précision plutôt que des décimales.

### 5. Deux limites déclarées au chapitre 13, de sens opposés

Elles forment un troisième bloc de la table à deux colonnes, distinct des défauts d'estimation et
des choix de prudence, et **elles ne se compensent pas, elles s'additionnent en incertitude** :

- **l'attritionnel est absent de la donnée**, la base étant tronquée à son seuil de collecte : le
  capital publié est un capital de **queue**, et il exclut cette composante par absence
  d'observation et non par choix. Sens clair, il sous-estime ; taille non chiffrable. Deux
  atténuations à garder : à 99,5 % l'attritionnel pèse peu par construction, le quantile étant
  porté par un sinistre unique, et à l'échelle d'entité 98,8 % des années sont sans aucun
  incident matériel, donc il n'y a pas de régime courant à modéliser à cette échelle ;
- **la sévérité n'est pas plafonnée à l'échelle d'entité.** L'élasticité sévérité/taille vaut
  0,087, intervalle $[0{,}026 ; 0{,}148]$ qui contient presque zéro : le modèle affirme qu'une
  entité de quelques milliards subit à peu près la sévérité d'une institution mondiale. C'est la
  cause de la borne inférieure de validité et de la requalification du 169 en borne supérieure.
  Le correctif est identifié, un plafond adossé à l'exposition propre, du même type que celui qui
  rend le capital PRC calculable quand $\hat\xi > 1$ — mais il déplacerait tous les résultats
  d'entité, donc **il relève de la recalibration et le gel l'interdit**. Cette ligne n'affecte que
  le *niveau* d'entité, jamais les écarts entre états, qui sont des rapports.

### 6. Trois valeurs périmées, de la famille des queues Bâle et du Hill à 1,42

- **le $\kappa^\star$, que le script 58 imprimait à la fois à 76 % et à 78 %.** Sa différence
  finie utilisait un pas de 50 M€ sur une portée de 170, soit 30 %, donc elle mesurait une
  moyenne d'intervalle et non une pente en $L = \mathrm{SCR}$ ; la prime étant concave, le biais
  était haussier. Pas relatif (1 % de la portée), les deux impressions concordent à **78 %**.
  Le mémoire citait les deux valeurs à 25 lignes d'écart, corrigé ;
- **le taux marginal de prime, 1,16 % devenu 1,04 %**, même cause ;
- **un gain de $-47\,\%$ codé en dur** dans le script 58, valeur de l'ancienne échelle, alors que
  le script calcule $-64\,\%$ à l'échelle corrigée. Il est désormais relu et non récité.

### 7. Ce qui a bougé côté decks

- **le deck du 7 août a perdu sa slide de comparaison au forfait de Formule Standard**, sur
  décision de Kélian. Motif : le rapport besoin ORSA / forfait va de 0,04 à 2,07 selon le mix de
  bilan, donc son niveau ne mesure rien, et les trois entités où il dépasse 1 sont hors du
  domaine de validité de la sévérité. Ses réponses préparées sont passées dans la **banque de
  questions de l'aide-mémoire**, qui compte six entrées. Le sujet n'a pas disparu du call, il est
  passé du côté des questions ;
- **le deck du 14 août** compte 16 slides, dont trois répondent aux questions du call (échelles,
  CTE, postures) et deux exposent le traitement des états de conformité. Il est passé sous le
  harnais, de 35 à 96 % de couverture ;
- **nouveau deck `2026-08-10_point_caroline.tex`**, huit slides pour quinze minutes, pour la
  tutrice de stage. Voir plus bas ce qui l'engage personnellement.

### 8. Le facteur 3,34 entre états, maintenant imprimé

« Un facteur 3,3 entre l'état non conforme et l'état conforme » était un rapport écrit sur une
slide et calculé à la main. Le **script 43** l'imprime (3,34), avec la mention que seuls les
quatre canaux bougent, à sévérité de base et échelle inchangées.

## Ce qui a été fait le 12 août 2026, sur les quatre suites du call du 7

Quatre demandes d'Hugo, toutes traitées. Deux tenaient du calcul, deux de la rédaction, et les
deux réécritures ont fait tomber un défaut chacune.

### 1. Les conclusions tirées du bootstrap de $\xi$ sont retirées

Motif d'Hugo : un intervalle de $[0{,}30 ; 0{,}83]$ sur l'indice de queue est trop large pour
être interprété, donc il ne peut pas porter de conclusion. L'intervalle **reste affiché comme un
fait** et la limite déclarée du mémoire ne bouge pas ; ce qui disparaît est la lecture qu'on en
faisait. Deux trouvailles en faisant ce retrait :

- **la slide du 7 portait une valeur fausse**, `[0,32 ; 0,84]`, qu'aucun script ne reproduit : le
  script 47 imprime `[0,320 ; 0,871]` par delta-méthode et `[0,304 ; 0,831]` par bootstrap, et la
  slide mélangeait la borne basse du premier avec une borne haute qui n'appartient à aucun des
  deux, sous l'étiquette du second. Corrigée avec le couple publié. C'est l'exception au gel d'un
  deck : une valeur qu'on sait fausse se corrige ;
- **le même travers vivait au chapitre 06**, dont le paragraphe « Stabilité du paramètre de
  forme » écrivait que $\hat\xi$ « se stabilise autour de 0,6 » et que Hill « reste compatible
  avec la référence MLE ». Le balayage du script 47 le fait descendre à 0,38 au percentile 95, et
  Hill vaut 1,315 soit plus du double du MLE. **Le script imprimait en clair l'interdiction de
  l'écrire** (« A NE PAS ECRIRE : xi est stable quand on fait varier le seuil ») : la sortie
  versionnée portait la consigne depuis le 6 août et personne ne l'avait lue. Paragraphe et
  légende de figure réécrits sur la mesure, avec renvoi à la section de validation qui la porte.

### 2 et 3. La table complète des leviers, et où vivent les 5 001 M€ (script 68)

Le script 43 imprimait l'interaction en **résidu**. Un résidu n'est pas un résultat. Le
**script 68** énumère les seize configurations du treillis des quatre canaux et en tire trois
choses. Nouveau module partagé `canaux_conformite.py` : 43 et 68 tournent sur le même moteur,
mêmes graines, même résolution, sans quoi la réconciliation serait une coïncidence de tirages. Le
43 reproduit sa sortie versionnée ligne pour ligne après extraction.

**Trois lectures d'un canal, et elles ne sont pas interchangeables.** Isolée (depuis l'état
conforme), fermeture (depuis l'état non conforme) et Shapley :

| Canal | isolé | fermeture | Shapley |
|---|---|---|---|
| Fréquence | 4 328 ± 463 | **8 775** ± 1 004 | 6 546 ± 457 |
| Détection | 1 448 ± 277 | 4 562 ± 819 | 2 928 ± 343 |
| Accumulation P4 | 1 728 ± 210 | 3 402 ± 493 | 2 576 ± 222 |
| Propagation W | 1 633 ± 188 | 2 402 ± 442 | 2 088 ± 152 |
| **somme** | 9 138 | 19 141 | **14 139** |

La colonne isolée **manque** 5 001 M€, celle de fermeture le **dépasse** d'autant, et le rapport
va de 1,5 à 3,1 selon le canal. Conséquence de gestion : **remédier un canal rapporte davantage à
une entité défaillante partout qu'à une entité déjà conforme**, puisque le canal ferme aussi les
croisés qu'il portait. C'est la colonne de fermeture, et non l'isolée, qu'un plan de remédiation
doit citer. Shapley est la seule colonne additive, mais c'est une **convention** d'attribution :
deux canaux sur quatre sont bornés, leur part n'est pas un budget.

**La réconciliation est une identité, pas une mesure.** Décomposition de Möbius : ordre 1
9 138 M€, ordre 2 **5 345**, ordre 3 $-691$, ordre 4 $+346$, somme des quinze termes = 14 139 à la
précision machine. Ce qu'elle atteste est que la table est **complète**, pas que chaque terme est
précis. Sur seize graines, neuf termes sur quinze ont un signe résolu ; **aucun** des cinq d'ordre
3 et 4. Leur quasi-annulation ne se lit donc pas comme cinq mesures.

**Les effets croisés, et deux choses à ne pas surinterpréter.** freq×det 1 739 ± 708,
freq×accum 1 666 ± 354, freq×prop 1 182 ± 444, det×accum 573 ± 202, det×prop 515 ± 247,
prop×accum **−330** ± 242.

- **il n'y a pas de paire dominante et il ne faut pas en nommer une.** Les deux premières se
  tiennent à 73 M€ pour des écarts-types de 708 et 354, et leur ordre **s'inverse** en perte
  moyenne. Ce qui est résolu : les trois paires porteuses passent toutes par la **fréquence** et
  font 86 % de l'ordre 2 ;
- **une seule paire est négative, et c'est un résultat.** prop×accum est négative sur les seize
  graines et sur les deux métriques : les deux canaux de co-occurrence sont **substituts** et non
  compléments, un pilier déjà touché ne pouvant l'être deux fois. La cascade est super-additive
  en bloc mais **sous-additive entre ses deux canaux de co-occurrence**, ce qui borne l'amplitude
  imputable à la contagion prise en général.

**DEUX INTERACTIONS DISTINCTES, À NE JAMAIS ADDITIONNER.** Celle entre les quatre **canaux**
(+5 001 M€, signe résolu, script 68) et celle entre les cinq **piliers** (+1 395 M€, signe **non**
résolu entre graines, scripts 20 et 20b). Deux partitions du même écart. Le titre de la slide
Shapley annonçait « la suite des 5 001 M€ d'interaction », ce qui invitait précisément à les
additionner : corrigé.

### 4. « Portage » et « plancher », et une borne annoncée à l'envers

Les deux mots n'ont pas été compris au call, et la relecture montre qu'ils étaient mal employés.
Le mémoire écrivait que le **retour** (une durée) était un « plancher », alors que ce qui est
minoré est le **bénéfice**. Or minorer le bénéfice **majore** la durée : le sens de la borne
était inversé, dans le mémoire, dans le script 50 et dans le titre de la figure J6. Les trois
sont corrigés.

- **portage** : détenir du capital coûte, chaque année, un pourcentage du capital immobilisé (la
  marge de risque). Libérer 14 139 M€ économise donc 848 M€/an à 6 %, et non une fois ;
- **plancher** : le bénéfice a deux composantes et une seule est monétisée. Le portage vaut
  848 M€/an, la **sinistralité évitée** 3 247 M€/an, la charge annuelle moyenne passant de 3 869 à
  622. Ce qui est laissé de côté vaut **3,8 fois** ce qui est retenu. L'affirmation
  « majoritairement de la perte évitée » était dans le mémoire depuis le début **sans être
  chiffrée** : le script 50 l'imprime désormais ;
- **d'où le sens de la borne** : le retour de 6 à 35 ans est un **MAJORANT**. Les deux composantes
  réunies donneraient 1 à 7 ans, mais cette addition mêle un flux de compte de résultat à un coût
  du capital : convention de ROI, pas sortie de modèle. Le chiffre de référence reste le portage
  seul, avec le sens de sa borne.

**Réserve sur le taux, déclarée et non corrigée.** Le projet portait **deux taux** pour la même
notion sans que rien ne les relie : 6 % dans le script 50, **4,75 %** dans les scripts 58 et 60
depuis la directive (UE) 2025/2. Le mémoire citait le premier, le deck du 14 le second. Au taux
révisé le portage tombe à 672 M€/an et le majorant du retour passe de 35 à 45 ans. **Rien ne
bascule** et la chaîne publiée reste au taux historique : la calibration est gelée, et l'écart est
désormais imprimé plutôt que laissé au lecteur. Même traitement que le `p_u` gelé.

### Ce qui a bougé côté document

- **le corps reste à 104 pages**, le total passe de 126 à **127**. La page ajoutée est dans
  l'**annexe C** (le chapitre `12b` est une annexe, pas un chapitre du corps : vérifier avant de
  conclure qu'un ajout grossit le corps). Compte relu sur le PDF, pas sur un index ;
- **le deck du 14 passe de 16 à 20 slides** : le retrait demandé, la table complète, les effets
  croisés, et portage/plancher. Cinq cadres débordaient après ces ajouts, tous corrigés, et les
  six slides touchées ont été rendues en PNG et regardées ;
- **harnais : 1 398 nombres, 1 363 confirmés, 97,5 %**, couverture inchangée. Une correction
  d'instrument : `\begin{column}{0.46\linewidth}` était lu comme le nombre 0,46. Les
  `\includegraphics[width=...]` étaient neutralisés, les largeurs de colonne non. Le défaut ne se
  voyait pas tant que la largeur tombait par hasard sur une sortie de script, ce qui était le cas
  de 0,45 et 0,52 dans ce même deck.

### Un point ouvert trouvé en passant, et il n'est pas traité

**Le deck du 07-08 est à 0 % de couverture** : 105 nombres, aucun sous contrôle, parce qu'il ne
cite aucun script. C'est exactement la faille qui a laissé passer le `[0,32 ; 0,84]`. Le retrofit
n'a pas été fait : ajouter des lignes « Sources : scripts… » à dix slides d'un deck déjà présenté
risque de casser des cadres, et cela sort des quatre demandes.

Un contrôle de repli a été passé à la place, en lecture seule : chacun des 87 nombres distincts du
deck a été cherché dans **tout** le pool des 71 sorties versionnées, et **un seul** est introuvable,
le $-30$ de $1{,}6\times10^{-30}$, qui est un exposant. **Ce contrôle est beaucoup plus faible que
le harnais** : il demande si un script quelconque imprime la valeur, pas si le script que la slide
cite l'imprime, et un nombre rond se trouve par hasard dans un pool de 2 212 valeurs. Il ne
certifie donc rien ; il dit seulement qu'il n'y a pas de second `[0,32 ; 0,84]` évident.

## Les retours de Caroline appliqués, le 12 août 2026 au soir

**L'élicitation est abandonnée, décision de Kélian ce jour.** La slide G du deck du 14 tient,
et la contradiction avec l'enthousiasme de Caroline pour la méthode de Cooke se règle donc en
sa défaveur. **Ne pas rouvrir.** Conséquence à traiter : sa demande de mettre la méthode et le
questionnaire en annexe reste pertinente, mais elle change de sens. L'annexe doit documenter
**ce qui a été préparé et pourquoi il n'a pas été lancé**, pas un protocole à venir. C'est un
actif devant un jury qui demanderait pourquoi il n'y a pas de jugement d'expert, et ce n'est
pas fait.

### Le script 08h est relancé et sa sortie versionnée

C'était le seul endroit du dossier Hawkes hors contrôle, et le pire possible puisque le rejet
est adossé aux travaux de Caroline. `sorties_verif/08h.txt` existe désormais : noyau
exponentiel $n = 0{,}551$ avec demi-vie 5,4 h, noyau à retard de Bessy-Roland $n = 0{,}517$
avec **pic à 3,3 h** et lag moyen 6,7 h, et l'endogénéité tombe de $0{,}551$ à ${\sim}0$ dès
que les co-occurrences du même jour passent en exogène. La table du chapitre 13 cite maintenant
`08h` et ses deux nombres sont confirmés. **Le « pic à 3 h » n'est plus lu sur une figure.**

### L'étage de modèle sort de la bande reportée, il n'est pas supprimé

Caroline demandait de chiffrer avant de retirer. C'était déjà chiffré par le script 48, et le
résultat va contre l'intuition de l'arbitrage : **l'étage de modèle est le plus gros des
trois**, facteur 5,5 sur l'axe de la famille de queue contre 2,5 pour le paramètre et une bande
de 6 858 à 8 697 pour l'identification. Le retirer rétrécit donc l'affichage plus que tout
autre retrait alors que l'incertitude ne bouge pas.

Nouvelle sous-section du chapitre 13, `sec:etage-modele-hors-bande`. La bande reportée ne cumule
plus que **paramètre et identification** ; l'étage de modèle devient un **axe de sensibilité
déclaré**, et il reste publié deux fois : la sixième posture (pire cas à $\xi$ posé à 0,90)
*est* l'ambiguïté de famille, et la bande de dépendance 5 322 à 9 806 reste dans la section.
Le motif écrit est que les deux premiers étages sont statistiques, donc portables par un
intervalle, et que le troisième est épistémique, un choix de famille ne se moyennant pas.
**Ne pas transformer ce déplacement en suppression.**

### Il n'y a jamais eu de test de martingalité, et c'est la réponse à sa réserve

Vérifié : le mémoire n'en contient aucun. Il a **deux** usages du mot, tous deux légitimes et
tous deux sous mesure physique. Au chapitre 09, la forme de Dirichlet d'une chaîne de Markov,
qui est la variation quadratique de la martingale associée à une fonction test. À l'annexe C,
un brownien sans dérive et le premier passage de P4 par principe de réflexion. Aucun prix,
aucun actif répliqué, aucun changement de mesure.

Deux paragraphes de précaution ajoutés, un dans chaque endroit, disant explicitement qu'aucun
test de martingalité au sens des générateurs de scénarios n'est conduit. Et le lien rhétorique
de l'annexe C est corrigé : il annonçait que le seuil de P4 « rejoint le cadre martingale de
l'identification », alors que **le lien entre les deux usages est de vocabulaire et non de
mathématique**. Ce qu'ils ont en commun est plus modeste, ils vivent sous la même mesure.
Le seuil $z^\star$ ne se déduit d'aucun test : il vient de la calibration du facteur tiers.

### La confusion « gravité » n'était pas dans le mémoire, elle est dans le code

Balayage fait, et le résultat est inattendu : **le mémoire n'utilise nulle part « gravité »
pour le caractère systémique.** Les seules occurrences sont la locution AMDEC
« probabilité $\times$ gravité », qui est le terme consacré du domaine et qu'il faut garder, un
« centre de gravité » métaphorique, et une occurrence au sens monétaire corrigée en
« sévérité ». La confusion vient des decks de juillet (17/07, 20/07, 24/07 : « la gravité
propre de chaque pilier », « criticité = probabilité croisée avec gravité »), qui sont archivés.

**En revanche il y a une vraie collision dans le code, et elle n'est pas corrigée :**

| Nom | Ce que c'est | Où |
|---|---|---|
| `G_BASE` | le **gain de propagation** $g = 0{,}90$ | `scr_engine.py`, `euro_cascade_model.py` |
| `GBASE` | l'**échelon de sévérité** par pilier, chaque échelon doublant la médiane | `severite_model.py`, `cascade_model.py` |

Deux objets sans rapport, des noms qui ne diffèrent que par un tiret bas, et le second est
documenté avec le mot « gravité ». C'est exactement la confusion que Caroline a pointée, et
elle vit dans le moteur. **Le renommage n'a pas été fait** : il touche 27 fichiers et le
pipeline est gelé, donc c'est un arbitrage. En attendant, la distinction est verrouillée dans
la table des notations, l'entrée $g$ portant « mesure une criticité, jamais un montant ».

### Coût et contrôles

**Le corps passe de 104 à 105 pages, le total de 127 à 129.** L'ajout du chapitre 13 (l'étage
de modèle) et le paragraphe du chapitre 09 sont dans le corps ; le reste est en annexe. Cela va
contre l'arbitrage de format, et c'est le prix de la demande de Caroline. Harnais à
**1 400 nombres, 1 366 confirmés, 97,6 %**, 0 vbox, 0 référence indéfinie, 0 annotation hors
page.

### Ce qui reste de sa liste

- **la section dédiée à la sensibilité des probabilités de propagation.** Une bonne partie
  existe et il faut la rassembler plutôt que la refaire : l'invariance en g (script 66), les
  sensibilités du script 22, et l'écart-type de chaque terme croisé (script 68) ;
- **la méthode de Cooke et le questionnaire en annexe**, dans la version « ce qui a été
  préparé et pourquoi il n'a pas été lancé » ;
- **la CTE à 95 %** en diagnostic à côté de la VaR 99,5 %, jamais à sa place ;
- **la renormalisation par taille** dans sa version à deux canaux, fréquence par le lien
  logarithmique et sévérité par l'élasticité mesurée, la proportionnalité au SCR de marché
  restant le repère contre lequel la méthode se distingue et non une méthode ;
- **la contrainte conformité 1 et 2 vers 3** sur la dépendance des états, à ne pas confondre
  avec la propagation ;
- **le renommage `GBASE`**, arbitrage ouvert.

## Le point de stage avec Caroline Hillairet

Elle est **tutrice de stage**, et son rôle dans le projet n'est pas symétrique de celui d'Hugo :
trois choses l'engagent personnellement, et un deck avec elle doit partir de là.

1. **Sa remarque « le quantile d'un objet incertain est mauvais »** a produit deux briques du
   mémoire, la VaR prédictive (script 46) et la bande de modèle (script 48). Le résultat lui est
   rendu tel qu'il est, **y compris en ce qu'il la contredit** : intégrer l'incertitude ne
   déplace pas le point à 99,5 %, l'écart au plug-in valant 5 M€ en moyenne sur les
   rééchantillonnages pour un bruit de 7. Ce qui était fragile n'était pas le point mais la
   **largeur**. Formulation retenue : sa remarque était juste, mais pas par le mécanisme attendu,
   et elle ne condamne pas le quantile mais le quantile *cité seul*.
2. **Le rejet du Hawkes est adossé à ses propres travaux** (Bessy-Roland/Boumezoued/Hillairet
   2021 ; Boumezoued/Cherkaoui/Hillairet 2023). Le script 08h le teste contre **leur** noyau à
   retard $\varphi(a) = \alpha a e^{-\beta a}$ et contre leur logique *two-phase*, pas contre un
   noyau de paille : excitation intra-journalière, pic à 3 h, et ratio de branchement qui passe
   de 0,55 à quasiment zéro dès que les co-occurrences du même jour passent en exogène.
3. **Le mémoire lui emprunte** la logique d'états de conformité (Hillairet et Lopez, chapitre 3).

**Le choix de posture à reporter est le seul arbitrage qui lui revient**, et c'est la seule slide
du deck qui appelle une décision. Le mémoire publie aujourd'hui le plug-in avec sa bande.

**Réserve à connaître avant ce call, et elle est sérieuse :** la sortie du script 08h **n'est pas
versionnée**, ce script exigeant `Data_Breach_Chronology.xlsx`, absent du Mac qui n'a que le
`.csv`. Les chiffres de la slide Hawkes sont donc lus sur la figure O2. **À relancer sur le PC et
à versionner**, c'est le seul endroit du deck hors contrôle et c'est le plus mauvais endroit
possible puisque c'est le point qui la concerne le plus directement.

## Ce qui est ouvert

**Ne dépend pas de l'assistant :**
- le **second codage en aveugle** (kit prêt, dix récits, une heure ; script 54 attend le CSV) ;
- l'**élicitation** et les autres documents ;
- **vérifier les quatre jeux de chiffres SFCR** contre les PDF (tableau en tête du script 65,
  deux SCR sur quatre sont déduits d'un taux de couverture) ;
- l'arbitrage de **format** : le corps est à 104 pages pour 126 au total, contre les ~70 de corps
  recommandés par l'Institut, et il a gagné trois pages les 9 et 10 août ;
- **le choix de la posture à reporter**, plug-in avec sa bande, prédictive ou robuste, à trancher
  avec Caroline. La grille pour le faire existe désormais : table des six postures au chapitre 13,
  avec le bruit de chacune. Passer au robuste 95 % multiplierait le capital par 1,6 ;
- **relancer le script 08h sur le PC et versionner sa sortie** (il exige
  `Data_Breach_Chronology.xlsx`, absent du Mac). C'est ce qui met les chiffres du rejet du Hawkes
  sous contrôle, et ils sont adossés aux travaux de Caroline : à faire avant le point avec elle ;
- le registre de sous-traitance.

**Deux arbitrages, trouvés et tranchés le 6 août 2026 en dépouillant les 36 non confirmés.**

1. **Le seuil de la calibration est celui de `config.py`, et les scripts s'y ancrent.**
   Le mémoire publie partout la calibration figée : `u = 20,03 M€`, `91 excès`,
   `xi = 0,5954`, `sigma = 57,97`, `VaR = 662,78`, `IC90 = [411,5 ; 1037]`, facteur 2,5.
   Les scripts 46, 47 et 51 redérivaient chacun leur propre seuil comme le q85 des données
   courantes, soit `22,03 M€` et `88 excès` : ils validaient et bootstrapaient un ajustement
   que le mémoire ne publie pas. C'est de là que venait le facteur 2,6 du chapitre 13 contre
   2,5 aux chapitres 05 et 06. **Les trois scripts lisent désormais le seuil dans
   `config.py`.** Vérifications faites : le seuil publié donne exactement 91 excès dans la
   donnée courante ; les paramètres publiés, imposés, passent Anderson-Darling à p = 0,99 et
   Kolmogorov-Smirnov à p = 0,89 ; l'indice de queue ne bouge que de 0,5 % entre les deux
   seuils. Le résidu 2,52 contre 2,56 est du bruit de bootstrap sur la borne haute d'une
   queue lourde, pas un désaccord de méthode. `config.py` n'a pas été touché :
   `euro_cascade_model.py` le lit, donc y toucher déplacerait tous les SCR.
   **Reste un point à trancher, signalé par le script 47 et non corrigé :** `config.py` porte
   `n_excess = 91` et `p_u = 0,1509`, or `p_u` correspond à 87,8 excès. La VaR publiée est
   calculée avec `p_u` et reste reproductible ; c'est le champ descriptif `n_excess` qui est
   en désaccord. Corriger `p_u` déplacerait la VaR, donc tous les SCR.
2. **La table des queues par catégorie Bâle a été recalculée et adoptée.** Les cinq queues
   0,92 / 0,98 / 1,03 / 1,27 / 1,37 et les 105 observations de *Business Disruption and
   System Failures* venaient d'une sonde dont le filtre n'a pas été conservé, et n'étaient
   imprimées par aucun script. Aucune combinaison du pipeline ne les reproduisait. Elles sont
   remplacées par la table du **script 67, section 5**, qui la calcule et l'imprime avec un
   filtre écrit : convention de sévérité du projet (`load_clean`, colonne `Loss Amount ($M)`,
   `filter_finance` sur `Industry Sector Name`), seuil q75 par catégorie, ajustement GPD
   libre. Nouvelles valeurs : **0,865 / 1,031 / 1,038 / 1,355 / 1,368**, dispersion 0,50, et
   **111 observations** pour la catégorie TIC. Le script 37 en est le consommateur.
   Conséquence au chapitre 12b : la borne du SCR passe de +38 / +82 % à **+55 / +96 %**, le
   classement reste dominé par P1 dans 83 % des assignations, et la conclusion du chapitre,
   supposer une queue commune sous-estime le capital, en sort renforcée.

3. **La tolérance du harnais a été resserrée, et le seuil de contrôle change avec elle.**
   L'ancienne tolérance était `max(0,5 ; 0,6 %)`. Le plancher absolu de 0,5 était écrasant sous
   83 : il faisait confirmer 0,9 par un 0,99 sans rapport. La nouvelle est
   `max(0,6 % ; demi-unité du dernier chiffre écrit)`, c'est-à-dire la borne de l'arrondi
   d'écriture : 0,05 pour un nombre écrit « 2,1 », 0,5 pour « 122 ». **Le taux passe de 98,8 à
   95,7 %, et ce n'est pas une régression : c'est la même vérification, faite honnêtement.**
   Le contrôle de fin de tâche devenait alors **harnais ≥ 99 %** : une fois les grandeurs dérivées
   imprimées et les artefacts de lecture corrigés, le résidu tombait à **quatre** nombres, tous
   irréductibles par nature (l'exposant de $10^{-30}$, deux sommes à $100\,\%$ par
   construction, le niveau de confiance $99{,}9\,\%$).
   **Ce seuil de 99 % est périmé et ne s'applique plus** : il valait sur le périmètre restreint
   d'alors, 74,7 % des nombres publiés. Depuis l'élargissement à 100 % de couverture, le contrôle
   est **couverture = 100 % et confirmation ≥ 97 %**, dans cet ordre. Voir la section « Contrôles
   à passer avant de dire que c'est fini », qui fait foi.

4. **Le périmètre du harnais a été élargi, et c'est ce qui a fait remonter le reste.**
   Deux angles morts, tous deux dans l'instrument et non dans le mémoire.
   *Le premier* : la liste d'exemption du harnais était indexée sur la **valeur**, pas sur le
   contexte, et elle retirait les nombres **en silence**. Le dénominateur n'était donc pas
   « les nombres publiés » mais « les nombres publiés moins une liste », et le rapport ne
   disait pas laquelle. Deux entrées y figuraient à tort : le **2,5**, facteur d'incertitude
   de calibration sur la VaR, qui est un résultat central et l'objet même de l'arbitrage
   2,5 contre 2,6 (le harnais ne pouvait pas le trancher, il ne le regardait pas), et le
   **19**, qui désigne tantôt l'article de la directive, tantôt une part de 19 %. Les deux
   sont retirés de la liste ; les exemptions restantes (niveaux de confiance, entiers
   d'énumération, millésimes) sont **comptées et affichées par motif**.
   *Le second* : la **table des paramètres de l'annexe 17**, celle qu'un jury lit en premier
   pour savoir ce qui est calibré et ce qui est posé, **ne citait aucun script** : elle
   échappait entièrement au contrôle. Elle est rattachée aux scripts 08b, 22, 34, 47, 60
   et 67, ce qui a fait ressortir sept grandeurs non imprimées, toutes traitées depuis.
   Trois artefacts de lecture ont été corrigés au passage : la mantisse d'une notation
   scientifique (garder 1,53 dans « 1,53·10⁻⁵ » et jeter l'exposant, pas l'inverse), la
   virgule décimale française des sorties (qui versait « 99,9 » dans le pool sous forme de
   deux entiers, 99 et 9, perdant la vraie valeur et en injectant deux fausses), et les
   `\vspace{}`. Le contrôle de fin de tâche restait alors harnais ≥ 99 % ; **ce seuil est périmé**,
   voir la remarque au point 3 ci-dessus.

5. **`p_u` est tranché : gelé, chiffré, publié comme limite.** `p_u` n'est pas un paramètre
   libre : la formule POT a trois entrées pour deux degrés de liberté, et le taux de
   dépassement se **compte** une fois le seuil et l'échantillon fixés. Publier
   (u = 20,03 ; p_u = 0,1509) n'est donc pas une hypothèse assumable, c'est une incohérence
   arithmétique. L'effet est calculé : VaR 99,5 % mono-perte de 662,78 à **678,60 M€**,
   soit **+2,4 %**, ou 15,8 M€, soit 2,5 % de la largeur de l'IC90 de cette même VaR.
   La valeur reste gelée, et le raisonnement est écrit dans `config.py` : rejouer un pipeline
   stochastique (bootstrap à 200 tirages) pour un écart de cette taille déplacerait des
   centaines de nombres publiés sans qu'aucun déplacement soit attribuable à la correction.
   **Deux prudences à ne pas confondre**, et le script 47 l'imprime : côté solvabilité l'écart
   est anti-conservateur, il sous-estime le capital et une sous-estimation se déclare ; côté
   thèse il va dans l'autre sens, le chiffre avancé est minoré et non gonflé. Seul le premier
   engage. Le tout est publié au **chapitre 13, section « Un défaut de calibration, chiffré
   plutôt que corrigé »**, et le bloc `OPRISK_COHERENCE` de `config.py` recalcule l'écart à
   chaque import, donc il ne peut plus se périmer en silence.

6. **La stabilité de $\xi$ au seuil était surévaluée, aux chapitres 06 et 17.** Le mémoire
   écrivait « $\hat\xi$ reste stable autour de 0,60 quand on fait varier le seuil », et le
   script 47 imprimait la même conclusion en dur. Le balayage qu'il calcule lui-même dit
   autre chose : $\xi$ décroît de 0,98 (percentile 75) à 0,38 (percentile 95), six seuils à
   trente excès au moins. La lecture correcte coupe le balayage au seuil publié. **Au-dessus**,
   $\xi$ va de 0,60 à 0,38 et reste **entièrement dans l'IC90 déjà publié [0,30 ; 0,83]** :
   la sensibilité au seuil ne crée pas d'incertitude nouvelle, elle se lit dans celle qui est
   déclarée. **En dessous**, $\xi$ remonte à 0,98 et sort de l'intervalle : biais de seuil
   classique, et c'est ce qui justifie de ne pas descendre plus bas. La table de l'annexe
   annonçait une sensibilité « 0,68 à 0,93 selon le seuil » qu'aucun calcul ne reproduit, et
   qui **sous-estimait** la vraie amplitude ; elle est remplacée par la mesure.

**Le `-53 %`, et l'état exact de la question.** Ce paragraphe a été écrit quand le chiffre
semblait n'être imprimé par rien ; le point 7 ci-dessous l'a démenti le même jour, et c'est le
point 7 qui fait foi. Le script 25 l'imprime : « gain de conformite (NC->C) : 8861 M de SCR en
moins (-53 %) », à $g$ fixé à 0,9 et en balayant $q$ de 0 à 1, soit 16 847 vers 7 987 M€. Sa
sortie n'était simplement pas versionnée.

**Ce qui reste ouvert n'est donc pas sa source mais sa définition.** Le script 20 donne `-64 %`
sous OpRisk et `-75 %` sous PRC, et le script 43 donne un facteur 3,34 entre les deux états de
référence : ces chiffres ne mesurent pas la même chose, parce qu'ils ne bougent pas les mêmes
canaux. Celui du script 25 garde $g$ au niveau **non conforme** pendant qu'il fait varier $q$, ce
qui explique que son état « conforme » soit à 7 987 et non à 6 049. Le mémoire doit dire lequel il
publie et sous quelle définition. **Ne pas remplacer un de ces chiffres par un autre sans avoir
tranché ce point**, ce serait échanger un chiffre mal défini contre un autre.

7. **Le périmètre du contrôle est passé de 74,7 % à 100 %, et c'est le vrai travail de la
   journée.** Dix-neuf sorties de scripts ont été versionnées (01 à 06, 09 à 13, 15, 24, 25,
   29, 31, 32, 34, 45, 61) et toutes les sections du mémoire ont été rattachées à leurs
   scripts. Ce qui en est sorti :
   - **le chapitre 07, qui porte la contribution centrale, n'était vérifié par rien.** Ses
     67 nombres étaient entièrement hors contrôle. Il est aujourd'hui à 95,5 % sur 67 nombres ;
   - **le `-53 %` n'était pas faux, il était invisible.** Le script 25 l'imprime :
     « gain de conformite (NC->C) : 8861 M de SCR en moins (-53 %) ». Sa sortie n'était pas
     versionnée, voilà tout ;
   - **désaccord de normalisation entre le script 03 et le reste du pipeline, TRANCHÉ depuis.**
     Le script 03 divisait par la **réception** maximale (2,3) quand le reste divise par
     l'**émission** maximale (2,60). D'où $\rho(W) = 0{,}572$ contre 0,506, et le chapitre 07
     publiait 0,506 et 1,78 (convention d'émission) **et** $R_0 = 0{,}062$ (convention de
     réception) dans la même phrase. Voir le point 11 ;
   - trois scripts (09, 10, 11) n'étaient pas lançables depuis la racine du dépôt, faute
     d'amorce de `sys.path` ; corrigé ;
   - le commentaire de `03_calibration_W.py` annonçait une incidence de fond de 7 % là où
     $\Phi(-1{,}7) = 4{,}5\,\%$, la valeur que le chapitre publie ; corrigé et imprimée ;
   - la table Hackmageddon 2023 contre 2026 ne vivait que dans la prose. Elle est enregistrée
     dans `config.py` sous le **même statut de citation externe** que les 1 041 incidents, et
     imprimée par le script 63. Son écart de cybercriminalité était écrit $-7{,}1$ pour
     $81{,}1 - 73{,}9 = 7{,}2$ ; corrigé.

   **Le harnais distingue désormais trois états, pas deux :** sous contrôle, **déclaré hors
   script** (par un commentaire `% HARNAIS-HORS-SCRIPT:` ou `% HARNAIS-HORS-SECTION:` dans le
   chapitre, avec son motif), et hors contrôle. Seul le dernier doit valoir zéro. Sont
   déclarés : les chapitres démonstrations, état de l'art et cadre réglementaire, et la
   section des théorèmes du chapitre socle.

   **Trente-cinq non confirmés restent**, et ce sont de vraies pistes, pas du bruit : les huit
   du choc MOVEit (script 35, qui exige `Data_Breach_Chronology.xlsx`, absent du Mac qui n'a
   que le `.csv` : **à relancer sur le PC**), les 8 301 / 2 589 / 5 900 / 5 275 / 2 554 des
   préambules résultats et résumé, le 3 000 du knockout, le $-0{,}8$ et le $-63{,}9$ du biais
   de sévérité, le 81 % de direction du classeur.

8. **L'écart Hill contre MLE est démontré, plus seulement invoqué, et c'est le point le
   plus exposé du mémoire qui tombe.** Dire « Hill est biaisé en échantillon fini » est un
   argument d'autorité. L'enjeu ne l'est pas : à $\xi = 0{,}595$ la variance de la sévérité
   est infinie mais l'espérance existe ; à $\xi = 1{,}32$ **l'espérance cesse d'exister** et
   le modèle de perte agrégée n'a plus d'objet. On simule donc 2 000 échantillons sous le
   modèle publié et l'on applique le même estimateur de Hill aux mêmes $k$. **Les six valeurs
   observées tombent dans l'intervalle simulé à 90 %**, moyennes coïncidant à quelques
   millièmes : 1,315 observé contre 1,327 simulé à $k=86$. L'écart de 120,8 % est donc
   exactement ce qu'un $\xi$ de 0,595 produit, et les données corroborent la calibration par
   un troisième chemin après Anderson-Darling et Kolmogorov-Smirnov. Deux dérives de sens
   contraire l'achèvent : Hill croît avec $k$ (0,93 à 1,72) quand le balayage de seuil fait
   décroître $\xi$ (0,60 à 0,38). Si la queue valait 1,32, les deux dérives seraient inversées.

9. **Les quatre mesures de surdispersion sont réconciliées, et la couverture de l'IC était
   mal lue.** L'indice de dispersion vaut $1+\lambda/r$, donc **il n'est pas invariant
   d'échelle** : 1,19 sur les cellules firme-année, 2,24 sur la série annuelle détendancée,
   9,20 au moteur qui est un choix posé. Une échelle de lecture, une agrégation, une marge
   prudentielle. Par ailleurs le script 47 qualifiait de « bonne calibration » une couverture
   réelle de 86 % pour un IC annoncé à 90 % : c'est l'inverse, **l'intervalle est trop
   étroit**, l'incertitude sur $\xi$ est sous-estimée, et il faudrait élargir la demi-largeur
   d'environ 10 %.

   **D'où une table à deux colonnes au chapitre 13, qui vaut mieux que trois mentions
   éparses.** Les deux seuls écarts *involontaires* du mémoire (le $p_u$ gelé, la couverture
   de l'IC) sous-estiment le capital de quelques pour cent chacun ; les trois choix
   *délibérés* ($\xi = 0{,}90$, $a = 0{,}60$, $\varphi = 9{,}20$) le majorent, et de beaucoup
   plus. Le mémoire ne se protège pas derrière ses erreurs : sa prudence vient de choix
   assumés, et corriger les deux premiers ne changerait aucune conclusion.

10. **Les deux SCR déduits du panel SFCR sont bornés.** Deux entités sur quatre ne publient
    pas leur SCR : il se déduit des fonds propres divisés par le taux de couverture, et ce
    sont justement celles dont la part attribuée à DORA est la plus frappante, 26,3 et
    41,3 %. Sous un stress de ±10 %, borne large, les parts deviennent [23,9 ; 29,3] et
    [37,6 ; 45,9] : les ordres de grandeur tiennent. **Cette borne ne remplace pas la lecture
    des quatre rapports SFCR, qui reste due** et qui ne dépend pas de l'assistant.

11. **La convention de normalisation de $W$ est tranchée, et le script 03 est aligné.**
    Ce n'est pas un arbitrage de goût. La normalisation de Leontief existe pour garantir que le
    pilier le plus prolifique engendre **au plus $g$** descendants directs, $e_k = g\,s_k/c$ où
    $s_k$ est son **émission**. Avec le diviseur de réception ($c = 2{,}3$) on obtenait
    $e_{P1} = 0{,}9 \times 2{,}60/2{,}3 = 1{,}02$, donc plus que $g = 0{,}9$ : la borne que la
    normalisation est censée poser était franchie, et $g$ cessait de désigner ce qu'il désigne.
    Avec le diviseur d'émission ($c = 2{,}60$) on a $e_{P1} = 0{,}90$ exactement, et la
    contrainte de réception reste satisfaite puisque 2,3 est sous 2,60.
    **Ce qui ne bouge pas :** $\rho(W) = 0{,}506$, le rapport 0,562, le $g$ critique de 1,78,
    tous déjà publiés et tous corrects. **Ce qui bouge :** $R_0$ passe de 0,062 à **0,054**, le
    seuil critique de $R_0$ de 7,2 à **8,1**, la progéniture de 0,127/0,080/0,068/0,063/0,030 à
    **0,109/0,069/0,058/0,054/0,026**, et à $g = 1$ le couple (0,635 ; 0,070) devient
    (0,562 ; 0,061). Les figures K1, K2 et K3 sont régénérées et relues. La conclusion se
    renforce : un $R_0$ plus petit veut dire une cascade qui s'éteint plus vite.
    Deux conclusions codées en dur ont été corrigées au passage dans le script 03 : le titre de
    la figure K1 annonçait un logit gonflé de 60 % là où les pentes calculées donnent **96 %**,
    et l'en-tête annonçait un facteur 1,6 pour un facteur 2 mesuré.

12. **LA CALIBRATION EST GELÉE À COMPTER DU 7 AOÛT 2026. Règle, pas préférence.**
    Plus aucune **recalibration** : ni `config.py`, ni les paramètres figés, ni le pipeline
    stochastique. Les **corrections d'erreur** restent autorisées et attendues, et la distinction
    est nette : une erreur est une valeur qu'aucun calcul du projet ne reproduit (les queues
    Bâle, le Hill à 1,42, le $\kappa^\star$ à 76 %, la plage de $\xi$, le diviseur du script 03) ;
    une recalibration est un changement d'entrée qui déplace des résultats corrects (corriger
    $p_u$, rejouer un bootstrap, changer un seuil).
    **Pourquoi ce gel plutôt que la correction de $p_u$.** L'écart vaut 2,4 %, soit un
    quarantième de l'IC90 de la même VaR. Rejouer un pipeline à 200 tirages réinjecterait un
    bruit de Monte-Carlo du même ordre : des centaines de nombres publiés bougeraient sans
    qu'aucun déplacement soit attribuable à la correction, et la piste d'audit serait perdue
    pour un gain immatériel. Surtout, une limite chiffrée, signée et recalculée à chaque import
    vaut **mieux** devant un jury qu'un nombre corrigé en silence : la section
    « Un défaut de calibration, chiffré plutôt que corrigé » du chapitre 13 est un actif du
    mémoire, pas une dette. La faire disparaître serait un mauvais échange.

**Faisable :**
- **mettre le deck du 07-08 sous harnais.** Il est à **0 % de couverture**, 105 nombres, parce
  qu'il ne cite aucun script : c'est la faille qui a laissé passer le `[0,32 ; 0,84]`. Le
  retrofit demande une ligne « Sources : scripts… » par slide, et chaque ligne ajoutée peut
  faire déborder un cadre d'un deck déjà présenté. Un contrôle de repli a été passé le 12 août,
  qui ne trouve pas de second défaut évident, **mais il est beaucoup plus faible que le
  harnais** : voir la fin de la section du 12 août ;
- les **14 grandeurs dérivées** encore non imprimées, sorties par la tolérance resserrée :
  le $z=-0{,}33$ du test de réversibilité (script 40), cinq quantités du corpus étendu
  (script 59), le multiple de capital 8,3 (script 58), le $\xi$ de Hill 1,42 (script 47).
  Même traitement que les six déjà traitées : les faire imprimer par le script qui les
  possède. Le reste du résidu, 25 nombres, est légitimement hors script : 9 entrées posées
  du modèle, 13 constantes statistiques ou réglementaires, 3 sources externes ;
- l'**ancrage des valeurs de g** sur des sources publiques (ACPR, EIOPA), devenu optionnel
  depuis l'invariance — en attente de la décision d'Hugo ;
- les **7 % de blanc résiduels** sous trois titres de figures : cosmétique, refusé deux fois,
  le corriger imposerait de changer de moteur de mise en page sur sept scripts déjà validés.

**Clos, à ne pas rouvrir :** le **statut de citation** de Hackmageddon (la source reste
utilisée, voir plus haut), le **Hawkes** (celui-là est bien rejeté, et le rejet est documenté et
positionné par rapport à Boumezoued et Hillairet), la **non-transitivité** (réfutée par son
auteur, remplacée par la dépendance à l'ordre), le périmètre, l'anonymisation des entités, les
decks du 07, 14 et 21 août, la **convention de normalisation de $W$** (diviseur d'émission,
2,60), le **gel de la calibration**, la **convention `\VaR`/`\qsev`** (voir la section du 10
août), et le **détecteur de contradictions inter-scripts** dans le harnais, instruit et écarté
pour une raison, non par manque de temps.

## Note d'honnêteté

Ce mémoire vaut aujourd'hui environ 17/20 en évaluation interne. Ce qui le tient, c'est qu'il
publie ses propres limites : la non-transitivité qui lui donnait son titre a été réfutée par son
auteur, le chiffre central a été requalifié en borne supérieure, la borne inférieure de validité
de la méthode est publiée, et le harnais signale ce qu'il ne peut pas confirmer. **Ne pas défaire
cela.** Toute reformulation qui rendrait une réserve moins visible dégrade le travail, même si
elle le fait paraître plus assuré.

**Deux additions du 10 août vont dans le même sens, et il faut les protéger de la même façon.**
Les grandeurs simulées sont désormais publiées **avec leur bruit** : une posture citée à
« 1 247 ± 24 » est plus utile qu'à « 1 247 », et la tentation d'enlever le ± pour faire plus net
est exactement la dégradation contre laquelle ce paragraphe met en garde. Et la table des postures
dit que **la plus prudente est la moins précise**, ce qui affaiblit en apparence la posture la
plus rassurante : c'est un résultat, pas une faiblesse, et le supprimer rendrait le mémoire moins
défendable, pas plus.

**Une dernière chose sur la méthode de travail, apprise trois fois cette semaine.** Les défauts
trouvés ne l'ont pas été en relisant le mémoire : ils l'ont été en **regardant une slide** et en
allant vérifier ce qu'elle affirmait. Le κ⋆ contradictoire, les six postures non définies, la
prédictive à deux valeurs, le facteur 3,3 non imprimé, le compte de pages périmé — tous. Une
figure ou une slide est le meilleur détecteur de défauts du projet, parce qu'elle force à
énoncer un chiffre hors du contexte qui le justifiait.
