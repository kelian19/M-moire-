"""
utils/config.py
---------------
Configuration centrale du projet SCR_DORA.
Tous les paramètres calibrés sont centralisés ici.

MISE À JOUR : les résultats centraux (SCR_DORA, COPULE) ont été synchronisés
avec les vrais résultats du pipeline (grille bootstrap Δ_DORA + LDA 4 briques
+ allocation d'Euler). Les anciennes valeurs placeholder ont été retirées.
"""

# ---------------------------------------------------------------------------
# PARAMÈTRES CALIBRÉS — PRC 2025
# ---------------------------------------------------------------------------

PRC = {
    "source": "Privacy Rights Clearinghouse 2025",
    "period": "2019–2025",
    "n_records": None,           # à renseigner après accès
    "seuil_u_eur": 0.128,        # M€ (seuil POT après conversion Jacobs)
    "xi": 1.30,                  # paramètre de queue GPD
    "sigma_eur": 0.257,          # M€ (paramètre d'échelle)
    "p_u": 0.15,                 # P(X > u)
    "jacobs_a": 7.68,            # paramètre conversion log-log
    "jacobs_b": 0.76,            # paramètre conversion log-log
    "usd_eur": 0.92,             # taux de conversion
}

# ---------------------------------------------------------------------------
# PARAMÈTRES CALIBRÉS — SAS OpRisk Global (juin 2026)
# ---------------------------------------------------------------------------

OPRISK = {
    "source": "SAS OpRisk Global Data, juin 2026",
    "perimetre": "Systems Security + Business Disruption — Finance (2000–2026)",
    "n_incidents": 582,          # périmètre cyber×finance reconstruit (filtrage validé)
    "n_excess": 91,              # excès > seuil (conversion EUR appliquée aux pertes)
    "seuil_u_eur": 20.03,        # M€ (percentile 85%)
    "xi": 0.5954,                # paramètre de queue GPD
    "sigma_eur": 57.97,          # M€
    "p_u": 0.1509,
    "xi_ic90": [0.3044, 0.8313],
    "sigma_ic90": [41.88, 82.80],
    "var_995": 662.78,           # M€ (formule POT corrigée)
    "tvar_99": 1133.05,
    "n_years": 27,               # période 2000–2026 (fréquence propre OpRisk = 582/27 ≈ 21,6/an)          # M€
    "var_995_ic90": [411.5, 1037.1],
    "note": (
        "Source de montants de pertes RÉELS. Biais vers les grandes entités "
        "financières → queue possiblement sous-estimée. Complémentaire de la PRC "
        "(qui couvre un spectre de tailles plus large mais via sévérité dérivée Jacobs). "
        "Pas de hiérarchie 'primaire' en sévérité : deux estimations indépendantes. "
        "Fréquence propre OpRisk ≈ n_incidents/27 ≈ 21,6/an (2000-2026), "
        "à ne JAMAIS mélanger avec λ_ref PRC."
    ),
}

# ---------------------------------------------------------------------------
# PARAMÈTRES CALIBRÉS — FRÉQUENCE (PRC 2019-2025)
# ---------------------------------------------------------------------------

FREQUENCY = {
    "source": "PRC 2025 — MLE NegBin",
    "lambda_ref": 341,           # incidents/an (fréquence de référence)
    "r": None,                   # à calibrer sur PRC
    "p": None,
    "dispersion_factor": 9.20,   # Var/Mean observé — MAINTENU constant entre scénarios
    "facteur_recalibration": 1.30,
}

# ---------------------------------------------------------------------------
# PARAMÈTRES DÉPENDANCE — COPULE GUMBEL & FACTEUR COMMUN
# ---------------------------------------------------------------------------

COPULE = {
    "famille": "Gumbel",
    "theta": 1.8,                # τ de Kendall ≈ 0.444 (validé : écart empirique 0.0013)
    "justification": "Dépendance de queue supérieure entre les 4 briques",
    "alternative": "Facteur commun B~Bernoulli(p_sys)",
    # p_sys ancré sur γ de la variable latente (concentration marché cloud),
    # et non plus une valeur arbitraire. Voir compliance/latent.py ANCHORED_PARAMS.
    "p_sys": 0.68,               # proxy = part de marché AWS+Azure+GCP (Synergy/Canalys 2025)
    # Chargement systémique sur l'aggravation (couplage à la copule) —
    # HYPOTHÈSE DE MODÉLISATION non sourcée, bornée conservativement.
    "aggravation_stress_range": [0.0, 0.15],
}

