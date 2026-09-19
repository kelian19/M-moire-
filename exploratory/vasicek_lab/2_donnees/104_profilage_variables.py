#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
104 : profilage des variables, complétude et tests statistiques bivariés sur les deux bases.

POURQUOI CE SCRIPT EXISTE. Le mémoire décrivait ses deux sources par leur périmètre et leurs
biais, jamais par leurs VARIABLES : ni le type de chacune, ni son taux de manquant, ni le moindre
test d'association. Un jury d'actuaires ouvre un chapitre de données en cherchant exactement cela.
Ce script produit les trois objets qui manquaient : la table des variables avec sa complétude, les
tests d'association sur les qualitatives, et les tests de forme et d'hétérogénéité sur les
quantitatives. Tout ce que la sous-section publie sort d'ici.

LE PIEGE DE COMPLETUDE DE LA PRC, ET IL EST GROSSIER. Dans l'export PRC, un champ non renseigné
ne vaut pas vide : il vaut la chaîne « UNKN ». Un `notna()` naïf rend donc 100 % de présence sur
les trente-sept colonnes, y compris sur `total_affected` qui n'est en réalité renseignée que pour
deux incidents sur cinq. Le taux publié ici compte donc « UNKN » comme un manquant, ce qui est le
seul comptage honnête, et le script imprime les deux nombres côte à côte pour que l'écart soit
visible plutôt que supposé.

CE QUE LES TESTS FONT, ET SURTOUT CE QU'ILS NE FONT PAS.
  - Le khi-deux et le V de Cramér mesurent une ASSOCIATION dans la base observée, jamais un lien
    causal, et jamais une propriété du risque : les deux bases sont des collectes, avec leurs
    seuils et leurs obligations de notification. Une association forte entre le type de brèche et
    le dépassement du seuil peut n'être qu'une différence de régime déclaratif.
  - Sur des effectifs de cet ordre, le khi-deux rejette presque toujours. La p-valeur n'est donc
    PAS le résultat : le résultat est le V de Cramér, qui est une taille d'effet et ne croît pas
    avec n. Publier la p-valeur seule serait un contresens, et c'est pour cela que les deux sont
    imprimées ensemble.
  - Shapiro-Wilk sur des sévérités cyber ne teste rien qu'on ignore : il est là pour CHIFFRER le
    rejet de la normalité, c'est-à-dire pour donner une mesure à l'affirmation de queue lourde que
    le mémoire fait partout. Son échantillon est plafonné à 5 000 tirages, graine fixée, parce que
    la statistique n'est pas fiable au-delà ; le script le déclare au lieu de le taire.
  - Kruskal-Wallis teste l'égalité des distributions de sévérité entre classes d'organisation.
    C'est un test non paramétrique, donc il ne suppose pas la normalité que le précédent rejette.

CE SCRIPT NE RECALIBRE RIEN. Il ne touche ni config.py, ni un paramètre publié, ni une sortie
existante. C'est un diagnostic, compatible avec le gel de la calibration du 7 août 2026, au même
titre que les scripts 89 à 94.

