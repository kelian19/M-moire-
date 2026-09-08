# Guide de rédaction du mémoire

Ce fichier dit **comment écrire**, pas quoi écrire. Le quoi est dans `PLAN_MEMOIRE.md`, les
règles du projet dans le `CLAUDE.md` de la racine.

## D'où viennent ces règles

De deux documents de l'Institut des actuaires, lus dans leur texte et non résumés de seconde
main :

- **« Mémoire d'actuariat, recommandations à l'usage des étudiants, des filières académiques et
  des membres du Jury en vue de la préparation du mémoire d'actuariat »**, validé par le Conseil
  d'administration de l'Institut le 20 janvier 2026, **applicable à compter du 1er avril 2026**.
  C'est la version qui fait foi pour une soutenance de fin 2026 ;
- « Mémoires d'actuariat, stages, soutenances et jury, recommandations », groupe de travail
  Mémoires, avril 2010, validé par la Commission scientifique le 6 mai 2010. Plus ancien, mais
  il porte l'annexe ISFA avec les règles typographiques, que la version 2026 ne reprend pas.

Ce qui suit distingue **ce que l'Institut écrit** de **ce qui est une recommandation de
travail** pour ce mémoire-ci. Ne pas confondre les deux devant le jury.

---

## 1. La règle qui coûte le plus de travail : le ton impersonnel

**Texte de l'Institut, section 5.2.** Le ton doit être « le plus impersonnel possible sauf
lorsque l'étudiant prend une position dont il assume la responsabilité ». Les trois pronoms
sont écartés un par un, et pour trois motifs différents :

| Forme | Ce que l'Institut lui reproche |
|---|---|
| « je » | peut paraître « prétentieux et dangereux », notamment s'il laisse penser que l'étudiant s'approprie une démarche déjà développée ailleurs |
| « nous » | « peut donner un caractère pompeux et cérémonieux » |
| « on » | « impersonnel et vague, donne souvent une impression d'imprécision et à la longue peut lasser le lecteur » |

La consigne qui suit est explicite : « il convient donc, autant que possible, d'éviter
l'utilisation des "je", "nous" et "on" et de **chercher le véritable sujet du verbe** et d'y
recourir. Le travail ne peut que gagner en précision. » L'exemple donné est celui-ci :

> « Le seuil de confiance a été fixé à 99 % » au lieu de « J'ai fixé le seuil de confiance à
> 99 % ».

**État de ce mémoire, compté et non estimé** (comptage sur les dix-neuf chapitres) :

| Forme | Occurrences |
|---|---|
| « je » | 7 |
| « nous » | 16 |
| « notre » / « nos » | 20 |
| **« on »** | **273** |

Le mémoire est donc déjà presque exempt de première personne, ce qui est bon, mais il s'appuie
massivement sur « on ». **C'est le chantier de rédaction le plus rentable qui reste**, parce
qu'il est visible à chaque page et qu'il ne demande aucun calcul.

**Comment convertir, et le piège.** Chercher le vrai sujet, ce n'est pas remplacer « on » par
une tournure passive partout : une succession de passives est aussi lourde que le « on ». Trois
patrons couvrent la quasi-totalité des cas :

| Ce qui est écrit | Ce qu'il faut écrire | Le vrai sujet est |
|---|---|---|
| « on obtient un rayon spectral de 0,506 » | « le rayon spectral vaut 0,506 » | la grandeur |
| « on suppose que les coûts s'additionnent » | « le modèle suppose que les coûts s'additionnent » | le modèle |
| « on ne peut pas identifier la direction » | « la donnée n'identifie pas la direction » | la donnée |
| « on retire les onze arêtes » | « le script 64 retire les onze arêtes » | le dispositif |

**L'exception, et elle est dans le texte de l'Institut** : la première personne reste permise
« lorsque l'étudiant prend une position dont il assume la responsabilité ». Ce mémoire en
contient plusieurs, et ce sont ses meilleurs passages : la réfutation de sa propre thèse de
départ, la requalification du chiffre central en borne supérieure, le gel de la calibration,
l'abandon de l'élicitation. **Ne pas dépersonnaliser ces phrases-là** : un arbitrage assumé
perd sa force à la voix passive, et l'Institut l'autorise précisément là.

