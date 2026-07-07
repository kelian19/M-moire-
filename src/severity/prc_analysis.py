"""
severity/prc_analysis.py
--------------------------
Conversion Jacobs (2014) et calibration GPD sur la base PRC brute
(Privacy Rights Clearinghouse — Data_Breach_Chronology.xlsx).

La PRC ne contient pas de montant financier : seul le nombre d'enregistrements
compromis (`total_affected`) est renseigné. Jacobs (2014) — repris par Eling &
Loperfido (2017), cf. également Dountio Zaboué (2026, §3.2) — propose une
relation log-log entre le coût financier L (en $) et la taille de la brèche X
(nombre d'enregistrements), calibrée sur les rapports Cost of Data Breach
(Ponemon Institute) :

    ln(L) = a + b * ln(X),   a = 7.68,  b = 0.76

Base du logarithme : NATURELLE (ln), pas décimale. Une conversion en log10 avec
les mêmes coefficients produit des coûts totalement irréalistes (dizaines de
millions de dollars pour une brèche d'un seul enregistrement) ; en ln, le
coût par enregistrement reste dans la fourchette 100-200 $/enregistrement
usuellement rapportée par Ponemon sur la plage de validité du modèle
(jusqu'à ~100 000 enregistrements). Vérifié empiriquement (voir
notebooks/13_prc_jacobs_calibration.py) : c'est la seule des 4 combinaisons
testées (log10/ln × coefficients 2014/2018) qui reste dans un ordre de
grandeur plausible.

⚠️ Les valeurs ξ=1.30 / u=0.128 M€ / σ=0.257 M€ précédemment présentes dans
config.py provenaient d'une référence externe (jamais recalculées sur ce
fichier brut dans ce projet — n_records=None en attestait). Ce module fournit
la PREMIÈRE calibration réalisée directement sur les données PRC brutes.
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

JACOBS_A = 7.68
JACOBS_B = 0.76
USD_EUR = 0.92

PERIOD_MIN_YEAR = 2019
PERIOD_MAX_YEAR = 2025


def load_prc(path: str,
             year_min: int = PERIOD_MIN_YEAR,
             year_max: int = PERIOD_MAX_YEAR) -> pd.DataFrame:
    """
    Charge la PRC brute, filtre sur la période retenue (2019-2025, cohérent
    avec config.py::PRC["period"]) et sur les incidents avec un nombre
    d'enregistrements strictement positif renseigné.
    """
    if str(path).lower().endswith(".csv"):
        # Export PRC brut : délimiteur pipe « | », champs entre guillemets
        # pouvant contenir des retours à la ligne. On ne charge que les
        # colonnes utiles pour éviter de matérialiser les 660 Mo en mémoire.
        df = pd.read_csv(path, sep="|", usecols=["breach_date", "total_affected"],
                         dtype=str, engine="c")
    else:
        df = pd.read_excel(path)
    df["year"] = pd.to_datetime(df["breach_date"], errors="coerce").dt.year
    df["total_affected"] = pd.to_numeric(df["total_affected"], errors="coerce")

    d = df[(df["year"] >= year_min) & (df["year"] <= year_max)].copy()
    d = d[d["total_affected"] > 0].dropna(subset=["total_affected"])

    print(f"PRC chargée : {len(d):,} incidents avec total_affected > 0 "
          f"({year_min}-{year_max})")
    return d


def jacobs_severity_eur_m(total_affected: np.ndarray,
                          a: float = JACOBS_A,
                          b: float = JACOBS_B,
                          usd_eur: float = USD_EUR) -> np.ndarray:
    """
    Applique la conversion Jacobs (2014) : ln(L_usd) = a + b*ln(X).
    Retourne la sévérité en M€.
    """
    X = np.asarray(total_affected, dtype=float)
    ln_L_usd = a + b * np.log(X)
    L_usd = np.exp(ln_L_usd)
    return L_usd * usd_eur / 1e6


def load_prc_severity_eur_m(path: str,
                            year_min: int = PERIOD_MIN_YEAR,
                            year_max: int = PERIOD_MAX_YEAR) -> np.ndarray:
    """Charge la PRC et retourne directement la sévérité dérivée (M€)."""
    d = load_prc(path, year_min, year_max)
    return jacobs_severity_eur_m(d["total_affected"].values)


if __name__ == "__main__":
    import os
    PRC_PATH = "data/raw/Data_Breach_Chronology.xlsx"

    if not os.path.exists(PRC_PATH):
        print(f"Fichier non trouvé : {PRC_PATH}")
    else:
        severities = load_prc_severity_eur_m(PRC_PATH)
        print(f"Sévérité dérivée (M€) : médiane={np.median(severities):.4f} | "
              f"P85={np.percentile(severities, 85):.4f} | "
              f"max={severities.max():.1f}")
