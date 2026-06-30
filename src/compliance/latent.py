"""
compliance/latent.py
--------------------
Variable latente de conformité DORA — modèle structurel de Merton-Vasicek.

OBJECTIF
========
Modéliser la probabilité qu'une entité d'assurance se retrouve en défaut de
conformité DORA à un instant t, comme une variable latente (score continu
[0,1]), conditionnellement à l'état de l'environnement cyber.

Cadre (cf. section réglementaire du mémoire, §3) :

    C*_{i,t} = β^T X_{i,t} + γ·Θ_t + sqrt(1-γ²)·Z_{i,t}

avec :
    C*_{i,t}  capacité de conformité latente de l'entité i (loi N(0,1))
    X_{i,t}   covariables observables de qualité du cadre TIC
    β         sensibilités associées
    Θ_t       facteur de risque systématique du secteur ~ N(0,1)
    γ         corrélation de conformité (sensibilité aux chocs systémiques)
    Z_{i,t}   choc idiosyncratique ~ N(0,1)

Le défaut survient si C*_{i,t} < K_i, avec K_i = Φ⁻¹(p_i).

La probabilité de défaut conditionnelle (point-in-time) à Θ_t = θ :

    PCD_i(θ) = Φ( (Φ⁻¹(p_i) - β^T X_{i,t} - γ·θ) / sqrt(1-γ²) )

═══════════════════════════════════════════════════════════════════════════
⚠️  STATUT MÉTHODOLOGIQUE — À LIRE AVANT TOUTE UTILISATION
═══════════════════════════════════════════════════════════════════════════
Ce module est un SIMULATEUR PARAMÉTRIQUE, pas un modèle estimé.

  - DORA est entré en application le 17/01/2025 ; il n'existe pas encore de
    panel d'entités avec leurs métriques de conformité observées sur la durée.
  - Les coefficients β, la corrélation γ et la probabilité de référence p_i
    ne sont donc PAS estimés empiriquement (pas de PLS-SEM possible faute de
    données) : ce sont des valeurs ILLUSTRATIVES, choisies plausibles.
  - Le module démontre la MÉCANIQUE du modèle (effet d'un profil d'entité,
    effet d'amplification systémique via γ), pas un résultat calibré.

Tout chiffre produit ici doit être présenté dans le mémoire comme une
illustration du mécanisme, jamais comme une probabilité estimée pour une
entité réelle. Les paramètres sont isolés dans ILLUSTRATIVE_PARAMS pour qu'on
puisse les remplacer par des valeurs ancrées sur données dès qu'elles existent
(amélioration "Option B" : proxies ACPR, taux de pénétration cloud pour γ…).
═══════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from scipy.stats import norm
from dataclasses import dataclass, field
from typing import Dict, List


# ---------------------------------------------------------------------------
# 1. PARAMÈTRES ILLUSTRATIFS (à remplacer par des valeurs estimées — Option B)
# ---------------------------------------------------------------------------

# Covariables de conformité (vecteur X). Chaque covariable est NORMALISÉE :
# valeur centrée réduite, 0 = profil médian du marché, +1 = un écart-type
# meilleur que la médiane, -1 = un écart-type moins bon.
#
# Convention de signe : un β POSITIF signifie que la covariable AUGMENTE la
# capacité de conformité (donc RÉDUIT la probabilité de défaut). Les bornes
# sont des choix illustratifs cohérents avec l'intuition réglementaire.
ILLUSTRATIVE_PARAMS = {
    # Covariable : (libellé, coefficient β illustratif)
    "covariates": {
        "art30_contracts_pct":   ("% contrats tiers conformes Art. 30", 0.45),
        "rto_inverse":           ("Rapidité de rétablissement (1/RTO)",  0.35),
        "phishing_resist":       ("Taux de résistance au phishing",      0.40),
        "security_budget_ratio": ("Budget sécurité / CA",                0.30),
    },
    # Corrélation de conformité γ ∈ [0,1] : sensibilité au choc systémique.
    # Illustratif : 0.35 = dépendance systémique modérée. Une entité très
    # dépendante d'un cloud unique aurait un γ plus élevé (→ contagion externe).
    "gamma": 0.35,
    # Probabilité de non-conformité "through-the-cycle" de référence (p_i).
    # Illustratif : 8% — niveau plausible en phase de montée en charge DORA.
    "p_ref": 0.08,
}


# ═══════════════════════════════════════════════════════════════════════════
# PARAMÈTRES ANCRÉS SUR DONNÉES (Option B) — proxies sourcés
# ═══════════════════════════════════════════════════════════════════════════
# Contrairement à ILLUSTRATIVE_PARAMS ci-dessus, les valeurs suivantes sont
# ancrées sur des sources publiques. Elles restent des PROXIES (DORA est trop
# récent pour une estimation économétrique propre), mais chaque chiffre est
# traçable. Le choix de traduction proxy → paramètre reste un jugement de
# modélisation, signalé comme tel.
#
# ── p_ref (probabilité de non-conformité de référence) ────────────────────
#   Sources convergentes fin 2025 / début 2026 :
#     • ~50% des institutions se déclarent pleinement conformes fin 2025
#       (industry surveys, doragrc.com) → non-conformité globale ~50%.
#     • Deloitte European Survey 2025 (36 entités, 28 pays), conformité par
#       pilier : Incidents 48%, Risque ICT 25%, Tests 8%, Risque tiers 8%
#       → non-conformité par pilier de 52% à 92%.
#     • ESA dry-run 2024 : 6,5% des ~1000 entités passent les 116 contrôles
#       qualité du Registre d'Informations → 93,5% en échec sur ce volet.
#   ⇒ p_ref n'est PAS unique : il dépend du pilier considéré. On fournit un
#     dictionnaire par pilier, plus une valeur "globale" (~50%).
#
# ── gamma (corrélation systémique, proxy = dépendance cloud partagée) ──────
#   Sources :
#     • AWS + Azure + Google Cloud = ~68% du marché mondial de l'infra cloud
#       en 2025 (Synergy/Canalys). Concentration sur 3 fournisseurs.
#     • 87% des organisations en multi-cloud, 73% en hybride (Q1 2026).
#   ⇒ La part du marché captée par les 3 hyperscalers (~0,68) est un proxy
#     direct de la corrélation systémique : si une grande partie du secteur
#     dépend des mêmes fournisseurs, un choc sur l'un d'eux est systémique.
#     On retient gamma ≈ 0,68 comme borne "haute" (dépendance forte), et on
#     conserve un balayage de gamma dans le rapport pour montrer la
#     sensibilité — la valeur exacte par entité dépend de son architecture.
# ═══════════════════════════════════════════════════════════════════════════

ANCHORED_PARAMS = {
    "covariates": ILLUSTRATIVE_PARAMS["covariates"],  # β toujours illustratifs (pas estimables)
    "gamma": 0.68,  # proxy = part de marché des 3 hyperscalers (Synergy/Canalys 2025)
    "p_ref": 0.50,  # proxy = non-conformité globale fin 2025 (industry surveys)
}

# Probabilité de non-conformité PAR PILIER DORA (Deloitte 2025 + ESA dry-run)
# Valeur = 1 - taux de pleine conformité observé.
P_REF_BY_PILLAR = {
    "incident_mgmt":   1 - 0.48,   # Gestion des incidents ICT
    "ict_risk_mgmt":   1 - 0.25,   # Gestion du risque ICT
    "resilience_test": 1 - 0.08,   # Tests de résilience (TLPT)
    "third_party":     1 - 0.08,   # Gestion du risque tiers (Art. 28-44)
    "roi_data_quality": 1 - 0.065, # Qualité Registre d'Informations (ESA dry-run)
}

SOURCES_ANCHORED = {
    "p_ref_global": "Industry surveys fin 2025 (~50% pleinement conformes) — doragrc.com",
    "p_ref_pillar": "Deloitte European Survey 2025 (36 entités, 28 pays) ; "
                    "ESA dry-run 2024 (6,5% RoI conformes sur ~1000 entités)",
    "gamma": "Synergy Research / Canalys 2025 — AWS+Azure+GCP ≈ 68% du marché "
             "cloud mondial ; 87% multi-cloud, 73% hybride (Q1 2026)",
    "beta": "NON estimés — pas de panel d'entités avec métriques observées "
            "(DORA trop récent). Valeurs illustratives conservées.",
}


# ---------------------------------------------------------------------------
# 2. PROFIL D'ENTITÉ
# ---------------------------------------------------------------------------

@dataclass
class EntityProfile:
    """
    Profil de conformité d'une entité, exprimé en covariables normalisées.
    0 = médiane marché ; valeurs positives = meilleur que la médiane.
    """
    name: str
    covariates: Dict[str, float] = field(default_factory=dict)

    def beta_dot_x(self, params: dict) -> float:
        """Calcule β^T X pour cette entité, selon les coefficients fournis."""
        total = 0.0
        for key, (_label, beta) in params["covariates"].items():
            x = self.covariates.get(key, 0.0)  # 0 = médiane si non renseigné
            total += beta * x
        return total


# Trois profils types illustratifs
PROFILS_TYPES = {
    "leader": EntityProfile("Entité mature (leader)", {
        "art30_contracts_pct": 1.5, "rto_inverse": 1.2,
        "phishing_resist": 1.3, "security_budget_ratio": 1.0,
    }),
    "median": EntityProfile("Entité médiane", {
        "art30_contracts_pct": 0.0, "rto_inverse": 0.0,
        "phishing_resist": 0.0, "security_budget_ratio": 0.0,
    }),
    "retard": EntityProfile("Entité en retard", {
        "art30_contracts_pct": -1.3, "rto_inverse": -1.0,
        "phishing_resist": -1.2, "security_budget_ratio": -0.8,
    }),
}


# ---------------------------------------------------------------------------
# 3. PROBABILITÉ DE DÉFAUT DE CONFORMITÉ
# ---------------------------------------------------------------------------

def threshold_K(p_ref: float) -> float:
    """Seuil de défaut K_i = Φ⁻¹(p_i)."""
    return norm.ppf(p_ref)


def pcd_conditional(entity: EntityProfile, theta: float,
                    params: dict = None) -> float:
    """
    Probabilité de défaut de conformité POINT-IN-TIME, conditionnelle à
    l'état de l'environnement cyber Θ_t = θ.

        PCD_i(θ) = Φ( (Φ⁻¹(p_i) - β^T X - γ·θ) / sqrt(1-γ²) )

    Parameters
    ----------
    entity : profil de l'entité (covariables)
    theta  : état de l'environnement cyber. θ=0 médian, θ<0 = crise
             systémique (menace élevée), θ>0 = environnement clément.
    params : dict de paramètres (défaut : ILLUSTRATIVE_PARAMS)

    Returns
    -------
    float : probabilité de défaut ∈ [0,1]
    """
    params = params or ILLUSTRATIVE_PARAMS
    gamma = params["gamma"]
    K = threshold_K(params["p_ref"])
    bx = entity.beta_dot_x(params)

    numerator = K - bx - gamma * theta
    denominator = np.sqrt(1.0 - gamma ** 2)
    return float(norm.cdf(numerator / denominator))


def pcd_unconditional(entity: EntityProfile, params: dict = None,
                      n_sim: int = 100_000, seed: int = 42) -> dict:
    """
    Probabilité de défaut INCONDITIONNELLE, en intégrant sur la loi de Θ.
    Calculée par simulation Monte Carlo de l'environnement systémique.

    Renvoie la PCD moyenne ET sa distribution (car selon l'état systémique,
    la PCD varie — c'est tout l'intérêt du modèle à facteur commun).
    """
    params = params or ILLUSTRATIVE_PARAMS
    rng = np.random.default_rng(seed)
    thetas = rng.standard_normal(n_sim)
    pcds = np.array([pcd_conditional(entity, t, params) for t in thetas])

    return {
        "entity": entity.name,
        "pcd_mean": float(pcds.mean()),
        "pcd_median": float(np.median(pcds)),
        "pcd_p95": float(np.percentile(pcds, 95)),   # PCD en environnement dégradé
        "pcd_p99": float(np.percentile(pcds, 99)),   # PCD en crise systémique
        "distribution": pcds,
    }


# ---------------------------------------------------------------------------
# 4. EFFET D'AMPLIFICATION SYSTÉMIQUE (rôle de γ)
# ---------------------------------------------------------------------------

def systemic_amplification(entity: EntityProfile,
                           gammas: List[float] = None,
                           theta_crisis: float = -2.5,
                           params: dict = None) -> Dict[float, dict]:
    """
    Montre comment la corrélation γ amplifie la PCD en cas de crise cyber.

    Pour différentes valeurs de γ, compare la PCD en environnement normal
    (θ=0) vs en crise systémique (θ=theta_crisis, ex. -2.5 ≈ choc à 0.6%).
    Plus γ est élevé (entité dépendante d'infrastructures partagées), plus
    l'écart est dramatique → contagion EXTERNE.
    """
    params = params or ILLUSTRATIVE_PARAMS
    gammas = gammas or [0.1, 0.3, 0.5, 0.7, 0.9]
    base = dict(params)
    out = {}
    for g in gammas:
        p = dict(base); p["gamma"] = g
        pcd_normal = pcd_conditional(entity, 0.0, p)
        pcd_crisis = pcd_conditional(entity, theta_crisis, p)
        out[g] = {
            "pcd_normal": pcd_normal,
            "pcd_crisis": pcd_crisis,
            "amplification": pcd_crisis / pcd_normal if pcd_normal > 0 else np.inf,
        }
    return out


# ---------------------------------------------------------------------------
# 5. RAPPORT ILLUSTRATIF
# ---------------------------------------------------------------------------

def full_report(params: dict = None):
    """Génère un rapport illustratif complet du modèle de variable latente."""
    params = params or ILLUSTRATIVE_PARAMS

    print("=" * 64)
    print("  VARIABLE LATENTE DE CONFORMITÉ DORA — modèle Merton-Vasicek")
    print("  (SIMULATEUR PARAMÉTRIQUE — paramètres illustratifs, non estimés)")
    print("=" * 64)
    print(f"  γ (corrélation systémique) = {params['gamma']}")
    print(f"  p_i (défaut de référence)  = {params['p_ref']:.1%}")
    print(f"  Seuil K = Φ⁻¹(p_i)         = {threshold_K(params['p_ref']):.4f}")

    print(f"\n  --- PCD par profil d'entité ---")
    print(f"  {'Profil':28s} {'PCD(θ=0)':>10s} {'PCD moy.':>10s} {'PCD crise':>11s}")
    for key, entity in PROFILS_TYPES.items():
        pcd0 = pcd_conditional(entity, 0.0, params)
        unc = pcd_unconditional(entity, params, n_sim=50_000)
        pcd_crisis = pcd_conditional(entity, -2.5, params)
        print(f"  {entity.name:28s} {pcd0:>9.2%} {unc['pcd_mean']:>9.2%} {pcd_crisis:>10.2%}")

    print(f"\n  --- Amplification systémique (entité médiane) ---")
    print(f"  Effet de γ sur le ratio PCD(crise)/PCD(normal) :")
    amp = systemic_amplification(PROFILS_TYPES["median"], params=params)
    print(f"  {'γ':>5s} {'PCD normal':>12s} {'PCD crise':>12s} {'amplif.':>10s}")
    for g, r in amp.items():
        print(f"  {g:>5.1f} {r['pcd_normal']:>11.2%} {r['pcd_crisis']:>11.2%} {r['amplification']:>9.1f}x")

    print(f"\n  → Plus γ est élevé (dépendance à des infrastructures partagées),")
    print(f"    plus une crise cyber systémique amplifie la probabilité de défaut.")
    print(f"    C'est le lien quantitatif avec la CONTAGION EXTERNE (tiers ICT).")
    print("=" * 64)


def report_anchored():
    """
    Rapport Option B — PCD avec paramètres ancrés sur données (proxies sourcés).
    Décline la probabilité de défaut par PILIER DORA, en utilisant les taux
    de non-conformité réellement observés (Deloitte 2025, ESA dry-run).
    """
    print("=" * 66)
    print("  VARIABLE LATENTE DORA — PARAMÈTRES ANCRÉS (Option B)")
    print("  Proxies sourcés — voir SOURCES_ANCHORED")
    print("=" * 66)
    print(f"  γ (proxy concentration cloud) = {ANCHORED_PARAMS['gamma']}")
    print(f"     [AWS+Azure+GCP ≈ 68% du marché — Synergy/Canalys 2025]")
    print(f"  p_ref global = {ANCHORED_PARAMS['p_ref']:.0%}")
    print(f"     [~50% pleinement conformes fin 2025 — industry surveys]")

    print(f"\n  --- PCD de référence PAR PILIER DORA (entité médiane, θ=0) ---")
    print(f"  {'Pilier':22s} {'Non-conf.':>10s} {'PCD(θ=0)':>10s} {'PCD crise':>11s}")
    median = PROFILS_TYPES["median"]
    for pillar, p_ref in P_REF_BY_PILLAR.items():
        params = dict(ANCHORED_PARAMS); params["p_ref"] = p_ref
        pcd0 = pcd_conditional(median, 0.0, params)
        pcd_crisis = pcd_conditional(median, -2.5, params)
        print(f"  {pillar:22s} {p_ref:>9.1%} {pcd0:>9.1%} {pcd_crisis:>10.1%}")

    print(f"\n  Lecture : les piliers Tests de résilience et Risque tiers")
    print(f"  (non-conformité ~92%) dominent le risque de défaut DORA. En cas")
    print(f"  de crise systémique (θ=-2.5) avec γ=0.68 (forte dépendance cloud),")
    print(f"  la quasi-totalité des entités médianes bascule en défaut sur ces")
    print(f"  piliers — c'est le scénario de contagion externe le plus sévère.")
    print("=" * 66)


def compare_A_vs_B():
    """
    Compare les deux paramétrisations du modèle de variable latente :
      A — paramètres illustratifs (pédagogiques, non sourcés)
      B — paramètres ancrés sur données (proxies sourcés, Option B)

    Montre l'effet du choix de paramètres sur la PCD, pour une même entité
    médiane. L'écart entre A et B EST un résultat : il mesure de combien la
    conclusion dépend des hypothèses, et illustre pourquoi l'ancrage sur
    données change la lecture du risque.
    """
    median = PROFILS_TYPES["median"]

    print("=" * 70)
    print("  COMPARAISON A (illustratif) vs B (ancré sur données)")
    print("  Entité médiane — effet du choix de paramètres sur la PCD")
    print("=" * 70)

    print(f"\n  {'Paramètre':28s} {'A (illustratif)':>18s} {'B (ancré)':>18s}")
    print(f"  {'-'*64}")
    print(f"  {'γ (corrélation systémique)':28s} {ILLUSTRATIVE_PARAMS['gamma']:>18.2f} "
          f"{ANCHORED_PARAMS['gamma']:>18.2f}")
    print(f"  {'p_ref (non-conformité)':28s} {ILLUSTRATIVE_PARAMS['p_ref']:>17.0%} "
          f"{ANCHORED_PARAMS['p_ref']:>17.0%}")

    pcd0_A = pcd_conditional(median, 0.0, ILLUSTRATIVE_PARAMS)
    pcd0_B = pcd_conditional(median, 0.0, ANCHORED_PARAMS)
    pcdc_A = pcd_conditional(median, -2.5, ILLUSTRATIVE_PARAMS)
    pcdc_B = pcd_conditional(median, -2.5, ANCHORED_PARAMS)

    print(f"\n  {'PCD (environnement normal)':28s} {pcd0_A:>17.1%} {pcd0_B:>17.1%}")
    print(f"  {'PCD (crise systémique)':28s} {pcdc_A:>17.1%} {pcdc_B:>17.1%}")

    print(f"\n  Lecture :")
    print(f"  • B donne une PCD bien plus élevée que A, parce que les taux de")
    print(f"    non-conformité réellement observés fin 2025 (~50% global, jusqu'à")
    print(f"    92% sur tests et tiers) sont supérieurs à l'hypothèse illustrative.")
    print(f"  • Sous B, la dépendance cloud forte (γ=0.68) rend la crise")
    print(f"    systémique presque certaine de faire basculer en défaut.")
    print(f"  • L'écart A↔B mesure la sensibilité de la conclusion aux hypothèses :")
    print(f"    il faut présenter B comme reflet de la PHASE TRANSITOIRE de DORA,")
    print(f"    pas comme un régime permanent (p_ref baissera avec la mise en")
    print(f"    conformité progressive du marché).")
    print("=" * 70)


if __name__ == "__main__":
    full_report()
    print("\n")
    report_anchored()
    print("\n")
    compare_A_vs_B()
