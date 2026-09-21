# Phase 1 — Conformité au dépôt

Référentiel : **Recommandations Jury de l'Institut des actuaires, applicables depuis le 1er avril 2026**
(validées par le CA du 20 janvier 2026). Il n'existe pas de consignes d'école distinctes : ce document
est le seul référentiel opposable. Relevé du 21 septembre 2026, document audité `main_ensae.pdf`, 196 pages.

**Le point de vigilance n°2 du prompt est résolu**, et autrement que prévu. Le § 6.5 dit : « Le mémoire
doit faire l'objet d'une note de synthèse **séparée**, en 2 versions : français et anglais. » La question
n'était donc pas de savoir si elles vont en tête ou en fin du mémoire — les deux sont acceptables — mais
qu'un **document distinct** doit exister en plus. Les commentaires périmés de `main_ensae.tex` sont à
corriger, et le livrable séparé reste à produire.

---

## 1. Tableau de conformité

| # | Exigence | Source | Statut | Gravité |
|---|---|---|---|---|
| 1 | Mémoire rédigé en français | § 5.1.a | ✔ conforme | — |
| 2 | Page de garde **homogénéisée**, commune à toutes les filières | § 5.1.b | ✘ **la version Institut ne se compile plus** | critique |
| 3 | Page de garde **signée par l'étudiant et le responsable du stage** | § 5.1.b | ✘ **aucun champ de signature** | critique |
| 4 | Résumé FR **150 à 250 mots** | § 5.1.c | ✘ **547 mots** | majeure |
| 5 | Résumé EN **150 à 250 mots** | § 5.1.c | ✘ **367 mots** | majeure |
| 6 | Mots-clés | § 5.1.c | ✔ 10 mots-clés, p. 5 | — |
| 7 | **Phrases sur l'usage de l'IA générative, à la fin du résumé et distinctes de lui** | § 5.1.c | ✘ **absent** | **critique** |
| 8 | Introduction de 2 à 3 pages | § 5.1.d | ⚠ absorbée dans un ch. 1 de 15 pages | mineure |
| 9 | Corps d'environ 70 pages | § 5.1.e | ⚠ ~130 pages — **écart assumé** | mineure |
| 10 | Conclusion de 2 à 3 pages | § 5.1.f | ✔ 3 pages (p. 149–151) | — |
| 11 | Bibliographie alphabétique, toute entrée citée | § 5.1.g | ✔ 56 clés, toutes citées et résolues | — |
| 12 | Annexes précédées d'un **plan des annexes** | § 5.1.h | ✔ notice p. 158 | — |
| 13 | Annexes en **pagination à part**, numérotées | § 5.1.h | ✘ pagination continue, lettrage A–E | mineure |
| 14 | **Le corps doit être complet sans recours aux annexes** | § 5.1.h | ✘ **matériel déporté hors du PDF** | critique |
| 15 | **Annexe exigée : pistes pour de futurs mémoires** | § 5.1.h | ✘ **absente** | **critique** |
| 16 | **Annexe exigée : inventaire de l'usage de l'IA générative** | § 5.1.h | ✘ **absente** | **critique** |
| 17 | Ton impersonnel, éviter « je », « nous », « on » | § 5.2 | ✔ 2 occurrences, toutes deux légitimes | — |
| 18 | **Note de synthèse séparée, FR et EN** | § 6.5 | ✘ livrable distinct non produit | majeure |
| 19 | Support de présentation, oral de 25 min max | § 6.6 | hors périmètre de ce dépôt | — |
| 20 | Note de contexte (facultative, 2 pages, jury seul) | § 6.4 | ○ opportunité non saisie | — |
| 21 | Demande de confidentialité formulée avant la soutenance | § 5.4 | ✔ non confidentiel, décision du 16 sept. | — |
| 22 | Lien du dépôt numérique fonctionnel | — | ✘ `LIEN_VERS_LE_DEPOT.com` | critique |

---

## 2. Les constats critiques

### F1 — L'usage de l'IA générative n'est déclaré nulle part, et la sanction prévue est l'ajournement · **critique**

**Où** : absent du résumé (p. 5), absent des annexes, absent du chapitre du stage.
`chapitres/19_enseignements_stage.tex:16-18`.

**Constat.** Le mémoire ne comporte aucune mention d'outil d'IA générative. Ce n'est pas un oubli : une
consigne écrite en tête du chapitre du stage l'impose.

> « AUCUNE MENTION D'OUTILS D'INTELLIGENCE ARTIFICIELLE GÉNÉRATIVE, de près ni de loin. Le paragraphe
> d'usage qui existait depuis le 16 septembre est supprimé. Ne pas le réintroduire. »

