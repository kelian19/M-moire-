# SCR_DORA — Quantification interne du capital lié à la non-conformité DORA

**Mémoire d'actuariat — ENSAE Paris / Institut des Actuaires — Promotion 2026**  
**Auteur :** Kélian Kaddouri  
**Encadrant Nexialog :** Hugo Rapior  
**Directrice de mémoire :** Caroline Hillairet (ENSAE Paris)

---

## Positionnement

> *Le SCR cyber n'est pas un nombre, c'est une distribution large.*

Ce projet développe une **mesure interne de capital de type ORSA / Pilier 2**, notée **SCR_DORA**, destinée à quantifier le surcroît de risque cyber associé à une non-conformité partielle ou totale au règlement **DORA** (Digital Operational Resilience Act, UE 2022/2554). Cette démarche ne vise pas à proposer une nouvelle formule réglementaire de Pilier 1, mais à construire un **pont quantitatif entre DORA et Solvabilité II** dans une logique actuarielle prospective [file:34].

L'objet du mémoire est de mesurer les **pertes potentielles futures** liées à un défaut de conformité DORA, puis d'en déduire une distribution de capital et un différentiel de capital contrefactuel \(\Delta_{DORA}\) [file:34].

---

## Question de recherche

**Que se passe-t-il si une entité financière n'est pas conforme à DORA — partiellement ou totalement — et comment quantifier les pertes potentielles associées à ce défaut de conformité ?** [file:34]

---

## Architecture méthodologique

```text
Fréquence (NegBin)          Sévérité (EVT / GPD)
  λ ~ NegBin(r, p)            X ~ GPD(ξ, σ, u)
  Source : PRC 2025           Sources : PRC + OpRisk Global
        │                            │
        └──────────┬─────────────────┘
                   │
        Agrégation LDA à quatre briques
        [remédiation, prestataire, sanction, aggravation]
                   │
        Dépendance : facteur commun + copule de Gumbel
                   │
        Monte Carlo + bootstrap à deux niveaux
                   │
        VaR 99.5% / ES 99.5%
                   │
        Δ_DORA = SCR(stress conformité) − SCR(contrefactuel conforme)
```

Le cœur du modèle repose sur une approche **Loss Distribution Approach** enrichie de scénarios de fréquence conditionnels au niveau de conformité DORA [file:34]. La fréquence de référence est calibrée sur la PRC à \(\lambda_{ref}=341\) incidents annuels, puis modulée par vecteur d’attaque selon la structure observée dans Hackmageddon [file:34].

---

## Scénarios de conformité DORA

| Scénario | Niveau | Logique |
|----------|--------|---------|
| S0 | Conformité totale | Régime de référence |
| S1 | Non-conformité partielle | Hausse intermédiaire de fréquence selon l’exigence DORA affectée |
| S2 | Non-conformité totale | Hausse maximale de fréquence par vecteur |

Les multiplicateurs de fréquence sont calibrés à partir d’un mapping **vecteurs d’attaque \(\rightarrow\) exigences DORA** sur la base de **Hackmageddon S1 2026 (1 041 incidents)** [file:32][file:34].

---

## Sources de données

| Source | Usage principal | Limite principale |
|--------|-----------------|------------------|
| **PRC 2025** | Fréquence \(\lambda\), calibration NegBin, sévérité indirecte via conversion Jacobs | Sévérité dérivée, non observée directement [file:32] |
| **SAS OpRisk Global Data** | Sévérité observée, calibration GPD, validation croisée | Biais vers les grandes entités financières [file:32] |
| **Hackmageddon** | Structure du risque, mapping DORA, multiplicateurs de fréquence | Biais de visibilité, taxonomie instable [file:32] |

> ⚠️ **Données sensibles** : les fichiers `data/raw/` sont exclus du dépôt (`.gitignore`) et ne doivent jamais être poussés sur GitHub, en particulier les extractions sous licence Nexialog [file:32].

---

## Principaux résultats

| Indicateur | Valeur | Intervalle / commentaire |
|------------|--------|--------------------------|
| Capital total (fourchette globale) | 1 406 – 20 105 M€ | selon source, profil de conformité et mesure (VaR/ES) [file:24] |
| \(\Delta_{DORA}\) — PRC, S1 | 91,5 M€ | IC 90% : [71,6 ; 114,2] M€ [file:34] |
| \(\Delta_{DORA}\) — PRC, S2 | 238,7 M€ | IC 90% : [191,6 ; 288,0] M€ [file:34] |
| \(\Delta_{DORA}\) — OpRisk, S1 | 1 086,9 M€ | IC 90% : [410,5 ; 4 348,4] M€ [file:34] |
| \(\Delta_{DORA}\) — OpRisk, S2 | 4 092,2 M€ | IC 90% : [1 463,9 ; 19 659,2] M€ [file:34] |
| \(\hat{\xi}_{PRC}\) | 1,30 | queue très lourde, espérance infinie \(\rightarrow\) cap à 40 M€ [file:32] |
| \(\hat{\xi}_{OpRisk}\) | 0,595 | IC 90% : [0,31 ; 0,85] [file:32] |

Trois résultats structurants ressortent du mémoire :
- le choix de la **source de sévérité** domine l’effet du scénario de conformité [file:34][file:24] ;
- la brique de **remédiation** concentre l’essentiel du capital alloué par Euler, souvent plus de 85% et jusqu’à près de 99% selon la source [file:22] ;
- la **sanction** a un poids marginal sous OpRisk mais plus visible sous PRC, du fait de l’échelle relative des pertes [file:22][file:23].

---

## Limites

Le projet assume explicitement plusieurs limites méthodologiques :
- Hackmageddon décrit la **structure** du risque mais pas son niveau absolu [file:32] ;
- la taxonomie des attaques n’est pas stable dans le temps, ce qui impose des reclassements documentés [file:32] ;
- OpRisk Global surexpose les grandes entités et peut sous-estimer la lourdeur de queue d’un univers plus large [file:32] ;
- la PRC ne permet pas, dans l’environnement courant, un bootstrap complet du second niveau sur la sévérité [file:34] ;
- lorsque \(\xi \ge 1\), la simulation doit être gouvernée par un plafond de sévérité pour rester numériquement stable [file:32].

---

## Structure du projet

```text
M-moire/
├── src/
│   ├── frequency/          # Modèle NegBin + scénarios de fréquence
│   ├── severity/           # EVT/GPD, calibration PRC et OpRisk
│   ├── aggregation/        # Copule, Monte Carlo, LDA
│   ├── scenarios/          # Scénarios DORA, multiplicateurs, Δ_DORA
│   └── utils/              # Logging, configuration, visualisation
├── data/
│   ├── raw/                # ⛔ données brutes gitignorées
│   └── processed/          # tables nettoyées, agrégats
├── notebooks/              # exploration, diagnostics, figures
├── outputs/
│   ├── figures/            # graphiques exportés
│   └── tables/             # tables de résultats
├── docs/                   # documentation méthodologique
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/kelian19/M-moire-.git
cd M-moire-
pip install -r requirements.txt
```

---

## Références clés

- Maillart & Sornette (2010) — *Heavy-tailed distributions of cyber risks*.
- Hillairet & Lopez (2021) — travaux sur la modélisation du risque cyber.
- Farkas, Lopez & Thomas (2021) — quantification actuarielle du risque cyber.
- Kher, Lopez & Rapior (2023) — SCR cyber sous Solvabilité II.
- Lopez, Denuit, Rapior et al. (2025) — extensions CAS et applications.
- Règlement **DORA** (UE 2022/2554).

---

*Nexialog Consulting — BU Cyber Risk — Paris, 2026*