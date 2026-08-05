# Sorties de scripts, pour la vérification des chiffres

Ce dossier contient la sortie texte des scripts cités par les chapitres du mémoire, une
par fichier `NN.txt`. Il sert d'entrée à `exploratory/memoire_cascade/verif_chiffres.py`,
qui confronte chaque nombre publié aux sorties des scripts que sa section cite.

```powershell
cd exploratory\memoire_cascade
..\..\.venv\Scripts\python.exe verif_chiffres.py ..\..\sorties_verif chapitres\12_resultats.tex
```

## État du dernier passage (4 août 2026, chapitre Résultats)

**339 nombres vérifiables, 306 confirmés, soit 90,3 %.**

Les 33 non confirmés se répartissent ainsi, et aucun n'est une erreur :

| Cause | Nombre | Exemple |
|---|---|---|
| Numéro de script lu comme un résultat | 13 | `script~\texttt{27}` donne 27 |
| Spécification `\cmidrule{6-8}` | 4 | donne 6 et −8 |
| Résolution Monte-Carlo, pas un résultat | 3 | 60 000 années, 150 et 240 mille |
| Arrondi de rédaction | 2 | 122 pour 121,894 ; 8 123 pour 8 122,9 |
| Rapport dérivé de deux valeurs imprimées | 5 | 38 % = 1 − 6 760/10 927 |
| Valeur d'une autre section ou historique | 6 | parts d'amorce ROOT, part cédée à λ = 0,21 |

## Ce que ce passage a effectivement rattrapé

Quatre erreurs réelles dans le chapitre Résultats, toutes corrigées :

1. **multiple de capital 48,6 au lieu de 46,5.** Le nombre était en dur dans la narration
   du script 60 *et* recopié dans le mémoire. C'est exactement la faute que le harnais a
   été écrit pour trouver.
2. **« P1 premier dans 45 % des configurations, P4 dans 36 % »** alors que le script 30
   calcule 43,6 % et 37,7 %.
3. **fourchette d'interaction « −1,9 à +2,1 Md€ »** annoncée sans qu'aucun script ne la
   produise : elle venait de relances manuelles non tracées. Un balayage de six graines a
   été ajouté au script 20b, qui donne −137 à +1 395 M€, quatre positifs sur six. La
   conclusion (le signe n'est pas résolu en VaR, la moyenne reste positive) est inchangée
   et désormais imprimée.
4. **part cédée de référence 63 %** dans le script 60, reconstruite par un rapport approché
   alors que la valeur imprimée par le script 58 était 61 %.

## Règle qui en découle

**Tout rapport cité dans le mémoire doit être imprimé par un script.** Un ratio calculé
pendant la rédaction n'est vérifiable par personne, et trois des quatre erreurs ci-dessus
sont de cette nature.

Les sorties sont purement agrégées : aucun nom de firme, aucune donnée individuelle de la
base sous licence n'y figure.

## Ajouts du 5 aout 2026

Deux scripts nouveaux, et une lecon de harnais.

- **64** biais de narration : loi nulle EXACTE de l'asymetrie par convolution sur les paires
  (plus aucune permutation), jackknife par incident, point de rupture du biais, et effet sur
  la bande de capital d'entite. A a = 0 il reproduit par un chemin de code independant les
  trois chiffres publies au chapitre resultats (169,0 et [131,5 ; 183,3]), ce qu'aucun script
  ne verifiait jusqu'ici.
- **65** entites reelles : le SCR DORA calcule sur les chiffres SFCR publies de quatre
  assureurs francais, avec la provenance de chaque champ (publie / deduit) et la borne
  INFERIEURE de validite de la descente d'echelle, que le memoire publie desormais.

**Deux modules extraits**, pour cesser de recopier ce que deux scripts partagent :
`postmortem_corpus.py` (corpus des post-mortems, lu par 59 et 64) et `descente.py` (panel
OpRisk et elasticites, lu par 60 et 65). Dans les deux cas la sortie du script d'origine a
ete rejouee et comparee caractere par caractere a celle versionnee ici : identique.

**Le separateur de milliers casse le harnais.** Un nombre imprime `2,319` ou `2 319` n'est
pas apparie au `2\,319` du memoire : quinze chiffres de la nouvelle section du chapitre 12
ressortaient non confirmes pour cette seule raison. Les formats `:,.0f` des scripts 64 et 65
ont ete remplaces par `:.0f`. **Regle : dans une sortie de script, un nombre s'ecrit sans
separateur de milliers.**