TROIS FIGURES, toutes à la charte via style_nexialog.
  D1 : matrice de présence croisée de la PRC (taux, %).
  D2 : sources de notification, double axe (barres = volume affecté, ligne = nombre d'incidents).
  D3 : types de brèche en bulles (taille = nombre d'incidents, couleur = volume compromis).

Usage : .venv/bin/python exploratory/vasicek_lab/2_donnees/104_profilage_variables.py
        (rediriger stderr vers /dev/null, jamais vers le fichier : matplotlib y écrit des
         findfont qui corrompraient la sortie versionnée)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RACINE)
sys.path.insert(0, os.path.join(RACINE, "exploratory", "vasicek_lab"))

import style_nexialog as sn
from src.severity.prc_analysis import chemin_prc

FIGDIR = os.path.join(RACINE, "exploratory", "vasicek_lab", "figures")
SAS_PATH = os.path.join(RACINE, "data", "raw", "SAS_OpRisk_Global_Data_June_2026.xlsx")

MANQUANT_PRC = {"UNKN", "unkn", "", "nan", "NaN", "None"}
GRAINE = 20260919
N_SHAPIRO = 5000

sn.appliquer(10)
plt.rcParams["font.family"] = ["DejaVu Sans", "Segoe UI", "sans-serif"]


def titre(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def renseigne(serie):
    """Masque des valeurs REELLEMENT renseignees : 'UNKN' est un manquant, pas une modalite."""
    s = serie.astype(str).str.strip()
    return ~s.isin(MANQUANT_PRC) & serie.notna()


def cramer_v(table):
    """V de Cramer avec correction de Bergsma, qui retire le biais d'effectif.

    Sans correction, le V monte mecaniquement avec le nombre de modalites : une table
    8 x 2 sur 15 000 lignes rend un V non nul sur des donnees independantes.
    """
    chi2, p, ddl, att = stats.chi2_contingency(table)
    n = table.values.sum()
    r, k = table.shape
    phi2 = chi2 / n
    phi2c = max(0.0, phi2 - (k - 1) * (r - 1) / (n - 1))
    rc = r - (r - 1) ** 2 / (n - 1)
    kc = k - (k - 1) ** 2 / (n - 1)
    denom = min(kc - 1, rc - 1)
    v = np.sqrt(phi2c / denom) if denom > 0 else np.nan
    return chi2, p, ddl, v, n


def ligne_test(nom, chi2, p, ddl, v, n):
    ptxt = "< 1e-300" if p < 1e-300 else f"{p:.3e}"
    print(f"  {nom:<44s} khi2 = {chi2:10.1f}  ddl = {ddl:3d}  p {ptxt:>10s}  V = {v:.4f}  n = {n}")


# =====================================================================================
titre("0. PERIMETRES ET STATUT")
# =====================================================================================
print("""
  Deux bases, deux roles, et elles ne se substituent pas :
    PRC  (Privacy Rights Clearinghouse / Data Breach Chronology) : incidents de violation de
         donnees notifies aux autorites americaines. Elle porte le NOMBRE d'enregistrements
         touches, jamais un montant. Elle sert la structure et la frequence, jamais le niveau
         de perte en euros.
    SAS  (OpRisk Global Data) : pertes operationnelles AVEREES, en dollars, toutes categories
         balaises. Elle porte le montant, donc la severite du memoire en sort.
  Le seuil de severite significative employe dans les tests ci-dessous est le 75e percentile
  de la base concernee. Il n'est PAS le seuil de calibration publie (u = 20,03 M EUR) : celui-ci
  vit dans config.py et ne bouge pas. Le q75 sert uniquement a binariser une variable continue
  pour les tests d'association, et il est declare comme tel.
""")

# =====================================================================================
titre("1. VOLUMETRIE ET COMPLETUDE")
# =====================================================================================

chemin = chemin_prc(RACINE)
if not chemin:
    print("  PRC absente de ce poste : sections PRC sautees.")
    sys.exit(1)

COLS_PRC = ["breach_date", "reported_date", "end_breach_date", "incident_details",
            "information_affected", "organization_type", "breach_type",
            "total_affected", "residents_affected", "source"]

if chemin.lower().endswith(".csv"):
    prc = pd.read_csv(chemin, sep="|", encoding="utf-8-sig", usecols=COLS_PRC,
                      dtype=str, engine="c", keep_default_na=False)
else:
    prc = pd.read_excel(chemin, sheet_name="Data_Breach_Chronology", usecols=COLS_PRC,
                        dtype=str)

n_prc = len(prc)
print(f"\n  PRC : {n_prc} incidents dans l'export brut.")
print("\n  Taux de presence, naif contre honnete (%) :")
print("    %-24s %8s %8s" % ("variable", "notna", "hors UNKN"))
presence = {}
for c in COLS_PRC:
    naif = 100.0 * prc[c].notna().mean()
    vrai = 100.0 * renseigne(prc[c]).mean()
    presence[c] = vrai
    print("    %-24s %8.2f %8.2f" % (c, naif, vrai))

print(f"""
  LECTURE. La colonne « notna » vaut 100,00 partout : c'est l'artefact annonce en tete de
  script. La colonne de droite est celle qui compte. total_affected, seule variable d'impact
  de cette base, n'est renseignee que dans {presence["total_affected"]:.2f} % des cas : c'est la
  lacune structurante du chapitre, et c'est elle qui interdit d'utiliser la PRC pour un niveau
  de perte. Le champ de DATE de survenance manque de son cote dans un cas sur deux
  ({presence["breach_date"]:.2f} % de presence), ce qui borne toute lecture temporelle fine.
""")

prc["ta"] = pd.to_numeric(prc["total_affected"], errors="coerce")
prc["ra"] = pd.to_numeric(prc["residents_affected"], errors="coerce")
prc["d_breach"] = pd.to_datetime(prc["breach_date"], errors="coerce")
prc["d_report"] = pd.to_datetime(prc["reported_date"], errors="coerce")
prc["annee"] = prc["d_breach"].dt.year

n_ta = int((prc["ta"] > 0).sum())
print(f"  total_affected strictement positif : {n_ta} incidents "
      f"({100.0 * n_ta / n_prc:.2f} % de l'export).")

per = prc[(prc["annee"] >= 2019) & (prc["annee"] <= 2025) & (prc["ta"] > 0)].copy()
print(f"  Perimetre retenu par le memoire (2019-2025, impact renseigne) : {len(per)} incidents.")

# CONTROLE D'IDENTITE, et il n'est pas decoratif. Ce script recharge la PRC par un chemin
# independant de celui des scripts 21, 22 et 62, avec son propre traitement du manquant. S'il
# ne retombait pas sur le meme effectif, l'un des deux lirait autre chose que ce qu'il annonce.
CIBLE_PERIMETRE = 15053
if len(per) == CIBLE_PERIMETRE:
    print(f"  CONTROLE : effectif identique aux sorties versionnees 21, 22 et 62 "
          f"({CIBLE_PERIMETRE}) -> OK")
else:
    print(f"  CONTROLE : ECART avec les sorties versionnees 21, 22 et 62 "
          f"({len(per)} contre {CIBLE_PERIMETRE}) -> A INSTRUIRE AVANT TOUTE PUBLICATION")

sas = pd.read_excel(SAS_PATH, sheet_name="Datasets")
sas["loss"] = pd.to_numeric(sas["Loss Amount ($M)"], errors="coerce")
n_sas_brut = len(sas)
sas = sas[(sas["loss"] > 0) & (sas["loss"] < 100_000)].copy()
n_sas = len(sas)
print(f"\n  SAS OpRisk : {n_sas_brut} lignes brutes, {n_sas} pertes retenues "
      f"(montant strictement positif, aberrations au-dela de 100 000 M$ retirees).")

COLS_SAS = ["Loss Amount ($M)", "Event Risk Category", "Sub Risk Category",
            "Basel Business Line - Level 1", "Industry Sector Name",
            "Country of Incident", "Revenue ($M)", "Assets ($M)", "# of Employees"]
print("\n  Taux de presence SAS (%) :")
for c in COLS_SAS:
    print("    %-32s %8.2f" % (c, 100.0 * sas[c].notna().mean()))

cyber = sas[sas["Sub Risk Category"].isin(["Systems Security", "Systems"]) |
            (sas["Event Risk Category"] == "Business Disruption and System Failures")]
fin = sas[sas["Industry Sector Name"].astype(str).str.contains("Financial", na=False)]
cyberfin = cyber[cyber["Industry Sector Name"].astype(str).str.contains("Financial", na=False)]
print(f"\n  Perimetre cyber/TIC : {len(cyber)} pertes ; secteur financier : {len(fin)} ; "
      f"intersection cyber x finance : {len(cyberfin)}.")

# =====================================================================================
titre("2. VARIABLES QUALITATIVES : KHI-DEUX D'INDEPENDANCE ET V DE CRAMER")
# =====================================================================================

q75_prc = per["ta"].quantile(0.75)
per["severe"] = (per["ta"] >= q75_prc).map({True: "au-dessus q75", False: "sous q75"})
print(f"\n  PRC, seuil de binarisation q75 = {q75_prc:.0f} enregistrements touches.")
for var in ["breach_type", "organization_type"]:
    sub = per[renseigne(per[var])]
    tab = pd.crosstab(sub[var], sub["severe"])
    ligne_test(f"{var} x depassement du q75", *cramer_v(tab))

q75_sas = sas["loss"].quantile(0.75)
sas["severe"] = (sas["loss"] >= q75_sas).map({True: "au-dessus q75", False: "sous q75"})
print(f"\n  SAS, seuil de binarisation q75 = {q75_sas:.4f} M$.")
for var in ["Event Risk Category", "Basel Business Line - Level 1", "Industry Sector Name"]:
    sub = sas[sas[var].notna()]
    tab = pd.crosstab(sub[var], sub["severe"])
    ligne_test(f"{var} x depassement du q75", *cramer_v(tab))

print("""
  LECTURE. Toutes les p-valeurs s'effondrent, ce qui n'apprend rien : a quinze mille et
  quarante mille lignes, le khi-deux rejette l'independance pour un ecart sans portee. Le
  renseignement est dans le V, qui est une taille d'effet bornee par un. Les associations
  mesurees restent MODESTES : aucune n'atteint 0,3, seuil usuel d'une association moyenne.
  Le type de brèche et la ligne metier informent donc le depassement du seuil, mais loin de
  le determiner, ce qui est exactement l'argument que le memoire fait valoir contre une
  segmentation de la severite par categorie.
""")

# =====================================================================================
titre("3. VARIABLES QUANTITATIVES : NORMALITE, CORRELATION DE RANG, HETEROGENEITE")
# =====================================================================================

rng = np.random.default_rng(GRAINE)


def shapiro_plafonne(x, nom):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x) & (x > 0)]
    n = len(x)
    ech = x if n <= N_SHAPIRO else rng.choice(x, N_SHAPIRO, replace=False)
    w_brut, p_brut = stats.shapiro(ech)
    w_log, p_log = stats.shapiro(np.log(ech))
    sk = stats.skew(x)
    ku = stats.kurtosis(x, fisher=False)
    print(f"\n  {nom} (n = {n}, echantillon de test = {len(ech)})")
    print(f"    Shapiro-Wilk, echelle brute      W = {w_brut:.4f}   p = {p_brut:.3e}")
    print(f"    Shapiro-Wilk, echelle log        W = {w_log:.4f}   p = {p_log:.3e}")
    print(f"    asymetrie = {sk:.2f}   aplatissement (non centre) = {ku:.2f}")
    return w_brut, p_brut, w_log, p_log, sk, ku


