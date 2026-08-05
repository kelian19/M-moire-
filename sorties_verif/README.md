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

## Correction du harnais, 5 aout 2026 (remplace la regle ci-dessus)

La regle « dans une sortie de script, un nombre s'ecrit sans separateur de milliers » etait un
contournement. La cause etait dans le harnais : son motif d'extraction ne franchissait pas la
virgule, si bien que « 8,122.9 » devenait DEUX nombres, 8 et 122.9. Deux consequences, la
seconde plus grave que la premiere.

- **Fausses alertes** sur toute la classe des montants a quatre chiffres et plus.
- **FAUSSES CONFIRMATIONS** ailleurs : le jeton « 100,000 » produisait un 100,0 qui confirmait
  a tort un « 99,9 % » a la tolerance d'arrondi pres. Une confirmation a tort est plus grave
  qu'une fausse alerte, puisque personne ne va verifier derriere.

`verif_chiffres.py` recolle desormais les groupes de milliers de forme anglo-saxonne stricte
(1 a 3 chiffres commencant par un chiffre non nul, puis exactement 3 chiffres), ce qui exclut
« 0,807 ». Il reste un cas indecidable, « 2,150 » voulant dire 2,150 en decimal francais ; le
risque est alors une confirmation a tort, et le commentaire du code le dit.

**Il n'est donc plus necessaire de proscrire le separateur dans les scripts.** Les scripts 64,
65, 20b et 62 l'ont perdu au passage, sans inconvenient, mais ce n'est plus une regle.

## Les quatre classes du residu, et la seule qui soit un defaut

Un passage complet sur les dix-neuf chapitres a montre que le residu se repartit ainsi :

1. **separateur de milliers** : corrige dans le harnais ;
2. **unite** : le memoire cite en pourcentage ce que le script imprime en fraction (« 15,8 % »
   contre « 0.158 ») ; le script 67 imprime les deux formes ;
3. **valeur legitimement hors script** : un seuil statistique pose (n = 91 > 30), un point de
   lecture sur un graphique (k = 200), un exposant (10^-30) ; ceux-la ne doivent pas etre
   produits par un script ;
4. **grandeur citee mais jamais imprimee** : la seule classe fautive, objet du script 67.

DEUX CHIFFRES PERIMES trouves par ce passage : la table de severite du chapitre donnees, non
reproductible par aucun filtre du dispositif (elle venait de la version pre-cascade et decrivait
une population de 583 observations qui n'existe plus), et le facteur entre les trois frequences,
reste a 1600 alors que lambda d'entite est passe de 0,21 a 0,092 (vrai rapport : 3719).

ATTENTION : la classification AUTOMATIQUE du residu ne fonctionne pas. Les correspondances
trouvees a un facteur 100 pres sur des nombres ronds sont fortuites, un pool de plusieurs
milliers de valeurs en produit toujours une. Les 36 nombres restants doivent etre lus un par un.
