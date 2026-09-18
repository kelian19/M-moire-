# Matériel complémentaire du mémoire

Trois annexes du mémoire *Quantification du SCR lié à la non-conformité au règlement DORA*
ont été sorties du document déposé le **18 septembre 2026**, sur décision de Kélian, pour
alléger la lecture. Elles vivent ici et sont destinées à un dépôt numérique pérenne
(GitHub ou Zenodo), dont l'adresse est annoncée en tête des annexes du mémoire.

**Aucun de ces trois fichiers n'est appelé par un fichier maître.** `main_ensae.tex`,
`main.tex` et `main_v2.tex` ne les compilent plus. Les remettre dans `chapitres/` et
rétablir leurs `\input` suffirait à revenir en arrière, mais il faudrait aussi défaire les
cinquante et un `\matcomp` posés dans le corps (voir plus bas).

## Ce que contient chaque fichier

| Fichier | Ancienne place | Contenu |
|---|---|---|
| `15_demonstrations.tex` | annexe B | démonstrations du socle : Fisher-Tippett, Balkema-de Haan, Hill, théorème des types, VaR contre espérance de VaR |
| `17_pieces_justificatives.tex` | annexe D | vingt-deux sections de pièces justificatives : dispositif de vérification, table des paramètres, réconciliations, postures, corrections d'instrument, horloges, plafond et saturation, séquences ordonnées, quantile des configurations, registre des limites |
| `21_complements_corps.tex` | annexe E | dix-huit compléments aux sections du corps : lecture de marché LUCY, cadre réglementaire comparé, Hill, choix du seuil, backtest, sensibilité à la propagation, ancrage d'échelle, détenir contre transférer, corpus étendu, agrégation |

## Ce qu'il faut savoir avant de les compiler à part

Ces fichiers ne sont pas autonomes. Pour en faire un document séparé il faut :

1. **un préambule** : reprendre `preambule_v2.tex` du mémoire, qui porte les macros
   (`\VaR`, `\qsev`, `\figover`, les environnements `cle` et `attention`, les couleurs) ;
2. **les figures** : elles sont lues dans `../../vasicek_lab/figures/` et, pour les trois
   figures LUCY, dans `../figures_externes/` ;
3. **la bibliographie** : `../references.bib` avec le style `../plainnat-fr.bst` ;
4. **accepter les renvois cassés vers le corps** : ces annexes citent des chapitres du
   mémoire qui, eux, ne sont pas ici. Un document autonome imprimera des `??` sur ces
   renvois. Le remède propre est de compiler le mémoire **entier** avec ces trois `\input`
   rétablis, puis d'extraire les pages d'annexe du PDF obtenu : les renvois sont alors
   tous résolus dans les deux sens.

## Les renvois du mémoire vers ces fichiers

Les trois fichiers définissaient **78 étiquettes**. Les **54 renvois** que le corps y
faisait ont été remplacés par la macro `\matcomp`, définie dans `preambule_v2.tex` et dans
`preambule.tex` :

```latex
\newcommand{\matcomp}{\emph{(voir le Matériel Complémentaire en ligne)}}
```

Elle ne contient aucun `\ref`, donc elle est insensible à la disparition des étiquettes :
le mémoire compile à zéro `??`. **Ne pas la remplacer par un `\ref`** tant que ces annexes
sont déportées.

## Ce qui est parti avec elles, et qu'il faut savoir

- **deux des trois figures du rapport LUCY** (divergence prix contre risque, répartition
  par taille de sinistre) vivaient dans l'annexe E et ne sont plus dans le mémoire. La
  troisième, la trajectoire primes, sinistres et ratio, reste : elle est appelée par les
  notes de synthèse. Hugo Rapior avait validé la reproduction des trois le 17 septembre ;
  l'autorisation tient, seul l'usage a changé ;
- **la table des paramètres** avec sa colonne de statut (estimé, posé, gelé), que le
  chapitre 11 annonçait comme l'endroit où aucun chiffre n'est sans origine déclarée ;
- **la description du dispositif de vérification**, que la conclusion et le chapitre du
  stage citaient.

Ces trois pertes sont assumées et signalées ici parce qu'elles portent sur du matériel
qu'un jury peut demander : le lien vers le dépôt doit être en état de marche au dépôt du
30 septembre.

## Le harnais

Ces fichiers ne sont plus balayés par `verif_tous_chapitres.ps1`, qui ne lit que
`chapitres/`. Leurs nombres ne sont donc plus sous contrôle. Au 18 septembre, le mémoire
déposé est à **1 434 nombres publiés, 1 434 confirmés**, hors contrôle non déclaré à zéro.
Si ces annexes reviennent dans le document, il faut repasser le harnais dessus : elles
citaient leurs scripts section par section et étaient à 100 % avant le déport.
