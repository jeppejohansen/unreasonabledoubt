"""
Generate figures for the "Demand for Investment Is Inelastic" blog post.

Uses data from:
  - ge_sweep_results.json: GE sweep (R_f endogenous at each R_s)
  - ge_results.json: converged general equilibrium
  - sweep_results.json: partial equilibrium sweep (R_f fixed, for decomposition)

Produces:
  1. savings_vs_return.png — savings rate vs expected stock return (near-vertical)
  2. portfolio_share_vs_return.png — stock share vs expected return (elastic)
  3. supply_demand.png — supply-demand diagram for savings market
  4. decomposition.png — how portfolio choice absorbs return changes
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (7, 5),
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
})


def load_ge_sweep():
    with open(Path(__file__).parent / "ge_sweep_results.json") as f:
        return json.load(f)


def load_ge():
    with open(Path(__file__).parent / "ge_results.json") as f:
        return json.load(f)


def load_pe_sweep():
    with open(Path(__file__).parent / "sweep_results.json") as f:
        return json.load(f)


def deterministic_savings_rate(R, gamma=5, beta=0.96, y_bar=1.0,
                               t_work=30, t_ret=10):
    """
    Compute lifecycle-average savings rate in the deterministic case
    (no stock return risk — all savings in bonds earning gross return R).
    Solved via backward induction with borrowing constraint.
    """
    from scipy.optimize import minimize_scalar

    t_total = t_work + t_ret
    w_grid = np.exp(np.linspace(np.log(0.01), np.log(40), 100))
    n_w = len(w_grid)

    def u(c):
        if gamma == 1.0:
            return np.log(max(c, 1e-10))
        return max(c, 1e-10) ** (1 - gamma) / (1 - gamma)

    def y(t):
        return y_bar if t < t_work else 0.0

    v = np.array([u(w) for w in w_grid])
    c_pol = np.zeros((t_total, n_w))
    c_pol[t_total - 1, :] = w_grid

    for t in range(t_total - 2, -1, -1):
        v_next = v.copy()
        v_new = np.zeros(n_w)
        y_next = y(t + 1)
        for i, w in enumerate(w_grid):
            def neg_val(c):
                s = w - c
                w_next = R * s + y_next
                v_interp = np.interp(w_next, w_grid, v_next)
                return -(u(c) + beta * v_interp)
            res = minimize_scalar(neg_val, bounds=(0.01 * w, 0.99 * w),
                                  method='bounded')
            c_pol[t, i] = res.x
            v_new[i] = -res.fun
        v = v_new

    # Simulate forward
    w = y_bar
    savings_rates = []
    for t in range(t_total - 1):
        c = np.interp(w, w_grid, c_pol[t])
        c = min(c, w - 0.01)
        c = max(c, 0.01)
        s = w - c
        savings_rates.append(s / w)
        w = R * s + y(t + 1)

    return np.mean(savings_rates)


def plot_savings_vs_return():
    """Total savings rate vs expected stock return — the core inelasticity result."""
    sweep = load_ge_sweep()
    ge = load_ge()

    returns = [(r["r_s_input"] - 1) * 100 for r in sweep]
    savings = [r["avg_savings_rate"] * 100 for r in sweep]
    eq_rs = (ge["r_s"] - 1) * 100
    eq_savings = ge["avg_savings_rate"] * 100

    fig, ax = plt.subplots()
    ax.plot(savings, returns, "o-", color="#2c7fb8", linewidth=2.5, markersize=8,
            zorder=3)
    ax.plot(eq_savings, eq_rs, "s", color="#2ca02c", markersize=12, zorder=5)
    ax.annotate(f"Equilibrium\nR_s = {eq_rs:.1f}%",
                xy=(eq_savings, eq_rs),
                xytext=(eq_savings + 0.3, eq_rs + 2.5),
                fontsize=10, color="#2ca02c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax.set_ylabel("Expected stock return (%)")
    ax.set_xlabel("Average savings rate (%)")
    ax.set_title("Savings supply is nearly inelastic")
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    sr_range = max(savings) - min(savings)
    ret_range = max(returns) - min(returns)
    ax.text(np.mean(savings), min(returns) + 1,
            f"Savings varies {sr_range:.1f}pp\nwhile R_s varies {ret_range:.0f}pp",
            fontsize=10, color="gray", style="italic", ha="center")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "savings_vs_return.png", dpi=200)
    plt.close(fig)
    print("Saved savings_vs_return.png")


def plot_portfolio_share_vs_return():
    """Stock portfolio share vs expected return — elastic portfolio reallocation."""
    sweep = load_ge_sweep()
    ge = load_ge()

    returns = [(r["r_s_input"] - 1) * 100 for r in sweep]
    shares = [r["avg_portfolio_share"] * 100 for r in sweep]
    eq_rs = (ge["r_s"] - 1) * 100
    eq_alpha = ge["avg_portfolio_share"] * 100

    fig, ax = plt.subplots()
    ax.plot(shares, returns, "s-", color="#d95f02", linewidth=2.5, markersize=8,
            zorder=3)
    ax.plot(eq_alpha, eq_rs, "s", color="#2ca02c", markersize=12, zorder=5)
    ax.annotate(f"Equilibrium\nα = {eq_alpha:.0f}%",
                xy=(eq_alpha, eq_rs),
                xytext=(eq_alpha - 15, eq_rs + 2.5),
                fontsize=10, color="#2ca02c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax.set_ylabel("Expected stock return (%)")
    ax.set_xlabel("Average stock portfolio share (%)")
    ax.set_title("Portfolio allocation is highly elastic")
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "portfolio_share_vs_return.png", dpi=200)
    plt.close(fig)
    print("Saved portfolio_share_vs_return.png")


def plot_supply_demand():
    """Supply-demand diagram: near-vertical savings supply, downward-sloping demand."""
    sweep = load_ge_sweep()
    ge = load_ge()

    returns = [(r["r_s_input"] - 1) * 100 for r in sweep]
    savings = [r["avg_savings_rate"] * 100 for r in sweep]
    eq_rs = (ge["r_s"] - 1) * 100
    eq_savings = ge["avg_savings_rate"] * 100

    savings_range = np.linspace(min(savings) - 5, max(savings) + 5, 50)
    demand_slope = -0.4
    demand_returns = eq_rs + demand_slope * (savings_range - eq_savings)

    fig, ax = plt.subplots()

    ax.plot(savings, returns, "o-", color="#2c7fb8", linewidth=2.5, markersize=7,
            label="Savings supply\n(from model)", zorder=3)
    ax.plot(savings_range, demand_returns, "--", color="#d95f02", linewidth=2,
            label="Capital demand\n(illustrative)")

    # Shifted demand
    shift = -3.0
    ax.plot(savings_range, demand_returns + shift, "--", color="#d95f02",
            linewidth=2, alpha=0.4, label="Demand after\nnegative shift")

    # Arrow showing the price adjustment
    ax.annotate("", xy=(eq_savings, eq_rs + shift), xytext=(eq_savings, eq_rs),
                arrowprops=dict(arrowstyle="->", color="gray", lw=2))
    ax.text(eq_savings + 1.0, eq_rs + shift / 2,
            "Return falls,\nquantity barely\nchanges",
            fontsize=9, color="gray")

    ax.plot(eq_savings, eq_rs, "s", color="#2ca02c", markersize=10, zorder=5)

    ax.set_xlabel("Savings / Investment quantity (%)")
    ax.set_ylabel("Return (%)")
    ax.set_title("Inelastic supply: demand shifts move prices, not quantities")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "supply_demand.png", dpi=200)
    plt.close(fig)
    print("Saved supply_demand.png")


def plot_decomposition():
    """
    Compare the full model (risky stocks available) with a deterministic
    bonds-only baseline. Both have the same lifecycle/retirement structure.

    The deterministic model shows what savings would look like if households
    could only hold safe bonds — savings responds more to the return because
    the substitution/income effects operate unopposed. With risky stocks
    available, portfolio reallocation absorbs most of the adjustment.
    """
    sweep = load_ge_sweep()

    returns_pct = np.array([(r["r_s_input"] - 1) * 100 for r in sweep])
    savings_pct = np.array([r["avg_savings_rate"] * 100 for r in sweep])

    print("  Computing deterministic (bonds-only) savings rates...")
    det_savings = np.array([
        deterministic_savings_rate(r["r_s_input"]) * 100
        for r in sweep
    ])

    fig, ax = plt.subplots()

    ax.plot(returns_pct, savings_pct, "o-", color="#2c7fb8", linewidth=2.5,
            markersize=7, label="Full model\n(stocks + bonds)", zorder=3)
    ax.plot(returns_pct, det_savings, "^--", color="#7570b3", linewidth=2,
            markersize=6, label="Bonds only\n(no portfolio choice)")

    ax.fill_between(returns_pct, det_savings, savings_pct,
                    where=savings_pct >= det_savings,
                    alpha=0.15, color="#2ca02c")
    ax.fill_between(returns_pct, det_savings, savings_pct,
                    where=savings_pct < det_savings,
                    alpha=0.15, color="#d62728")

    ax.set_xlabel("Expected stock return (%)")
    ax.set_ylabel("Average savings rate (%)")
    ax.set_title("Portfolio choice absorbs return changes,\nleaving total savings stable")
    ax.legend(fontsize=9, loc="best")
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "decomposition.png", dpi=200)
    plt.close(fig)
    print("Saved decomposition.png")


if __name__ == "__main__":
    plot_savings_vs_return()
    plot_portfolio_share_vs_return()
    plot_supply_demand()
    plot_decomposition()

    print(f"\nAll figures saved to {OUTPUT_DIR}/")