---

## 2. L'intelligence artificielle générative, et c'est éliminatoire

**Section 4.5, et il faut la lire en entier.** Son usage « n'est pas interdit », mais il est
soumis à trois règles :

1. « Les fondements théoriques et les références bibliographiques sous-jacents au résultat
   fourni [...] doivent être maîtrisés » ;
2. « L'explicabilité des résultats obtenus [...] doit être la même que celle des résultats
   obtenus en l'absence de son usage » ;
3. « La transparence quant à l'usage de l'intelligence artificielle doit être **totale**. Tout
   manquement à cette règle conduira l'étudiant à être **ajourné par le jury, sans besoin d'une
   autre motivation**. »

**Conséquence pratique, et elle est à trancher par Kélian, pas ici.** La troisième règle est une
obligation de déclaration, et sa sanction est la plus lourde du document. Deux choses en
découlent :

- la contrainte de style du projet, « pas de tournures qui trahissent l'IA », est une question
  de **qualité d'écriture**, pas un moyen de dissimulation. Les deux sujets sont distincts et il
  ne faut pas les confondre ;
- la règle 2 est déjà satisfaite par construction ici, et c'est un point fort : chaque nombre
  publié sort d'un script versionné, et le dispositif de vérification est décrit en annexe. Un
  mémoire dont tous les chiffres sont traçables répond à l'exigence d'explicabilité mieux qu'un
  mémoire écrit à la main.

---

## 3. Le format, et il est chiffré

- **Volume du corps : environ 70 pages**, hors introduction, conclusion et annexes (section 5.1
  de la version 2026). La version ISFA le formule autrement : « le jury estime que l'essentiel
  d'une étude peut s'exprimer en 70 pages, en moyenne, hors annexes ».
  **Ce mémoire est à 123 pages de corps.** L'écart est assumé et tranché par Hugo, mais il se
  paye à la lecture, et le jury lit avec le chiffre de 70 en tête.
- **Pagination obligatoire.**
- Le mémoire doit contenir : un résumé en français précédé des mots clés, un résumé en anglais
  précédé des mots clés, une bibliographie, un lexique des noms, concepts et notations, des
  annexes avec les développements usuels.
- **Les données volumineuses et les listings ne figurent pas dans le corps mais en annexe.**
- L'introduction « décrit avec précision et concision la problématique de l'étude et son
  contexte ».
- La conclusion « fait le bilan des principaux résultats de l'étude et propose des perspectives
  de développement ». Elle peut porter « l'échec de la méthode proposée, ses imperfections et
  les prolongements possibles ».
- **En annexe**, l'étudiant est invité à énoncer les sujets qu'il n'a pas traités et qui
  pourraient faire l'objet d'un mémoire pour un autre étudiant.

---

## 4. Les figures, et la consigne de Kélian rejoint celle de l'Institut

**Ce que l'Institut exige.** Chaque graphique, figure, schéma ou tableau porte **un titre et un
numéro**. Pour tout élément issu d'une référence bibliographique, indiquer la source et la
référence : « l'étudiant doit absolument rendre "traçable" les informations mises dans son
mémoire ».

**Ce qui s'ajoute pour ce mémoire.** Une figure se justifie par ce qu'elle **montre et que le
texte ne peut pas dire**. Trois questions avant d'en garder une :

1. quelle affirmation du texte cette figure soutient-elle ? Si aucune, elle sort ;
2. la même information tiendrait-elle en une phrase ou en trois nombres ? Alors elle sort, et
   les trois nombres restent ;
3. un lecteur qui ne lit que la légende comprend-il le point ? Sinon, la légende est à réécrire,
   pas la figure.