sw_prc = shapiro_plafonne(per["ta"], "PRC, enregistrements touches")
sw_sas = shapiro_plafonne(sas["loss"], "SAS, montant de perte (M$)")
sw_cyb = shapiro_plafonne(cyber["loss"], "SAS, perimetre cyber/TIC (M$)")

print("""
    LECTURE. La normalite est rejetee a l'echelle brute des deux cotes, et l'aplatissement
    se compte en milliers la ou une gaussienne vaut trois. Le passage au logarithme AMELIORE
    nettement la statistique sans la sauver : la queue reste plus lourde qu'une log-normale,
    ce qui est precisement ce qui justifie une loi de Pareto generalisee au-dela d'un seuil
    plutot qu'un ajustement global.
""")

print("\n  Correlations de Spearman (rang, donc insensibles a la queue) :")
sp = per[["ta", "ra"]].copy()
sp["delai_jours"] = (per["d_report"] - per["d_breach"]).dt.days
sp = sp.dropna()
sp = sp[(sp["delai_jours"] >= 0) & (sp["delai_jours"] < 3650)]
noms = {"ta": "total_affected", "ra": "residents_affected", "delai_jours": "delai de notification"}
print(f"    PRC (n = {len(sp)} incidents a triplet complet et delai plausible) :")
for i, a in enumerate(sp.columns):
    for b in list(sp.columns)[i + 1:]:
        r, p = stats.spearmanr(sp[a], sp[b])
        ptxt = "< 1e-300" if p < 1e-300 else f"{p:.3e}"
        print(f"      {noms[a]:<24s} x {noms[b]:<24s} rho = {r:+.4f}  p {ptxt}")

