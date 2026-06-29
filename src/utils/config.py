"""
utils/config.py
---------------
Configuration centrale du projet SCR_DORA.
Tous les paramètres calibrés sont centralisés ici.
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
    "n_incidents": 570,
    "n_excess": 86,
    "seuil_u_eur": 20.03,        # M€ (percentile 85%)
    "xi": 0.5954,                # paramètre de queue GPD
    "sigma_eur": 57.97,          # M€
    "p_u": 0.1509,
    "xi_ic90": [0.3044, 0.8313],
    "sigma_ic90": [41.88, 82.80],
    "var_995": 663.0,        # M€ (corrigé)
    "tvar_99": 1133.7,
    "var_995_ic90": [410.7, 1018.7],
    "note": "Validation croisée qualitative uniquement (seuils incomparables avec PRC)",
}

# ---------------------------------------------------------------------------
# PARAMÈTRES CALIBRÉS — FRÉQUENCE (PRC 2019-2025)
# ---------------------------------------------------------------------------

FREQUENCY = {
    "source": "PRC 2025 — MLE NegBin",
    "lambda_ref": 341,           # incidents/an (fréquence de référence)
    "r": None,                   # à calibrer sur PRC
    "p": None,
    "dispersion_factor": 9.20,   # Var/Mean observé
    "facteur_recalibration": 1.30,
}

# ---------------------------------------------------------------------------
# PARAMÈTRES DÉPENDANCE — COPULE GUMBEL
# ---------------------------------------------------------------------------

COPULE = {
    "famille": "Gumbel",
    "theta": 1.8,
    "justification": "Queue upper tail dependence, incidents systémiques",
    "alternative": "Facteur commun B~Bernoulli(p_sys)",
    "p_sys": 0.05,               # probabilité choc systémique
    "choc_factor": 3.0,          # multiplicateur sévérité sous choc
}

# ---------------------------------------------------------------------------
# RÉSULTATS CENTRAUX — SCR_DORA
# ---------------------------------------------------------------------------

SCR_DORA = {
    "scr_central_eur": 83.2,     # M€ (NegBin référence)
    "delta_dora_eur": 33.5,      # M€ (approche C)
    "bootstrap_ic90": [90, 117], # M€
    "cap_eur": 40.0,             # M€ (~5% fonds propres)
    "note": (
        "Le SCR_DORA est une distribution large, pas un point. "
        "L'IC90% représente l'incertitude de calibration uniquement. "
        "L'incertitude de modèle (choix copule, scénarios) est supplémentaire."
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
        "judiciarisées. Les pertes < seuil de notification sont absentes."
    ),
    "biais_hackmageddon": (
        "Base déclarative à fort biais de médiatisation. Le niveau absolu de "
        "fréquence n'est pas calibrant ; seules les proportions relatives le sont."
    ),
    "quantile_995": (
        "Présenter un SCR_DORA ponctuel au 99.5% serait une surinterprétation. "
        "L'incertitude de paramètre seule génère un IC d'un facteur 2.5 sur la VaR."
    ),
}
