# Figures externes du mémoire

Ce dossier est une **exception déclarée** à une règle du projet, et il est le seul.

## La règle à laquelle il fait exception

Les cinquante figures du mémoire vivent dans `exploratory/vasicek_lab/figures/` et sont
**produites par un script**, donc rejouables et traçables : on sait quel code les a
dessinées, sur quelle donnée, avec quelle palette. C'est ce qui permet de répondre à un
jury qui demande d'où vient un point.

Les trois figures de ce dossier ne le sont pas. Elles sont **extraites du rapport LUCY 2026
de Nexialog Consulting**, co-écrit par Hugo Rapior et Kélian Kaddouri, lui-même une analyse
de l'édition 2026 de l'étude LUCY de l'AMRAE. Elles portent donc la charte de graphique du
rapport et non celle du mémoire, et aucun script du dépôt ne les redessine.

## Pourquoi elles sont là malgré cela

Décision de Kélian le 9 septembre 2026 : la lecture de marché doit occuper une part
substantielle de l'introduction, de façon à ce que le mémoire situe le risque cyber dans le
marché qui l'assure avant de le charger en capital. Les trois figures sont le support de
cette lecture, et les redessiner aurait supposé de versionner la donnée AMRAE, ce que la
licence interdit.

## Ce qui compense l'absence de script

**Les nombres, eux, sont sous contrôle.** L'intégralité des séries que portent ces figures
est transcrite dans `src/utils/config.py`, sous la clé `LUCY_2026` et sous le statut de
**citation externe non recalculable**, le même que Hackmageddon. Le **script 63** les
imprime, et il en tire **quatre contrôles d'identité** qui valident la transcription :

1. sinistres / primes doit redonner la série des ratios, année par année ;
2. la somme des quatre classes de taille doit redonner la charge annuelle, sur sept
   exercices, soit vingt-huit valeurs contraintes par sept sommes ;
3. la somme des charges des trois blocs doit redonner la charge du marché ;
4. les multiplicateurs transcrits doivent se retrouver depuis les niveaux.

Le quatrième a fait tomber une **coquille du rapport publié** (un multiplicateur de charge
écrit 2,53 pour 3,53) et le premier a fait corriger une valeur relevée de travers sur une
étiquette partiellement masquée. Ces contrôles ne valident pas le rapport, qui est une
source externe : ils valident la transcription, et c'est tout ce qu'ils prétendent.

## Provenance figure par figure

| Fichier | Origine | Retouche |
|---|---|---|
| `lucy_primes_sinistres_ratio.png` | figure 1 du rapport, p. 5 | légende incrustée recadrée, la légende LaTeX la remplace |
| `lucy_divergence_prix_risque.png` | figure de la section 7.3, p. 18 | **légende de couleurs recadrée**, voir ci-dessous |
| `lucy_taille_des_sinistres.png` | figure 8 du rapport, p. 25 | légende incrustée recadrée |

La deuxième est le seul cas où le recadrage retire une information et non un doublon : la
légende de couleurs de la source a ses cartouches qui se chevauchent, et la deuxième ligne se
lit « S/P Entreprises moyennes⬛⬛Taux de prime ETI ». Plutôt que de publier une légende
illisible, la légende LaTeX décrit les trois séries **par position**, de gauche à droite pour
chaque exercice. L'ordre a été vérifié contre les trois valeurs que le corps du rapport donne en
clair pour 2025, soit 22, 42 et 33 %, et il correspond.

**Aucune valeur n'a été modifiée sur ces images.** Les seules retouches sont des recadrages
sous la ligne de légende du rapport, pour éviter deux légendes superposées.

## Une quatrième figure a été écartée, et le motif compte

La figure 2 du rapport (capacité, franchise et taux de prime) n'est pas reprise : sa
légende commune déclare **six** millésimes quand deux de ses trois panneaux en portent
**sept**, le troisième n'en portant que cinq. Le défaut est dans la source et il est
visible. Les trois séries sont donc **reproduites en tableau** dans le mémoire, depuis la
transcription du script 63, ce qui donne la même information sans importer le défaut.

## Ce qu'il ne faut pas en faire

- **ne pas les recolorier** pour les accorder à la charte Nexialog du mémoire : une figure
  retouchée cesse d'être une citation ;
- **ne pas en lire un point** qui ne serait pas une étiquette imprimée. Relever une
  étiquette est licite, mesurer une hauteur de barre ne l'est pas, et c'est la règle posée
  après le « pic à trois heures » du script 08h ;
- **ne pas les rapprocher en niveau des grandeurs du mémoire.** La charge de LUCY est
  **indemnisée**, donc nette de franchise et plafonnée par la capacité, et sommée sur un
  portefeuille de marché ; la sévérité du mémoire est une perte opérationnelle **brute**
  d'entité. L'encadré d'échelle de l'introduction pose ce garde-fou avant tout usage.
