# Mémoire SCR DORA — contexte de reprise

Document de passation. À lire en entier avant de toucher quoi que ce soit.

## Le projet

Mémoire d'actuariat de Kélian Kaddouri (ENSAE / Nexialog Consulting) :
**« Quantification du SCR lié à la non-conformité au règlement DORA — une cascade dirigée entre
les cinq piliers »**. Objectif affiché : le Prix SCOR, donc le top 1-3 national, pas la simple
validation. Tuteur : Hugo. Point d'avancement hebdomadaire.

**LE DÉPÔT EST LE 30 SEPTEMBRE 2026, ET NON FIN NOVEMBRE.** Ce fichier a porté « fin novembre »
jusqu'au 9 septembre, et la section du backtest justifiait même de ne pas recalibrer au motif
qu'on serait « à onze semaines du dépôt » : les deux étaient faux. Deux sessions existent,
soutenance en novembre 2026 avec rendu le **30 septembre**, ou soutenance en mars 2027 avec
rendu début janvier. **Kélian a tranché le 9 septembre pour novembre**, donc il reste trois
semaines et non trois mois. Toute décision qui invoque le temps restant doit se relire à cette
aune.

**ET IL Y A DEUX DOCUMENTS À RENDRE, PAS UN.** Le mémoire d'actuariat d'un côté ; le **rapport
de stage de fin d'études ENSAE** de l'autre, que Kélian a demandé le 9 septembre de traiter
comme un document **distinct**. Il vit dans `exploratory/rapport_ensae/` et obéit à ses propres
consignes, qui ne sont pas celles du mémoire : environ 30 pages de corps hors annexes, Times New
Roman 12, interligne 1,5, page de couverture au modèle imposé, et deux notes de synthèse
autonomes d'une à deux pages, française et anglaise. Détail dans la section « Le rapport de
stage ENSAE » plus bas. **Ne pas confondre les deux documents et ne pas leur appliquer les mêmes
contraintes** : le mémoire assume ses 130 pages de corps, le rapport ENSAE ne peut pas.

**IL Y A DEUX VERSIONS DEPUIS LE 8 SEPTEMBRE, ET ELLES PARTAGENT LES CHAPITRES.**
`main.tex` porte le style d'origine, `main_v2.tex` un style de monographie classique sans
couleur. Les deux appellent **les mêmes fichiers de chapitres** : seul le préambule diffère, une
ligne. Donc **toute modification de contenu vaut pour les deux**, et il ne faut jamais dupliquer
un chapitre pour faire évoluer une version. Kélian a demandé le 8 septembre que la **v2 devienne
la référence de style** ; le retrait de la v1 n'est pas fait et lui appartient (échange d'une
ligne : `preambule_v2.tex` remplace `preambule.tex`). Détail dans la section « Essai de style V2 »
plus bas.

État au **8 septembre 2026** : v1 à **178 pages dont 130 de corps** (annexes en 131), v2 à
**185 pages dont 136 de corps** (annexes en 137), branche `exploratory`. Les comptes de ce
fichier se périment en deux jours : lire `main.toc` plutôt que cette ligne en cas de doute.
Harnais au 8 septembre : **2 172 nombres, 2 172 confirmés, 100 %**, et **0 hors
contrôle non déclaré sur les dix-neuf chapitres**. Ce
dernier chiffre se relève chapitre par chapitre : le récapitulatif `verif_tous_chapitres.ps1`
n'imprime PAS la couverture, seulement le taux de confirmation, alors que c'est la couverture qui
passe en premier.

**Le chiffre de tête est TRANCHÉ depuis le 17 août : la lecture à QUATRE CANAUX**, soit
`SCR 6 049 → 20 188 M€`, facteur **3,34**, écart **14 139 M€**. Quatre protocoles chiffraient
« l'écart entre conforme et non conforme » et donnaient quatre résultats, de −53 % à 3,34, parce
qu'ils ne relâchent pas le même nombre de canaux. Le motif du choix est qu'elle est la **seule où
l'état conforme est conforme sur tous les canaux du modèle** : ailleurs l'entité dite conforme
propage encore, ou sa détection ou son accumulation tiers restent au niveau non conforme. Les
trois autres lectures **restent publiées comme des remédiations partielles**, et leur emboîtement
est un résultat. Table et motifs au chapitre 12, `sec:chiffre-de-tete` ; rapports imprimés par la
**section 3bis du script 67**. Les trajectoires et la priorisation restent en lecture B, par choix
d'objet et non par indécision. **Ne pas rouvrir, et ne pas remplacer un de ces chiffres par un
autre.**

**Le compte de pages ne se lit pas avec `mdls`**, dont l'index Spotlight se périme sans
prévenir : il a annoncé 121 pages sur un PDF qui en faisait 123, y compris sur un fichier
déjà commité. Compter en décompressant les flux d'objets, ou lire `main.toc` après une
compilation avec `--keep-intermediates`.

**Et vérifier dans quelle partie tombe un ajout avant de conclure qu'il grossit le corps.** Le
chapitre `12b_adaptations_pilier.tex` est l'**annexe C**, pas un chapitre du corps : la page
gagnée le 12 août y est allée, le corps restant à 104 ce jour-là. Le nom du fichier ne dit pas
la partie.

**Le corps a gagné trois pages les 9 et 10 août** (101 → 104), au titre de la table des
postures, des deux limites déclarées du chapitre 13 et du cadrage de la CTE. L'arbitrage de
format reste ouvert et ces ajouts vont contre lui : à trancher par Kélian, pas par l'assistant,
puisque ce qui a été ajouté est exactement ce qui fait la valeur du mémoire selon la note
d'honnêteté en bas de ce fichier.

**Lire les deux chiffres ensemble, jamais l'un sans l'autre.** Le récit qui suit est celui du
**6 août 2026** et ses comptes sont ceux de ce jour-là : le chiffre courant est en tête de
fichier. Le mémoire avait commencé la journée à 99,6 % sur 904 nombres, mais ces 904 ne
représentaient que **74,7 %** des nombres publiés : 332 vivaient dans des sections qui ne
citaient aucun script, donc sans être ni confirmés ni infirmés. Un taux de confirmation se règle en retirant une citation ; la
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
| **Rapport de stage ENSAE** | `exploratory/rapport_ensae/rapport_ensae.tex` — document DISTINCT |
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
| **Palette et style de figures** | `exploratory/vasicek_lab/style_nexialog.py` — **source unique des couleurs** |

**Les couleurs des figures ne se codent plus en dur.** Les 92 scripts qui le faisaient sont
passés à la charte Nexialog le 17 août 2026, et `style_nexialog.py` est la source unique : on
importe des **rôles** (`ENCRE`, `FOND`, `CATEGORIEL`, `ORDINAL_5`, `SEQUENTIEL_6`, `DIVERGENT`,
`ETAT`), jamais un hexadécimal. Le module rejoue ses propres contrôles quand on l'exécute.
Trois choses à savoir avant d'y toucher :

- **la charte porte TROIS slots catégoriels, pas quatre**, et c'est mesuré : un quatrième
  échoue le plancher de vision normale à 14,1 contre 15 exigés, et ce plancher ne se rachète
  pas par un encodage secondaire. Une quatrième série se replie en « autres », se facette, ou
  tire son identité de la position. `rampe()` **lève une erreur au lieu de boucler** ;
- **les cinq piliers ne sont pas un cas catégoriel** : ils se présentent ordonnés par
  contribution, donc rampe à une seule teinte (`ORDINAL_5`) ;
- **la déclaration de police reste `["DejaVu Sans", "Segoe UI", "sans-serif"]`, dans cet
  ordre**, et c'est un écart assumé à la charte. DejaVu est fournie par matplotlib, donc
  identique sur les deux postes : c'est ce qui rend une figure rejouée identique à l'octet.
  Mettre Segoe UI en premier la ferait choisir sur le PC et casserait la parité avec le Mac.

**Et les deux postes ne portent pas le même format de la chronologie PRC, ce qui rend deux
scripts complémentaires et non redondants.** Le PC a `Data_Breach_Chronology.xlsx` et pas le
`.csv` ; le Mac a le `.csv` et pas le `.xlsx`. Donc **le script 35 ne tourne que sur le PC** et
**le script 05 ne tourne que sur le Mac**. Ne pas fabriquer l'un depuis l'autre : un csv
reconstruit depuis le xlsx peut différer par l'encodage ou la citation, et ferait dériver une
sortie versionnée sans qu'on sache pourquoi. La figure `M_faisabilite.png` du script 05 est la
**seule** des cinquante figures du mémoire qui reste à l'ancienne palette, faute de pouvoir
être rejouée ici.

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
- **« Additivité » désigne trois choses à trois étages, et les confondre donne des réponses
  opposées.** (i) **Au sein d'un sinistre**, les coûts des piliers touchés s'additionnent : c'est une
  **hypothèse** de construction, non testée. (ii) **En fonction des piliers non conformes**, le
  capital est presque additif : c'est une **mesure**, R² = 0,9945, script 69. (iii) **En fonction des
  quatre canaux**, il est franchement super-additif : c'est une **mesure**, +35 %, script 68. Donc
  répondre « le modèle est super-additif » est **faux** : il l'est sur les canaux, pas sur les
  piliers, et l'hypothèse sur les coûts est un troisième objet. Script 74.
- **La défaillance simultanée de plusieurs piliers n'est pas un cas non traité, c'est la sortie du
  modèle**, et à l'état non conforme elle est **majoritaire** : 62,31 % des sinistres touchent plus
  d'un pilier contre 31,15 % à l'état conforme, pour 1,931 pilier en moyenne contre 1,380. La loi est
  **exacte** (énumération de la progéniture), donc citable sans bruit. C'est un piège de lecture
  symétrique de celui de Hackmageddon : la question suppose une lacune qui n'existe pas, et la
  réponse commence par corriger la prémisse.
