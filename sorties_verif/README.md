# Sorties de scripts, pour la vérification des chiffres

Ce dossier contient la sortie texte des scripts cités par les chapitres du mémoire, une
par fichier `NN.txt`. Il sert d'entrée à `exploratory/memoire_cascade/verif_chiffres.py`,
qui confronte chaque nombre publié aux sorties des scripts que sa section cite.

Sur le PC :

```powershell
cd exploratory\memoire_cascade
..\..\.venv\Scripts\python.exe verif_chiffres.py ..\..\sorties_verif chapitres\12_resultats.tex
```

Sur le Mac, depuis la racine du dépôt :

```bash
.venv/bin/python exploratory/memoire_cascade/verif_chiffres.py \
    sorties_verif exploratory/memoire_cascade/chapitres/12_resultats.tex
```

Quand on régénère un `NN.txt` sur le Mac, rediriger stderr à part : `> NN.txt 2>/dev/null`.
matplotlib y écrit des avertissements de police qui s'intercalent sinon au milieu d'une ligne
de résultats. Le détail est dans la section « Comment construire » du `CLAUDE.md`.

## État du dernier passage (14 août 2026, tous chapitres)

**1 865 nombres vérifiables, 1 831 confirmés, soit 98,2 %**, et surtout **0 nombre hors contrôle
non déclaré sur les dix-neuf chapitres**, relevé chapitre par chapitre et non sur le
récapitulatif, qui n'imprime pas la couverture.

Huit sorties nouvelles, `79.txt` à `86.txt`. Cinq répondent aux notions empruntées au préprint de
cascade climatique, qui n'étaient jusque-là que **citées** ; trois répondent aux demandes du point
tuteur du 14 août. Ce qu'il faut en retenir si l'on reprend le dossier :

`82.txt` **répond au soupçon de double comptage dans la colonne « fermeture », et par une
identité.** Chaque colonne somme des termes de Möbius différents : l'isolée ne prend que l'ordre 1,
la fermeture prend chaque ordre EN ENTIER, Shapley le partage. D'où
`1×9 138 + 2×5 345 + 3×(−691) + 4×346 = 19 141`, à la précision machine. Il n'y a donc pas de
double comptage ; ce qui était fautif est d'imprimer une ligne « somme » sous une colonne qui ne
s'additionne pas. La vraie propriété est l'encadrement `9 138 ≤ 14 139 ≤ 19 141`. Le même fichier
**définit Euler** : conditionner par `L ≥ VaR` alloue la CTE et non la VaR, et les parts publiées
jusqu'ici sont celles de la CTE.

`84.txt` **tranche l'origine de la largeur des intervalles, et la réponse est « ni l'un ni
l'autre ».** Le ±708 n'est pas un intervalle de confiance : c'est un écart-type entre graines à
paramètres fixes, qui tombe de 1 785 à 339 M€ quand les années simulées passent de 10 000 à
160 000 (pente −0,60 contre −0,50 attendu). Il est donc réductible **par le calcul**. L'incertitude
qui ne l'est pas est dix fois plus grande : l'IC90 de ξ imprime 7 569 M€ sur le même croisé. Et le
1 739 vient de **quatre** graines quand le 708 vient de **seize**, ce que le script 68 déclare et
que le mémoire ne reportait pas.