Le référentiel dit l'inverse, à trois endroits :

- **§ 4.5** : « La transparence quant à l'usage de l'intelligence artificielle doit être totale.
  **Tout manquement à cette règle conduira l'étudiant à être ajourné par le jury, sans besoin d'une
  autre motivation.** »
- **§ 5.1.c** : « En complément et à la fin du résumé et distinct de ce dernier, quelques phrases
  concises mentionneront l'usage effectué de l'intelligence artificielle générative tant au cours des
  travaux que dans la rédaction du mémoire. »
- **§ 5.1.h** : l'inventaire de cet usage est l'**une des deux annexes exigées**. « Cet inventaire se
  doit d'être exhaustif et doit comprendre les mesures prises pour vérifier la validité des résultats. »

**Risque devant le jury.** C'est le seul manquement du référentiel dont la sanction soit écrite, nommée
et automatique : ajournement, sans qu'aucune autre motivation ne soit requise. Il ne se rattrape pas en
soutenance.

Et le risque est matériel, pas théorique. **Le dépôt GitHub est public** — `REPRISE.md:505` le déclare,
et le clone de ce matin s'est fait sans authentification, ce qui le confirme. Ce dépôt contient
`CLAUDE.md`, un dossier `.claude/agents/` avec quatre agents de relecture, un journal de session qui
décrit jour par jour le travail d'un assistant, et des commits co-signés. Un juré qui cherche le
matériel complémentaire promis p. 158 arrive sur ce dépôt.

**Correction.** Écrire les deux pièces que le référentiel demande : le paragraphe en fin de résumé, et
l'annexe d'inventaire. Le § 4.5 n'interdit pas l'usage — « L'utilisation de l'intelligence artificielle
générative n'est pas interdite en actuariat » — il exige trois choses : que les fondements théoriques et
les références soient maîtrisés, que l'explicabilité soit la même qu'en l'absence d'usage, et que la
transparence soit totale.

Le dossier est, sur les deux premiers points, **inhabituellement bien armé** : le harnais vérifie 1 824
nombres publiés contre les sorties de scripts, la note d'honnêteté documente les huit erreurs sémantiques
que ce harnais ne voyait pas, et la règle « un superlatif ou un comptage se calcule, il ne s'écrit pas »
est précisément une « mesure prise pour vérifier la validité des résultats » au sens du § 5.1.h. Cet
inventaire est donc plus facile à écrire ici que dans la plupart des mémoires, et il se retourne en
point fort.

**Coût : 2 à 3 heures.** C'est la première action à mener, avant toute autre.

### F2 — Les deux annexes exigées par l'Institut sont absentes · **critique**

**Où** : annexes A à E, p. 159–191.

**Constat.** Le § 5.1.h est sans ambiguïté : « **Deux annexes sont exigées par l'Institut des
actuaires** : Pistes éventuelles pour de futurs mémoires actuariels ; L'inventaire, le cas échéant, de
l'utilisation de l'intelligence artificielle générative. » Les annexes actuelles sont : A démonstrations,
B adaptations par pilier, C élicitation, D table des paramètres, E table des notations. Ni l'une ni
l'autre des deux exigées n'y figure. Aucune occurrence de « pistes pour de futurs mémoires » ni
équivalent dans les chapitres.

**Risque devant le jury.** Deux pièces obligatoires manquantes se voient à l'ouverture du plan des
annexes. Elles signalent que le référentiel n'a pas été lu jusqu'au bout — la pire impression possible
sur un dossier par ailleurs très travaillé.

**Correction.** L'annexe « pistes » est peu coûteuse et le matériau existe déjà : le chapitre 12
(la donnée manquante comme livrable) hiérarchise ce qui manque, le chapitre 13 inventorie les
hypothèses, le chapitre C décrit une élicitation **préparée et non exécutée** — qui est exactement une
piste de mémoire à léguer. Le référentiel précise que ces pistes « constituent un legs à l'entreprise
ayant accueilli l'étudiant mais aussi un apport pour la communauté actuarielle ».

**Coût : 2 heures pour « pistes », plus l'inventaire IA de F1.**

### F3 — Il n'existe plus de fichier maître produisant la version Institut · **critique**

**Où** : `page_de_garde.tex`, orpheline depuis le 19 septembre.

