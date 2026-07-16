# Plan du mémoire (version cascade) : ce qui est fait, ce qui reste

Document de travail. Objectif : Prix SCOR. Thèse centrale du mémoire refondu.

> **La non-conformité à DORA a un coût en capital de solvabilité, et ce coût se
> quantifie par une cascade dirigée entre les cinq piliers, dont les paramètres
> sont pilotés dans le temps par l'état de conformité de chaque pilier (chaîne de
> Markov multi-états). On obtient non pas un chiffre unique mais une trajectoire de
> SCR sur l'horizon de transition DORA, et un ordre de remédiation qui minimise le
> coût en capital.**

Le pivot est acté : la cascade dirigée remplace l'ancien couple (LDA 4 briques +
copule de Gumbel + variable latente Z). On garde les fondations agnostiques (données,
EVT/GPD, fréquence NegBin, cadre réglementaire, revue de littérature).

---

## Synthèse : les deux colonnes

### CE QU'ON A FAIT

**Fondations agnostiques (récupérées de l'ancien mémoire, `memoire/main.tex`)**
- Introduction, problématique, énoncé de contribution
- État de l'art (assurabilité, contagion, copules, EVT, Solvabilité II vers DORA)
- Cadre réglementaire complet (Bâle III, Solvabilité II, DORA 5 piliers, ORSA vs DORA)
- Données et limites (SII art. 19, trois biais, inflation cyber, PRC, Hackmageddon,
  SAS OpRisk, validation croisée ENISA)
- Théorie EVT/GPD et démonstrations (Fisher-Tippett-Gnedenko, Pickands-Balkema-de Haan,
  Hill, information de Fisher, VaR/TVaR de la GPD)
- Calibration sévérité (GPD OpRisk xi=0,595 ; PRC xi=1,033) et fréquence (NegBin
  lambda_ref=341, phi=9,2)

**Le nouveau modèle cascade (dans `exploratory/`, scripts 01-15)**
- Modèle qualitatif : l'ordre des piliers pilote proba/gravité/criticité (ROOT/TRANS/GBASE)
- Vasicek dirigé, fondations (01-06) : matrice de parts W normalisée à la Leontief,
  processus de branchement R0, estimateur probit, redondance de ROOT, verdict de
  faisabilité (W non calibrable sur les sources ouvertes), calibration du facteur
  systémique (routes A et B)
- SCR en unités normalisées (07-10) : sévérité, fréquence, agrégation, surface SCR(g, xi)
- Copules et allocation d'Euler (11)
- SCR en euros par la cascade (12-15) : SCR euro, prime de propagation, Delta_DORA
  bootstrap, IC honnête (IQR vs IC90), tornado de robustesse. Verdict robuste.

**Chantiers de robustesse déjà faits (anciens notebooks, partiellement réutilisables)**
- Réassurance / assurabilité de dernier recours (17_reinsurance)
- Ancrage empirique des multiplicateurs de fréquence (18_multiplier_anchoring)
- Tornado du Delta_DORA au mapping (16_delta_dora_mapping)

### CE QU'IL RESTE À FAIRE

**Le cœur neuf, la contribution Prix SCOR (scripts à écrire, 16-18)**
- Conformité multi-états par pilier : chaîne de Markov 3 états x 5 piliers (16)
- Trajectoire de SCR sur l'horizon DORA : couplage état -> cascade -> SCR(t) (17)
- Priorisation de la remédiation : quel ordre des piliers minimise le coût intégré (18)

**Rédaction / intégration LaTeX (nouveau `main.tex` cascade)**
- Réécrire le cœur modélisation (remplacer LDA 4 briques + Gumbel + latent Z par la cascade)
- Écrire le chapitre conformité multi-états
- Nouveau chapitre résultats (cascade + trajectoire + priorisation)
- Réécrire abstract / énoncé de contribution
- Re-trianguler et re-tester la robustesse sur le modèle cascade

**Décisions de périmètre : VALIDÉES par Hugo (juillet 2026)**
- Décision A : le Markov multi-états REMPLACE la variable latente statique du mémoire.
- Décision B : état de conformité PAR PILIER, mis en scène global d'abord (16a) puis par
  pilier (16b). L'état global est un cas particulier du par-pilier.
- Fait : script 16 (Vasicek multi-états global, latente à seuils ordonnés + 3 canaux, S10).
- Fait : script 16b (état par pilier, décomposition du Delta_DORA, S11). La décomposition
  euro reproduit le classement ROOT du modèle qualitatif (P1>P4>P2>P3>P5).
- Fait : ÉTAPE 2, script 17 (Markov NC->PC->C Erlang-2 + trajectoire SCR(t), couplage
  systémique Theta, bande d'incertitude, S12). Delta_DORA(t) résiduel -> 0.
- Fait : ÉTAPE 3, script 18 (priorisation de remédiation, S13). Ordre optimal par énumération
  des 120 ordres = ordre ROOT (P1>P4>P2>P3>P5), différent du glouton. Écart pire/optimal 21 %.
- Fait : ÉTAPE 5, script 19 (robustesse multi-états, S14). Tornado : xi domine (facteur 6,4),
  Delta > 0 partout, priorité P1 robuste sur tous les leviers ; ordre optimal invariant aux
  taux Markov. Classement robuste, niveau non (thèse du chantier cascade).
- Note LaTeX note_conformite_multietats.tex/.pdf : synthèse du chantier 16-19, compilée
  (Tectonic installé en local, memoire/tectonic.exe non versionné).
- En cours : ÉTAPE 4, nouveau mémoire cascade dans exploratory/memoire_cascade/main.tex
  (compile, figures intégrées). Parties agnostiques en sections-relais [À migrer] depuis
  l'ancien memoire/main.tex (non touché).
  - Chapitre cascade dirigée : ÉTOFFÉ (Vasicek 1 facteur -> gén. A -> gén. B -> normalisation
    Leontief -> branchement/R0 -> seuil K_j -> faisabilité), figures H1, K3.
  - Chapitre conformité multi-états : ÉTOFFÉ (deux échelles fast-slow, latente à seuils ordonnés,
    3 canaux, état par pilier, Markov Erlang, couplage Theta, analogie migration de rating).
  - Reste à étoffer : chapitre résultats (déjà avec les 5 figures + chiffres clés, à développer).
  - Reste à migrer : intro, état de l'art, réglementaire, données, socle mécaniste, annexes EVT.
- Reste : finir ÉTAPE 4 (migration + étoffage) ; décision canal détection avec Hugo.

---

## Plan détaillé du mémoire cible

Légende : **[FAIT]** existe et se garde tel quel. **[ADAPTER]** existe mais écrit pour
l'ancien modèle, à réécrire pour la cascade. **[FAIRE]** à produire.

### 0. Résumé, abstract, énoncé de contribution
- **[ADAPTER]** Le résumé actuel met en avant le pont Vasicek-conformité latent + LDA.
  Le nouveau doit annoncer : cascade dirigée + conformité markovienne + trajectoire de SCR.

### 1. Introduction et problématique
- **[FAIT]** La question centrale (traduire la non-conformité DORA en distribution de
  pertes, pas un audit de conformité) reste valable telle quelle.
- **[ADAPTER]** Le paragraphe qui annonce le pont Vasicek latent en partie 3 doit
  annoncer la cascade et le multi-états.

### 2. État de l'art
- **[FAIT]** Assurabilité, rareté des données, contagion et dynamique systémique,
  copules, EVT, Solvabilité II vers DORA. Tout se garde.
- **[FAIRE]** Ajouter un court paragraphe sur les processus de branchement multitype et
  les modèles multi-états en actuariat (chaînes de Markov, distributions de type phase),
  pour ancrer la contribution dans la littérature.

### 3. Cadre réglementaire
- **[FAIT]** Bâle III, Solvabilité II, DORA (5 piliers ICT), ORSA vs DORA. Se garde.
- **[FAIT]** La sous-section "les cinq piliers ICT" devient centrale : c'est le support
  des cinq chaînes de Markov et des cinq nœuds de la cascade.

### 4. Données et limites
- **[FAIT]** Article 19 SII, trois biais, inflation, PRC (fréquence), Hackmageddon
  (structure), SAS OpRisk (sévérité), ENISA (validation croisée), cadre épistémique.
- **[FAIT]** Le verdict de faisabilité "W non calibrable, seul xi l'est" (script 05) est
  un résultat honnête à mettre en avant, il renforce la crédibilité méthodologique.
- **[FAIRE]** Ajouter la faisabilité des taux de transition de conformité : aucune base
  ouverte ne les documente (DORA appliqué depuis 2025), donc axe de sensibilité et non
  calibrage. À ancrer sur calendriers réglementaires DORA et référentiels de maturité.

### 5. Modélisation, partie A : le socle mécaniste (fréquence, sévérité, agrégation)
- **[FAIT]** Sévérité EVT/GPD (script 07 + `src/severity`), calibration OpRisk, validation PRC.
- **[FAIT]** Fréquence NegBin / Poisson mélangé par facteur systémique commun (08 + `src/frequency`).
- **[ADAPTER]** L'agrégation : l'ancien texte décrit l'architecture LDA à 4 briques
  (remédiation, prestataire, sanction, aggravation) + Monte-Carlo. À remplacer par
  l'agrégation cascade (un incident amorce se propage sur un ensemble de piliers).
- **[FAIT]** Allocation d'Euler (11 + `src/aggregation/euler_allocation`), se garde.

### 6. Modélisation, partie B : la cascade dirigée (le coeur neuf, déjà codé)
- **[FAIT]** Modèle qualitatif ROOT/TRANS/GBASE (`cascade_qualitative/`).
- **[FAIT]** Vasicek dirigé : W = g·TRANS/max(ligne), normalisation Leontief, rho(W) < 1
  garanti (01-03 + `note_vasicek_dirige`).
- **[FAIT]** Processus de branchement multitype, R0 = rho(M), redondance de ROOT (03).
- **[FAIT]** Seuil K réglementaire + EVT, biais de sous-déclaration E[q(S)|S>=u] (02, 04).
- **[FAIT]** Calibration du facteur systémique Y_j, s_j, Sigma_Y, routes A et B (06).
- **[FAIRE]** Rédiger ce chapitre en LaTeX à partir des scripts et de la note (aujourd'hui
  la matière est dans le code et les PDF de `exploratory/`, pas dans un `main.tex`).

### 7. Modélisation, partie C : la conformité multi-états (LA contribution à écrire)
- **[ADAPTER puis REMPLACER]** L'ancienne sous-section "probabilité de défaut de
  conformité comme variable latente" (Vasicek latent, statique, global, un seul canal
  fréquence via `latent_bridge.py`). Recommandation : remplacer par le Markov.
- **[FAIRE]** Chaîne de Markov à 3 états {Non conforme, Partiellement conforme, Conforme}
  par pilier, 5 chaînes. Générateur à temps continu, Conforme absorbant en cas de base.
- **[FAIRE]** Durées de séjour réalistes par distributions de type phase (Erlang/Coxian)
  au lieu d'exponentielles, pour capter une durée minimale de projet de remédiation.
- **[FAIRE]** Couplage aux trois canaux déjà codés : l'état c_j(t) module la fréquence
  lambda_j, la propagation g_j de la cascade, et le seuil de détection u_j.
- **[FAIRE]** Réduction mean-field (5 chaînes indépendantes) assumée, variante couplée
  (budget de remédiation unique) en test.

### 8. Scénarios de conformité et Delta_DORA
- **[FAIT]** Les trois niveaux S0/S1/S2 existent (deviennent les 3 états du Markov).
- **[FAIT]** Mapping vecteurs d'attaque vers exigences DORA, multiplicateurs différenciés.
- **[FAIT]** Delta_DORA comme distribution et non un point, bootstrap, IC (12-15).
- **[FAIRE]** Passer du Delta_DORA statique (conforme vs non conforme) à la trajectoire
  Delta_DORA(t) le long de la mise en conformité progressive.

### 9. Résultats et discussion
- **[ADAPTER]** Distribution du SCR sur une entité de 15 000 M€ : les chiffres existent
  déjà en version cascade (12-15), à intégrer dans un chapitre résultats réécrit.
- **[FAIT]** Décomposition de l'incertitude, allocation d'Euler, sensibilité aux
  hypothèses porteuses, sensibilité au seuil POT, convergence Monte-Carlo : faits en
  version cascade (10, 11, 14, 15).
- **[FAIRE]** Résultat neuf : la trajectoire SCR(t) et la valeur d'accélération par
  pilier (l'ordre de remédiation optimal).
- **[ADAPTER]** Triangulation du SCR par plusieurs méthodes : existait sur l'ancien
  modèle, à refaire ou raccorder à la cascade.
- **[FAIT/ADAPTER]** Réassurance / assurabilité de dernier recours (ancien notebook 17),
  largement réutilisable.
- **[FAIT]** Comparaison à la Formule Standard (aveugle à la résilience) et à l'ORSA.

### 10. Annexes (démonstrations, notations, algorithmes, paramètres)
- **[FAIT]** Démonstrations EVT (FTG, Balkema, Hill, Fisher, VaR/TVaR GPD).
- **[ADAPTER]** "Sensibilité du modèle de Vasicek" et "queues de la copule de Gumbel" :
  à remplacer par la preuve de stabilité de la cascade (rho(W) < 1 par normalisation) et
  la propriété du processus de branchement.
- **[FAIRE]** Ajouter : générateur de la chaîne de Markov, distributions de type phase,
  algorithme de simulation de la trajectoire (uniformisation / Gillespie).

---

## Chantier restant, priorisé

**Étape 1 (code, le plus créateur de valeur).** Trois scripts, même discipline que
l'existant (portée déclarée, aucune modification de `src/` ni `memoire/`) :
- `16_etats_conformite_markov.py` : les 5 chaînes de Markov, validées seules (générateur,
  type phase, trajectoires, distribution d'état à l'horizon).
- `17_scr_trajectoire_dora.py` : couplage état -> (lambda_j, g_j, u_j) -> cascade -> SCR(t),
  extension du bootstrap 12-15.
- `18_priorisation_remediation.py` : valeur d'accélération par pilier, ordre optimal de
  remédiation, boucle avec l'allocation d'Euler (11) et le classement ROOT.

**Étape 2 (rédaction).** Monter le nouveau `main.tex` cascade : réutiliser les parties
agnostiques de l'ancien, brancher les chapitres 6-7-9 sur la matière de `exploratory/`.
Ne pas toucher à `memoire/main.tex` tant que le périmètre n'est pas validé (décision actée).

**Étape 3 (robustesse et triangulation).** Reporter sur la cascade les tests déjà faits
sur l'ancien modèle (mapping, multiplicateurs, réassurance) et compléter.

## Décision en attente

Le Markov multi-états remplace-t-il la variable latente de Vasicek-conformité statique ?
Recommandation : **oui, remplacement**. La chaîne de Markov fait en dynamique et par
pilier ce que le latent faisait en statique et en global ; garder les deux crée deux
modèles de conformité concurrents et brouille le récit. Le remplacement unifie les trois
strates en une seule chaîne causale (le qualitatif donne l'asymétrie inter-piliers, le
Vasicek dirigé donne la propagation, le Markov donne la dynamique de conformité qui
module la propagation), ce qui est le type de cohérence qu'un jury Prix SCOR récompense.