`85.txt` **remplace le rejet du Hawkes par une équivalence observationnelle**, ce qui est plus
fort et plus honnête. Prédiction analytique : dans une cascade, la fraction d'événements qui sont
des enfants vaut `(E[k]−1)/E[k] = 0,482`. Mesure : ajusté sur des dates engendrées par la cascade,
**sans aucune auto-excitation**, un Hawkes trouve `n = 0,480` à la résolution du jour, contre
`0,551` sur la chronologie réelle. Il retrouve même l'horloge, demi-vie 9,0 h pour un lag vrai de
6,7 h. Le 0,551 ne prouve donc rien. **Attention au sens de l'effet de résolution** : dégrader la
résolution fait MONTER le ratio (0,473 à l'heure, 0,739 au mois), parce qu'agréger fabrique du
groupement. C'est l'opération INVERSE de celle du script 08h, qui retire les co-occurrences et
voit le ratio tomber. Les deux encadrent le même fait par les deux côtés.

`83.txt` **documente la formule du retour et règle la question du taux par une identité.**
`T = C/B` reproduit les quatre nombres publiés. Mais escomptée au coût du capital, la valeur
présente de l'économie de portage vaut **exactement ΔSCR, indépendamment de CoC** : passer de 6 à
4,75 % déplace le nombre d'années de 35 à 45 et la valeur présente d'aucun euro. D'où un résultat
que le payback simple cachait : au portage seul, le seuil de rentabilité vaut 14 139 M€ contre un
coût haut de 30 000, donc **le projet ne se rentabilise jamais** à ce niveau de coût.

`79.txt`, `80.txt`, `81.txt` et `86.txt` complètent les notions : la séparation des horloges (le
capital est **concave** en la durée de non-conformité, un trimestre porte 33 % du surcoût annuel),
l'échelle des quantiles (la séparation en queue **ne vaut que pour la Student**, la seule à
dépendance de queue asymptotique), l'ablation en échelle (la brique la plus lourde est la **queue**
à −76 %, pas la propagation à −20 %), et le couple plafond/saturation (le plafond est un
**amortisseur**, pas un contrepoids : l'interaction change de signe à θ = 1).

`75.txt` traite les SEQUENCES ordonnées du corpus de post-mortems, et le résultat est négatif de
trois façons qu'il faut garder distinctes.

Les séquences étaient **déjà dans le corpus**, implicites : chaque incident code un ensemble
d'arêtes, et composer celles d'un même incident donne 9 chemins de longueur deux pour 4 séquences
distinctes. Personne ne les avait extraites.

La comparaison qu'on voulait faire, P1→P2→P3 contre P2→P3→P1, a un **support vide** : P2 n'émet
jamais, 0 fois sur 22 transitions, et P1 n'est jamais atteint. C'est un ensemble vide et non un
intervalle large, donc cela se répond en corrigeant la question.

Le test de dépendance au prédécesseur **n'a aucune puissance**, et la cause est structurelle : il
exige d'un même pilier qu'il soit atteint ET qu'il ait deux successeurs, et les deux manques sont
exclusifs dans ce corpus. Le critère de réouverture est donc précis, et il porte sur la structure
avant le volume : un pilier atteint avec deux successeurs, répété 158 à 589 fois selon la séquence.

**Un acquis positif quand même** : la chaîne des piliers n'est PAS sans mémoire, l'auto-évitement
renormalisant la loi du successeur (gonflement moyen 1,211, borne basse). Les triplets portent donc
une prédiction testable et ne sont pas redondants avec les paires, contrairement à l'intuition.

**Et une prudence à ne pas perdre** : la clôture transitive ordonne 8 des 10 paires et le graphe
agrégé est acyclique, mais cela ne renforce PAS la frontière d'identification. L'acyclicité
s'obtient deux fois sur trois au hasard sur un graphe aussi peu contraint (42 orientations sur 64),
et une clôture ne fournit aucune observation indépendante. Le nul « par observation », qui la
rendrait écrasante à 0,00 %, est le mauvais nul : il teste la constance du codeur, pas l'existence
d'une direction.

`74.txt` répond à la question des **défaillances simultanées** et de l'additivité de leurs coûts.
Trois choses à en retenir pour qui reprend le dossier.

La prémisse de la question était à corriger : la défaillance de plusieurs piliers n'est pas un cas
laissé de côté, c'est la sortie du modèle, et à l'état non conforme elle est **majoritaire**
(62,31 % des sinistres, contre 31,15 % à l'état conforme). La loi du cardinal est **exacte**,
calculée par énumération de la progéniture, donc sans bruit associé.

Le mot « additivité » recouvre **trois énoncés à trois étages** qu'il ne faut pas confondre :
hypothèse non testée sur les coûts au sein d'un sinistre, quasi-additivité **mesurée** en fonction
des piliers (R² = 0,9945, script 69), super-additivité **mesurée** en fonction des quatre canaux
(+35 %, script 68). Répondre « le modèle est super-additif » serait faux.

Le contrôle du script est le point θ = 1, qui doit redonner 6 049 et 20 188 au centime : il le fait.
Deux conclusions écrites en dur avant lecture des nombres ont dû être **inversées**, et c'est le
même travers que le 10 août. J'avais lu le 37,7 % comme la part multi-piliers alors que c'est la
part mono-pilier, et j'en avais tiré que le facteur de cardinal n'atteignait qu'une minorité des
tirages, donc que la sensibilité serait faible. C'est l'inverse : la plage vaut 76 % de l'écart
publié, soit 15 fois son bruit de ± 734 M€, et l'hypothèse est **la plus lourde des hypothèses
structurelles non testées**. Elle n'est pas non plus neutre entre les deux états, élasticités 0,95
contre 0,39, parce que l'exposant ne mord que sur les multi-piliers.

Deux entrées nouvelles ce jour-là.

`68.txt` décompose l'interaction que le script 43 imprimait en résidu. Les deux scripts tournent
désormais sur le **même moteur partagé**, `exploratory/vasicek_lab/canaux_conformite.py` : c'est
la condition pour que la réconciliation du 68 ne soit pas une coïncidence de tirages. Après
extraction, le script 43 reproduit `43.txt` **ligne pour ligne**, au chemin absolu près.

`50.txt` gagne deux sections. Le mot « plancher » y portait sur la durée de retour alors qu'il
qualifie le bénéfice : minorer le bénéfice **majore** la durée, donc la borne était annoncée à
l'envers, dans le script, dans le mémoire et dans le titre de la figure J6. Les trois sont
corrigés. La perte évitée, jusque-là affirmée « majoritaire » sans être chiffrée, vaut
3 247 M€/an contre 848 de portage.

Une correction d'instrument au passage : `verif_chiffres.py` lisait `\begin{column}{0.46\linewidth}`
comme le nombre 0,46. Les `\includegraphics[width=...]` étaient bien neutralisés, les largeurs de
colonne non. Le défaut ne se voyait pas tant que la largeur choisie tombait par hasard sur une
sortie de script, ce qui était le cas de 0,45 et 0,52 dans le deck du 14 : même classe que
`\tfrac12` et `p{4.3cm}`.

## État du passage précédent (6 août 2026, tous chapitres)

**983 nombres vérifiables, 981 confirmés, soit 99,8 %**, plus les exemptions, désormais
comptées et affichées par motif au lieu d'être retirées en silence : niveaux de confiance,
entiers d'énumération, millésimes. Un taux calculé sur une population filtrée sans le dire
n'est pas un contrôle, c'est une mesure de soi-même ; le rapport donne maintenant les trois
lignes.

Le périmètre a été élargi le 6 août sur deux points qui échappaient au contrôle. La valeur
`2,5`, facteur d'incertitude de calibration sur la VaR, et la valeur `19` figuraient dans la
liste d'exemption : le harnais ne les regardait donc nulle part, alors que la première est
un résultat central et l'objet même de l'arbitrage 2,5 contre 2,6. Et la table des paramètres
de l'annexe, celle qu'un jury lit en premier pour savoir ce qui est calibré et ce qui est
posé, ne citait aucun script : elle était entièrement hors contrôle. Elle y entre, ce qui a
fait ressortir sept grandeurs non imprimées, traitées depuis.

Deux non confirmés subsistent, et un seul est un défaut : le `-53 %` de baisse du SCR de
l'état non conforme à l'état conforme, cité dans deux tables de synthèse, qu'aucun script
n'imprime et qu'aucune grandeur publiée ne reproduit (le script 20 donne `-64 %` sous OpRisk
et `-75 %` sous PRC). Sa définition exacte reste à établir avant de le corriger.

### Ancien état (4 août 2026, chapitre Résultats seul)

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
