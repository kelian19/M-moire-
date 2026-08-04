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
