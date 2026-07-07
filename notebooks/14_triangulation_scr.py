"""
14_triangulation_scr.py
------------------------
TRIANGULATION MÉTHODOLOGIQUE DU SCR_DORA (Axe 2 du mémoire).

Le SCR reporté dans le mémoire est un quantile Monte Carlo. Un quantile MC à
99,5 % est entaché d'une erreur de simulation (cf. notebook 10). On confronte
donc l'estimation MC à trois méthodes INDÉPENDANTES sur la brique dominante
(remédiation, ~86 % du risque), isolée de la surcharge systémique multiplicative
afin que toutes les méthodes portent sur le MÊME objet : le compound

        S = sum_{i=1}^{M} X_i ,   X_i = u + GPD(xi, sigma),

où M est le nombre annuel de pertes non nulles (fréquence NegBin amincie par p_u).

Méthodes comparées :
  A. Monte Carlo direct (référence stochastique).
  B. Single Loss Approximation (Böcker & Klüppelberg 2005) — analytique,
     1er ordre puis correction de moyenne (Böcker & Sprittulla 2006).
  C. Inversion par FFT de la fonction génératrice composée (agrégation exacte ;
     réalisation numériquement stable de la récursion de Panjer, inadaptée aux
     queues très lourdes).
  D. Estimation bayésienne de la GPD (Metropolis) — VaR mono-perte prédictive
     a posteriori intégrant nativement l'incertitude de paramètre (à opposer au
     bootstrap fréquentiste du mémoire).

Sorties :
  outputs/tables/results_triangulation_scr.csv
  outputs/figures/triangulation_scr.png

Nécessite data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx pour le bloc D.
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import genpareto

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config import OPRISK, FREQUENCY
from src.frequency.negbin import compute_lambda_scenario

BRAND_BLUE = "#2563eb"
BRAND_ORANGE = "#f59e0b"
BRAND_GREEN = "#059669"
BRAND_DARK = "#111317"
BRAND_LIGHT = "#f6f7f9"
plt.rcParams["axes.facecolor"] = BRAND_LIGHT
plt.rcParams["figure.facecolor"] = BRAND_LIGHT

ALPHA = 0.995
OPRISK_PATH = "data/raw/SAS_OpRisk_Global_Data_June_2026.xlsx"
USD_EUR = 0.92


# ---------------------------------------------------------------------------
# Paramètres du compound (OpRisk, profil médian non-conforme)
# ---------------------------------------------------------------------------
def compound_params():
    xi, sigma, u, p_u = (OPRISK["xi"], OPRISK["sigma_eur"],
                         OPRISK["seuil_u_eur"], OPRISK["p_u"])
    disp = FREQUENCY["dispersion_factor"]
    lambda_ref = OPRISK["n_incidents"] / OPRISK["n_years"]
    lam = compute_lambda_scenario(lambda_ref, "S2_non_conforme",
                                  mode="center")["lambda_global"]
    r = lam / (disp - 1)
    p = r / (r + lam)
    # Amincissement Bernoulli(p_u) d'une NegBin(r, p) -> NegBin(r, p2)
    A = 1.0 - (1.0 - p) * (1.0 - p_u)
    p2 = p / A
    lam_eff = lam * p_u
    return dict(xi=xi, sigma=sigma, u=u, p_u=p_u, disp=disp, lam=lam,
                r=r, p=p, p2=p2, lam_eff=lam_eff)


# ---------------------------------------------------------------------------
# A. Monte Carlo direct
# ---------------------------------------------------------------------------
def var_monte_carlo(par, n_sim=2_000_000, seed=1):
    rng = np.random.default_rng(seed)
    N = rng.negative_binomial(par["r"], par["p"], size=n_sim)
    tot = int(N.sum())
    nz = rng.random(tot) < par["p_u"]
    sev = np.zeros(tot)
    k = int(nz.sum())
    sev[nz] = par["u"] + genpareto.ppf(rng.random(k), c=par["xi"], scale=par["sigma"])
    splits = np.cumsum(N)[:-1]
    S = np.array([s.sum() for s in np.split(sev, splits)])
    return float(np.quantile(S, ALPHA)), float(S.mean())


# ---------------------------------------------------------------------------
# B. Single Loss Approximation
# ---------------------------------------------------------------------------
def var_sla(par, alpha=ALPHA):
    xi, sigma, u, lam_eff = par["xi"], par["sigma"], par["u"], par["lam_eff"]
    tail = (1.0 - alpha) / lam_eff              # 1 - F_X(VaR)
    var1 = u + (sigma / xi) * (tail ** (-xi) - 1.0)   # 1er ordre
    EX = u + sigma / (1.0 - xi)                 # E[X] (xi < 1)
    var2 = var1 + (lam_eff - 1.0) * EX          # correction de moyenne (BS 2006)
    return float(var1), float(var2), float(EX)


# ---------------------------------------------------------------------------
# C. Inversion FFT de la fonction génératrice composée
# ---------------------------------------------------------------------------
def var_fft(par, h=1.0, M=1 << 22, alpha=ALPHA):
    xi, sigma, u, p2, r = par["xi"], par["sigma"], par["u"], par["p2"], par["r"]
    edges = (np.arange(M + 1) - 0.5) * h
    cdfX = np.where(edges <= u, 0.0,
                    genpareto.cdf(np.maximum(edges - u, 0.0), c=xi, scale=sigma))
    fX = np.diff(cdfX)
    fX = fX / fX.sum()
    phi = np.fft.rfft(fX)
    G = (p2 / (1.0 - (1.0 - p2) * phi)) ** r     # PGF NegBin(r, p2) o phi_X
    g = np.fft.irfft(G, n=M)
    g = np.maximum(g, 0.0)
    cdf = np.cumsum(g)
    x = np.arange(M) * h
    var = float(x[np.searchsorted(cdf, alpha)])
    return var, float(g.sum()), float((g * x).sum())


# ---------------------------------------------------------------------------
# D. GPD bayésienne (Metropolis) sur les excès OpRisk
# ---------------------------------------------------------------------------
def load_oprisk_excesses(path):
    df = pd.read_excel(path, sheet_name="Datasets")
    cyber = ["Systems Security", "Systems"]
    biz = ["Business Disruption and System Failures"]
    d = df[(df["Sub Risk Category"].isin(cyber) | df["Event Risk Category"].isin(biz)) &
           (df["Industry Sector Name"].apply(lambda v: "Financial" in str(v) if pd.notna(v) else False))].copy()
    d["loss_eur_M"] = pd.to_numeric(d["Loss Amount ($M)"], errors="coerce") * USD_EUR
    losses = d["loss_eur_M"].dropna()
    losses = losses[losses > 0].values
    u = OPRISK["seuil_u_eur"]
    return losses[losses > u] - u, u


def gpd_loglik(exc, xi, sigma):
    if sigma <= 0:
        return -np.inf
    z = 1.0 + xi * exc / sigma
    if np.any(z <= 0):
        return -np.inf
    if abs(xi) < 1e-8:
        return -len(exc) * np.log(sigma) - exc.sum() / sigma
    return -len(exc) * np.log(sigma) - (1.0 + 1.0 / xi) * np.log(z).sum()


def bayesian_gpd(exc, n_iter=60000, burn=15000, seed=7):
    rng = np.random.default_rng(seed)
    # priors faiblement informatifs : xi ~ U(-0.5, 2), sigma ~ log-uniforme
    xi, log_sig = 0.6, np.log(50.0)
    lp = gpd_loglik(exc, xi, np.exp(log_sig))
    chain = np.empty((n_iter, 2))
    step = np.array([0.13, 0.14])   # pas relevé -> meilleur mélange (acc ~ 0.3-0.4)
    acc = 0
    for t in range(n_iter):
        xi_p = xi + step[0] * rng.standard_normal()
        log_sig_p = log_sig + step[1] * rng.standard_normal()
        if -0.5 < xi_p < 2.0:
            lp_p = gpd_loglik(exc, xi_p, np.exp(log_sig_p)) + log_sig_p  # jacobien log-uniforme
            if np.log(rng.random()) < (lp_p - (lp + log_sig)):
                xi, log_sig, lp = xi_p, log_sig_p, gpd_loglik(exc, xi_p, np.exp(log_sig_p))
                acc += 1
        chain[t] = (xi, np.exp(log_sig))
    return chain, burn, acc / n_iter


def autocorr(x, nlags=60):
    x = x - x.mean()
    ac = np.correlate(x, x, mode="full")[len(x) - 1:]
    ac = ac / ac[0]
    return ac[:nlags]


def plot_mcmc_diagnostics(chain, burn, fig_path):
    post = chain[burn:]
    fig, ax = plt.subplots(2, 2, figsize=(13, 8))
    # trace xi
    ax[0, 0].plot(chain[:, 0], color=BRAND_BLUE, lw=0.4)
    ax[0, 0].axvline(burn, color=BRAND_ORANGE, ls="--", lw=1.2, label="fin du rodage")
    ax[0, 0].set_title(r"Trace de $\xi$ (chaîne de Metropolis)", fontweight="bold")
    ax[0, 0].set_xlabel("itération"); ax[0, 0].set_ylabel(r"$\xi$")
    ax[0, 0].legend(fontsize=9); ax[0, 0].grid(alpha=0.3)
    # trace sigma
    ax[0, 1].plot(chain[:, 1], color=BRAND_GREEN, lw=0.4)
    ax[0, 1].axvline(burn, color=BRAND_ORANGE, ls="--", lw=1.2)
    ax[0, 1].set_title(r"Trace de $\sigma$ (M\euro)".replace("\\euro", "€"), fontweight="bold")
    ax[0, 1].set_xlabel("itération"); ax[0, 1].set_ylabel(r"$\sigma$"); ax[0, 1].grid(alpha=0.3)
    # ACF xi
    ac = autocorr(post[:, 0])
    ax[1, 0].bar(range(len(ac)), ac, color=BRAND_BLUE, width=0.8)
    ax[1, 0].set_title(r"Autocorrélation de $\xi$ (post-rodage)", fontweight="bold")
    ax[1, 0].set_xlabel("décalage"); ax[1, 0].set_ylabel("ACF"); ax[1, 0].grid(alpha=0.3)
    # posterior joint
    ax[1, 1].scatter(post[::10, 0], post[::10, 1], s=3, alpha=0.25, color=BRAND_DARK)
    ax[1, 1].set_title(r"Loi jointe a posteriori $(\xi,\sigma)$", fontweight="bold")
    ax[1, 1].set_xlabel(r"$\xi$"); ax[1, 1].set_ylabel(r"$\sigma$ (M€)"); ax[1, 1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()


def var_single_loss(xi, sigma, u, p_u, alpha=ALPHA):
    # VaR mono-perte : quantile de X sachant qu'une perte survient (dépassement),
    # au niveau alpha rapporté à la probabilité de queue p_u.
    q = 1.0 - (1.0 - alpha) / p_u
    return u + (sigma / xi) * ((1.0 - q) ** (-xi) - 1.0)


# ---------------------------------------------------------------------------
def main():
    par = compound_params()
    print("=" * 74)
    print("  TRIANGULATION DU SCR_DORA — brique remédiation (OpRisk, médian S2)")
    print("=" * 74)
    print(f"  xi={par['xi']:.4f}  sigma={par['sigma']:.3f}  u={par['u']:.3f}")
    print(f"  lambda_nc={par['lam']:.2f}  p_u={par['p_u']:.4f}  "
          f"=> lambda_eff (pertes/an)={par['lam_eff']:.3f}")

    var_mc, mean_mc = var_monte_carlo(par)
    var1, var2, EX = var_sla(par)
    var_f, mass, mean_f = var_fft(par)

    print("\n  --- VaR 99,5 % du compound agrégé (M€) ---")
    print(f"  A. Monte Carlo (2e6)        : {var_mc:9.1f}   (E[S]={mean_mc:.1f})")
    print(f"  B. SLA 1er ordre            : {var1:9.1f}")
    print(f"     SLA 2e ordre (BS 2006)   : {var2:9.1f}   (E[X]={EX:.2f})")
    print(f"  C. FFT (inversion exacte)   : {var_f:9.1f}   (masse={mass:.4f}, E[S]={mean_f:.1f})")
    print(f"     écart FFT vs MC          : {100*(var_f-var_mc)/var_mc:+.2f} %")
    print(f"     écart SLA-2 vs MC        : {100*(var2-var_mc)/var_mc:+.2f} %")

    rows = [
        ("Monte Carlo (2e6 tirages)", "stochastique", var_mc),
        ("SLA 1er ordre (Böcker-Klüppelberg)", "analytique", var1),
        ("SLA 2e ordre (Böcker-Sprittulla)", "analytique", var2),
        ("FFT (inversion de la FGP composée)", "numérique exact", var_f),
    ]

    # --- D. Bayésien ---
    post = None
    chain = None
    if os.path.exists(OPRISK_PATH):
        exc, u = load_oprisk_excesses(OPRISK_PATH)
        chain, burn, acc = bayesian_gpd(exc)
        post = chain[burn:]
        xi_hat, sig_hat = post.mean(0)
        xi_lo, xi_hi = np.percentile(post[:, 0], [5, 95])
        var_bayes = np.array([var_single_loss(xi, sg, u, par["p_u"])
                              for xi, sg in post])
        vb_med = np.median(var_bayes)
        vb_lo, vb_hi = np.percentile(var_bayes, [5, 95])
        print(f"\n  D. GPD bayésienne (Metropolis, n_exc={len(exc)}, taux acc={acc:.2f})")
        print(f"     posterior xi  = {xi_hat:.3f}  IC90%=[{xi_lo:.3f}, {xi_hi:.3f}]")
        print(f"     bootstrap  xi = {OPRISK['xi']:.3f}  IC90%={OPRISK['xi_ic90']}")
        print(f"     VaR 99,5 % mono-perte prédictive = {vb_med:.1f} M€  "
              f"IC90%=[{vb_lo:.1f}, {vb_hi:.1f}]")
    else:
        print(f"\n  D. sauté (fichier absent : {OPRISK_PATH})")

    # --- CSV ---
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "tables")
    os.makedirs(out_dir, exist_ok=True)
    df = pd.DataFrame(rows, columns=["methode", "nature", "var_995_MEUR"])
    df.to_csv(os.path.join(out_dir, "results_triangulation_scr.csv"), index=False)
    print(f"\nCSV : {os.path.join(out_dir, 'results_triangulation_scr.csv')}")

    # --- Figure ---
    fig_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    if post is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(7, 5))

    labels = ["Monte\nCarlo", "SLA\n1er ordre", "SLA\n2e ordre", "FFT\nexact"]
    vals = [var_mc, var1, var2, var_f]
    colors = [BRAND_BLUE, "#9ca3af", BRAND_ORANGE, BRAND_GREEN]
    bars = ax1.bar(labels, vals, color=colors, edgecolor=BRAND_DARK, linewidth=0.6)
    ax1.axhline(var_mc, color=BRAND_BLUE, ls="--", lw=1, alpha=0.6)
    for b, v in zip(bars, vals):
        ax1.text(b.get_x() + b.get_width() / 2, v, f"{v:,.0f}",
                 ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax1.set_ylabel("VaR 99,5 % du compound (M€)", fontsize=11)
    ax1.set_title("Triangulation : quatre méthodes indépendantes\n"
                  "sur la brique remédiation (OpRisk, médian $S_2$)",
                  fontsize=12, fontweight="bold")
    ax1.grid(True, axis="y", alpha=0.3)

    if post is not None:
        ax2.hist(post[:, 0], bins=60, color=BRAND_BLUE, alpha=0.75,
                 density=True, edgecolor="white", linewidth=0.3)
        ax2.axvline(OPRISK["xi"], color=BRAND_ORANGE, lw=2,
                    label=f"EMV (mémoire) = {OPRISK['xi']:.3f}")
        ax2.axvline(post[:, 0].mean(), color=BRAND_GREEN, lw=2, ls="--",
                    label=f"Moyenne a posteriori = {post[:,0].mean():.3f}")
        ax2.axvspan(*OPRISK["xi_ic90"], color=BRAND_ORANGE, alpha=0.12,
                    label="IC90 % bootstrap")
        ax2.set_xlabel(r"Paramètre de queue $\xi$", fontsize=11)
        ax2.set_ylabel("Densité a posteriori", fontsize=11)
        ax2.set_title("Incertitude de paramètre : posterior bayésien\n"
                      r"vs point EMV et IC bootstrap ($\xi$ GPD OpRisk)",
                      fontsize=12, fontweight="bold")
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fig_path = os.path.join(fig_dir, "triangulation_scr.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Figure : {fig_path}")

    if chain is not None:
        diag_path = os.path.join(fig_dir, "mcmc_diagnostics.png")
        plot_mcmc_diagnostics(chain, burn, diag_path)
        print(f"Figure : {diag_path}")


if __name__ == "__main__":
    main()