**Constat.** Le § 5.1.b impose une page de garde « homogénéisée pour tous les mémoires **quelle que soit
la filière d'origine de l'étudiant** ». Le PDF déposé porte `page_de_garde_ensae.tex`, la couverture de
l'école. La couverture officielle de l'Institut, `page_de_garde.tex`, existe toujours au dépôt mais
**plus aucun fichier maître ne l'appelle** : `main.tex` et `main_v2.tex`, qui le faisaient, ont été
supprimés le 19 septembre.

**Risque devant le jury.** Le dépôt du 30 septembre est le dépôt école. La soutenance Institut est en
novembre, et la version qu'elle exige **ne se compile plus aujourd'hui**. Le travail de remise en état
n'est pas nul et il n'est pas planifié.

**Correction.** Recréer un maître Institut qui appelle `preambule_v2`, `page_de_garde.tex` et les mêmes
chapitres, sans `\formatensae`, sans `19_enseignements_stage` (l'Institut ne le demande pas, le § 5.1.b
et suivants ne le prévoient nulle part). La règle du projet — ne jamais dupliquer un chapitre — est
respectée par construction. **Coût : 1 à 2 heures**, à ne pas laisser passer après le 30 septembre.

### F4 — La page de garde ne porte aucune signature, et la signature conditionne la publication · **critique**

**Où** : `page_de_garde_ensae.tex`. Champs définis : année scolaire, entreprise, ville, maître de stage,
dates, confidentialité. **Aucun champ de signature.**

**Constat.** Le § 5.1.b : « la page de garde du mémoire doit être signée par l'étudiant et par le
responsable du stage. L'Institut des actuaires insiste sur ce point car la page de garde faisant mention
de l'**autorisation de publication**, la signature par le responsable du stage, en tant que représentant
de l'entreprise, est nécessaire pour justifier de l'accord de publication. » Et le § 6.10 : « La
signature ouvre l'autorisation de diffusion et de mise en ligne du mémoire. »

**Risque.** L'absence de signature n'empêche pas de soutenir, mais elle **bloque la publication** — donc
la mention « publiable », donc toute perspective de prix. C'est directement contraire à l'objectif Prix
SCOR affiché par le projet.

**Correction.** Ajouter les deux blocs de signature sur la couverture Institut de F3, et faire signer
Hugo Rapior. **Coût : 30 minutes**, plus le délai de signature — à lancer tôt.

### F5 — Le déport du matériel complémentaire heurte une règle explicite · **critique**

**Où** : notice p. 158, macro `\matcomp` (45 occurrences dans le PDF), `materiel_complementaire/`.

**Constat.** Le § 5.1.h : « **Les annexes ne dispensent en rien d'être complet dans le corps du texte et
le lecteur ne doit pas se sentir obligé de se reporter aux annexes pour comprendre le raisonnement
suivi.** » Le mémoire va plus loin que des annexes : il renvoie **45 fois hors du document** vers une
ressource en ligne, dont la Phase 0 a établi qu'elle n'existe qu'à l'état de sources LaTeX non
compilables, derrière une URL encore fictive.

**Risque devant le jury.** Un juré qui bute sur un `(voir le Matériel Complémentaire en ligne)` au milieu
d'une démonstration, suit le lien et ne trouve rien d'exploitable, conclut que le raisonnement n'est pas
complet dans le document. C'est la lecture la plus défavorable possible d'un déport qui visait à alléger.

**Correction, deux niveaux.** Le minimum : produire le PDF du matériel complémentaire et poser l'URL
réelle (C1 de la Phase 0, 2–3 h). Le sûr : vérifier chapitre par chapitre qu'aucun `\matcomp` ne porte un
maillon nécessaire du raisonnement, et rapatrier dans le corps les énoncés dont la démonstration dépend.
La Phase 3 traitera ce second point.

---

## 3. Les constats majeurs

### F6 — Les deux résumés font deux fois la longueur autorisée · **majeure**

Le § 5.1.c fixe **150 à 250 mots**. Mesuré sur le PDF : **résumé FR 547 mots**, **abstract EN 367 mots**.
Le résumé dépasse de 2,2 fois la borne haute.

C'est une des rares prescriptions chiffrées du référentiel, donc une des plus faciles à vérifier pour un
juré. Le § 5.1.c précise aussi que ces textes servent à l'indexation sur le site de l'Institut.

**Correction** : réduire à 250 mots chacun. La matière ne se perd pas : la note de synthèse (p. 14–17) et
l'executive summary (p. 18–21) portent déjà le détail, et le référentiel ne leur fixe aucune longueur.
**Coût : 1 heure.**

### F7 — La note de synthèse séparée n'est pas produite · **majeure**