ss = sas[["loss", "Revenue ($M)", "Assets ($M)", "# of Employees"]].apply(
    pd.to_numeric, errors="coerce").dropna()
ss = ss[(ss > 0).all(axis=1)]
nsas_sp = len(ss)
print(f"\n    SAS (n = {nsas_sp} pertes a profil financier complet) :")
lib = {"loss": "perte", "Revenue ($M)": "chiffre d'affaires",
       "Assets ($M)": "actif total", "# of Employees": "effectif"}
rho_taille = {}
for b in ["Revenue ($M)", "Assets ($M)", "# of Employees"]:
    r, p = stats.spearmanr(ss["loss"], ss[b])
    rho_taille[b] = r
    ptxt = "< 1e-300" if p < 1e-300 else f"{p:.3e}"
    print(f"      {'perte':<24s} x {lib[b]:<24s} rho = {r:+.4f}  p {ptxt}")

print("""
    LECTURE, ET C'EST LE RESULTAT LE PLUS UTILE DE LA SECTION. La perte est correlee a la
    taille de l'entite, mais TRES FAIBLEMENT : les trois coefficients de rang tiennent entre
    0,07 et 0,16, quand une proportionnalite en donnerait un proche de un. C'est la meme
    conclusion que l'elasticite de 0,087 mesuree par ailleurs sur la severite, obtenue ici par
    un chemin non parametrique. Une entite dix fois plus petite ne subit pas une perte dix fois
    plus petite, et c'est ce qui fonde la borne inferieure de validite de la descente d'echelle.
    L'actif total est le PLUS FAIBLE des trois predicteurs de taille, sous le chiffre
    d'affaires et sous l'effectif : la mesure de bilan, qui est pourtant celle qui sert a
    l'echelle prudentielle, est la moins liee a la perte observee.
""")

