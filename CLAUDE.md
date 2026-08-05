# Mémoire SCR DORA — contexte de reprise

Document de passation. À lire en entier avant de toucher quoi que ce soit.

## Le projet

Mémoire d'actuariat de Kélian Kaddouri (ENSAE / Nexialog Consulting) :
**« Quantification du SCR lié à la non-conformité au règlement DORA — une cascade dirigée entre
les cinq piliers »**. Objectif affiché : le Prix SCOR, donc le top 1-3 national, pas la simple
validation. Tuteur : Hugo. Point d'avancement hebdomadaire.

État au 5 août 2026 : corps de 94 pages (annexes à partir de la 99, 119 pages au total),
harnais de vérification à 96,1 % sur 915 nombres, branche `exploratory`, dernier commit
`a95f7a3`.

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

Après compilation, **supprimer** `main.aux`, `main.bbl`, `main.out`, `main.toc` : ils ne sont
pas versionnés.

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
cette section cite en `\texttt{NN}`. Tolérance d'arrondi : 0,6 % en relatif, au moins 0,5 en
absolu.

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
0 page tournée (/Rotate absent) · harnais ≥ 96 % · git status propre
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

**Faisable :**
- les **36 nombres non confirmés** restants, à lire un par un : chapitre 12 (13), 06 (7),
  09 (5), 12b (4), 13 (4), 10 (2), 17 (2). Le passage précédent a trouvé deux périmés sur huit
  examinés, dont une table entière non reproductible : ça vaut le coup ;
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