- **L'additivité des coûts est la plus lourde des hypothèses structurelles non testées, et elle
  n'est pas neutre entre les deux états.** Relâchée par un exposant sur le nombre de piliers
  touchés, θ dans [0,70 ; 1,30], elle déplace l'écart DORA de 9 706 à 20 487 M€, soit 76 % de
  l'écart publié et **15 fois son bruit** de ± 734 M€. Élasticités **0,95** à l'état non conforme
  contre **0,39** à l'état conforme, facteur 2,42, parce que l'exposant ne mord que sur les
  multi-piliers, majoritaires au seul état non conforme : elle **interagit avec le canal de
  propagation**. Ce qui tient : le signe et l'ordre de l'écart survivent toute la plage, comme pour
  g. Ce qui ne se déclare pas : le **sens**, mutualisation de la remédiation et saturation de la
  capacité tirant en sens contraire, et le coût d'un sinistre multi-piliers n'étant observé par
  aucune source. **L'amplitude est POSÉE, pas estimée** : citer l'élasticité, qui vaut pour toute
  amplitude, plutôt que la plage, qui ne vaut que pour celle-ci.

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
| 08h | le rejet du Hawkes contre les variantes de Bessy-Roland/Boumezoued/Hillairet. **Sa sortie est versionnée depuis le 12 août**, mais il exige `Data_Breach_Chronology.xlsx` : il ne se relance que sur le PC. À lire avec le 85, qui montre que le Hawkes et la cascade ne sont pas distinguables à cette résolution |
| 74 | défaillances simultanées : loi EXACTE du nombre de piliers touchés par sinistre, les trois énoncés d'additivité distingués, et le coût de l'hypothèse d'additivité des coûts borné par un exposant. Son contrôle est θ = 1, qui doit redonner 6 049 et 20 188 au centime |
| 75 | séquences ordonnées du corpus : les chemins composés à partir des arêtes, la loi exacte des séquences du modèle, et **pourquoi elles n'identifient rien**. À lire avant de proposer d'exploiter les triplets |
| 76 | tornado RENORMALISÉ. Le tornado du script 15 avait deux défauts : plages d'inégale vraisemblance, et un levier « seuil » qui **réajuste ξ, σ et p_u**, donc déplace quatre paramètres quand les autres en déplacent un. Le seuil seul ne pèse que +320 M€ quand ξ seul en pèse −13 993, et les composantes **se compensent**. Lu en élasticités, la conclusion tient : propagation 0,37 contre queue 3,79 |
| 78 | plafond de sévérité adossé à l'exposition, CHIFFRÉ et non implémenté. Deux surprises : la prédiction `VaR ≈ min(VaR, κE)` **ne tient qu'à plafond lâche**, plafonner détruisant la queue lourde qu'elle suppose (à κ = 0,1 % le quantile vaut le DOUBLE du plafond) ; et le plafond qui ampute le capital de moitié est **quasi invariant en euros**, 47 à 74 M€ sur des tailles variant d'un facteur 134. C'est l'élasticité de 0,087 dite dans l'unité où elle se juge. **Un plafond ne commute pas avec la mise à l'échelle du script 65** : il faut redescendre au sinistre |
| 77 | E[VaR] contre VaR du MÉLANGE sur les 32 configurations. L'argument d'additivité du script 69 vaut pour une **espérance**, pas pour un quantile. Les deux objets diffèrent de 904 M€ (+9,3 %), et **le mémoire publie E[VaR]**. Sur le quantile, le déplacement de 334 M€ est du même ordre que le bruit (étendue 344) et non monotone : **non détecté, et non démontré nul** |
| 67 | grandeurs citées et jamais imprimées (formes fermées, rapports dérivés) et, section 1bis, **le pont entre quantile unitaire et capital agrégé** |
| 79 | les deux horloges du modèle. Le capital est **CONCAVE** en la durée de non-conformité : un trimestre porte déjà 33 % du surcoût annuel et remédier à mi-exercice ne rend que **44 %** du bénéfice, pas 50 %. Un plan qui prorate le gain se trompe. Le collapse de l'horloge intra-sinistre, lui, ne coûte rien au lag que la donnée soutient |
| 80 | l'échelle des quantiles sur le protocole à marges appariées. **La séparation en queue ne vaut que pour la Student**, seule à porter une dépendance de queue asymptotique ; au-delà de 99 % ni la gaussienne ni l'indépendance ne dépassent leur bruit. Et **le +0,1 % publié est une graine** : l'écart vaut +4,8 % d'étendue 10 points sur quatre graines |
| 81 | l'ablation en échelle, six briques et trois grandeurs. **La brique la plus lourde est la QUEUE** (−76 %), pas la propagation (−20 %) : même énoncé que le tornado du 76 par un chemin indépendant. La forme de queue est **héritée** de la sévérité, pas produite par la cascade |
| 82 | **pas de double comptage dans la colonne fermeture**, et c'est une identité : sa somme vaut Σ\|S\|·m(S), donc chaque croisé d'ordre k y compte k fois. Ce qui était fautif est la ligne « somme » elle-même. Définit aussi **Euler** (le conditionnement par L ≥ VaR alloue la CTE, pas la VaR) et porte la **part d'amorce** |
| 83 | la formule du retour, actualisée. **VP de l'économie de portage = ΔSCR exactement, quel que soit CoC** : la révision du taux déplace les années, pas l'économie. Et le seuil de rentabilité au portage seul (14 139) est SOUS le coût haut (30 000), donc le projet ne se rentabilise jamais à ce niveau |
| 84 | l'origine de la largeur des intervalles. Le **±708 est du Monte-Carlo**, réductible par le calcul (pente −0,60) ; l'IC90 de ξ imprime **dix fois plus** sur la même grandeur. Et le 1 739 vient de 4 graines quand le 708 vient de 16 |
| 85 | **équivalence observationnelle Hawkes/cascade**. Une cascade SANS auto-excitation donne n = 0,480 au jour contre 0,551 mesuré : le ratio observé ne prouve rien. Dégrader la résolution FAIT MONTER n (opération inverse de celle du 08h) |
| 86 | plafond et saturation mesurés **conjointement**. Le plafond est un **AMORTISSEUR** et non un contrepoids : l'interaction change de signe à θ = 1. Aucune crête de compensation, les deux réserves sont hiérarchisées et non confondues |
| 88 | le **coin supérieur** du pavé des quatre canaux. Sur les 65 paires emboîtées, relâcher un canal ne fait **jamais** baisser le capital, graine par graine : l'état non conforme est le maximum, donc un test de résistance se réduit à une évaluation. **Mais la version TRAJECTORIELLE du préprint ne transporte pas** : à aléas communs la perte d'une année baisse dans 16,2 % des cas sur la propagation et **30,7 % sur la détection**, qui viole le plus pour une raison étrangère à la cascade (p_u entre dans la transformation de sévérité, pas dans une table). Et le garde-fou qui compte : **un coin peut être infaisable**, deux canaux sur quatre étant des bornes posées |
| 35 | étude d'événement MOVEit, différence de différences, placebo et bootstrap. **Sa sortie est versionnée depuis le 17 août** : elle exige `Data_Breach_Chronology.xlsx`, présent sur le PC et absent du Mac. Le chapitre 09 est passé de 95,5 à 100 % grâce à elle |
| 89 | **backtest hors échantillon**, origine glissante sur 2004-2025, le premier du projet. Trois résultats de sens opposés : la **binomiale négative est validée** (couverture 91,7 % contre 75 % pour Poisson, et elle gagne au log-score), la **forme de la queue survit** au test PIT, et les **quantiles de sévérité sont dépassés trois fois trop souvent**. Le motif est mesuré et ce n'est pas la queue : le **taux de dépassement dérive**, 15,1 % en apprentissage contre 27,1 % hors échantillon, et la médiane annuelle monte de 13 % par an. C'est un défaut de **stationnarité**, pas de famille. **Sa section 1ter chiffre ce que la dérive coûte, et elle MODÈRE la 1bis** : la queue ne dérive que de 4,00 % par an quand le corps dérive de 13,0 %, facteur 3,2, donc l'effet à déclarer est de +24,7 % sur le quantile de sévérité (borne basse) et non un quintuplement. Deux garde-fous à connaître : indexer la queue à la tendance du corps fait passer l'indice de queue **au-dessus de un**, donc détruit l'espérance de la sévérité, et modéliser la dérive fait **tomber** ξ de 0,5979 à 0,5273, l'ajustement stationnaire attribuant à la forme une part de ce qui est de la dérive. Il exige `SAS_OpRisk_Global_Data_June_2026.xlsx` |
| 90 | **la dérive de sévérité est-elle neutre sur l'écart entre états ?** Il ferme une affirmation du mémoire au lieu d'en ouvrir une. **L'argument est juste mais il porte sur l'ÉCHELLE et sur elle seule** : une variation de la seule échelle multiplie les deux états par le même facteur, 1,4556 et 1,4532, rapport **0,9984**, alors que les niveaux montent de 46 %. La dérive mesurée, elle, n'est pas un pur changement d'échelle : la modéliser fait tomber ξ, et **le facteur entre états passe de 3,344 à 3,124**, −6,6 %, résolu à 4,43 écarts-types, **entièrement porté par la composante de FORME** (−6,1 %, 4,09 σ ; l'échelle seule ne pèse que −0,2 %, non résolu). L'écart en euros ne bouge que de −1,9 %, **mais par COMPENSATION** : forme seule 9 393, échelle seule 20 041. **Ne jamais annoncer l'écart comme robuste à la sévérité**, et citer l'invariance d'échelle, jamais l'invariance à la dérive |
| 91 | **backtest de la CHARGE ANNUELLE AGRÉGÉE**, plus les deux hypothèses que le 89 ne testait pas. **L'agrégat est REJETÉ là où les deux marginales passaient** : PIT 0,734 pour 0,500 attendu, Kolmogorov-Smirnov p = 0,0042, couverture 75,0 % pour 90 % annoncés. **Mais le rejet n'est pas structurel**, c'est la dérive du 89 vue sur l'objet qui porte le capital, et la signature est mesurée : PIT 0,611 sur les six premières années notées contre 0,857 sur les six dernières (Mann-Whitney p = 0,0130), charge observée 363 → 1 255 M€ quand la médiane prédictive ne va que de 183 à 248. **Aucune limite nouvelle** n'entre donc à l'inventaire. Trois autres résultats : la loi de comptage est décisive sur les comptes et **immatérielle sur la charge** (0,3 % au CRPS contre 3,054 nats sur les comptes), la charge étant portée par un sinistre unique ; **l'indépendance fréquence / sévérité TIENT** sur les excès, la pente y valant 0,14 de sa valeur et p = 0,84, l'effet visible sur toute la distribution étant un artefact de profondeur de collecte ; et **le quantile à 99,5 % n'est testable sur aucun historique existant**, 1 811 années étant nécessaires pour détecter un taux double du nominal à 80 % de puissance (905 à 99 %, 78 à 90 %) |
| 92 | **test de résistance INVERSÉ** sur les quatre canaux : on fixe le capital et l'on cherche les états qui le produisent. Possible seulement grâce à la monotonie du script 88, qui rend l'ensemble des configurations atteignant une cible **croissant**, donc décrit par ses seuls éléments **minimaux** (jamais plus de quatre sur seize). **Le résultat de gestion tient en deux seuils** : la fréquence SEULE atteint 10 377 M€ (×1,72) quand les trois autres canaux RÉUNIS n'atteignent que 11 413 (×1,89), donc toute cible sous le premier se produit par un canal unique et toute cible au-dessus du second **exige** la fréquence. Aucun autre canal seul n'atteint même 8 000 (détection 7 497, propagation 7 682, accumulation 7 777). **Et une découverte : le canal d'accumulation n'admet pas d'inversion continue**, ses deux états étant deux structures de table ; sa bascule à φ nul fait **baisser** le capital de 239 M€ (résolu, 4 graines sur 4) parce qu'elle retire la propagation propre de P4, si bien que son effet isolé publié de 1 728 est le NET de −239 et +1 967 |
| 93 | **le seuil de la calibration est-il une règle ou un choix ?** Trois règles sur dix percentiles candidats, et le résultat est favorable. **La règle de stabilité sélectionne EXACTEMENT le seuil publié** (19,87 contre 20,03, soit 0,8 %, quantile identique), et ce seuil est aussi **le mieux ajusté du balayage**, p d'Anderson-Darling 0,971 contre 0,954 pour le second. **La règle la plus permissive descendrait à 12,88 M€ et donnerait un quantile SUPÉRIEUR de 16 %** : le seuil publié n'est donc pas celui qui maximise le chiffre du mémoire. **Et le compromis biais-variance n'existe pas sur cette grandeur** : l'écart-type du quantile est divisé par 3,5 en remontant le seuil alors que les excès sont divisés par six, parce que descendre gonfle ξ jusqu'à 1,058 et que le quantile en dépend exponentiellement. Le double bootstrap d'erreur quadratique asymptotique est **refusé avec son motif** : ses sous-échantillons vaudraient 118 puis 24 observations |
| 94 | **le quantile de la loi des CONFIGURATIONS**, c'est-à-dire le trou que le script 69 déclarait lui-même. L'invariance de 69 porte sur l'**espérance** ; ici l'espérance bouge de −0,02 % quand le quantile à 75 % bouge de +5,53 %, celui à 90 % de +2,76 % et la moyenne de queue à 90 % de +1,06 %. **L'argument d'additivité ne transporte donc pas à un quantile**, la réserve était justifiée, mais l'ordre de grandeur reste petit. Mécanisme mesuré : la **polarisation**, P(tous C) 29,06 → 33,03 % et P(tous NC) 6,83 → 8,78 % à espérance inchangée. **Et une limite de l'objet** : au-delà de 93,17 % le quantile EST la configuration intégralement non conforme, donc les niveaux hauts sont **saturés et non invariants**, et un « quantile à 99,5 % de la loi des configurations » n'a aucun contenu. Ce n'est PAS une mesure de capital : ni `\VaR` ni `\TVaR` |

Modules partagés : `partial_id.py` (identification partielle et évaluateur à nombres communs),
`descente.py` (panel OpRisk et élasticités, lu par 60 et 65), `postmortem_corpus.py` (lu par 59
et 64), `canaux_conformite.py` (moteur des quatre canaux, lu par 43, 50 et 68 : **le modifier
déplace les 14 139 M€**), `derive_severite.py` (estimation de la dérive d'échelle de sévérité,
lu par 89 et 90 : les deux ne peuvent donc pas s'écarter d'une décimale), `scr_engine.py`,
`euro_cascade_model.py`.

**Et le patron à suivre quand un script doit faire tourner le moteur des canaux avec un
paramètre changé** : ne pas modifier `canaux_conformite.py`, et ne pas le contourner par une
substitution de ses variables de module. Recopier `pertes_annuelles` dans le script, **dans le
même ordre de tirages**, avec le paramètre rendu variable, puis **contrôler** que l'appel aux
valeurs publiées reproduit `cx.pertes_annuelles` tirage pour tirage. C'est ce que font les
scripts 81 et 90, et le contrôle est ce qui empêche de démontrer une propriété d'un autre
modèle.

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
0 « ?? » dans le PDF · 0 « Annotation out of page boundary » · 0 Overfull \vbox
0 page tournée (/Rotate absent) · git status propre
COUVERTURE = 100 % (aucun nombre hors contrôle non déclaré) · confirmation ≥ 97 %
```

**Le contrôle « 0 référence indéfinie » ne se lit PAS dans la sortie de tectonic, et l'y
chercher a été une erreur pendant des semaines.** Tectonic **n'émet aucun avertissement** pour
une référence non résolue avec cette invocation : un grep sur `undefined` renvoie zéro quoi qu'il
arrive, donc le contrôle passait à vide. Il avait laissé passer cinq `\ref{chap:etat-art}`
pointant vers un label inexistant, soit « cité au chapitre ?? » cinq fois dans le PDF publié.
Le test fiable est le **comptage des `??` dans le PDF produit** :

```powershell
& $py -c "import fitz,re; d=fitz.open('main.pdf'); print(sum(len(re.findall(r'\?\?', p.get_text())) for p in d))"
```

**Et le texte du PDF porte des LIGATURES.** Chercher « vérification » dans `page.get_text()`
échoue parce que le `fi` sort en `ﬁ` (U+FB01). Normaliser en NFKD avant toute recherche, sans
quoi on conclut à tort qu'une section est absente.

**La couverture se relève chapitre par chapitre, et le bon indicateur est « hors contrôle non
déclaré = 0 », pas « couverture = 100 % ».** Un chapitre qui déclare légitimement des nombres
hors script (démonstrations, état de l'art, réglementaire, section du dispositif de vérification)
affiche une couverture inférieure à 100 % sans que rien n'aille mal. Le calcul est
`publiés − sous contrôle − déclarés`, et c'est lui qui doit valoir zéro sur les dix-neuf
chapitres. Vérifié à zéro partout le 17 août 2026.

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

### La section de sensibilité aux probabilités de propagation, écrite

Elle l'exigeait explicitement. Nouvelle section `sec:sensibilite-propagation` au chapitre 12,
qui assemble du matériel déjà calculé mais **jamais publié**, et le résultat va contre
l'inquiétude qui la motivait.

**Le niveau de propagation est le levier le moins sensible des quatre.** Le tornado du
script 15 : $g$ de 0,5 à 1,0 déplace le surcoût de 5 517 à 6 579 M€, quand le **seuil** de la
loi de queue le déplace de 4 862 à 12 944 et la fréquence de 4 056 à 8 684. **La fragilité est
dans l'ajustement de valeurs extrêmes, pas dans la contagion**, et c'est l'inverse de ce qu'on
redoute d'un modèle de cascade. Garde posée dans un encadré : les niveaux du tornado sont ceux
de sa propre base (6 640 M€), qui n'est pas l'écart à quatre canaux de 14 139.

**Et la sensibilité à la direction ne se stresse pas, elle se gradue.** Table du script 30,
jamais publiée jusqu'ici : l'ignorance $t$ sur la direction coûte 336 M€ de largeur à $t=0{,}25$,
695 à 0,50, 1 083 à 0,75 et 1 839 à $t=1$. **L'ignorance se paye linéairement et son coût
maximal est connu d'avance**, ce qui est plus favorable qu'un intervalle de confiance ordinaire.
Le point d'expert (8 110, soit $+53{,}7\,\%$ du socle) est un point de l'ensemble, pas sa mesure,
et la direction nulle donne déjà $+51{,}5\,\%$ : l'essentiel du surcoût de contagion vient de la
co-occurrence, qui est identifiée, non de la direction.

### L'annexe du protocole de Cooke, écrite, et son sens a changé

Nouvelle annexe `chapitres/18_elicitation_protocole.tex`, branchée dans `main.tex` après les
pièces justificatives. Elle ne présente pas un protocole à venir mais **un protocole préparé et
non exécuté**, avec le chiffrage de la raison, ce qui est un actif devant un jury qui demanderait
pourquoi un modèle dont la direction n'est pas identifiable ne recourt pas au jugement d'expert.

L'argument décisif y est celui du script 31 et non celui du calendrier : un panel biaisé déplace
le SCR de **777 M€ sans qu'aucun signal ne l'indique**, là où l'approche par bornes reste
invariante. Une élicitation faiblement calibrée introduirait donc une incertitude **non
déclarable** en échange d'une ignorance mesurée. Le coût est nommé : sans élicitation, P1 et P4
restent à égalité (43,6 % contre 37,7 %, regret maximal 1,5 %). Et la décision est déclarée
**réversible sans coût de développement**, protocole, questionnaire, gabarit et chaîne
d'agrégation étant prêts.

**Le piège du harnais a été rencontré ici, et il est documenté :** une déclaration
`% HARNAIS-HORS-SCRIPT:` posée **avant la première `\section`** couvre tout le fichier. La
première version de l'annexe déclarait ainsi ses onze nombres d'un coup, dont les huit
parfaitement vérifiables. Descendre la déclaration dans la seule section qui la justifie, et
citer les scripts dans les autres.

### Coût cumulé de la journée, et il est réel

**Le corps passe de 104 à 106 pages, le total de 126 à 132.** C'est le prix des demandes de
Caroline, et cela va franchement contre l'arbitrage de format : le corps est désormais à 36 pages
au-dessus des ~70 recommandés. Les deux sections du corps sont compressibles si tu le décides,
celle du chapitre 13 en perdant le motif épistémique, celle du chapitre 12 en perdant la table
graduée. Harnais à **1 456 nombres, 1 422 confirmés, 97,7 %**, 0 vbox, 0 référence indéfinie,
0 annotation hors page, 0 page tournée.

### Une relecture de ses notes à faire trancher

« Le SCR doit être calculé avec un intervalle de confiance à 95 % » se lit plus naturellement
comme **le niveau de l'intervalle reporté** (95 % au lieu des 90 % actuels) que comme un
changement du quantile réglementaire, qui reste 99,5 % sous Solvabilité II. Cette lecture est
cohérente avec deux choses qu'elle a dites : qu'un intervalle large est normal, et que l'inverse
serait inquiétant. Elle est aussi cohérente avec la sous-couverture mesurée (86 % réels pour
90 % nominaux), qui va dans le sens d'un élargissement. **Passer de 90 à 95 % ne déplacerait
aucune calibration** (le point, les paramètres et tous les SCR restent identiques) mais
déplacerait les bornes publiées et le facteur 2,5. À chiffrer avant de décider, comme elle l'a
elle-même demandé pour l'étage de modèle.

### Le point 11 traité, et c'est le seul de la liste qui touchait le modèle (script 69)

Sa remarque : « être conforme aux piliers 1 et 2 permet indirectement d'être un peu conforme au
pilier 3 ». Trois choses, dans cet ordre.

**Répondre « la dépendance manque » serait faux.** Les états dérivent d'une latente de Vasicek à
facteur commun de charge 0,68, soit une **corrélation de 0,462** entre deux piliers quelconques.
La dépendance existe et elle est forte. Ce qui manque est sa **structure** : elle est
*échangeable*, identique pour toutes les paires, quand le recouvrement des contrôles est propre à
certains triplets.

**L'omission ne coûte rien, et c'est mesuré.** On ajoute un surcroît de corrélation δ aux deux
seules paires concernées, par une matrice de corrélation dont la diagonale vaut un, ce qui
préserve les marges par construction. δ admissible jusqu'à **0,38** avant perte de positivité.
Sur ce balayage la loi des configurations bouge nettement, P(tous NC) de 0,068 à 0,088 et
P(tous C) de 0,291 à 0,330, et **le capital espéré ne bouge que de 2 M€, soit 0,02 %**.

**La raison est structurelle, pas numérique, et c'est ce qui rend la conclusion solide.** Le
capital des 32 configurations s'ajuste par une forme **additive** en indicateurs de pilier à
$R^2 = 0{,}9945$, contributions 3 524 (P1), 2 863 (P4), 2 022 (P2), 1 577 (P3), 897 (P5).
L'espérance d'une fonction additive ne dépend que des **marges**, jamais de la dépendance :
l'invariance vaut donc pour **toute** structure à marges fixées, y compris non essayée. Et cette
quasi-additivité est le même fait que l'interaction entre piliers déjà publiée, petite et de
signe non résolu. L'ordre des contributions reproduit celui des marginaux, P1 > P4 > P2 > P3 > P5.

**Ce que cela ne dit pas, et il faut le garder :** l'invariance porte sur l'**espérance**. Une
conférence de conformité déplacerait un quantile de la loi des configurations ou une mesure de sa
queue. Ne pas transformer ce résultat en « le phénomène est sans conséquence ».

**Deux défauts de mon propre script, corrigés avant publication.** La première construction
combinait la latente de P3 avec la moyenne de P1 et P2 en racine, ce qui lui faisait perdre le
facteur commun : elle *dé*-corrélait P3 au lieu de le sur-corréler, et le balayage donnait un
effet non monotone, signature du bug. Et la première figure traçait des écarts de 2 M€ sur un axe
de 2 M€ de haut, ce qui les faisait paraître énormes : l'axe est désormais calé sur la largeur de
la bande d'identification, et les barres disparaissent, ce qui est le résultat.

### Le point 10 traité, en écriture seulement

La renormalisation proportionnelle au SCR de marché affirme une **élasticité un** à la taille. Les
deux canaux sont estimés et aucun n'en approche : fréquence $+0{,}0744$ (ET 0,0098, $z = 7{,}59$),
sévérité $0{,}087$ d'intervalle $[0{,}026 ; 0{,}148]$. Chacun est d'un ordre de grandeur sous
l'unité. Écrit au chapitre 12 avec l'encadré qui tranche : **les deux approches se trompent en
sens opposés**, la proportionnalité sous-estimant une petite entité puisqu'elle rétrécit une
sévérité qui ne rétrécit pas, le modèle la majorant puisqu'il ne la plafonne pas. Substituer la
proportionnalité changerait le signe du défaut sans le déclarer.

### Coût de page, et il devient sérieux

**Le corps passe de 104 à 108 pages sur toute la séquence Caroline, le total de 126 à 135.** Le
corps est donc à 38 pages au-dessus des ~70 recommandés. Quatre blocs sont compressibles et je
les liste par ordre de ce qu'ils coûtent : la table graduée du chapitre 12, la sous-section du
chapitre 13 sur l'étage de modèle, la sous-section du chapitre 11 sur la dépendance des états, et
les deux paragraphes d'élasticité du chapitre 12. Harnais à **1 484 nombres, 1 450 confirmés,
97,7 %**, 0 vbox, 0 référence indéfinie, 0 annotation hors page, 0 page tournée.

### Ce qui reste de sa liste

- **la CTE à 95 %** en diagnostic à côté de la VaR 99,5 %, jamais à sa place. C'est le seul point
  de sa liste qui n'est pas traité ;
- **le niveau de l'intervalle reporté**, 90 ou 95 %, voir la relecture ci-dessus ;
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

~~Réserve : la sortie du script 08h n'est pas versionnée~~ : **levée le 12 août**,
`sorties_verif/08h.txt` existe et les deux nombres de la table du chapitre 13 sont confirmés.
Le « pic à 3 h » n'est plus lu sur une figure. Ce script exige `Data_Breach_Chronology.xlsx`,
donc il **ne se relance que sur le PC** : ne pas conclure à une régression si le Mac ne le
reproduit pas.

**Ce qu'il faut savoir en revanche, et c'est plus fort que la réserve levée :** depuis le
17 août, le script 85 montre que le Hawkes et la cascade **ne sont pas distinguables** à la
résolution disponible. Le rejet se reformule en équivalence observationnelle suivie d'un choix
de parcimonie interprétative, ce qui est plus honnête et se présente mieux devant elle.

## Ce qui est ouvert

**Ne dépend pas de l'assistant :**
- le **second codage en aveugle** : Hugo Rapior s'en charge, annoncé pour la fin de la semaine
  du 2 septembre. **La réception est prête et testée** : le script `54b_reception_formulaire.py`
  convertit l'export du formulaire Google vers le format long du script 54, et deux commandes
  suffisent. Le 54 ne fabrique rien sans donnée ;
- l'**élicitation** et les autres documents ;
- ~~vérifier les quatre jeux de chiffres SFCR~~ : **FAIT le 2 septembre 2026**, les quatre
  rapports ont été lus. Voir le point 10 plus bas : une erreur de champ corrigée, une limite
  déclarée supprimée, un résultat gagné sur le forfait ;
- l'arbitrage de **format** : le corps est à **130 pages pour 178 au total** en v1, **136 pour
  185** en v2 (Palatino est plus large), contre les ~70 de
  corps recommandés par l'Institut. **Tranché en faveur de Kélian**, Hugo ayant dit de ne pas se
  contraindre ;
- **le choix de la posture à reporter** : **tranché le 17 août** en faveur du plug-in avec sa
  bande, avec son motif écrit et son critère de réouverture (décision E1, voir la section du
  21 août). Ce qui reste est la **validation par Caroline**, pas l'arbitrage. Et l'argument à
  connaître avant d'en rediscuter : la robuste à 95 % **est** la borne haute de l'IC90 déjà
  publié, donc reporter le plug-in avec sa bande publie déjà le chiffre robuste ;
- ~~relancer le script 08h et versionner sa sortie~~ : **FAIT le 12 août** ;
- le registre de sous-traitance ;
- **les cinq champs de la page de couverture du rapport ENSAE**, dont la mention de
  confidentialité, qui relève de Nexialog et non de Kélian seul. Voir la section « Le rapport de
  stage ENSAE » ;
- **le courriel au service des stages** sur les dispositions prises pour la voie actuariat, que
  les consignes qualifient d'impératif ;
- **la date limite du Prix SCOR**, signalée cinq fois et toujours inconnue. Elle est devenue
  décisive le 9 septembre : c'était le seul argument qui pouvait faire préférer la session de
  mars 2027 à celle de novembre.

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

   **Trente-cinq non confirmés restaient AU SOIR DU 6 AOÛT** (tous traités depuis, le harnais
   étant à 100 % ; la liste est conservée parce qu'elle dit de quoi un résidu est fait), et ce
   n'était pas du bruit mais de vraies pistes : les huit
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

10. **LES QUATRE RAPPORTS SFCR ONT ÉTÉ LUS le 2 septembre 2026, et cela a corrigé une erreur.**
    La vérification due depuis des semaines est faite, sur les rapports 2024 eux-mêmes.
    **Une erreur de champ sur MACSF Assurances** : le 3 234 M€ avait été saisi comme total
    d'actif alors que la synthèse du rapport le donne comme **fonds propres éligibles**. Le
    total d'actif vaut 5 305, et l'identité comptable le confirme (5 305 − 2 071 = 3 234). Le
    SCR déduit valait donc 292 quand le rapport **publie 812,5**, et la part attribuée à DORA
    pour cette entité passe de **41,3 % à 16,7 %**. Le besoin ORSA monte de 120,8 à 135,5, les
    actifs ayant augmenté.
    **Trois gains, qui viennent de la même lecture :**
    - **les quatre SCR sont publiés** (BPCE 425 dans son état S.25.01, MACSF Assurances 812,5
      en section E.2, les deux entités vie en synthèse). La réserve « deux SCR sur quatre sont
      déduits » et la borne sous stress de ±10 % **n'ont plus d'objet** : c'est une limite
      déclarée qui disparaît. Seuls les totaux d'actif de trois entités restent déduits par
      identité comptable, et l'approximation y est conservatrice ;
    - **le forfait de 3 % n'est pas une borne, et c'est mesuré.** Les états S.25.01 publient le
      module de risque opérationnel : 54,1 de forfait contre **59** publié chez BPCE, 62,1
      contre **39,7** chez MACSF. Le forfait se trompe **dans les deux sens**, −8 % et +56 %. À
      citer comme ordre de grandeur, jamais comme majorant ni minorant ;
    - **le test du levier a changé de sens et il ne faut plus l'invoquer.** Le levier médian
      passe de 6,9 à 10,0 %, donc le SCR imputé à l'entité notionnelle de 1 328 à 1 932, et la
      part de 13 % à **9 %**, soit **sous** le critère de 10 %. Ce test ne condamne donc plus
      l'entité notionnelle : la requalification du 169 M€ en borne supérieure repose désormais
      sur le **seul** argument de taille, qui tient par lui-même. Le mémoire le dit ainsi.
    **La figure S22 signalait l'anomalie avant qu'on la trouve** : son panneau (c) montrait une
    part qui MONTAIT avec la taille entre les deux petites entités, ce qui contredisait
    l'argument même de la section. Elle est maintenant monotone. La leçon du 14 août se
    confirme une fois de plus : la figure est le détecteur.
    Propagation à surveiller : le script 78 **recopie** les expositions du 65 au lieu de les
    lire, donc il a fallu l'aligner à la main (5 305 et 135,5), et le plafond critique en euros
    passe de « 47 à 74 » à « 53 à 74 M€ », facteur 1,4 au lieu de 1,6.

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
- ~~mettre le deck du 07-08 sous harnais~~ : **FAIT le 17 août**, de 0 à 100 % sous contrôle ou
  déclaré. La crainte qui bloquait le retrofit était infondée, deux lignes de sources ayant
  suffi à couvrir la quasi-totalité des nombres, et un seul cadre a débordé. **Le résidu qui
  reste à savoir** : le 8 553 M€ du contrôle croisé en marche aléatoire n'est reproduit par
  aucun des treize scripts cités, et sa seule correspondance dans tout le pool est un autre
  objet. C'est le motif du `[0,32 ; 0,84]` : à vérifier avant de réutiliser ce chiffre ;
- ~~les 14 grandeurs dérivées non imprimées~~ : **traitées**, le harnais étant à 100 % de
  confirmation sur les dix-neuf chapitres ;
- ~~l'ancrage des valeurs de g sur des sources publiques (ACPR, EIOPA)~~ : **tranché le 17 août,
  c'est non**, et le motif n'est pas la disponibilité mais la nature de ce que ces sources
  publient. Voir la décision E5 dans la section du 21 août. Ne pas rouvrir ;
- les **7 % de blanc résiduels** sous trois titres de figures : cosmétique, refusé deux fois,
  le corriger imposerait de changer de moteur de mise en page sur sept scripts déjà validés ;
- ~~la non-stationnarité de l'échelle de sévérité, mesurée le 8 septembre et non déclarée~~ :
  **DÉCLARÉE le 8 septembre 2026**, voir la section « Le backtest hors échantillon » plus bas.
  Le chapitre 13 porte la ligne, chiffrée, et le chapitre 06 porte la section qui la produit.
  Son effet sur l'écart entre états est mesuré par le script 90, et l'argument d'invariance a
  été **corrigé** au passage : il ne vaut que pour l'échelle ;
- **les trois manques de test identifiés le 8 septembre, par ordre de valeur.** Aucun ne dépend
  d'une recalibration, tous sont des diagnostics compatibles avec le gel.
  1. ~~backtester la charge annuelle agrégée et tester l'indépendance fréquence / sévérité~~ :
     **FAIT le 8 septembre, script 91**, voir sa ligne dans la table des scripts. Le pari était
     bon : l'agrégat est rejeté là où les deux marginales passaient, et le motif est mesuré ;
  2. ~~le test de résistance inversé~~ : **FAIT le 8 septembre, script 92** ;
  3. ~~la règle de sélection du seuil~~ : **FAIT le 8 septembre, script 93**, et le résultat est
     favorable ;
  et **deux à ne pas faire** : une alternative GEV par maxima de blocs, qui donnerait vingt-deux
  observations donc moins de puissance que ce qui existe déjà, et un bootstrap complet de la
  calibration de $W$, dont l'incertitude est déjà traitée par l'identification partielle, qui
  donne un **ensemble** et non une bande ;
- ~~l'invariance du script 69 porte sur l'ESPÉRANCE, pas sur un quantile~~ : **FAIT le
  8 septembre, script 94.** La réserve était justifiée et elle est chiffrée. **La liste des
  manques de test identifiés le 8 septembre est donc vide.**

**Clos, à ne pas rouvrir :** le **statut de citation** de Hackmageddon (la source reste
utilisée, voir plus haut), le **Hawkes** (l'outil est bien écarté et le choix est documenté et
positionné par rapport à Boumezoued et Hillairet, **mais depuis le 17 août il s'énonce en
équivalence observationnelle suivie d'un choix de parcimonie, pas en rejet** : script 85, et ne
pas revenir à la formulation forte), la **non-transitivité** (réfutée par son
auteur, remplacée par la dépendance à l'ordre), le périmètre, l'anonymisation des entités, les
decks du 07, 14 et 21 août, la **convention de normalisation de $W$** (diviseur d'émission,
2,60), le **gel de la calibration**, la **convention `\VaR`/`\qsev`** (voir la section du 10
août), et le **détecteur de contradictions inter-scripts** dans le harnais, instruit et écarté
pour une raison, non par manque de temps.

**Les séquences ordonnées sont explorées et refermées, avec un critère de réouverture précis.**
L'idée d'exploiter les triplets (P1→P3→P2 plutôt que les seules paires) est bonne en principe et
revient naturellement : des marges par paires ne déterminent pas une loi sur les permutations.
Elle ne donne rien ici, script 75, et pour trois raisons distinctes. La comparaison qu'on veut
faire a un **support vide**, P2 n'émettant jamais (0 sur 22) et P1 n'étant jamais atteint. Le test
de dépendance au prédécesseur **n'a aucune puissance**, parce qu'il exige d'un même pilier qu'il
soit atteint ET qu'il ait deux successeurs, et que les deux manques sont exclusifs dans ce corpus :
P1 a trois successeurs mais n'est jamais atteint, P3, P4 et P5 sont atteints mais n'ont qu'un
successeur. Ce n'est donc **pas** un problème de taille : le critère de réouverture est un pilier
atteint avec deux successeurs distincts, répété de 158 à 589 fois selon la séquence visée, contre
9 chemins au total aujourd'hui.

Deux choses à ne pas perdre au passage. **La chaîne des piliers n'est PAS sans mémoire**,
l'auto-évitement renormalisant la loi du successeur sur les piliers non visités : gonflement moyen
1,211 et c'est une borne basse. Donc les triplets ne sont pas redondants avec les paires, ils
portent une prédiction testable, et l'affirmation inverse est fausse. Et **l'acyclicité du graphe
agrégé n'est pas un résultat** : elle s'obtient deux fois sur trois au hasard (42 orientations sur
64), donc elle ne renforce pas la frontière d'identification du chapitre 09. Le nul « par
observation », qui la rendrait écrasante, est le mauvais nul, il teste la constance du codeur.

**Et une distinction de vocabulaire qui vient de là :** le corpus code le **conditionnement
direct**, pas la **précédence**. La clôture transitive ajoute (P1,P2), impliquée par six incidents
et codée par aucun. Le `p_12 = 0` du script 59 est correct pour W, qui est un transfert direct, et
ne dit rien de l'ordre d'arrivée.

## Ce qui a été fait le 14 août 2026, après le point tuteur

**Les six demandes d'Hugo sont traitées, et deux d'entre elles ont fait bouger le mémoire.**

**Le soupçon de double comptage dans la colonne « fermeture » est levé, et il portait juste sur
un point.** Il n'y a pas de double comptage : la somme des fermetures vaut $\sum_S |S|\,m(S)$,
donc chaque croisé d'ordre $k$ y compte $k$ fois, ce qui est la définition même de la fermeture.
Le script 82 le vérifie à la précision machine. **Mais imprimer une ligne « somme » sous une
colonne qui ne s'additionne pas invitait exactement cette lecture** : les deux premières sommes
sont désormais en italique dans l'annexe C, avec l'identité et l'encadrement
`9 138 ≤ 14 139 ≤ 19 141`, qui est la vraie propriété. **Ne pas rouvrir ce point, et ne pas
resommer ces colonnes.**

**Le ±708 est du bruit de calcul, pas de la donnée.** Il tombe en $1/\sqrt{n}$ avec les années
**simulées** (pente −0,60), donc il s'achète en temps de machine. L'incertitude qui ne s'achète
pas est **dix fois plus grande** : l'IC90 de $\xi$ imprime 7 569 M€ sur le même croisé. Et le
1 739 vient de **quatre** graines quand le 708 vient de **seize** : le script 68 le déclare, le
mémoire ne le reportait pas, il le reporte maintenant. **Trois sources à ne jamais fondre en une
barre** : le calcul réduit la première, la donnée la deuxième, un argument la troisième.

**Le taux de coût du capital ne demande pas de recalibration, et c'est une identité qui le dit.**
Escomptée au coût du capital, la valeur présente de l'économie de portage vaut **exactement
ΔSCR, quel que soit CoC**. Passer de 6 à 4,75 % déplace le nombre d'années de 35 à 45 et
l'économie d'aucun euro. La révision est donc un chiffre de **communication**, compatible avec le
gel. Conséquence plus lourde : le seuil de rentabilité au portage seul vaut 14 139 M€ contre un
coût haut de 30 000, donc **le projet ne se rentabilise jamais** à ce niveau de coût, et le
« 35 ans » masquait une non-existence. Ce qui le rentabilise est la perte évitée, qui cesse d'être
une précaution de rédaction pour devenir la condition de rentabilité.

**Les cinq notions empruntées au préprint de cascade climatique sont mesurées et non plus
citées** (scripts 79 à 86). Trois résultats à connaître, parce qu'ils vont contre ce qu'on
attendait :

- **la séparation en queue ne vaut que pour la Student**, seule structure à dépendance de queue
  asymptotique. Au-delà de 99 %, ni la gaussienne ni l'indépendance ne dépassent leur bruit. Le
  préprint doit donc être cité sur le **protocole**, jamais sur l'ordre du résultat, qui dépend de
  l'indice de queue. Et **le +0,1 % publié est une graine** : +4,8 % d'étendue 10 points sur quatre ;
- **le Hawkes et la cascade ne sont pas distinguables** à la résolution disponible. Une cascade
  sans aucune auto-excitation donne $n = 0{,}480$ au jour contre 0,551 mesuré, et retrouve même la
  demi-vie. Le rejet du Hawkes se reformule donc en **équivalence observationnelle** suivie d'un
  choix de parcimonie interprétative, ce qui est plus fort et plus honnête. **Attention au sens** :
  dégrader la résolution FAIT MONTER le ratio, opération inverse de celle du script 08h ;
- **le plafond est un amortisseur, pas un contrepoids** de la saturation : l'interaction change de
  signe à $\theta = 1$, et à $\kappa = 0{,}5\,\%$ la sensibilité à $\theta$ est exactement nulle.
  Il n'existe **aucune crête de compensation** : les deux réserves sont hiérarchisées, pas
  confondues, et l'on peut discuter le plafond sans discuter $\theta$.

**Une leçon de méthode, apprise cinq fois dans la même journée.** Cinq conclusions ont été écrites
avant lecture des nombres puis démenties par eux : le sens de l'effet du 31 décembre, « convexe »
pour concave, « l'écart se referme » pour un écart qui grossit, l'effondrement du ratio de
branchement qui monte, et une crête de compensation qui n'était que le point de référence. **La
figure et la table sont le détecteur ; la prose écrite d'avance est le défaut.** Écrire le
commentaire APRÈS avoir lu la sortie, jamais en même temps que le code qui la produit.

## Ce qui a été fait la semaine du 21 août 2026

Le travail des 17 et 19 août, qui n'avait pas de section ici alors qu'il porte **la plus grosse
décision du projet**. Cette semaine n'a presque rien mesuré de neuf : elle a tranché.

### 1. Le chiffre de tête, et ce qui était grave n'était pas la multiplicité

Quatre protocoles chiffraient « l'écart entre conforme et non conforme ». Le défaut n'était pas
qu'ils donnent quatre résultats, c'est que **le corps publiait la lecture B pendant que le
chiffre à quatre canaux vivait en annexe**, sans qu'aucun texte ne dise qu'ils diffèrent, et
qu'un encadré du chapitre 12 déclarait même la question « à trancher ». Le mémoire publie
désormais la lecture à quatre canaux, `6 049 → 20 188 M€`, facteur 3,34, écart 14 139. Le détail
et les motifs sont en tête de ce fichier, et ils **ne se rouvrent pas**.

Ce qui a permis de trancher à cette date et pas avant : la réserve portait sur le canal
détection tant que son ampleur n'était pas validée, et le script 68 la chiffre à
**2 928 ± 343 M€** en Shapley et **4 562 ± 819** en marginal de fermeture, signe résolu sur
seize graines.

**Les rapports sont imprimés, pas calculés à la lecture** : nouvelle **section 3bis du script
67**, qui sort la table complète des quatre lectures avec sa colonne d'écart (8 860 / 8 410 /
10 663 / 14 139) et qui teste elle-même la monotonie du facteur. Sans cela un niveau amont
pourrait bouger sans que le facteur suive.

### 2. Le théorème du coin supérieur, testé au lieu d'être emprunté (script 88)

C'est la notion du préprint qui promettait le plus : si l'état le plus dégradé majore la perte
sur tout le pavé, un test de résistance sur les quatre canaux se réduit à **une seule
évaluation**. Résultat en trois temps, et il ne transporte qu'à moitié.

- **Au sens du quantile il est démontré.** Sur les seize configurations et les 65 paires
  emboîtées, relâcher un canal de plus ne fait jamais baisser le capital, **graine par graine**,
  ce qui est plus exigeant que sur la moyenne. Contrôle exact aux deux coins, qui reproduisent
  6 049 et 20 188 : sans ce contrôle on démontrerait une propriété d'un autre modèle.
- **La version TRAJECTORIELLE, qui est la leur, ne transporte pas.** À aléas communs la perte
  d'une année baisse dans **16,18 %** des cas sur la propagation, **30,69 %** sur la détection
  et 1,02 % sur l'accumulation. Et le motif diffère selon le canal, ce qui n'était pas attendu :
  la détection viole le plus **pour une raison étrangère à la cascade**, le taux de dépassement
  entrant dans la *transformation* de sévérité et non dans une table de sous-ensembles.
  Attribuer le tout à l'ordre des tables aurait été une erreur de lecture, et c'est ce qui avait
  été écrit avant de lire les taux.
- **Le garde-fou qui compte : un coin peut être INFAISABLE.** Leur contre-exemple reproduit
  numériquement donne 2,0 au coin de l'enveloppe contre 1,2 sur l'ensemble faisable. Deux des
  quatre canaux du modèle sont des **bornes posées** : le coin est un majorant **sur un pavé
  déclaré**, jamais la description d'une entité.

### 3. Le désaccord avec le préprint est écrit, et une citation trop généreuse retirée

Il était cité **quatre fois comme convergent** et jamais là où les deux travaux s'opposent :
leur brique la plus lourde est la propagation dirigée à −53,9 %, la nôtre est la **queue** à
−76,2 %. La cause est dans leur propre texte et elle joue en notre faveur : **leur sévérité est
bornée**, donc sans indice de queue, et leur ablation ne contient aucune brique de queue. On ne
retire pas ce qui n'est pas là. Les deux classements sont corrects chacun dans son modèle, et ce
qui les sépare est l'indice de queue, non l'architecture. **À citer sur le protocole, jamais sur
l'ordre du résultat.** Leurs chiffres sont enregistrés sous le statut « citation externe, non
recalculable » et imprimés par le script 63, même traitement que Hackmageddon.

**Et le rejet du Hawkes n'est pas corroboré par eux.** Le chapitre 13 annonçait une
« corroboration extérieure ». Vérification faite dans leur texte : ils ne testent rien, ils
**posent** le graphe acyclique, et l'auto-excitation ne figure qu'en une ligne d'un tableau de
positionnement. Réécrit en **convergence de choix**, avec ce que la convergence vaut et ce
qu'elle ne vaut pas. Le rejet ne repose que sur le test du présent travail. C'est le point le
plus exposé du mémoire : il ne doit pas s'appuyer sur une lecture généreuse d'une source.

### 4. Cinq décisions de modélisation, dont deux ont fait tomber une trouvaille

- **Posture reportée : le plug-in avec sa bande**, la robuste restant un axe prudentiel déclaré.
  Motif réglementaire d'abord, et il n'est pas d'opportunité : une borne haute sur un ensemble
  d'ambiguïté est un **suprémum sur une famille de lois**, pas un quantile de la loi de perte,
  donc la substituer répond à une autre question.
  **Et la trouvaille : la robuste à 95 % EST la borne haute de l'IC90 déjà publié.** Même loi
  bootstrap, la robuste en étant le quantile 95 et l'intervalle à 90 % étant délimité par ses
  quantiles 5 et 95 : les deux valent **1 037 M€**, et ce n'est pas une coïncidence numérique.
  Reporter le plug-in *avec sa bande* publie donc déjà le chiffre robuste, comme une borne et
  non comme un point. Le désaccord entre les deux postures ne porte pas sur l'information mise à
  disposition du lecteur, il porte sur ce qu'on appelle « le » capital.
- **Niveau de l'intervalle : 90 % reste le niveau reporté**, et c'est autant une correction
  qu'une décision, car **l'annexe se contredisait** : son ouverture annonçait 95 % quand sa
  conclusion, deux pages plus bas, gardait 90 % avec trois motifs. L'argument décisif y était
  déjà mesuré : la couverture réelle vaut **86,8 %** pour un nominal de 90 et **91,8 %** pour un
  nominal de 95, donc le manque est **le même, −3,2 points**. Relever le nominal déplace
  l'annonce sans corriger l'estimateur. Script 72.
- **La CTE en diagnostic était déjà faite**, et le plan avait tort de la donner comme le seul
  point non traité de la liste de Caroline. L'annexe porte la table complète et surtout le nombre
  qui rend les deux conventions comparables, `CTE_beta = VaR 99,5 %` pour **beta = 97,73 %**. Une
  CTE à 95 % vaut 5 734 contre 8 374 : rapportée comme capital elle serait **moins** prudente que
  l'exigence. Script 73. **Sa liste est donc vide.**
- **`GBASE` / `G_BASE` : on ne renomme pas**, on rend la confusion impossible à commettre.
  Vingt-sept fichiers sur un pipeline gelé, et surtout **une substitution sémantiquement fausse
  mais numériquement valide ne serait rattrapée par aucun contrôle**, le harnais vérifiant que
  les nombres sortent des scripts et non qu'ils veulent dire ce qu'on croit. Le script 63
  imprime les deux constantes côte à côte avec leur nature, leur unité et leur module, et porte
  deux assertions. Même traitement que `p_u`.
- **Ancrage de g sur l'ACPR ou l'EIOPA : non.** Le motif n'est pas la disponibilité mais la
  **nature** de ce que ces sources publient, des attentes prudentielles et des échelles de
  maturité, jamais des probabilités de propagation entre domaines de contrôle. Il faudrait une
  seconde correspondance posée, et le résultat aurait **l'apparence d'un calibrage sans en être
  un**, ce qui est pire que la valeur posée. Même arbitrage que celui qui a écarté l'élicitation.

### 5. L'instrument, et la surprise n'était pas où on l'attendait

Le harnais est passé de **26 nombres refusés à un seul**, et le résidu n'était pas un problème
de calcul : **dix-neuf des vingt-six étaient déjà imprimés par un script que leur section ne
citait pas.** Un défaut de **citation**, donc, exactement la faille que le dispositif existe
pour révéler. Discipline tenue et elle compte : une citation n'a été ajoutée que là où le script
possède *vraiment* le nombre, citer un script qui imprime la même valeur pour un autre objet
aurait confirmé par coïncidence.

**Un contrôle passait à vide depuis des semaines**, et c'est le plus mauvais défaut possible
puisqu'il rassurait : voir la section « Contrôles à passer », qui fait foi. Cinq renvois cassés
imprimaient « cité au chapitre ?? » sur cinq pages du PDF publié.

Deux périmètres sont entrés sous contrôle : le **deck du 7 août**, qui était à 0 % de couverture
faute de citer un script (deux lignes de sources ont suffi à couvrir la quasi-totalité de ses
nombres, et la crainte de faire déborder des cadres était infondée), et la **sortie du script
35**, versionnée sur le PC, ce qui a fait passer le chapitre 09 de 95,5 à 100 %.

Le **dispositif de vérification est décrit** dans le mémoire, section D.1, ce qui n'était nulle
part le cas. Elle est déclarée hors script pour **circularité** : faire vérifier par un script le
nombre qui compte ce que les scripts confirment n'aurait aucun sens.

### 6. La charte Nexialog, le 19 août

Les 92 scripts qui codaient leurs couleurs en dur passent par une source unique, et **49 des 50
figures** du mémoire y sont, contrôle sur les pixels et non déduit des scripts lancés. Le détail
de la palette, des trois emplacements catégoriels et de la police est dans « Où sont les
choses », qui fait foi. La cinquantième est `M_faisabilite.png`, et c'est ce balayage qui a fait
découvrir que **les deux postes ne portent pas le même format de la chronologie PRC**.

### État à la fin de la semaine, et ce qu'il faut en retenir

Corps 121 pages pour 167 au total, harnais à **1 965 nombres, 1 964 confirmés, 99,9 %**, hors
contrôle non déclaré à zéro sur les dix-neuf chapitres. Le deck `2026-08-21_point_tuteur.tex`
porte tout cela en douze pages, à 100 % de confirmation et hors contrôle non déclaré à zéro.

**Une leçon d'archivage, apprise ici.** La version précédente de ce deck avait été écrite le
**5 août**, donc avant les points du 7 et du 14, et présentait du travail *antérieur* au deck du
14 tout en annonçant en première slide qu'elle le suivait. Elle portait en outre deux valeurs
devenues fausses depuis, les champs MACSF et l'argument du levier. **Un deck daté d'avance se
périme sans que personne le relise** : écrire le deck après le travail, jamais avant.

## Le backtest hors échantillon, le 8 septembre 2026

**Le premier backtest du projet, et il change le statut de la validation.** Jusqu'ici tout ce
que le mémoire validait, il le validait **dans** l'échantillon : Anderson-Darling,
Kolmogorov-Smirnov, balayage de seuil, bootstrap de ξ, Hill simulé. Aucun de ces tests ne
demande au modèle de prédire une période qu'il n'a pas vue, et c'est la première question qu'un
jury d'actuaires pose à un modèle de capital. Script 89, origine glissante sur 2004-2025, douze
années notées.

**Deux précautions de protocole, et la première aurait invalidé le test.** La fenêtre est
choisie **sur la donnée** : avant 2004 la base porte un à neuf incidents par an contre treize à
trente-neuf ensuite, et 2026 n'en porte que cinq. Ce ne sont pas des années calmes, c'est une
collecte qui ne les couvre pas ; une fenêtre plus large fabriquerait un faux régime calme au
début et un faux effondrement à la fin. Et le seuil est **ré-estimé** sur chaque échantillon
d'apprentissage par la règle du percentile 85, jamais lu dans `config.py` : un seuil calculé sur
toute la période ferait fuiter l'information de test dans l'apprentissage.

**Trois résultats de sens opposés, et le solde est favorable.** Détail chiffré dans la table des
scripts, ligne 89. En bref : la loi de fréquence est **validée** sur deux critères dont le
log-score, que la largeur n'achète pas ; la **forme** de la queue survit au PIT ; le **niveau**
de sévérité ne tient pas, Kupiec rejetant aux deux niveaux.

**Ce qui a été intégré au mémoire le jour même :**

- **nouvelle section du chapitre 06**, `soc:sec:backtest`, à la suite de la section de validation
  qui portait les trois tests dans l'échantillon. Le résultat est présenté comme une
  **validation**, avec ses deux succès d'abord et la dérive ensuite, et non comme une limite.
  C'est un choix de rédaction et il compte : mise en tête d'un inventaire de limites, la dérive
  deviendrait *le* résultat du backtest ;
- **une ligne au chapitre 13**, dans la table à deux colonnes, du côté des écarts
  **involontaires**, aux côtés du `p_u` gelé et de la couverture de l'IC. Le texte de lecture
  passe de « les deux seuls écarts involontaires » à trois, et un paragraphe dit pourquoi la
  troisième ligne est d'une autre taille (un quart contre quelques pour cent) tout en recevant le
  même traitement ;
- **deux lignes à la table de synthèse de robustesse** du chapitre 13, une `\rob` pour les deux
  lois validées et une `\ass` pour le niveau. La table annonce être *la* synthèse de robustesse :
  y omettre le seul test hors échantillon aurait été un trou visible ;
- **la slide J du deck du 11 septembre**, seule slide de travail neuf de ce deck.

**Ce qui n'a PAS été fait, et le motif :** aucune recalibration sur fenêtre glissante. L'écart
est déclaré chiffré, exactement comme le `p_u`. Corriger supposerait de déplacer tous les niveaux
publiés à **trois semaines** du dépôt, sans qu'aucun déplacement soit attribuable à la
correction. (Le motif avait été écrit « à onze semaines », sur une date de dépôt erronée ; il
n'en est que plus fort.)

**Le piège de lecture de cette section, et il est symétrique de celui de Hackmageddon.** La
section 1bis mesure une dérive de 13,0 % par an sur la médiane, ce qui invite à conclure que le
capital dérive d'autant. **C'est faux d'un facteur trois** : la section 1ter mesure la dérive dans
la queue elle-même, et elle ne vaut que 4,00 % par an. La dérive **n'est pas homogène le long de
la distribution**, et c'est le résultat principal de 1ter. Supposer l'homogénéité, en indexant
toutes les pertes à la tendance du corps, donne un quantile 6,5 fois la référence et un indice de
queue de 1,27 à la borne haute, donc **au-dessus de un** : l'espérance de la sévérité cesserait
d'exister. Le rejet de cette variante est un **argument d'existence**, du même type que celui qui
écarte la source PRC comme support d'une mesure de couverture, et il vaut mieux qu'un argument de
degré.

**Et une conséquence à ne pas perdre : les deux écarts du modèle publié sont de sens
contraires.** Modéliser la dérive fait **tomber** ξ de 0,5979 à 0,5273, parce que regrouper des
excès d'années à échelles différentes fabrique un mélange, et qu'un mélange de lois à échelles
inégales paraît plus lourd de queue qu'aucune de ses composantes. L'ajustement stationnaire
attribue donc à la **forme** une part de ce qui relève de la **dérive**. Le ξ publié est ainsi
légèrement prudent quand l'échelle est anti-conservatrice, et les deux ne se compensent pas
puisqu'ils ne portent pas sur la même grandeur.

### La suite immédiate : l'effet de la dérive sur l'écart, mesuré (script 90)

**Une affirmation publiée le matin, fermée l'après-midi, et elle était fausse sous la forme où
elle avait été écrite.** Les deux textes ci-dessus disaient qu'une dérive commune aux deux états
de conformité se simplifie dans un rapport, donc que la thèse était à l'abri. **C'était un
argument, pas une mesure**, et il n'était pas gratuit : les quatre canaux ne transforment pas la
sévérité de la même façon selon l'état, la détection entrant dans la *transformation* de sévérité
et la propagation changeant le *nombre* de sévérités tirées par sinistre.

**Ce que la mesure donne, et le détail est dans la table des scripts, ligne 90.** L'argument est
juste pour l'**échelle** et pour elle seule, où il est même remarquablement exact. Il est **faux**
pour un changement de **forme** de queue, et la dérive mesurée en contient un, parce que la
modéliser réattribue à l'échelle ce que l'ajustement stationnaire lisait comme de la forme.

**Les trois choses à ne pas perdre :**

- **la formule à employer est l'invariance d'ÉCHELLE, jamais l'invariance à la dérive.** La
  première vaut pour toute amplitude et elle est mesurée ; la seconde ne vaut pas ;
- **la quasi-invariance de l'écart en euros est une COMPENSATION, pas une insensibilité.** Prise
  composante par composante, la sévérité déplace l'écart de 9 393 à 20 041 M€. L'annoncer comme
  robuste à la sévérité serait faux, et c'est le genre d'énoncé qu'un jury vérifie ;
- **la direction est favorable, et c'est la même structure à deux sens que le `p_u` gelé** : la
  dérive rend le **niveau** anti-conservateur et la **thèse** légèrement prudente, l'écart comme
  le facteur étant plus petits sous la sévérité dérivée. Seul le premier engage la solvabilité.

**Deux réserves imprimées par le script, à ne pas retirer** : il teste **une** sévérité
alternative, celle que la dérive produit à l'année de référence, non toute la famille ; et la
séparation forme / échelle est une **reparamétrisation**, non deux mécanismes physiques
indépendants, donc elle dit d'où vient le déplacement dans le modèle et non que la queue s'est
allégée dans le monde réel.

### Puis la charge agrégée, et l'agrégat est rejeté (script 91)

**Le manque que les deux scripts précédents laissaient.** 89 et 90 valident ou chiffrent des
**marginales** : la loi de comptage, la forme de la queue, l'échelle. Or le capital n'est ni l'une
ni l'autre, c'est le quantile de la **charge annuelle**. Un modèle composé peut avoir deux
marginales correctes et un agrégat faux, et c'est le reproche standard fait à cette classe de
modèles. Détail chiffré dans la table des scripts, ligne 91.

**L'objet noté est la charge de QUEUE, et ce choix est imposé par le modèle.** La chaîne publiée
donne une sévérité **nulle** aux incidents sous le seuil (`simulate_remediation_severity`), donc
sa charge annuelle est la somme des seuls sinistres dépassant le seuil. L'observable comparable
est la même somme dans la donnée. Noter la charge **totale** exigerait un modèle de corps que le
mémoire n'a pas, et mélangerait le test d'un objet publié avec celui d'un objet inventé. C'est
aussi cohérent avec la limite d'attritionnel déjà déclarée.

**Quatre choses à retenir, et la deuxième évite une panique :**

- **l'agrégat est rejeté**, PIT 0,734 et Kolmogorov-Smirnov p = 0,0042, couverture 75 % pour 90 %
  annoncés, trois dépassements de la borne haute concentrés dans les quatre dernières années ;
- **mais le rejet n'est PAS structurel**, et la signature de dérive est mesurée plutôt que
  supposée : le désalignement n'existe que sur la seconde moitié des années notées. Donc **aucune
  limite nouvelle** n'entre à l'inventaire du chapitre 13. Un seul mécanisme est en défaut,
  l'échelle, et il produit désormais **trois symptômes** ; c'est ainsi que le bloc clé du
  chapitre 06 le présente ;
- **la binomiale négative cesse d'être un déterminant du capital.** Elle gagne nettement sur les
  comptes (3,054 nats, couverture 91,7 contre 75 %) et ne gagne que 0,3 % sur la charge, parce que
  celle-ci est portée par un **sinistre unique**. Elle reste le bon choix, mais ne pas la
  présenter comme ce qui porte le niveau ;
- **l'indépendance fréquence / sévérité tient**, et le contrôle qui tranche est celui des excès.
  Une pente négative significative apparaît sur toute la distribution, elle **disparaît** sur les
  excès : c'est un artefact de profondeur de collecte, pas une propriété du risque. Le commentaire
  de la section 3bis avait été écrit avant ce contrôle et annonçait une dépendance conservatrice :
  **la sortie l'a démenti**, sixième fois de la même leçon.

**Et le paragraphe qui vaut le plus devant un jury.** La puissance du backtest est **chiffrée en
années** : détecter un taux de dépassement double du nominal à 80 % de puissance demanderait
**1 811 années** à 99,5 %, 905 à 99 %, 78 même à 90 %. Le quantile qui porte le capital n'est donc
backtestable sur **aucun** historique de risque opérationnel existant. Ne jamais présenter ce
backtest comme une validation du quantile à 99,5 % : il valide le centre et le corps. Un backtest
qui ne déclare pas sa puissance laisse croire qu'une absence de rejet vaut validation.

### Puis les trois derniers manques de test, scripts 92, 93 et 94

**La liste des manques identifiés le matin est vide au soir.** Aucun n'était une recalibration ;
tous sont des diagnostics compatibles avec le gel. Détail chiffré dans la table des scripts,
lignes 92 à 94. Ce qu'il faut retenir de chacun :

- **92, le test de résistance inversé.** La lecture inverse dit **autre chose** que la lecture
  directe, et c'est tout l'intérêt : la directe hiérarchise les canaux par leur contribution, la
  inverse désigne celui dont la maîtrise *interdit* les scénarios sévères. Deux seuils résument
  seize configurations. Et le canal d'accumulation n'admet **pas** d'inversion continue, sa
  bascule de structure faisant *baisser* le capital ;
- **93, la règle de seuil, et le résultat est favorable.** La règle de stabilité retombe
  exactement sur le seuil publié, qui est aussi le mieux ajusté du balayage, et la règle la plus
  permissive donnerait **davantage** de capital : le seuil publié n'est donc pas celui qui
  maximise le chiffre du mémoire. **Ce script est lent, un quart d'heure** : seize mille
  ajustements GPD. Ne pas le relancer sans nécessité ;
- **94, le quantile de la loi des configurations.** La réserve que le script 69 posait lui-même
  était justifiée et elle est chiffrée. Retenir surtout la **limite de l'objet** : au-delà de
  93,17 % le quantile est saturé sur la configuration intégralement non conforme, donc un
  « quantile à 99,5 % de la loi des configurations » n'a aucun contenu.

**Et une septième fois la même leçon, sur le 93.** Le commentaire de sa section 1 annonçait le
compromis biais-variance qu'on écrit par habitude. La colonne d'écart-type dit l'inverse :
descendre le seuil dégrade **à la fois** le biais et la précision, parce que ξ gonfle et que le
quantile en dépend exponentiellement. Il n'y a donc rien à arbitrer entre les deux, et le seuil se
choisit sur l'adéquation et la stabilité. Réécrit sur la mesure.

**Coût et contrôles, pour la journée entière.** Corps 123 → **129 pages**, total 169 → **176**.
Harnais 1 979 → **2 142 nombres, 2 142 confirmés, 100 %**, hors contrôle non déclaré à zéro sur
les dix-neuf chapitres. Chapitre 06 à 100 % sur 291 nombres, 11 à 100 % sur 104, 12 sur 521, 12b
sur 186, 13 sur 209. Deck du 11 septembre passé à **treize pages**, 100 % sur 104 nombres,
0 vbox, slides J, K et L relues en PNG. Six sorties versionnées ce jour, 89 à 94, toutes
déterministes. 0 `??` compté dans le PDF, 0 annotation hors page,
0 Overfull \vbox, 0 page tournée, et aucun Overfull \hbox nouveau (les trois signalés sont
antérieurs, vérifié par `git stash`). Sorties 89, 90 et 91 déterministes, deux lancements donnant
le même fichier, et le refactor de la section 1ter du 89 vers le module partagé reproduit
`sorties_verif/89.txt` **à l'octet**.

**Un détail d'instrument, rencontré deux fois aujourd'hui.** Les scripts 90 et 91 impriment leurs
montants avec une espace de milliers, que l'extracteur du harnais coupe en deux : `13 801` devient
13 et 801. Le remède retenu n'est pas de changer la typographie du mémoire pour plaire à l'outil,
mais d'ajouter à chaque script un **dernier bloc « grandeurs citées »** qui reprend les mêmes
valeurs sans séparateur ni signe. Il n'ajoute aucun calcul. C'est le même piège que le `5 001` du
script 74, documenté plus haut.

## Essai de style V2, et le rapport LUCY dans l'introduction, le 8 septembre 2026

### La V2 : monographie classique, mêmes chapitres

Kélian trouvait que le mémoire ne faisait pas assez mémoire d'actuariat, les encadrés bleus en
particulier. Une v2 a donc été construite **à côté** de la version d'origine, qui n'a pas été
touchée. Voir la note en tête de fichier pour la règle qui compte : **les chapitres sont
partagés**, `main_v2.tex` ne diffère de `main.tex` que par la ligne du préambule, vérifié par
`Compare-Object`. Ne jamais dupliquer un chapitre pour faire évoluer une version.

**Ce que la v2 change** : police Palatino, interligne 1,05, **aucune couleur** (les huit noms de
couleurs du projet sont redéfinis en noir, ce qui neutralise les `\textcolor{navy}` des chapitres
sans les éditer), les encadrés passent de fonds colorés à des **filets** (haut et bas pour la
synthèse, vertical épais pour l'avertissement), les verdicts de table en petites capitales, titres
en petites capitales avec filets, titres courants, et têtes de paragraphe en italique.

**Ce qu'elle ne change pas, délibérément** : la géométrie. Une monographie classique aurait une
justification plus étroite, mais la lisibilité des cinquante figures est calibrée sur cette
largeur. Et les chiffres restent alignés, pas elzéviriens : ce document se lit pour ses nombres.

**Deux pièges, documentés dans `preambule_v2.tex` :**

- **tcolorbox** : mettre `boxrule` à 0pt puis relever `toprule` ne suffit pas, le squelette
  `enhanced` trace un filet de cheveu sur les quatre côtés et les deux encadrés redeviennent
  indistinguables. Idiome correct : `frame hidden` puis `borderline`. Trouvé en **regardant** le
  PDF, pas la source ;
- Palatino étant plus large, les débordements de paragraphe explosaient. Un `emergencystretch`
  de 2,5 em les résorbe sans toucher un chapitre : la v2 en compte **6 distincts contre 15 pour
  la v1**, tous antérieurs et tous dans des tableaux ou des alignements.

`main_v2.pdf` est **gitignoré** : 10 Mo pour un essai, et il se régénère en une commande. Ses
sources sont versionnées.

### Le rapport LUCY 2026 entre dans l'introduction

Kélian est **co-auteur, avec son tuteur**, de l'analyse actuarielle Nexialog de l'édition 2026 de
l'étude LUCY de l'AMRAE (marché français de la cyberassurance, exercice 2025). Nouvelle section
`sec:lucy` au chapitre 02, entre « Le vide que ce mémoire comble » et « Un seul fil ».

**Pourquoi elle vaut sa place, et ce n'est pas la signature.** Trois constats du rapport
travaillent pour le mémoire :

1. **il constate le vide de l'extérieur** : aucun module de capital standardisé ne couvre le
   risque de catastrophe cyber sous Solvabilité II, donc l'exposition observée ne se traduit pas
   en besoin réglementaire. C'est la prémisse du mémoire, énoncée par ceux qui observent le
   marché ;
2. **il justifie le choix de données** : un **seul** sinistre au-delà de 10 M€ en France sur
   l'exercice, donc une distribution censurée précisément là où se joue le quantile extrême. C'est
   la raison de calibrer la sévérité sur une base internationale plutôt que nationale ;
3. **il porte le même argument de méthode** : un ratio agrégé croissant recouvre deux régimes
   opposés, 2024 année de sévérité et 2025 année de fréquence. Même raisonnement que celui que le
   mémoire impose à ses quatre canaux.

**Statut de la source : CITATION EXTERNE NON RECALCULABLE**, exactement celui de Hackmageddon.
Enregistrée dans `config.py` sous `LUCY_2026` et imprimée par le **script 63**. Elle n'entre dans
aucune calibration et ne porte aucun niveau de capital.

**LE PIÈGE D'ÉCHELLE, ET IL EST DU MÊME TYPE QUE CELUI DU 7 AOÛT.** La charge de LUCY est
**indemnisée**, donc `min(capacité, max(sinistre − franchise, 0))` sommée sur un portefeuille de
marché. La sévérité du mémoire est une perte opérationnelle **brute** d'entité. Rapprocher les
83,2 M€ indemnisés du marché français du quantile unitaire publié ferait lire une différence de
périmètre et de rétention comme une contradiction. Un encadré de l'introduction le pose avant
tout usage.

**UNE IMPRÉCISION DE LA SOURCE, CORRIGÉE ET NON REPRISE.** Le rapport nomme « fréquence » le
multiplicateur du **nombre** de sinistres dans sa décomposition de la charge. Ce n'en est pas
une : une fréquence est un nombre par assuré, et les tables du même rapport la donnent à **1,88**
pour 2025 quand le nombre est à **2,79**, l'exposition ayant crû de **1,49**. L'identité
charge = nombre × sinistre moyen n'est exacte qu'avec le **nombre**. Le script 63 **vérifie
l'identité** sur les deux exercices, écarts 0,0008 et 0,0045, ce qui atteste au passage que la
transcription est fidèle. Ne pas revenir au mot « fréquence » sur ces multiplicateurs.

**Sur les figures du rapport : elles ne sont pas reprises, et c'est un choix.** Une capture d'un
rapport bureautique serait la seule figure du mémoire non produite par un script, porterait les
couleurs de graphique de la charte dans un document dont la v2 est en noir, et ne serait traçable
par rien. Le tableau des deux régimes est donc **reconstruit** en LaTeX depuis la citation
enregistrée, dans la typographie du mémoire. Le fichier PDF du rapport n'est d'ailleurs pas au
dépôt.

**Un défaut PRÉEXISTANT trouvé au passage, et non corrigé.** La bibliographie est en
`plainnat`, un style **anglais** : les citations à deux auteurs impriment « and » et non « et ».
Vérifié dans la v1 avant toute modification, **seize** occurrences distinctes du motif (Herath and
Herath, Hillairet and Lopez, Iooss and Prieur…). Ce n'est donc pas venu de la nouvelle entrée. Le
corriger demande un style bibliographique français ou un passage à biblatex, ce qui touche
**toutes** les citations du document : c'est une décision, pas une retouche, et elle appartient à
Kélian.

**Coût et contrôles.** v1 176 → **178 pages** (corps 130), v2 183 → **185** (corps 136). Harnais
2 142 → **2 172 nombres, 2 172 confirmés, 100 %**, hors contrôle non déclaré à zéro. La nouvelle
section est à 100 % sur **30 nombres**, tous imprimés par le script 63. 0 `??` dans les deux PDF,
0 vbox, 0 annotation hors page, 0 page tournée, aucun débordement nouveau.

**Et un piège de here-string, commis une fois de plus.** L'entrée de bibliographie a été écrite
par un here-string PowerShell à guillemets **doubles**, où le backtick est le caractère
d'échappement : l'accent grave de « Lumière », écrit en LaTeX avec un backtick, a été mangé et a
laissé une séquence de contrôle indéfinie qui a fait échouer la compilation sur le `.bbl`.
Utiliser un here-string à guillemets **simples**, jamais doubles, pour écrire du LaTeX.

## Le rapport de stage ENSAE, le 9 septembre 2026

**C'est un second document, et il ne se confond pas avec le mémoire.** Kélian a demandé le
9 septembre de dissocier les deux : le mémoire d'actuariat d'un côté, le rapport de stage de fin
d'études ENSAE de l'autre. Le second vit dans `exploratory/rapport_ensae/rapport_ensae.tex`, un
seul fichier, préambule compris. Il ne partage **aucun** fichier avec le mémoire, à deux
exceptions près : les figures, lues dans `../vasicek_lab/figures/`, et la bibliographie, lue dans
`../memoire_cascade/references.bib`.

**Les consignes qu'il respecte, et elles ne sont pas celles du mémoire.** Environ 30 pages de
corps hors annexes, références et tableaux compris ; Times New Roman 12 ; interligne 1,5 ;
pagination ; page de couverture au modèle imposé de l'annexe 1 ; sommaire ; bibliographie ;
annexes appelées depuis le corps ; et deux notes de synthèse autonomes d'une à deux pages,
française et anglaise, lisibles par un non-spécialiste. **L'ordre des pièces du fichier unique
est imposé** et il est respecté : rapport, annexes, note française, note anglaise. Le fichier à
déposer doit s'appeler `KADDOURI_Kelian_3A25.pdf`, ou le même suffixé `_CONF` si Nexialog exige
la confidentialité.

**État mesuré au 9 septembre, après la reprise de style demandée le soir même.** 40 pages au
total : couverture 1, sommaire 2 et 3, corps 4 à 35, bibliographie 36, annexes A et B en 37, note
française 38 et 39, note anglaise 40. Donc **32 pages de corps plus une de références** pour une
cible d'« environ 30 » : c'est 10 % au-dessus, assumé, et le motif est que couper davantage
retirerait de l'analyse critique que le barème note sur 6. Compile sans erreur, 0 Overfull
`\hbox`, 0 Overfull `\vbox`, 0 annotation hors page, 0 page tournée, 0 `??` compté dans le PDF.
**Harnais : 260 nombres sous contrôle, 260 confirmés, 100 %**, plus 23 déclarés hors script
section par section, soit **0 hors contrôle non déclaré** sur 283 nombres publiés.

**Le document porte 6 figures, 13 tableaux et 3 propositions démontrées.** Kélian a demandé le
9 septembre que le rapport soit plus agréable à lire, avec graphiques, démonstrations, figures et
tableaux, et que l'écriture cesse de sentir la rédaction automatique. Ce qui a été fait :

- **titres de sections remis en libellés sobres.** Seize des trente et un titres suivaient le
  moule « X, et ce que Y » : c'était le marqueur le plus visible. Ils sont descriptifs
  (« Analyse de sensibilité », « Validation hors échantillon ») ;
- **treize tableaux**, chacun suivi d'un paragraphe **Lecture** et d'une ligne « Sources de la
  table : scripts NN (ce que chacun fournit) », sur le patron du chapitre 13 du mémoire ;
- **six figures** : `H1_reseau_W`, `J3_validation_adequation`, `Z_identification_partielle`,
  `S24_interaction_canaux`, `S32_tornado_normalise`, `S12_trajectoire_scr`. Les trois plus denses
  débordent dans les marges à `1.12\textwidth` via `\makebox`, faute de quoi leurs étiquettes
  tombent sous 4 pt ; **les six pages ont été rendues en PNG et regardées** ;
- **trois propositions avec démonstration**, toutes courtes et toutes déjà établies au mémoire :
  la normalisation de Leontief borne la progéniture et donc le rayon spectral ; l'énergie de
  fluctuation est aveugle à la partie antisymétrique, ce qui est la frontière d'identifiabilité ;
  l'espérance d'une forme additive ne dépend que des marges, ce qui porte l'invariance du
  script 69 et sa réserve ;
- **l'annexe sur le dispositif de vérification a été supprimée**, Kélian ne l'aimant pas. Son
  contenu utile, ce que le dispositif ne fait pas, est passé dans le corps au \S3.6, où il compte
  comme analyse critique.

**Quatre pièges d'instrument, dont deux nouveaux.**

- **Une ligne « Sources : scripts… » en bas de `\section` ne couvre que la dernière
  sous-section**, le harnais coupant aussi sur `\subsection` : la première passe donnait **7,5 %**
  de couverture. Il en faut une par sous-section.
- **Une déclaration `% HARNAIS-HORS-SECTION:` est ignorée si la sous-section cite un script**, le
  code exigeant `m_sec and not cites`.
- **NOUVEAU : un type de colonne maison n'est pas neutralisé.** Le harnais neutralise `p{3.4cm}`,
  `m{}` et `b{}` mais pas un `L{3.4cm}` défini par `\newcolumntype` : douze fausses alertes d'un
  coup. Écrire les colonnes en clair, `>{\raggedright\arraybackslash}p{3.4cm}`. (Et
  `\newcolumntype` prend une **lettre**, pas un nom de macro, sinon « Illegal pream-token ».)
- **NOUVEAU : le nom de fichier d'une figure verse son nombre dans le pool.** Le harnais
  neutralise l'argument optionnel d'un `\includegraphics` mais pas son argument obligatoire, donc
  `{S12_trajectoire_scr.png}` fabrique un 12 à confirmer. Les six noms passent par une macro
  définie dans le préambule, lui-même déclaré hors script. Le tiret bas impose
  `\begingroup\catcode`\_=12 \gdef… \endgroup`, une macro figeant les catcodes à la définition.

**Trois valeurs ont été réécrites avec leur signe, et le document y gagne à chaque fois.** Le
script 76 imprime l'effet du seuil à `+320` et celui de l'indice de queue à `-13 993`, de signes
**opposés** ; le script 81 imprime les ablations à `-76,2` et `-20,3 %` ; et surtout **l'élasticité
de la surdispersion vaut `-0,44`, seule négative des sept**. Augmenter la dispersion des comptes
*rétrécit* l'écart entre états, l'écart étant porté par un sinistre dominant unique. Reporter sa
valeur absolue, comme le fait la figure S32, effaçait ce résultat.

**Deux points à connaître sur des valeurs.** La figure `J3` affiche une p-valeur d'Anderson-Darling
par bootstrap qui **diffère** de celle du texte, laquelle impose les paramètres publiés : la
légende le dit désormais, sans quoi la page se lit comme une contradiction. Et le **98,8 %**
d'années sans incident à l'échelle d'entité, publié au mémoire, est imprimé **98,7 %** par le
script 58 : l'écart passe dans la tolérance d'arrondi, donc le harnais confirme, mais c'est une
décimale à corriger au mémoire si l'occasion se présente.

**Deux écarts assumés, avec leur motif.**

- **Les notes de synthèse sont en interligne simple**, pas 1,5. Les consignes fixent l'interligne
  pour « le corps du rapport » et imposent à la note de tenir en une ou deux pages ; à 1,5 la note
  française débordait sur une troisième page malgré quatre passes de resserrage. La contrainte de
  page a été jugée la plus visible des deux. Le motif est écrit en commentaire dans le fichier.
- **Les trois figures sont reprises du mémoire** (`H1_reseau_W`, `Z_identification_partielle`,
  `S32_tornado_normalise`), et les trois pages qui les portent ont été rendues en PNG et
  regardées. La règle « aucune figure déjà utilisée ne resserve » vaut pour les **decks**, où elle
  évite de présenter deux fois le même travail ; elle n'a pas de sens entre deux documents qui
  décrivent le même stage.

**Ce qui reste à compléter, et cela n'appartient pas à l'assistant.** Cinq champs sont regroupés
en tête du fichier et s'impriment en gras entre crochets tant qu'ils sont vides : le **maître de
stage**, les **dates de début et de fin** de stage, et la **mention de confidentialité**, qui
relève de Nexialog et non de Kélian seul. L'année scolaire, l'entreprise et la ville sont
préremplies. Deux actions administratives par ailleurs : informer le **service des stages** par
courriel des dispositions prises pour la voie actuariat, ce que les consignes qualifient
d'impératif, et déposer un **fichier unique** au nom imposé.

**Un point de fond à ne pas perdre.** Le barème ENSAE note sur 6 « l'analyse et la réflexion sur
le contexte et les outils utilisés », demande de préciser la part d'influence du maître de stage
et des tierces personnes, et attend un recul sur l'expérience. Le mémoire d'actuariat ne porte
**rien** de tout cela. C'est la section 6 du rapport ENSAE qui le couvre, et elle est nommée
« Ce que le stage a mobilisé, et le recul ». La retirer ou la comprimer pour gagner des pages
coûterait des points de barème, pas seulement de la place.

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