# ---------------------------------------------------------------------------
# RÉSULTATS CENTRAUX — SCR_DORA (synchronisés avec le pipeline)
# ---------------------------------------------------------------------------

# Grille Δ_DORA = SCR(scénario) - SCR(S0), bootstrap deux niveaux.
# Médiane et IC90% en M€. bootstrap_severity=True uniquement pour OpRisk
# (données brutes disponibles) ; False pour PRC (point fixe, IC sous-estimé).
# Régénérée via notebooks/07_bootstrap_delta_dora.py (n_boot=200, n_sim=20 000)
# APRÈS recalibration de la brique prestataire en surcoût relatif (commensurabilité).
# PRC et OPRISK régénérés et vérifiés dans cet environnement (voir
# outputs/tables/results_delta_dora_bootstrap.csv). PRC : niveau 2 (sévérité) au
# point fixe -> IC sous-estimé. OPRISK : bootstrap réel des 91 excès -> IC large.
DELTA_DORA_GRID = {
    ("PRC", "S1_partiel"):      {"median": 114.6,  "ic90": [89.3, 137.3],       "bootstrap_sev": False},
    ("PRC", "S2_non_conforme"): {"median": 310.6,  "ic90": [249.4, 358.7],      "bootstrap_sev": False},
    ("OPRISK", "S1_partiel"):   {"median": 1514.4, "ic90": [522.5, 7863.2],     "bootstrap_sev": True},
    ("OPRISK", "S2_non_conforme"): {"median": 3879.3, "ic90": [1496.9, 22249.3], "bootstrap_sev": True},
}

# Décomposition par brique (allocation d'Euler, VaR 99.5%, profil médian, theta=0),
# architecture à 3 briques additives (remediation/prestataire/sanction) — l'aggravation
# n'en fait PAS partie : c'est un delta contrefactuel (cf. src/aggregation/lda.py::
# scr_4_briques_report), pas une composante de la somme. Voir
# outputs/tables/results_euler_option_a.csv pour la grille complète par profil et source.
# Prestataire recalibré en surcoût relatif IBM/Ponemon (+8.3%/+11.8%) sur la
# sévérité de remédiation active, au lieu d'une Lognormale à échelle absolue :
# restaure la commensurabilité entre briques et entre sources PRC/OpRisk.
EULER_DECOMPOSITION = {
    "OPRISK": {"remediation": 0.860, "prestataire": 0.140, "sanction": 0.0003},
    "PRC":    {"remediation": 0.854, "prestataire": 0.141, "sanction": 0.005},
    "note": (
        "Remédiation dominante sous les deux sources (85-86%), prestataire "
        "minoritaire mais non négligeable (14%), structure cohérente entre "
        "sources depuis la recalibration du prestataire en surcoût relatif. "
        "La sanction reste marginale sous les deux sources."
    ),
}

SCR_DORA = {
    "cap_eur": 40.0,             # M€ — plafond de sévérité PRC (ξ≥1), ancré capacité réassurance
    "constat_source_domine": (
        "Le choix de source de sévérité (PRC ξ=1.30 vs OpRisk ξ=0.60) domine "
        "le résultat plus que le scénario de conformité : écart ×19 sur la VaR "
        "médiane (profil médian) entre sources, supérieur à l'écart S1↔S2 sous "
        "une même source."
    ),
    "note": (
        "Le SCR_DORA est une distribution large, pas un point. Trois sources "
        "d'incertitude se cumulent : calibration (bootstrap), source de sévérité "
        "(PRC vs OpRisk), et scénario de conformité (S0/S1/S2). L'IC90% PRC est "
        "structurellement sous-estimé (sévérité au point fixe, pas de données brutes)."
    ),
}