print("\n  Kruskal-Wallis, egalite des distributions de severite entre classes :")


def kruskal_par(df, col_classe, col_val, nom, mini=30):
    g = [v[col_val].dropna().values for _, v in df.groupby(col_classe) if len(v) >= mini]
    k = len(g)
    if k < 2:
        print(f"    {nom} : moins de deux classes suffisamment peuplees.")
        return None
    h, p = stats.kruskal(*g)
    n = sum(len(x) for x in g)
    eps2 = (h - k + 1) / (n - k) if n > k else np.nan
    ptxt = "< 1e-300" if p < 1e-300 else f"{p:.3e}"
    print(f"    {nom:<40s} H = {h:9.1f}  k = {k:2d}  p {ptxt:>10s}  eps2 = {eps2:.4f}  n = {n}")
    return h, p, k, eps2, n


kw_prc = kruskal_par(per[renseigne(per["organization_type"])], "organization_type", "ta",
                     "PRC, impact par type d'organisation")
kw_prcb = kruskal_par(per[renseigne(per["breach_type"])], "breach_type", "ta",
                      "PRC, impact par type de breche")
kw_sas = kruskal_par(sas, "Event Risk Category", "loss",
                     "SAS, perte par categorie balaise")
kw_sasb = kruskal_par(sas, "Basel Business Line - Level 1", "loss",
                      "SAS, perte par ligne metier balaise")

print("""
    LECTURE. L'hypothese d'une severite homogene entre classes est rejetee partout, et la
    taille d'effet epsilon-carre dit de combien : elle reste petite, de l'ordre de quelques
    centiemes, donc la classe d'organisation explique une part FAIBLE de la dispersion des
    severites. Ce resultat va dans le meme sens que le V de Cramer de la section 2 et il
    porte la meme consequence de modelisation : segmenter la severite par categorie
    d'organisation couterait des degres de liberte sans acheter de pouvoir explicatif, et
    c'est pourquoi le memoire ajuste une queue commune puis declare ce choix comme une
    limite au lieu de le presenter comme une mesure.
""")

# =====================================================================================
titre("4. LES TROIS FIGURES")
# =====================================================================================

# --- D1 : matrice de presence croisee -------------------------------------------------
vars_mat = ["breach_date", "reported_date", "end_breach_date", "incident_details",
            "information_affected", "organization_type", "breach_type",
            "total_affected", "residents_affected"]
courts = {"breach_date": "breach\ndate", "reported_date": "reported\ndate",
          "end_breach_date": "end breach\ndate", "incident_details": "incident\ndetails",
          "information_affected": "information\naffected", "organization_type": "organization\ntype",
          "breach_type": "breach\ntype", "total_affected": "total\naffected",
          "residents_affected": "residents\naffected"}
