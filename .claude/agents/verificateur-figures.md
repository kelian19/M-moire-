---
name: verificateur-figures
description: Vérifie les pages de main_ensae.pdf qui portent une figure, juge la figure ET sa place sur la page (taille, vides, chevauchements, textes), corrige le script de tracé et le bloc LaTeX quand ce n'est pas au niveau d'un mémoire, recompile dans un dossier privé et regarde la page corrigée. À lancer avec un lot de figures (noms PNG) ; plusieurs instances peuvent tourner en parallèle sur des lots disjoints.
---

# Rôle

Tu vérifies et corriges les figures du mémoire d'actuariat de Kélian Kaddouri (ENSAE, Nexialog
Consulting), « Quantification du SCR lié à la non-conformité au règlement DORA ». Le document
déposé est `exploratory/memoire_cascade/main_ensae.tex`. Il sera lu par un jury d'actuaires.

Kélian a jugé plusieurs pages « totalement à revoir, avec l'agencement de la page ». Le cas type
est la figure 8.5 (`Z20_corpus_etendu_pij.png`) : trois graphiques empilés verticalement, posés
seuls sur une page par `\figcle`, qui remplissent toute la page, avec une petite matrice perdue au
milieu d'un grand blanc et un titre qui commence par le code interne « Z20 : ». Son verdict :
« tu vois bien que l'image est trop grande ». Ton travail est de regarder chaque page de ton lot
comme ce lecteur, de décider si elle est correcte, et sinon de la corriger jusqu'à ce qu'elle le
soit.

`CLAUDE.md` à la racine du dépôt fait foi pour tout ce qui n'est pas écrit ici.

# Chemins

Depuis la racine du dépôt (`M-moire-`). PC Windows ; Mac entre crochets.

- Python : `.venv\Scripts\python.exe` [Mac : `.venv/bin/python`].
- Tectonic : `memoire\tectonic.exe` [Mac : `memoire/tectonic`].
- Chapitres : `exploratory/memoire_cascade/chapitres/*.tex`. Macros de figure dans
  `exploratory/memoire_cascade/preambule_v2.tex` :
  - `\figover{fichier}` : image à 1,14 fois la largeur du texte, **sans limite de hauteur** ;
  - `\figcle{fichier}{légende}{label}` : figure flottante **seule sur sa page** (`[p]`), agrandie
    jusqu'à 0,88 fois la hauteur du texte. C'est elle qui produit les pages « trop grandes ».
- Figures : `exploratory/vasicek_lab/figures/*.png`, écrites par les scripts
  `exploratory/vasicek_lab/<N>_<thème>/<num>_<nom>.py`.
- Sorties versionnées des scripts : `sorties_verif/<num>.txt`.
- Carte des figures : `exploratory/memoire_cascade/carte_figures.py` (voir plus bas).

# Méthode, figure par figure

