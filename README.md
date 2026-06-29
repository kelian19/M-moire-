# SCR_DORA — Quantification du Capital Réglementaire lié à la Non-Conformité DORA

**Mémoire d'actuariat — ENSAE Paris / Institut des Actuaires — Promotion 2026**  
**Auteur :** Kélian Kaddouri  
**Encadrant Nexialog :** Hugo Rapior  
**Directrice de mémoire :** Caroline Hillairet (ENSAE Paris)

---

## Problématique

> *Le SCR cyber n'est pas un nombre, c'est une distribution large.*

Ce projet modélise le **SCR_DORA** — une charge en capital Solvabilité II associée au risque de non-conformité au règlement DORA (Digital Operational Resilience Act, UE 2022/2554) — en s'appuyant sur un cadre LDA (Loss Distribution Approach) à quatre briques de perte, enrichi de scénarios de fréquence conditionnels au niveau de conformité.

**Question centrale :** que se passe-t-il si une entité financière n'est pas conforme à DORA — partiellement ou totalement — et comment quantifier la perte potentielle associée à ce défaut de conformité ?

---

## Architecture méthodologique

```
Fréquence (NegBin)          Sévérité (GPD/EVT)
   λ ~ NegBin(r, p)            X ~ GPD(ξ, σ, u)
   Source : PRC 2025            Source : PRC + OpRisk (validation)
        │                              │
        └──────────┬───────────────────┘
                   │
         Copule de Gumbel (θ = 1.8)
         [4 briques : remédiation, prestataire, sanction, aggravation]
                   │
         Monte Carlo ≥ 10⁶ simulations
                   │
         VaR 99.5% → SCR_DORA
         Bootstrap 2 niveaux → Distribution du SCR
                   │
         Δ_DORA = SCR_avec_DORA − SCR_contrefactuel
```

---

## Scénarios de conformité DORA

| Scénario | Niveau | Multiplicateur fréquence |
|----------|--------|--------------------------|
| S0 | Conformité totale | λ × 1.0 |
| S1 | Non-conformité partielle | λ × k (par exigence) |
| S2 | Non-conformité totale | λ × K (par exigence) |

Les multiplicateurs sont calibrés sur le mapping vecteurs d'attaque → exigences DORA (source : Hackmageddon S1 2026, 1 041 incidents).

---

## Sources de données

| Source | Usage | Statut |
|--------|-------|--------|
| **PRC 2025** (Privacy Rights Clearinghouse) | Fréquence λ, calibration NegBin | ✅ |
| **SAS OpRisk Global Data** (juin 2026) | Sévérité GPD, validation croisée | ✅ (licence Nexialog) |
| **Hackmageddon** (Paolo Passeri, S1 2026) | Mapping vecteurs → DORA, multiplicateurs | ✅ |

> ⚠️ **Données sensibles** : les fichiers `data/raw/` sont dans `.gitignore` et ne doivent jamais être poussés sur GitHub.

---

## Structure du projet

```
M-moire/
├── src/
│   ├── frequency/          # Modèle NegBin + scénarios de fréquence
│   ├── severity/           # EVT/GPD, calibration PRC et OpRisk
│   ├── aggregation/        # Copule Gumbel, Monte Carlo, LDA
│   ├── scenarios/          # Scénarios DORA, multiplicateurs, Δ_DORA
│   └── utils/              # Outils communs (logging, config, plots)
├── data/
│   ├── raw/                # ⛔ gitignorés — données brutes
│   └── processed/          # Agrégats, tables nettoyées
├── notebooks/              # Exploration, diagnostics, figures
├── outputs/
│   ├── figures/            # Graphiques exportés
│   └── tables/             # Tableaux de résultats
├── docs/                   # Documentation méthodologique
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

## Résultats préliminaires

| Indicateur | Valeur | IC 90% bootstrap |
|------------|--------|-----------------|
| SCR_DORA (central) | ~83.2 M€ | [90, 117 M€] |
| Δ_DORA (approche C) | ~33.5 M€ | — |
| ξ GPD (PRC) | 1.30 | — |
| ξ GPD (OpRisk, validation) | 0.60 | [0.30, 0.83] |

---

## Références clés

- Maillart & Sornette (2010) — Heavy-tailed distributions of cyber risks  
- Farkas, Lopez & Thomas (2021) — Cyber risk quantification  
- Kher, Lopez & Rapior (2023) — SCR cyber sous Solvabilité 2  
- Lopez, Denuit, Rapior et al. (2025, CAS) — Extensions et applications  
- Hillairet & Lopez (2021) — Cyber risk modelling  
- DORA (UE 2022/2554) — Règlement sur la résilience opérationnelle numérique

---

*Nexialog Consulting — BU Cyber Risk — Paris, 2026*