# ---------------------------------------------------------------------------
# HACKMAGEDDON — PROPORTIONS S1 2026
# ---------------------------------------------------------------------------

HACKMAGEDDON = {
    "source": "Hackmageddon (Paolo Passeri)",
    "periode": "Janvier–Juin 2026",
    "n_incidents": 1041,
    "n_identifies": 840,
    "taux_identification": 0.807,
    "proportions": {
        "phishing_social_eng": 0.388,
        "exploit_vuln":        0.338,
        "supply_chain_tiers":  0.158,
        "identifiants":        0.063,
        "autres":              0.053,
    },
    "surface_tlpt": 0.496,       # exploit + supply chain (art. 26)
    "surface_tiers": 0.158,      # supply chain seul (art. 28-44)
}

# ---------------------------------------------------------------------------
# MULTIPLICATEURS DORA — sources de calibration (résumé ; détail dans negbin.py)
# ---------------------------------------------------------------------------

MULTIPLICATEURS_SOURCES = {
    "phishing_social_eng": "Ponemon/IBM 2025 — formation réduit le risque jusqu'à 86%",
    "exploit_vuln":        "ENISA Threat Landscape 2025 — conversion 70% vs 27%, ratio ×2.6",
    "supply_chain_tiers":  "IBM/Ponemon + SecurityScorecard — surcoût +11.8%/+8.3%, part 15%→36%",
    "identifiants":        "Microsoft Research arXiv:2305.00945 — MFA réduit 99.22% (tempéré)",
    "multiplicateur_global_S2": 2.49,   # centre ; IC90% λ = [742.7, 947.4]
}

# ---------------------------------------------------------------------------
# VARIABLE LATENTE — paramètres ancrés (Option B)
# ---------------------------------------------------------------------------

LATENT_ANCHORED = {
    "gamma": 0.68,               # proxy concentration cloud (Synergy/Canalys 2025)
    "p_ref_global": 0.50,        # ~50% non pleinement conformes fin 2025 (industry surveys)
    "p_ref_by_pillar": {         # 1 - taux de pleine conformité (Deloitte 2025, ESA dry-run)
        "incident_mgmt": 0.52,
        "ict_risk_mgmt": 0.75,
        "resilience_test": 0.92,
        "third_party": 0.92,
        "roi_data_quality": 0.935,
    },
    "note": "Paramètres illustratifs de la PHASE TRANSITOIRE de DORA (2025), "
            "non représentatifs d'un régime stationnaire. β non estimés (illustratifs).",
}

# ---------------------------------------------------------------------------
# LIMITES ÉPISTÉMIQUES (pour la rédaction)
# ---------------------------------------------------------------------------

LIMITES = {
    "absence_donnees_dora": (
        "DORA est en vigueur depuis janvier 2025. Aucun historique de pertes "
        "conditionnel au niveau de conformité n'existe à ce stade."
    ),
    "biais_prc": (
        "La PRC est une base US de data breaches déclarées. Elle sous-représente "
        "les incidents de disponibilité/continuité et les petites pertes européennes."
    ),
    "biais_oprisk": (
        "OpRisk surreprésente les grandes entités financières et les pertes "
        "judiciarisées (46% US). Les pertes < seuil de notification sont absentes."
    ),
    "biais_hackmageddon": (
        "Base déclarative à fort biais de médiatisation. Le niveau absolu de "
        "fréquence n'est pas calibrant ; seules les proportions relatives le sont. "
        "Taxonomie des types d'attaque instable dans le temps (piège ransomware)."
    ),
    "quantile_995": (
        "Présenter un SCR_DORA ponctuel au 99.5% serait une surinterprétation. "
        "L'incertitude de paramètre seule génère un IC d'un facteur 2.5 sur la VaR."
    ),
    "sanction_marginale": (
        "La brique sanction pèse ~0.3% du capital : le plafond réglementaire "
        "(2-20M€) est négligeable face à la queue lourde du risque opérationnel."
    ),
    "aggravation_stress_non_source": (
        "Le chargement systémique sur l'aggravation (couplage copule) est une "
        "hypothèse de modélisation bornée à 15%, non issue d'une source externe."
    ),
}