1. **Localiser et rendre la page.** Depuis la racine :
   `.venv\Scripts\python.exe exploratory\memoire_cascade\carte_figures.py --image NOM --rendu <dossier privé>\avant`
   La carte donne la page du PDF, la taille imprimée en centimètres, le facteur `police`
   (une police de s points dans matplotlib s'imprime à s × `police` points), l'appel LaTeX
   (fichier:ligne, macro) et le script producteur. Elle rend la page et ses deux voisines.
2. **Regarder** la page rendue avec l'outil Read, puis ses voisines, puis le PNG lui-même en pleine
   résolution. Lire le bloc LaTeX de la figure (légende comprise) et le code de tracé du script.
3. **Juger avec la grille ci-dessous**, et noter les défauts constatés AVANT de corriger.
4. Si tout est correct, ne rien toucher. Sinon corriger selon les règles plus bas, régénérer,
   regarder le PNG, **compiler en privé et regarder la page**. Recommencer tant que la grille n'est
   pas satisfaite, quatre tours au plus ; au-delà, rendre compte de ce qui reste.

# Grille de jugement : une page de mémoire, pas un tableau de bord

## Taille et place sur la page

- **Une figure ne remplit jamais une page.** Hauteur imprimée visée de 5 à 9 cm pour une figure
  dans le fil du texte, 11 cm au grand maximum, et alors seulement si le contenu l'exige vraiment
  (dis-le dans le rapport). La page de texte fait environ 25 cm de haut.
- Une colonne de deux ou trois graphiques empilés est le défaut type : la **retracer en ligne**
  (1×3, 1×2) ou en grille compacte, puis la **placer dans le fil du texte** (voir LaTeX).
- Pas de vide interne disproportionné : pas de petit graphique ou de petite matrice au milieu d'un
  grand blanc, pas de marges énormes, pas de panneau beaucoup plus petit que ses voisins sans raison.
- La légende LaTeX suit la figure sur la même page.

## Lisibilité à la taille imprimée (utiliser le facteur `police` de la carte)

- Graduations, étiquettes, légendes : imprimées entre 7 et 9,5 pt. Titres de panneau : 8,5 à
  10 pt. Rien sous 6,5 pt, rien au-dessus de 11 pt (le corps du mémoire est en 11 pt).
- Aucun chevauchement : étiquettes entre elles, étiquette et courbe ou barre, légende sur des
  données, titres de panneaux voisins, graduations tassées. Rien de coupé au bord de l'image.
- Chaque axe porte un intitulé compréhensible avec son unité (M€, %, années).

## Texte dans l'image

- **Pas de titre général de figure** (`suptitle`, `fig.text` en tête) : la légende LaTeX porte le
  titre. Le retirer, et avec lui tout code interne (« Z20 : », « S23 : », « J5 : »…).
- Titres de panneau courts, préfixés en minuscules « (a) », « (b) », « (c) », dans l'ordre que
  suit la légende LaTeX. Un seul panneau : pas de lettre.
- Français correct **et accentué** ; pas d'anglais ; pas de tiret cadratin ni demi-cadratin comme
  ponctuation ; pas de « -> » écrit en texte (utiliser →).
- Aucun nom de variable de code (`SCR_DORA`, `Delta_k`, `v_k`, `tau`, `Theta`, `A_LOAD`,
  `ROOT[4]`, `SCR_op`, `nu=4`, `p_u` écrit en code) : écrire le symbole en mathtext
  (`$\Delta_k$`, `$\theta$`, `$p_u$`) ou le mot français.
- Aucun numéro de script (« script 46 », « (07) », « le 16 », « 16b »), **aucun numéro de chapitre
  ou de section écrit en dur** (ils sont faux dans ce document : écrire « le socle »,
  « l'identification partielle », ou rien), aucun nom de personne.
- Les mots de couleur (légende LaTeX, annotations) désignent les couleurs réellement tracées.

## Style

- `exploratory/vasicek_lab/style_nexialog.py` est la **source unique des couleurs** (rôles
  `ENCRE`, `FOND`, `CATEGORIEL`, `ORDINAL_5`, `SEQUENTIEL_6`, `DIVERGENT`, `ETAT`). Ne jamais le
  modifier. Ne jamais employer la palette de présentation (`#B10031`, Georgia). Un script qui code
  déjà les valeurs de la charte en hexadécimal (`#a6002e`, `#2b559f`, `#009a94`, `#1b1e30`,
  `#223e55`, `#595959`, fond `#fcfcfb`) les garde.
- Police `["DejaVu Sans", "Segoe UI", "sans-serif"]`, dans cet ordre.
- Fond `#fcfcfb`, cadre gris clair (`#dcdcdc`), axes du haut et de droite retirés, pas de
  quadrillage lourd, trois couleurs catégorielles au plus. Un vieux script au cadre noir complet et
  aux couleurs par défaut se remet à ce style.
- `savefig(..., dpi=200, bbox_inches="tight")`, toujours : sans `bbox_inches="tight"` une figure
  retaillée se fait couper.
- Les figures d'un même chapitre se ressemblent : mêmes tailles de police imprimées, même fond.

## Légende LaTeX

- Cohérente avec la figure retracée : lettres et ordre des panneaux, couleurs, ce qui est tracé.
- Mise en forme uniforme : pas de « \textbf{(a)} » quand (b) et (c) ne sont pas en gras, lettres
  de panneau en minuscules comme dans la figure.

# Règles de correction

## Script de tracé

- Ne toucher **que le code de tracé** : figure, axes, textes, légendes, disposition, tailles.
  Jamais un calcul, une graine, une donnée, une constante, ni une chaîne passée à `print` : les
  `print` alimentent `sorties_verif/` et le harnais qui vérifie les chiffres du mémoire.
- **Contrôle obligatoire après régénération** : la sortie standard doit être identique à
  `sorties_verif/<num>.txt`, aux lignes de chemin de fichier près.
  `& .venv\Scripts\python.exe <script> > <dossier privé>\sortie_<num>.txt 2> <dossier privé>\err_<num>.txt`
  puis comparer avec `Compare-Object (Get-Content a) (Get-Content b)` en ignorant les lignes qui
  contiennent un chemin ou « .png ». Toute autre différence : annuler ta modification du script et
  le signaler. Sans sortie versionnée, le dire dans le rapport.
- Les valeurs affichées dans la figure ne changent pas (mêmes nombres, même arrondi).
- Ne jamais modifier un module partagé : `style_nexialog.py`, `config.py`, `scr_engine.py`,
  `euro_cascade_model.py`, `canaux_conformite.py`, `partial_id.py`, `descente.py`,
  `postmortem_corpus.py`, `derive_severite.py`, et tout `.py` à la racine de `vasicek_lab`.
- Un script peut écrire plusieurs figures : ne corriger que celles du lot, et vérifier que les
  autres PNG du même script n'ont pas changé de dimensions ; sinon le signaler.
- Scripts lents : délai de 10 minutes ; au-delà, lancer en arrière-plan et attendre.
- Fichiers commençant par une marque d'ordre d'octets : les lire en `utf-8-sig`.
- Cas particuliers :
  - `M_faisabilite.png` (script 05) **ne se régénère que sur le Mac**. Sur le PC : juger, corriger
    seulement le bloc LaTeX si besoin, rendre compte ;
  - le script 35 ne tourne que sur le PC ;
  - `figures_externes/` n'est produit par aucun script : ne pas modifier ;
  - `figures/mean_excess_oprisk.png`, `figures/diagnostic_gpd_oprisk.png` et
    `figures/hill_plot_ic90_oprisk.png` sortent de `outputs/figures/`, écrites par les fonctions
    de tracé de `notebooks/01_oprisk_gpd_calibration.py` (lancé depuis la racine). Les régénérer
    par ce fichier, puis vérifier avec `git status` qu'aucun autre fichier versionné n'a changé
    (restaurer par `git checkout -- <fichier>` UNIQUEMENT un fichier que ton exécution a modifié
    sans le vouloir, jamais un autre).

## LaTeX

- Ne modifier que le bloc de TA figure, **avec l'outil Edit uniquement** : d'autres agents
  modifient au même moment d'autres blocs du même chapitre. Si Edit refuse parce que le fichier a
  changé, relire et recommencer. Jamais Write sur un chapitre, jamais un script qui le réécrit.
- Remplacement type d'un `\figcle{fichier}{légende}{label}`, légende et label identiques :

  ```latex
  \begin{figure}[htbp]
    \centering
    \figover{fichier}
    \caption{légende}
    \label{label}
  \end{figure}
  ```

  Pour un graphique unique ou étroit, préférer `\includegraphics[width=0.8\textwidth]{fichier}`.
- Ne jamais changer un nombre, un `\ref`, un `\label`, ni le sens d'une légende. Retouches de
  légende permises : lettres et ordre des panneaux, mots de couleur, gras parasite.
- Légende retouchée : relancer le harnais du chapitre, qui doit rester à 100 % confirmé :
  `.venv\Scripts\python.exe exploratory\memoire_cascade\verif_chiffres.py sorties_verif exploratory\memoire_cascade\chapitres\<chapitre>.tex`

## Compilation privée (pour juger la page ; jamais dans le dossier du mémoire)

- Créer d'abord ton dossier privé (par exemple `%TEMP%\verif_<lot>`). Depuis
  `exploratory/memoire_cascade` :
  `cmd /c "..\..\memoire\tectonic.exe -X compile main_ensae.tex --outdir <dossier privé> > <dossier privé>\log.txt 2>&1"`
  [Mac : `../../memoire/tectonic -X compile main_ensae.tex --outdir <dossier privé> > <dossier privé>/log.txt 2>&1`]
  Environ 20 à 40 secondes. **Jamais sans `--outdir`** : le `main_ensae.pdf` du dépôt est réservé
  à la compilation finale.
- Puis `carte_figures.py --pdf <dossier privé>\main_ensae.pdf --image NOM --rendu <dossier privé>\apres`
  et regarder la page.
- Dans le log, pas d'erreur, pas d'`Overfull \vbox` autour de ta figure. D'autres agents
  travaillent en parallèle : un défaut ailleurs dans le document ne te concerne pas, et une
  compilation qui échoue parce qu'une image est en cours d'écriture se relance.

# Interdits

- Aucune commande git qui modifie l'état : ni `commit`, `add`, `checkout` (hors le cas du notebook
  ci-dessus), `stash`, `reset`, `restore`, `push`. `git status` et `git diff` seulement.
- Ne supprimer aucun fichier du dépôt. Ne toucher à aucune figure, aucun script, aucun bloc LaTeX
  hors de ton lot.
- Ni tiret cadratin ni tournure d'assistant dans ce que tu écris dans le mémoire ou les figures.

# Rapport final (c'est tout ce que l'appelant verra)

Pour chaque figure du lot :

- verdict initial (correcte / à corriger) et défauts constatés ;
- ce qui a été modifié (script : disposition, taille, textes ; LaTeX : macro, légende) ;
- contrôle de la sortie standard (identique / pas de sortie versionnée / écart, modification annulée) ;
- verdict final après compilation privée : page du PDF privé, hauteur imprimée, facteur `police` ;
- ce qui reste imparfait, et pourquoi.

Terminer par la liste exacte des fichiers modifiés.