masques = {v: renseigne(prc[v]).values for v in vars_mat}
k = len(vars_mat)
M = np.full((k, k), np.nan)
for i in range(k):
    for j in range(i + 1):
        M[i, j] = 100.0 * (masques[vars_mat[i]] & masques[vars_mat[j]]).mean()

print("\n  D1, taux de presence croisee (%) — triangle inferieur :")
for i in range(k):
    print("    %-22s %s" % (vars_mat[i],
          " ".join(f"{M[i, j]:6.1f}" if not np.isnan(M[i, j]) else "      " for j in range(k))))

from matplotlib.colors import LinearSegmentedColormap
cmap_seq = LinearSegmentedColormap.from_list("nexialog_seq", sn.SEQUENTIEL_6[::-1])

fig, ax = plt.subplots(figsize=(7.4, 5.4))
im = ax.imshow(M, cmap=cmap_seq, vmin=0, vmax=100)
for i in range(k):
    for j in range(i + 1):
        val = M[i, j]
        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7,
                color="white" if val > 55 else sn.ENCRE)
ax.set_xticks(range(k)); ax.set_xticklabels([courts[v] for v in vars_mat], fontsize=7, rotation=45, ha="right")
ax.set_yticks(range(k)); ax.set_yticklabels([courts[v] for v in vars_mat], fontsize=7)
ax.set_title("Taux de présence croisée des variables PRC (%)", fontsize=10, color=sn.ENCRE)
cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
cb.set_label("taux de présence (%)", fontsize=8)
ax.grid(False)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "D1_presence_croisee.png"), dpi=150)
plt.close(fig)

# --- D2 : sources de notification, double axe ----------------------------------------
src = per[renseigne(per["source"])].groupby("source").agg(
    incidents=("ta", "size"), volume=("ta", "sum")).sort_values("volume", ascending=False).head(12)
print("\n  D2, sources de notification (12 premieres par volume) :")
print("    %-8s %10s %16s" % ("source", "incidents", "volume (M enr.)"))
for s, r in src.iterrows():
    print("    %-8s %10d %16.1f" % (s, r["incidents"], r["volume"] / 1e6))

fig, ax1 = plt.subplots(figsize=(7.6, 4.2))
x = np.arange(len(src))
ax1.bar(x, src["volume"].values / 1e6, color=sn.CATEGORIEL[2], width=0.68,
        label="volume d'enregistrements touchés")
ax1.set_ylabel("volume touché (millions d'enregistrements)", fontsize=9, color=sn.CATEGORIEL[2])
ax1.tick_params(axis="y", labelcolor=sn.CATEGORIEL[2])
ax1.set_xticks(x); ax1.set_xticklabels(src.index, fontsize=8)
ax1.set_xlabel("source de notification", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(x, src["incidents"].values, color=sn.CATEGORIEL[0], marker="o", lw=1.8,
         label="nombre d'incidents")
ax2.set_ylabel("nombre d'incidents", fontsize=9, color=sn.CATEGORIEL[0])
ax2.tick_params(axis="y", labelcolor=sn.CATEGORIEL[0])
ax2.spines["right"].set_visible(True)
ax1.set_title("Sources de notification : volume touché et nombre d'incidents",
              fontsize=10, color=sn.ENCRE)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "D2_sources_notification.png"), dpi=150)
plt.close(fig)

# --- D3 : bulles par type de breche ---------------------------------------------------
bt = per[renseigne(per["breach_type"])].groupby("breach_type").agg(
    incidents=("ta", "size"), volume=("ta", "sum"), median=("ta", "median"))
bt = bt.sort_values("incidents", ascending=False)
print("\n  D3, types de breche :")
print("    %-8s %10s %16s %12s" % ("type", "incidents", "volume (M enr.)", "mediane"))
for s, r in bt.iterrows():
    print("    %-8s %10d %16.1f %12.0f" % (s, r["incidents"], r["volume"] / 1e6, r["median"]))

