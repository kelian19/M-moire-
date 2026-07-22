# Le mémoire : état réel et ce qui reste

Dernière mise à jour : 2026-07-21. **Le document est `main.tex`**, 54 pages compilées.

```powershell
cd exploratory\memoire_cascade
New-Item -ItemType Directory -Force -Path build | Out-Null
..\..\memoire\tectonic.exe -X compile main.tex --outdir build
```

## La thèse

Une défaillance de conformité ne reste pas dans son pilier DORA : elle se propage, **dans
un sens**, et ce sens change le capital. Le mémoire construit ce mécanisme, le traduit en
SCR, et démontre **jusqu'où la donnée permet d'aller** dans son estimation.

## Structure et statut

Document éclaté : `main.tex` (orchestre, 30 lignes) + `preambule.tex` + un fichier par
chapitre dans `chapitres/`.

| Fichier | Statut |
|---|---|
| `01_resume` | réécrit : mène sur la frontière d'identifiabilité et les bornes ; FR + abstract EN |
| `02_introduction` | réécrite : ouverture rédigée, le vide comblé, contribution en 3 points, encadré « ce que le mémoire ne prétend pas » |
| `03_etat_art_positionnement` | intégré ; reste à fusionner l'état de l'art de l'ancien mémoire |
| `04_cadre_reglementaire` | migré de l'ancien mémoire |
| `05_donnees_limites` | migré |
| `06_socle_mecaniste` | migré (EVT + calibration) |
| `07_cascade_dirigee` | rédigé 16/07 ; section faisabilité corrigée (temps inversé dégénéré) |
| `08_proprietes_formelles` | neuf, vérifié (script 32) |
| `09_identifiabilite` | neuf ; + event-study MOVEit (script 35) |
| `10_identification_partielle` | neuf, chapitre central ; + échelle u_ij (script 34) |
| `11_conformite_multietats` | rédigé 16/07, à relire |
| `12_resultats` | rédigé 16/07 ; cadrage corrigé ; chiffres vérifiés à 88 %, interaction corrigée |
| `13_inventaire_hypotheses` | intégré |
| `14_conclusion` | réécrite : établi / non mesurable / régulateur / limites / ouvertures |
| `15_demonstrations`, `16_notations` | migrés |

## Ce qui reste, par ordre de rentabilité

1. **Relire les ~1100 lignes migrées.** Deux audits automatiques (mots-clés de l'ancien
   modèle, puis numérotation de l'ancien document), pas une lecture. Une phrase périmée
   sans aucun de ces motifs passerait au travers.
2. **Compléter le chapitre Résultats** avec le benchmark Formule Standard (0/62/100 % de
   l'effet DORA) et le test VCDB des sous-piliers. Les tableaux actuels restent valides.
3. **Basculer les références du chapitre positionnement dans `references.bib`.** La
   bibliographie ne compte que 4 entrées (les seules en `\citep`, venues de l'EVT) ; les
   ~14 références cyber y sont en liste texte.
4. **Retirer les 4 encadrés `[À migrer]` restants** (renvois « voir aussi » vers les notes
   de travail) avant toute diffusion : bénins mais visibles en orange dans le PDF.
5. **Mener les séances d'élicitation.** Le chapitre 10 démontre qu'elles ne servent qu'à
   départager P1 et P4 et à resserrer la bande ; tant qu'elles ne sont pas faites, la
   couche bayésienne tourne sur le classeur qualitatif.

## Contrôle qualité

`verif_chiffres.py` recalcule les chiffres publiés contre les sorties des scripts et
signale les écarts. À rejouer avant toute diffusion : sur trois scripts de cette session
(01, 34, 35), la même faute a resurgi, une conclusion écrite en dur puis démentie par les
chiffres. Le harnais est le garde-fou.

## Règles de rédaction

Pas de littéraux `«` `»` `§` (glyphes faux sous Tectonic) : `\og … \fg{}` et `\S`. L'euro
s'écrit `\euro{}`. Pas de tirets cadratins. **`W` n'est jamais présenté comme calibré**, et
le niveau absolu du SCR est toujours cadré comme illustratif (démontré au chapitre 10).
