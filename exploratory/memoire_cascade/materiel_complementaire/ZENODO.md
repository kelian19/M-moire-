# Publier le dépôt Zenodo

Ce fichier existe pour une raison précise : le DOI `10.5281/zenodo.22874525` est **déjà imprimé et
cliquable page 156 du mémoire déposé**, et 39 renvois du corps y conduisent par la macro
`\matcomp`. Tant que le dépôt reste un brouillon, ces 39 renvois pointent vers un lien mort.

**État au 23 septembre 2026** : non publié. `https://doi.org/10.5281/zenodo.22874525` et
`https://zenodo.org/records/22874525` rendent tous deux **404**, ce qui est le comportement normal
d'un DOI réservé sur un brouillon.

## La règle qui commande tout le reste

**Publier CE brouillon, jamais en créer un nouveau.** Un nouvel enregistrement recevrait un autre
DOI, et le lien imprimé dans le PDF déposé serait faux. Le corriger imposerait de recompiler le
mémoire et de régénérer les deux fichiers de dépôt.

Et une publication Zenodo **ne se défait pas** : le DOI est enregistré définitivement, les fichiers
deviennent immuables et l'enregistrement n'est pas supprimable par son auteur. Une correction passe
par une nouvelle version, qui reçoit son propre DOI de version pendant que le DOI de concept
continue de résoudre. Donc on vérifie avant, pas après.

## Le fichier à déposer

`materiel_complementaire.pdf`, **70 pages, 0 renvoi non résolu**, reconstruit le 23 septembre 2026.

Le reconstruire d'abord si le mémoire a bougé depuis, la procédure étant dans le `README.md` :
il est extrait d'une compilation du mémoire **entier**, donc ses renvois et sa bibliographie
portent l'état du document au jour de la construction.

## Ce qui a été vérifié sur ce PDF

| Contrôle | Résultat |
|---|---|
| Renvois non résolus | 0 |
| Annexes H, I et J présentes | oui |
| Assureurs nommés | **aucun**, l'anonymisation du mémoire tient ici aussi |
| Donnée sous licence redistribuée | **aucune** : le dépôt ne porte que des sources LaTeX et ce PDF, jamais la base OpRisk |

## Le seul point de décision : la licence

Le PDF embarque les **trois figures du rapport LUCY 2026**. L'autorisation de Hugo Rapior du
17 septembre porte sur leur **reproduction dans le mémoire** mis en ligne par l'Institut. Une
licence ouverte de type CC BY accorderait à quiconque le droit de les **redistribuer**, ce qui est
un acte plus large que celui qui a été autorisé.

**Choix recommandé, qui n'exige aucun accord supplémentaire : CC BY-NC-ND 4.0**, accompagné de la
réserve ci-dessous dans la description. Elle sort les figures de tiers du périmètre de la licence,
ce qui est la pratique courante pour un dépôt ouvert contenant du matériel tiers.

## Métadonnées à coller

**Titre**

```
Matériel complémentaire : Quantification du SCR lié à la non-conformité au règlement DORA, une cascade dirigée entre les cinq piliers
```

**Type** : Publication, puis « Other » (ou « Annex » si la liste le propose).

**Auteur** : Kaddouri, Kélian — ENSAE Paris, Nexialog Consulting.

**Date de publication** : la date réelle de publication du dépôt.

**Langue** : français. **Version** : 1.0.

**Description**

```
Matériel complémentaire du mémoire d'actuariat « Quantification du SCR lié à la non-conformité au règlement DORA, une cascade dirigée entre les cinq piliers » (ENSAE Paris et Nexialog Consulting, 2026).

Ce document rassemble les trois annexes sorties du mémoire pour en alléger la lecture. Elles en conservent la numérotation : le mémoire porte les annexes A à G, ce document prend la suite avec les annexes H, I et J.

Annexe H, démonstrations du socle : les théorèmes de la théorie des valeurs extrêmes mobilisés au chapitre du socle mécaniste.
Annexe I, pièces justificatives : le dispositif de vérification, les réconciliations entre sources, les corrections d'instrument et le registre des limites.
Annexe J, compléments aux chapitres du corps : lecture de marché détaillée, diagnostics de queue, backtests complémentaires, analyses de sensibilité.

Les renvois faits vers les chapitres du mémoire portent les numéros de celui-ci.

Réserve de droits sur les figures de tiers : les trois figures reproduites de l'étude LUCY 2026 restent la propriété de leurs auteurs et sont reproduites avec leur autorisation. Elles ne sont pas couvertes par la licence du présent dépôt et ne peuvent pas être redistribuées séparément.
```

**Mots-clés**

```
DORA ; risque cyber ; Solvabilité II ; besoin de capital ; théorie des valeurs extrêmes ; cascade dirigée ; identification partielle ; bornes de capital
```

**Identifiants liés** : ajouter le mémoire en relation « is supplement to » dès qu'il porte une
adresse stable, celle de la bibliothèque en ligne de l'Institut des Actuaires.

## Après publication, dans cet ordre

1. ouvrir `https://doi.org/10.5281/zenodo.22874525` et vérifier qu'il **résout** ;
2. vérifier que le PDF servi est bien celui de 70 pages ;
3. **seulement ensuite**, déposer `KADDOURI_Kelian_3A25.pdf`.

Déposer le mémoire avant d'avoir vérifié le lien reviendrait à remettre au jury un document qui
renvoie 39 fois vers une page absente.