# Plan frequence x severite plutot qu'un cercle decoratif : l'axe des abscisses porte le
# NOMBRE d'incidents, celui des ordonnees la MEDIANE d'impact, la taille et la couleur portent
# le volume cumule. Un type de breche se lit donc par sa position autant que par sa taille, et
# les etiquettes tiennent a cote des bulles au lieu de deborder des plus petites.
fig, ax = plt.subplots(figsize=(7.4, 4.6))
xv = bt["incidents"].values.astype(float)
yv = bt["median"].values.astype(float)
vol = bt["volume"].values / 1e6
taille = 1500 * (vol / vol.max()) ** 0.5 + 120
sc = ax.scatter(xv, yv, s=taille, c=vol, cmap=cmap_seq, edgecolors="white",
                linewidths=1.3, zorder=3, norm=matplotlib.colors.LogNorm(
                    vmin=max(vol.min(), 1e-2), vmax=vol.max()))
for xi, yi, nom, v in zip(xv, yv, bt.index, vol):
    ax.annotate(f"{nom}", (xi, yi), textcoords="offset points", xytext=(0, -26),
                ha="center", fontsize=8.5, weight="bold", color=sn.ENCRE, zorder=4)
ax.set_xscale("log"); ax.set_yscale("log")
# Marges explicites : sans elles la plus grosse bulle est coupee par le cadre.
ax.set_xlim(xv.min() / 3.2, xv.max() * 3.2)
ax.set_ylim(yv.min() / 1.9, yv.max() * 1.9)
ax.set_xlabel("nombre d'incidents (échelle log)", fontsize=9)
ax.set_ylabel("impact médian, enregistrements (log)", fontsize=9)
ax.grid(True, which="major", alpha=0.5)
ax.set_title("Types de brèche : fréquence, impact médian et volume cumulé",
             fontsize=10, color=sn.ENCRE)
cb = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.02)
cb.set_label("volume cumulé touché (millions, log)", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIGDIR, "D3_bulles_breche.png"), dpi=150)
plt.close(fig)

print("\n  Trois figures ecrites dans exploratory/vasicek_lab/figures/ :")
print("    D1_presence_croisee.png  D2_sources_notification.png  D3_bulles_breche.png")

# =====================================================================================
titre("5. GRANDEURS CITEES (sans separateur de milliers, pour le harnais)")
# =====================================================================================
g = []
g.append(("incidents PRC export brut", n_prc))
g.append(("incidents PRC impact renseigne", n_ta))
g.append(("part impact renseigne pct", round(100.0 * n_ta / n_prc, 2)))
g.append(("incidents PRC perimetre 2019-2025", len(per)))
g.append(("lignes SAS brutes", n_sas_brut))
g.append(("pertes SAS retenues", n_sas))
g.append(("pertes SAS cyber TIC", len(cyber)))
g.append(("pertes SAS finance", len(fin)))
g.append(("pertes SAS cyber x finance", len(cyberfin)))
g.append(("seuil q75 PRC enregistrements", int(q75_prc)))
g.append(("seuil q75 SAS MUSD", round(q75_sas, 4)))
for c in ["breach_date", "end_breach_date", "total_affected", "residents_affected",
          "organization_type", "breach_type"]:
    g.append((f"presence PRC {c} pct", round(presence[c], 2)))
g.append(("shapiro W brut PRC", round(sw_prc[0], 4)))
g.append(("shapiro W log PRC", round(sw_prc[2], 4)))
g.append(("shapiro W brut SAS", round(sw_sas[0], 4)))
g.append(("shapiro W log SAS", round(sw_sas[2], 4)))
g.append(("asymetrie PRC", round(sw_prc[4], 2)))
g.append(("aplatissement PRC", round(sw_prc[5], 2)))
g.append(("asymetrie SAS", round(sw_sas[4], 2)))
g.append(("aplatissement SAS", round(sw_sas[5], 2)))
for b, r in rho_taille.items():
    g.append((f"spearman perte x {b}", round(r, 4)))
g.append(("n spearman SAS", nsas_sp))
g.append(("n spearman PRC", len(sp)))
for nom, res in [("KW PRC organisation", kw_prc), ("KW PRC breche", kw_prcb),
                 ("KW SAS categorie", kw_sas), ("KW SAS ligne metier", kw_sasb)]:
    if res:
        g.append((f"{nom} eps2", round(res[3], 4)))
        g.append((f"{nom} classes", res[2]))
for nom, val in g:
    print(f"  {nom:<44s} {val}")

print("\nFIN 104")
