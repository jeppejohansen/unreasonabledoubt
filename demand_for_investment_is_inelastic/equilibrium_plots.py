"""
Equilibrium figures from the lifecycle model with S = I.

All data comes from:
  - ge_results.json: the converged general equilibrium
  - ge_sweep_results.json: model solved at various R_s with R_f endogenous
  - sweep_results.json: partial equilibrium sweep (R_f fixed)

Key insight: the simple supply curve R_s = 1 + E/(α·S) doesn't work because
α and savings are correlated across the lifecycle (E[α·s] ≠ E[α]·E[s]).
So we plot the actual model output directly.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (8, 5.5),
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
})


def load_ge():
    with open(Path(__file__).parent / "ge_results.json") as f:
        return json.load(f)


def load_ge_sweep():
    with open(Path(__file__).parent / "ge_sweep_results.json") as f:
        return json.load(f)


def load_pe_sweep():
    with open(Path(__file__).parent / "sweep_results.json") as f:
        return json.load(f)


def plot_savings_supply():
    """
    The core result: savings is nearly inelastic.

    Left: savings rate vs stock return — near-vertical.
    Right: portfolio share vs stock return — elastic.

    Data from the GE sweep where R_f is endogenous at each point.
    """
    sweep = load_ge_sweep()
    ge = load_ge()

    stock_returns = [(r["r_s_input"] - 1) * 100 for r in sweep]
    savings_rates = [r["avg_savings_rate"] * 100 for r in sweep]
    alpha_pct = [r["avg_portfolio_share"] * 100 for r in sweep]

    eq_rs = (ge["r_s"] - 1) * 100
    eq_savings = ge["avg_savings_rate"] * 100
    eq_alpha = ge["avg_portfolio_share"] * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)

    # ── Left: savings rate vs return ──
    ax1.plot(savings_rates, stock_returns, "o-", color="#2c7fb8",
             linewidth=2.5, markersize=9, zorder=3)
    ax1.plot(eq_savings, eq_rs, "s", color="#2ca02c", markersize=12, zorder=5)
    ax1.annotate(f"Equilibrium\nR_s = {eq_rs:.1f}%",
                 xy=(eq_savings, eq_rs),
                 xytext=(eq_savings + 0.3, eq_rs + 2.5),
                 fontsize=10, color="#2ca02c", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    sr_range = max(savings_rates) - min(savings_rates)
    rs_range = max(stock_returns) - min(stock_returns)
    ax1.text(np.mean(savings_rates), min(stock_returns) + 1,
             f"Savings varies {sr_range:.1f}pp\nwhile R_s varies {rs_range:.0f}pp",
             fontsize=10, color="gray", style="italic", ha="center")

    ax1.set_xlabel("Average savings rate (%)")
    ax1.set_ylabel("Expected stock return (%)")
    ax1.set_title("Savings supply (nearly inelastic)")
    ax1.grid(True, alpha=0.15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ── Right: portfolio share vs return ──
    ax2.plot(alpha_pct, stock_returns, "o-", color="#d95f02",
             linewidth=2.5, markersize=9, zorder=3)
    ax2.plot(eq_alpha, eq_rs, "s", color="#2ca02c", markersize=12, zorder=5)
    ax2.annotate(f"Equilibrium\nα = {eq_alpha:.0f}%",
                 xy=(eq_alpha, eq_rs),
                 xytext=(eq_alpha - 18, eq_rs + 2.5),
                 fontsize=10, color="#2ca02c", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax2.set_xlabel("Portfolio share in stocks (%)")
    ax2.set_title("Portfolio allocation (highly elastic)")
    ax2.grid(True, alpha=0.15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Two margins of adjustment — only one moves",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "savings_supply.png", dpi=200)
    plt.close(fig)
    print("Saved savings_supply.png")


def plot_equilibrium():
    """
    General equilibrium: R_s_input vs R_s_implied.

    For each candidate R_s, we solve the model (with R_f endogenous to clear
    the bond market), compute actual stock holdings, and check what R_s would
    clear the stock market given those holdings.

    Equilibrium: where R_s_input = R_s_implied (45-degree line).
    """
    sweep = load_ge_sweep()
    ge = load_ge()

    r_s_input = [(r["r_s_input"] - 1) * 100 for r in sweep]
    r_s_implied = [(r["r_s_implied"] - 1) * 100 for r in sweep]

    fig, ax = plt.subplots()

    # 45-degree line
    ax.plot([0, 20], [0, 20], "--", color="gray", linewidth=1, alpha=0.5,
            label="R_s input = R_s implied")

    # Model curve
    ax.plot(r_s_input, r_s_implied, "o-", color="#d95f02", linewidth=2.5,
            markersize=9, zorder=3)

    # Equilibrium
    eq_rs = (ge["r_s"] - 1) * 100
    ax.plot(eq_rs, eq_rs, "s", color="#2ca02c", markersize=14, zorder=5)
    ax.annotate(f"Equilibrium\nR_s = {eq_rs:.1f}%",
                xy=(eq_rs, eq_rs),
                xytext=(eq_rs + 2, eq_rs + 3),
                fontsize=11, color="#2ca02c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    # Explain the regions
    ax.text(4, 14, "Stock market\nunderpriced\n(excess demand)",
            fontsize=10, color="gray", style="italic", ha="center")
    ax.text(12, 4, "Stock market\noverpriced\n(excess supply)",
            fontsize=10, color="gray", style="italic", ha="center")

    ax.set_xlabel("R_s input to model (%)")
    ax.set_ylabel("R_s implied by stock market clearing (%)")
    ax.set_title("General equilibrium: S = I")
    ax.set_xlim(1, 17)
    ax.set_ylim(1, 30)
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ge_equilibrium.png", dpi=200)
    plt.close(fig)
    print("Saved ge_equilibrium.png")


def plot_returns_and_premium():
    """
    Both returns and the equity premium from the GE sweep.

    Shows how R_s, R_f, and the premium vary with portfolio share α.
    Uses actual model output (not analytical approximation).
    """
    sweep = load_ge_sweep()
    ge = load_ge()

    alpha_pct = [r["avg_portfolio_share"] * 100 for r in sweep]
    r_s_pct = [(r["r_s_input"] - 1) * 100 for r in sweep]
    r_f_pct = [(r["r_f"] - 1) * 100 for r in sweep]
    premium = [(r["r_s_input"] - r["r_f"]) * 100 for r in sweep]

    eq_alpha = ge["avg_portfolio_share"] * 100
    eq_rs = (ge["r_s"] - 1) * 100
    eq_rf = (ge["r_f"] - 1) * 100

    fig, ax = plt.subplots()

    ax.plot(alpha_pct, r_s_pct, "o-", color="#d95f02", linewidth=2.5,
            markersize=8, zorder=3, label="Stock return (R_s)")
    ax.plot(alpha_pct, r_f_pct, "o-", color="#2c7fb8", linewidth=2.5,
            markersize=8, zorder=3, label="Bond yield (R_f)")

    # Equilibrium points
    ax.plot(eq_alpha, eq_rs, "s", color="#2ca02c", markersize=12, zorder=5)
    ax.plot(eq_alpha, eq_rf, "s", color="#2ca02c", markersize=12, zorder=5)

    # Premium bracket
    ax.annotate("", xy=(eq_alpha + 3, eq_rs),
                xytext=(eq_alpha + 3, eq_rf),
                arrowprops=dict(arrowstyle="<->", color="#2ca02c", lw=2))
    ax.text(eq_alpha + 5, (eq_rs + eq_rf) / 2,
            f"Premium\n{eq_rs - eq_rf:.1f}pp",
            fontsize=11, color="#2ca02c", fontweight="bold", va="center")

    # Vertical line at equilibrium
    ax.axvline(eq_alpha, color="gray", linewidth=1, linestyle="--", alpha=0.4)
    ax.text(eq_alpha + 1, 0.5, f"α = {eq_alpha:.0f}%", fontsize=10, color="gray")

    ax.set_xlabel("Portfolio share in stocks (%)")
    ax.set_ylabel("Expected return (%)")
    ax.set_title("Returns from general equilibrium")
    ax.set_xlim(0, 65)
    ax.set_ylim(0, 17)
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "ge_returns.png", dpi=200)
    plt.close(fig)
    print("Saved ge_returns.png")


def load_savings_sweep():
    with open(Path(__file__).parent / "savings_sweep_results.json") as f:
        return json.load(f)


def plot_savings_comparative_statics():
    """
    The supply-side story: what happens when total savings S changes,
    holding asset supply (E, B) fixed?

    More savings → higher P/E, lower safe rate.
    Shows that savings determines prices, not the other way around.
    """
    sweep = load_savings_sweep()
    ge = load_ge()

    s_mult = [r["s_multiplier"] for r in sweep]
    pe = [r["pe_ratio"] for r in sweep]
    r_f_pct = [(r["r_f"] - 1) * 100 for r in sweep]
    r_s_pct = [(r["r_s"] - 1) * 100 for r in sweep]

    eq_idx = next(i for i, r in enumerate(sweep) if r["s_multiplier"] == 1.0)
    eq_pe = pe[eq_idx]
    eq_rf = r_f_pct[eq_idx]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), sharex=True)

    # ── Left: P/E vs savings ──
    ax1.plot(s_mult, pe, "o-", color="#d95f02", linewidth=2.5, markersize=9, zorder=3)
    ax1.plot(1.0, eq_pe, "s", color="#2ca02c", markersize=12, zorder=5)
    ax1.annotate(f"Baseline\nP/E = {eq_pe:.1f}",
                 xy=(1.0, eq_pe),
                 xytext=(1.12, eq_pe + 2),
                 fontsize=10, color="#2ca02c", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax1.set_xlabel("Total savings (× baseline)")
    ax1.set_ylabel("P/E ratio")
    ax1.set_title("More savings → higher P/E")
    ax1.grid(True, alpha=0.15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ── Right: R_f vs savings ──
    ax2.plot(s_mult, r_f_pct, "o-", color="#2c7fb8", linewidth=2.5, markersize=9, zorder=3)
    ax2.plot(1.0, eq_rf, "s", color="#2ca02c", markersize=12, zorder=5)
    ax2.annotate(f"Baseline\nR_f = {eq_rf:.1f}%",
                 xy=(1.0, eq_rf),
                 xytext=(1.12, eq_rf + 0.3),
                 fontsize=10, color="#2ca02c", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax2.set_xlabel("Total savings (× baseline)")
    ax2.set_ylabel("Safe interest rate (%)")
    ax2.set_title("More savings → lower safe rate")
    ax2.grid(True, alpha=0.15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Equilibrium prices when savings changes (asset supply fixed)",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "savings_comparative_statics.png", dpi=200,
                bbox_inches="tight")
    plt.close(fig)
    print("Saved savings_comparative_statics.png")


def load_supply_curve_sweep():
    with open(Path(__file__).parent / "supply_curve_sweep.json") as f:
        return json.load(f)


def plot_simultaneous_clearing():
    """
    Two-panel (stacked) figure showing how α clears both markets.

    Top panel: R_s(α) falling, R_b(α) rising, with the equity premium
    shaded between them.

    Bottom panel: supply-implied premium (decreasing in α) vs household
    demand for premium (increasing in α). The supply curve comes from
    market clearing; the demand curve from the lifecycle model solved at
    supply-implied returns. Where they cross = equilibrium α*.
    """
    ge = load_ge()
    sc = load_supply_curve_sweep()

    E_agg = ge["E_agg"]
    B_agg = ge["B_agg"]
    eq_alpha = ge["avg_portfolio_share"]
    eq_rs = (ge["r_s"] - 1) * 100
    eq_rf = (ge["r_f"] - 1) * 100
    eq_premium = eq_rs - eq_rf
    S_repr = ge["avg_savings_amount"]

    # ── Smooth analytical curves for top panel ──
    alpha_smooth = np.linspace(0.10, 0.72, 300)
    R_s_curve = E_agg / (alpha_smooth * S_repr) * 100
    R_b_curve = B_agg / ((1 - alpha_smooth) * S_repr) * 100

    # ── Supply curve sweep data for bottom panel ──
    # Supply: at each α_input, market clearing implies a premium
    alpha_input = np.array([r["alpha_input"] for r in sc])
    premium_supply = np.array([r["premium"] * 100 for r in sc])
    # Demand: the household chose α_model when shown that premium
    # So the demand curve is: (α_model, premium) — "this premium makes
    # the household choose this α"
    alpha_model = np.array([r["avg_portfolio_share"] for r in sc])

    # ── Find the actual crossing point by interpolation ──
    # Supply: (alpha_input, premium_supply) — decreasing
    # Demand: (alpha_model, premium_supply) — increasing
    # At the crossing, both curves give the same (α, premium).
    # Interpolate both to a fine grid and find where they match.
    from scipy.interpolate import interp1d
    # Supply: premium as function of α (decreasing)
    f_supply = interp1d(alpha_input, premium_supply, kind='linear',
                        fill_value='extrapolate')
    # Demand: premium as function of α (increasing) — invert (α_model, premium)
    # Sort by alpha_model for interpolation
    sort_idx = np.argsort(alpha_model)
    f_demand = interp1d(alpha_model[sort_idx], premium_supply[sort_idx],
                        kind='linear', fill_value='extrapolate')

    # Find crossing: where f_supply(α) = f_demand(α)
    alpha_fine = np.linspace(max(alpha_input.min(), alpha_model.min()),
                             min(alpha_input.max(), alpha_model.max()), 1000)
    diff = f_supply(alpha_fine) - f_demand(alpha_fine)
    cross_idx = np.where(np.diff(np.sign(diff)))[0][0]
    # Linear interpolation for precise crossing
    a1, a2 = alpha_fine[cross_idx], alpha_fine[cross_idx + 1]
    d1, d2 = diff[cross_idx], diff[cross_idx + 1]
    cross_alpha = a1 - d1 * (a2 - a1) / (d2 - d1)
    cross_premium = float(f_supply(cross_alpha))

    # Get R_s and R_b at the crossing α from the analytical curves
    cross_rs = E_agg / (cross_alpha * S_repr) * 100
    cross_rb = B_agg / ((1 - cross_alpha) * S_repr) * 100

    # ── Figure ──
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), sharex=True,
                                    gridspec_kw={"height_ratios": [1, 1],
                                                 "hspace": 0.08})
    a_pct = alpha_smooth * 100

    # ── Top panel: R_s(α) and R_b(α) ──
    ax1.plot(a_pct, R_s_curve, "-", color="#d95f02", linewidth=2.5,
             label=r"$R_s(\alpha)$ — stock market clearing", zorder=2)
    ax1.plot(a_pct, R_b_curve, "-", color="#2c7fb8", linewidth=2.5,
             label=r"$R_b(\alpha)$ — bond market clearing", zorder=2)

    # Shade the premium
    ax1.fill_between(a_pct, R_b_curve, R_s_curve,
                     where=R_s_curve > R_b_curve,
                     alpha=0.12, color="#7570b3", label="Equity premium")

    # Equilibrium points — at the actual crossing α
    ax1.plot(cross_alpha * 100, cross_rs, "s", color="#2ca02c", markersize=12,
             zorder=5)
    ax1.plot(cross_alpha * 100, cross_rb, "s", color="#2ca02c", markersize=12,
             zorder=5)
    ax1.axvline(cross_alpha * 100, color="#2ca02c", linewidth=1.5,
                linestyle="--", alpha=0.4, zorder=1)

    ax1.annotate(r"$R_s^*$",
                 xy=(cross_alpha * 100, cross_rs),
                 xytext=(cross_alpha * 100 + 10, cross_rs + 1.0),
                 fontsize=12, color="#d95f02", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.5))
    ax1.annotate(r"$R_b^*$",
                 xy=(cross_alpha * 100, cross_rb),
                 xytext=(cross_alpha * 100 - 12, cross_rb + 2.5),
                 fontsize=12, color="#2c7fb8", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#2c7fb8", lw=1.5))

    ax1.set_ylabel("Expected return (%)")
    ax1.set_title(r"Market-clearing returns")
    ax1.set_xlim(12, 68)
    ax1.set_ylim(0, 14)
    ax1.legend(fontsize=9, loc="upper right")
    ax1.grid(True, alpha=0.15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelbottom=False)

    # ── Bottom panel: premium supply vs demand ──
    # Supply curve: (α_input, premium) — decreasing
    ax2.plot(alpha_input * 100, premium_supply, "o-", color="#7570b3",
             linewidth=2.5, markersize=7, zorder=2,
             label="Supply-implied premium\n(from market clearing)")
    # Demand curve: (α_model, premium) — increasing
    # Same premium values, but plotted at the α the household chose
    ax2.plot(alpha_model * 100, premium_supply, "o-", color="#e7298a",
             linewidth=2.5, markersize=7, zorder=3,
             label="Household demand for premium\n(from lifecycle model)")

    # Equilibrium — at the actual crossing
    ax2.plot(cross_alpha * 100, cross_premium, "s", color="#2ca02c",
             markersize=13, zorder=5)
    ax2.axvline(cross_alpha * 100, color="#2ca02c", linewidth=1.5,
                linestyle="--", alpha=0.4, zorder=1)
    ax2.annotate(r"$\alpha^*$",
                 xy=(cross_alpha * 100, cross_premium),
                 xytext=(cross_alpha * 100 + 8, cross_premium + 3),
                 fontsize=12, color="#2ca02c", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax2.set_xlabel(r"Portfolio share in stocks, $\alpha$ (%)")
    ax2.set_ylabel("Equity premium (pp)")
    ax2.set_title(r"Why $\alpha^*$ clears the market")
    ax2.set_xlim(12, 68)
    ax2.set_ylim(-1, 14)
    ax2.legend(fontsize=9, loc="upper right")
    ax2.grid(True, alpha=0.15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "simultaneous_clearing.png", dpi=200)
    plt.close(fig)
    print("Saved simultaneous_clearing.png")


def _find_crossing(alpha_input, premium_supply, alpha_model):
    """Find the (α, premium) where supply and demand curves cross."""
    from scipy.interpolate import interp1d
    f_supply = interp1d(alpha_input, premium_supply, kind='linear',
                        fill_value='extrapolate')
    sort_idx = np.argsort(alpha_model)
    f_demand = interp1d(alpha_model[sort_idx], premium_supply[sort_idx],
                        kind='linear', fill_value='extrapolate')
    alpha_fine = np.linspace(max(alpha_input.min(), alpha_model.min() + 0.001),
                             min(alpha_input.max(), alpha_model.max() - 0.001), 1000)
    diff = f_supply(alpha_fine) - f_demand(alpha_fine)
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    if len(sign_changes) == 0:
        return None, None
    idx = sign_changes[0]
    a1, a2 = alpha_fine[idx], alpha_fine[idx + 1]
    d1, d2 = diff[idx], diff[idx + 1]
    cross_alpha = a1 - d1 * (a2 - a1) / (d2 - d1)
    cross_premium = float(f_supply(cross_alpha))
    return cross_alpha, cross_premium


def plot_earnings_shift():
    """
    Comparative static: what happens when E falls (fewer earnings claims)
    while household income stays the same?

    Shows baseline and shifted equilibria on the same two-panel figure.
    R_s curve shifts down (lower returns at each α), equilibrium α falls,
    premium compresses, but S barely moves.
    """
    ge = load_ge()
    sc_base = load_supply_curve_sweep()
    with open(Path(__file__).parent / "supply_curve_sweep_low_E.json") as f:
        sc_low = json.load(f)

    E_agg = ge["E_agg"]
    E_low = E_agg * 0.7
    B_agg = ge["B_agg"]
    S_repr = ge["avg_savings_amount"]

    # ── Smooth analytical curves ──
    alpha_smooth = np.linspace(0.10, 0.72, 300)
    a_pct = alpha_smooth * 100

    R_s_base = E_agg / (alpha_smooth * S_repr) * 100
    R_b_base = B_agg / ((1 - alpha_smooth) * S_repr) * 100

    R_s_low = E_low / (alpha_smooth * S_repr) * 100
    # R_b doesn't change (B and S unchanged)

    # ── Sweep data ──
    ai_base = np.array([r["alpha_input"] for r in sc_base])
    ps_base = np.array([r["premium"] * 100 for r in sc_base])
    am_base = np.array([r["avg_portfolio_share"] for r in sc_base])

    ai_low = np.array([r["alpha_input"] for r in sc_low])
    ps_low = np.array([r["premium"] * 100 for r in sc_low])
    am_low = np.array([r["avg_portfolio_share"] for r in sc_low])

    # ── Find crossings ──
    ca_base, cp_base = _find_crossing(ai_base, ps_base, am_base)
    ca_low, cp_low = _find_crossing(ai_low, ps_low, am_low)

    cr_s_base = E_agg / (ca_base * S_repr) * 100
    cr_b_base = B_agg / ((1 - ca_base) * S_repr) * 100
    cr_s_low = E_low / (ca_low * S_repr) * 100
    cr_b_low = B_agg / ((1 - ca_low) * S_repr) * 100

    # ── Savings rate data ──
    sr_base = np.array([r["avg_savings_rate"] * 100 for r in sc_base])
    sr_low = np.array([r["avg_savings_rate"] * 100 for r in sc_low])

    # Interpolate savings rate at equilibrium crossings
    from scipy.interpolate import interp1d as interp1d_sr
    f_sr_base = interp1d_sr(am_base, sr_base, kind='linear', fill_value='extrapolate')
    f_sr_low = interp1d_sr(am_low, sr_low, kind='linear', fill_value='extrapolate')
    sr_at_base = float(f_sr_base(ca_base))
    sr_at_low = float(f_sr_low(ca_low))

    # ── Figure ──
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 13), sharex=True,
                                         gridspec_kw={"height_ratios": [1, 1, 0.6],
                                                      "hspace": 0.08})

    # ── Top panel: R_s(α) and R_b(α) ──
    # Baseline
    ax1.plot(a_pct, R_s_base, "-", color="#d95f02", linewidth=2.5,
             label=r"$R_s(\alpha)$ — baseline $E$", zorder=2)
    ax1.plot(a_pct, R_b_base, "-", color="#2c7fb8", linewidth=2.5,
             label=r"$R_b(\alpha)$ — bond clearing", zorder=2)

    # Shifted R_s
    ax1.plot(a_pct, R_s_low, "--", color="#d95f02", linewidth=2, alpha=0.6,
             label=r"$R_s(\alpha)$ — reduced $E$ (0.7×)", zorder=2)



    # Baseline equilibrium
    ax1.plot(ca_base * 100, cr_s_base, "s", color="#2ca02c", markersize=11,
             zorder=5)
    ax1.plot(ca_base * 100, cr_b_base, "s", color="#2ca02c", markersize=11,
             zorder=5)
    ax1.axvline(ca_base * 100, color="#2ca02c", linewidth=1.2,
                linestyle="--", alpha=0.35, zorder=1)

    # New equilibrium
    ax1.plot(ca_low * 100, cr_s_low, "D", color="#e41a1c", markersize=10,
             zorder=5)
    ax1.plot(ca_low * 100, cr_b_low, "D", color="#e41a1c", markersize=10,
             zorder=5)
    ax1.axvline(ca_low * 100, color="#e41a1c", linewidth=1.2,
                linestyle="--", alpha=0.35, zorder=1)

    # Arrow from old to new equilibrium on R_s
    ax1.annotate("", xy=(ca_low * 100, cr_s_low),
                 xytext=(ca_base * 100, cr_s_base),
                 arrowprops=dict(arrowstyle="->", color="gray", lw=2,
                                 connectionstyle="arc3,rad=-0.2"))

    ax1.set_ylabel("Expected return (%)")
    ax1.set_title(r"Effect of lower earnings supply ($E$)")
    ax1.set_xlim(12, 68)
    ax1.set_ylim(0, 14)
    ax1.legend(fontsize=9, loc="upper right")
    ax1.grid(True, alpha=0.15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelbottom=False)

    # ── Bottom panel: premium supply vs demand ──
    # Baseline
    ax2.plot(ai_base * 100, ps_base, "o-", color="#7570b3",
             linewidth=2.5, markersize=6, zorder=2,
             label="Supply premium — baseline $E$")
    ax2.plot(am_base * 100, ps_base, "o-", color="#e7298a",
             linewidth=2.5, markersize=6, zorder=3,
             label="Household demand")

    # Shifted supply (demand stays ~fixed since it depends on premium, not level)
    ax2.plot(ai_low * 100, ps_low, "s--", color="#7570b3",
             linewidth=2, markersize=5, alpha=0.6, zorder=2,
             label="Supply premium — reduced $E$")

    # Baseline equilibrium
    ax2.plot(ca_base * 100, cp_base, "s", color="#2ca02c",
             markersize=12, zorder=5)
    ax2.axvline(ca_base * 100, color="#2ca02c", linewidth=1.2,
                linestyle="--", alpha=0.35, zorder=1)

    # New equilibrium
    ax2.plot(ca_low * 100, cp_low, "D", color="#e41a1c",
             markersize=10, zorder=5)
    ax2.axvline(ca_low * 100, color="#e41a1c", linewidth=1.2,
                linestyle="--", alpha=0.35, zorder=1)

    # Arrow
    ax2.annotate("", xy=(ca_low * 100, cp_low),
                 xytext=(ca_base * 100, cp_base),
                 arrowprops=dict(arrowstyle="->", color="gray", lw=2,
                                 connectionstyle="arc3,rad=-0.2"))

    ax2.set_ylabel("Equity premium (pp)")
    ax2.set_title(r"Equilibrium shift when $E$ falls")
    ax2.set_xlim(12, 68)
    ax2.set_ylim(-1, 14)
    ax2.legend(fontsize=8, loc="upper right", ncol=2)
    ax2.grid(True, alpha=0.15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelbottom=False)

    # ── Third panel: savings rate vs α ──
    ax3.plot(am_base * 100, sr_base, "o-", color="#2c7fb8",
             linewidth=2.5, markersize=6, zorder=3,
             label="Baseline $E$")
    ax3.plot(am_low * 100, sr_low, "s--", color="#2c7fb8",
             linewidth=2, markersize=5, alpha=0.6, zorder=3,
             label="Reduced $E$ (0.7×)")

    # Baseline equilibrium
    ax3.plot(ca_base * 100, sr_at_base, "s", color="#2ca02c",
             markersize=12, zorder=5)
    ax3.axvline(ca_base * 100, color="#2ca02c", linewidth=1.2,
                linestyle="--", alpha=0.35, zorder=1)

    # New equilibrium
    ax3.plot(ca_low * 100, sr_at_low, "D", color="#e41a1c",
             markersize=10, zorder=5)
    ax3.axvline(ca_low * 100, color="#e41a1c", linewidth=1.2,
                linestyle="--", alpha=0.35, zorder=1)

    # Arrow
    ax3.annotate("", xy=(ca_low * 100, sr_at_low),
                 xytext=(ca_base * 100, sr_at_base),
                 arrowprops=dict(arrowstyle="->", color="gray", lw=2,
                                 connectionstyle="arc3,rad=0.2"))

    ax3.set_xlabel(r"Portfolio share in stocks, $\alpha$ (%)")
    ax3.set_ylabel("Savings rate (%)")
    ax3.set_title("Total savings barely moves")
    ax3.set_xlim(12, 68)
    ax3.set_ylim(69, 73)
    ax3.legend(fontsize=9, loc="upper right")
    ax3.grid(True, alpha=0.15)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "earnings_shift.png", dpi=200)
    plt.close(fig)
    print("Saved earnings_shift.png")


def plot_savings_supply_curve():
    """
    Savings supply S(E, B) as a function of exogenous asset supply.

    Two panels:
      Left: S vs E (B fixed)
      Right: S vs B (E fixed)

    Each point is a full GE equilibrium. The flatness of S across a wide
    y-axis (0.2–0.8) visually demonstrates the inelasticity.
    """
    with open(Path(__file__).parent / "sweep_E.json") as f:
        sweep_E = json.load(f)
    with open(Path(__file__).parent / "sweep_B.json") as f:
        sweep_B = json.load(f)

    # ── Extract data ──
    E_mults = [r["E_mult"] for r in sweep_E]
    S_rate_E = [r["avg_savings_rate"] for r in sweep_E]

    B_mults = [r["B_mult"] for r in sweep_B]
    S_rate_B = [r["avg_savings_rate"] for r in sweep_B]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)

    # ── Left: S vs E (B fixed) ──
    ax1.plot(E_mults, S_rate_E, "o-", color="#2c7fb8", linewidth=2.5,
             markersize=9, zorder=3)

    ax1.set_xlabel("Earnings supply $E$ (multiple of baseline)")
    ax1.set_ylabel("$S(E, B)$  —  Savings rate")
    ax1.set_title("Varying earnings supply $E$\n(bond supply $B$ fixed)")
    ax1.set_ylim(0.2, 0.8)
    ax1.grid(True, alpha=0.15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ── Right: S vs B (E fixed) ──
    ax2.plot(B_mults, S_rate_B, "o-", color="#d95f02", linewidth=2.5,
             markersize=9, zorder=3)

    ax2.set_xlabel("Bond supply $B$ (multiple of baseline)")
    ax2.set_title("Varying bond supply $B$\n(earnings supply $E$ fixed)")
    ax2.set_ylim(0.2, 0.8)
    ax2.grid(True, alpha=0.15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Savings supply is inelastic: $S(E, B)$ barely moves",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "savings_supply_curve.png", dpi=200,
                bbox_inches="tight")
    plt.close(fig)
    print("Saved savings_supply_curve.png")


if __name__ == "__main__":
    plot_savings_supply()
    plot_equilibrium()
    plot_returns_and_premium()
    plot_simultaneous_clearing()
    plot_earnings_shift()
    plot_savings_supply_curve()

    # Only plot savings comparative statics if the data exists
    if (Path(__file__).parent / "savings_sweep_results.json").exists():
        plot_savings_comparative_statics()

    print(f"\nFigures saved to {OUTPUT_DIR}/")