Et la règle du projet, qui ne se négocie pas : **toute figure modifiée s'ouvre et se regarde**.
Cinq défauts réels de lisibilité ont été trouvés de cette façon, aucun par relecture du code.

---

## 5. Ce que le mémoire ne doit pas être

Liste de la section 5.3, et les cinq items « peuvent amener le jury de soutenance à refuser la
validation » :

- une description sans étude actuarielle ;
- **la simple présentation des résultats sans indication des méthodes mises en œuvre ou sans
  commentaires pertinents** ;
- un discours ou une traduction de travaux existants ;
- une paraphrase de travaux antérieurs ;
- un plagiat même partiel, qui conduit à la non-intégration à l'Institut.

Le deuxième item est celui à surveiller ici : un mémoire riche en sorties de scripts peut
glisser vers le catalogue de résultats. Chaque table publiée doit porter **ce qu'elle établit**,
et pas seulement ce qu'elle vaut.

---

## 6. Ce que le jury regarde, et ce n'est pas seulement la technique

- « Le jury attache une **attention particulière à l'esprit critique et à l'éthique** pour juger
  la qualité du mémoire » (section 4.6).
- L'étudiant « rédige son mémoire comme le ferait un actuaire en activité, dans le but de
  faciliter une prise de décision par un décideur en tenant compte des contraintes de son
  environnement ». Il doit « sortir du cadre scolaire, se considérant déjà comme un
  professionnel en activité ».
- Il doit « mettre en avant les apports et les avancées, **tout comme les échecs ou risques
  d'erreurs** dans la méthodologie suivie, les calculs réalisés ou l'interprétation des
  résultats ».
- **Ne pas aboutir n'est pas un échec.** Le texte est explicite : « ce n'est pas un échec que de
  ne pas aboutir à des résultats pour peu que l'étudiant fasse preuve d'esprit critique sur son
  travail [...] Le cheminement du candidat dans sa démarche intellectuelle est en soi
  important. »
- Analyser « la fragilité » et « le domaine de confiance » des modèles, par exemple par des
  études de sensibilité, et « émettre un avis critique sur son travail pour pouvoir répondre aux
  questions du jury sans se retrouver dans une position délicate ».
- **La recherche bibliographique peut être éliminatoire** si elle est jugée insuffisante, et elle
  doit inclure les mémoires d'actuariat de l'Institut liés au sujet.

**Ce que cela dit de ce mémoire.** Ces six points décrivent exactement ce qui fait sa valeur :
une thèse de départ réfutée par son auteur, un chiffre central requalifié en borne supérieure,
une borne inférieure de validité publiée, un défaut de calibration chiffré plutôt que corrigé.
**Ce ne sont pas des faiblesses à atténuer, ce sont les critères du jury.** La note d'honnêteté
du `CLAUDE.md` dit la même chose, et elle est confirmée par le texte officiel.

---

## 7. Typographie

Règles de l'annexe ISFA, qui restent les seules écrites :

- **espaces insécables** avant le symbole monétaire, avant `%`, et avant `:` `;` `!` `?` ;
- le séparateur décimal est **la virgule**, pas le point ;
- graphiques, figures et tableaux : titre et numéro ;
- sauf exception, **deux titres ne se suivent pas** sans texte entre eux ;
- les équations sont écrites avec un éditeur approprié ;
- les mots en langue étrangère sont en italique ou entre guillemets, « et leur usage ne doit pas
  être exagéré ».

S'y ajoutent deux règles propres à ce projet, et elles sont dans le `CLAUDE.md` : **pas de tiret
cadratin**, et le contrôle se fait **sur le PDF produit**, jamais sur la source, parce que le
babel français en insère un en puce d'itemize par défaut.

---

## 8. La soutenance, puisqu'elle se prépare en écrivant

- **25 minutes maximum** de présentation, **20 minutes** de questions, puis délibération, sans
  interruption entre les phases. Le président du jury a autorité pour interrompre au-delà du
  temps imparti, et « le non-respect du délai imparti peut être pénalisant ».