Le § 6.5 demande un document **séparé**, en français et en anglais, qui « va permettre l'indexation et le
référencement du mémoire sur le site de l'institut des actuaires ». Le mémoire porte ces deux textes en
interne (p. 14–21), ce qui est utile mais ne tient pas lieu du livrable.

Le § 6.5 demande en outre « un court paragraphe, à destination de l'ensemble des membres du Jury
sollicités », à fournir à la filière en même temps que la recherche de jurés.

**Correction** : extraire les deux textes existants en un document autonome. La matière est écrite.
**Coût : 1 heure.**

---

## 4. Les constats mineurs, et un écart assumé

| Constat | Référence | Position |
|---|---|---|
| **Annexes en pagination continue** et lettrées, là où le § 5.1.h demande une pagination à part et une numérotation | § 5.1.h | Le lettrage A–E est contigu et correct (Phase 0). La pagination à part est un changement de préambule non trivial pour un gain faible. **À laisser**, sauf si le temps le permet |
| **Introduction absorbée** dans un chapitre 1 de 15 pages, là où le § 5.1.d attend 2 à 3 pages | § 5.1.d | Le § 5.1.d décrit ce qu'une introduction doit contenir (préambule, énoncé de la problématique, éléments différenciants). Si la section 1.1 les porte dans les trois premières pages, l'esprit est respecté. **À vérifier en Phase 5** |
| **Corps à ~130 pages** contre « environ 70 » | § 5.1.e | **Écart assumé, sur ta décision.** Le référentiel écrit « environ » et ne prévoit aucune sanction. Défense à tenir en soutenance : le volume vient des données et de la robustesse, non du remplissage — 22 pages de données, 19 de robustesse, et 100 % des nombres publiés rattachés à un script |
| **Note de contexte** non produite (§ 6.4, facultative, 2 pages, jury seul) | § 6.4 | **Opportunité à saisir.** Elle sert à exposer au jury les difficultés réelles du stage — ici l'indisponibilité de la donnée de direction, qui est le cœur du mémoire. Elle prépare le terrain à l'identification partielle avant même la soutenance. **Coût : 1 heure**, fort rendement |

---

## 5. Ce qui est propre, et qu'il faut savoir défendre

Le référentiel valorise explicitement plusieurs choix déjà faits dans ce mémoire.

- **§ 4.6** : « Ce n'est pas un échec que de ne pas aboutir à des résultats pour peu que l'étudiant fasse
  preuve d'esprit critique. » Le mémoire réfute sa propre hypothèse de départ et requalifie son chiffre
  central en borne. C'est exactement ce que le référentiel dit valoriser.
- **§ 4.6** encore : « Analyse la fragilité et considère le domaine de confiance des modèles… en mettant
  en place des études de sensibilité. » Le chapitre 11 fait 12 pages sur ce seul sujet.
- **§ 5.3**, critères de la mention **publiable** : « des recherches originales qui offrent une avancée de
  la science actuarielle comme par exemple **l'application de méthodes issues de domaines autres que
  l'assurance** ». L'identification partielle à la Manski vient de l'économétrie. La mention publiable est
  atteignable — d'où l'importance de F4, sans signature elle ne sert à rien.
- **§ 5.2** : ton impersonnel. Deux « je » seulement dans tout le document, l'un dans une option de
  réponse citée, l'autre dans un titre du chapitre du stage où la première personne est assumée.

---

## 6. Ordre d'exécution recommandé

| Ordre | Action | Gravité | Coût |
|---|---|---|---|
| 1 | **F1** — paragraphe IA en fin de résumé + annexe d'inventaire | critique | 2–3 h |
| 2 | **F2** — annexe « pistes pour de futurs mémoires » | critique | 2 h |
| 3 | **F4** — blocs de signature, et solliciter Hugo Rapior **tout de suite** (délai externe) | critique | 30 min + délai |
| 4 | **F5 / C1** — compiler le matériel complémentaire, créer le dépôt, poser l'URL | critique | 2–3 h |
| 5 | **F6** — ramener les deux résumés à 250 mots | majeure | 1 h |
| 6 | **F7** — note de synthèse séparée FR + EN | majeure | 1 h |
| 7 | **F3** — recréer le maître Institut (après le 30 septembre, avant novembre) | critique | 1–2 h |
| 8 | Note de contexte § 6.4 | opportunité | 1 h |

Total avant le 30 septembre : **environ 10 à 12 heures**, hors délai de signature. F3 peut attendre le
dépôt école, mais pas la soutenance.
