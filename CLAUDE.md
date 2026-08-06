# Mémoire SCR DORA — contexte de reprise

Document de passation. À lire en entier avant de toucher quoi que ce soit.

## Le projet

Mémoire d'actuariat de Kélian Kaddouri (ENSAE / Nexialog Consulting) :
**« Quantification du SCR lié à la non-conformité au règlement DORA — une cascade dirigée entre
les cinq piliers »**. Objectif affiché : le Prix SCOR, donc le top 1-3 national, pas la simple
validation. Tuteur : Hugo. Point d'avancement hebdomadaire.

État au 6 août 2026, fin de journée : corps de 95 pages (120 pages au total), branche
`exploratory`. Le harnais est à **97,2 % de confirmation sur 1 234 nombres, pour une
couverture de 100 %**.

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
machine. Le mémoire compile en 119 pages, 0 référence indéfinie, 0 annotation hors page,
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
- `W(g) = g · TRANS / max_j(s_j)`, rayon spectral 0,506, sous-critique. `R_0 = 0,062`.
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
| 67 | grandeurs citées et jamais imprimées (VaR/TVaR fermées, rapports dérivés) |

Modules partagés : `partial_id.py` (identification partielle et évaluateur à nombres communs),
`descente.py` (panel OpRisk et élasticités, lu par 60 et 65), `postmortem_corpus.py` (lu par 59
et 64), `scr_engine.py`, `euro_cascade_model.py`.

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
0 page tournée (/Rotate absent) · harnais ≥ 99 % · git status propre
```

Et, pour toute figure modifiée : **l'ouvrir et la regarder**. L'outil Read affiche les PNG. Le
contrôle des proportions ne remplace pas la lecture : quatre défauts de lisibilité réels ont
été trouvés cette semaine sur des figures dont le ratio était correct.

## Ce qui est ouvert

**Ne dépend pas de l'assistant :**
- le **second codage en aveugle** (kit prêt, dix récits, une heure ; script 54 attend le CSV) ;
- l'**élicitation** et les autres documents ;
- **vérifier les quatre jeux de chiffres SFCR** contre les PDF (tableau en tête du script 65,
  deux SCR sur quatre sont déduits d'un taux de couverture) ;
- l'arbitrage sur les **six pages** regagnées par le corps (88 vers 94) ;
- la posture sur la VaR prédictive, le registre de sous-traitance.

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
   Le contrôle de fin de tâche devient **harnais ≥ 99 %** : une fois les grandeurs dérivées
   imprimées et les artefacts de lecture corrigés, le résidu tombe à **quatre** nombres, tous
   irréductibles par nature (l'exposant de $10^{-30}$, deux sommes à $100\,\%$ par
   construction, le niveau de confiance $99{,}9\,\%$).

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
   `\vspace{}`. **Le contrôle de fin de tâche reste harnais ≥ 99 %.**

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

**Le seul non confirmé qui soit un défaut, et il attend une décision :** le **`-53 %`** de
baisse du SCR de l'état non conforme à l'état conforme, cité dans la table de robustesse du
chapitre 13 et dans celle de l'annexe 17. **Aucun script ne l'imprime, et aucune grandeur
publiée ne le reproduit** : le script 20 donne `-64 %` sous OpRisk (6 085 contre 17 012 M€)
et `-75 %` sous PRC. C'est le cinquième de la même famille cette semaine, après les queues
Bâle, le Hill à 1,42, le κ* à 76 % et la plage de $\xi$ « 0,68 à 0,93 ». Il n'a pas été
corrigé parce que sa **définition** reste à établir : à $g$ fixé, en $q$ continu, par entité ?
Ne pas le remplacer par le `-64 %` sans avoir tranché ce point, ce serait échanger un chiffre
non sourcé contre un autre.

7. **Le périmètre du contrôle est passé de 74,7 % à 100 %, et c'est le vrai travail de la
   journée.** Dix-neuf sorties de scripts ont été versionnées (01 à 06, 09 à 13, 15, 24, 25,
   29, 31, 32, 34, 45, 61) et toutes les sections du mémoire ont été rattachées à leurs
   scripts. Ce qui en est sorti :
   - **le chapitre 07, qui porte la contribution centrale, n'était vérifié par rien.** Ses
     67 nombres étaient entièrement hors contrôle. Il est aujourd'hui à 95,5 % sur 67 nombres ;
   - **le `-53 %` n'était pas faux, il était invisible.** Le script 25 l'imprime :
     « gain de conformite (NC->C) : 8861 M de SCR en moins (-53 %) ». Sa sortie n'était pas
     versionnée, voilà tout ;
   - **désaccord de normalisation entre le script 03 et le reste du pipeline, à trancher.**
     Le script 03 transpose TRANS et divise par la **réception** maximale (2,3) ; le reste
     divise par l'**émission** maximale (2,60), qui est la convention du projet. D'où
     $\rho(W) = 0{,}572$ contre 0,506, et un $g$ critique de 1,57 contre 1,78. Le chapitre 07
     publie 0,506 et 1,78 (seconde convention) **et** $R_0 = 0{,}062$ (première) dans la même
     phrase. Les deux lectures restent sous-critiques sur tout le domaine admissible, donc la
     conclusion tient, mais un seul diviseur doit gouverner les nombres publiés. Le script 03
     imprime maintenant les deux lectures et le dit ;
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

**Faisable :**
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
decks du 07, 14 et 21 août.

## Note d'honnêteté

Ce mémoire vaut aujourd'hui environ 17/20 en évaluation interne. Ce qui le tient, c'est qu'il
publie ses propres limites : la non-transitivité qui lui donnait son titre a été réfutée par son
auteur, le chiffre central a été requalifié en borne supérieure, la borne inférieure de validité
de la méthode est publiée, et le harnais signale ce qu'il ne peut pas confirmer. **Ne pas défaire
cela.** Toute reformulation qui rendrait une réserve moins visible dégrade le travail, même si
elle le fait paraître plus assuré.