- Le support « ne constitue pas une photocopie du mémoire et ne doit pas nécessairement suivre
  l'ordre des parties ». Il ne doit pas être trop long, et la présentation « ne devra pas se
  résumer à la lecture du support ».
- **Le jury est attentif à la manière de s'exprimer** : « débit de parole, attention portée aux
  réactions des membres du jury, captation de l'attention, **expressions familières, apocopes et
  acronymes** ». Point concret pour ce mémoire : dire « la valeur en risque » ou « la VaR » une
  fois définie, jamais un acronyme non introduit, et éviter les raccourcis d'atelier comme
  « le harnais » ou « le 169 » sans les avoir posés.
- Les membres du jury « prennent en général des notes et essaient de retrouver dans le texte du
  mémoire ce que l'étudiant présente à l'oral ». **Donc l'oral ne doit rien affirmer que le
  document ne porte pas**, et c'est la principale raison de tenir les deux alignés.
- Fiches autorisées, mais garder le contact visuel. S'entraîner devant un **jury fictif** est
  « vivement recommandé ».
- Critères d'évaluation : intérêt actuariel du mémoire, présentation du mémoire, présentation
  orale, comportement professionnel en entreprise.

---

## 9. Le registre, phrase par phrase

Cette section n'est **pas** dans les recommandations : c'est la mise en pratique du ton
impersonnel pour ce mémoire. Elle est là pour éviter d'avoir à réinventer une tournure à chaque
paragraphe.

**À préférer.** Le sujet est la grandeur, le modèle, la donnée, le dispositif, ou l'auteur quand
il tranche.

- « Le capital croît en $g$ » plutôt que « on observe que le capital croît en $g$ » ;
- « La donnée identifie la co-occurrence, pas la direction » plutôt que « on ne peut pas
  identifier la direction » ;
- « Le modèle suppose que les coûts s'additionnent, et cette hypothèse n'est pas testée » plutôt
  que « on fait l'hypothèse que » ;
- « Ce mémoire publie la lecture à quatre canaux » plutôt que « on retient la lecture » ;
- « La calibration est gelée depuis le 7 août » plutôt que « nous avons décidé de geler ».

**À éviter, et pas seulement pour le style.**

| Tournure | Pourquoi |
|---|---|
| « il est évident que », « naturellement » | une évidence affirmée est une démonstration absente |
| « très », « extrêmement », « particulièrement » | l'adverbe d'intensité remplace le chiffre. Donner le chiffre |
| « permet de mettre en évidence » | périphrase. « montre », ou mieux, le résultat lui-même |
| « dans le cadre de », « au niveau de » | remplissage, se supprime sans perte |
| « nous allons voir que », « comme nous le verrons » | annonce de plan à l'intérieur d'un paragraphe |
| « robuste » employé seul | robuste à quoi ? Le mémoire a un sens technique précis pour ce mot, ne pas le diluer |
| « significatif » hors test | réserver au sens statistique, sinon écrire « important » ou donner l'ampleur |

**Une règle de fond qui vient du projet et qui vaut pour l'écriture.** Le commentaire s'écrit
**après** avoir lu la sortie, jamais en même temps que le code qui la produit. Cinq conclusions
ont été écrites d'avance puis démenties par les nombres dans la seule journée du 14 août.

---

## 10. Ordre de travail sur la rédaction

Par rendement décroissant, et le premier est loin devant :

1. **Les 273 « on »**, en commençant par les pièces les plus lues : le résumé, l'introduction
   générale, la conclusion. Le jury les lit en premier et les relit en dernier ;
2. la chasse aux tournures de la section 9, sur les mêmes pièces d'abord ;
3. le contrôle que chaque table publiée dit **ce qu'elle établit** et pas seulement ce qu'elle
   vaut, au titre du deuxième item de la section 5 ;
4. l'annexe des sujets non traités, que la version 2026 invite à écrire et qui n'existe pas
   encore ;
5. la compression du corps vers les 70 pages recommandées, qui est une décision de Kélian et non
   une règle.
