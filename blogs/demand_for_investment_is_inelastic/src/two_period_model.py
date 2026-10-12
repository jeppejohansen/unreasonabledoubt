"""Two-period saving, portfolio choice, and fixed-claim market clearing.

Run from the repository root with:
    uv run python blogs/demand_for_investment_is_inelastic/src/two_period_model.py

The model is deliberately a one-shot exchange economy. A cohort of workers
buys one aggregate unit of each existing claim from initial owners, regardless
of price. The claims pay at retirement from exogenous resources. There is no
new stock or safe-claim issuance, and no firm decision to create new capital.
All quantities are illustrative model-period units, not annual calibration.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from tempfile import gettempdir

os.environ.setdefault("MPLCONFIGDIR", str(Path(gettempdir()) / "unreasonabledoubt-mpl"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


POST_DIR = Path(__file__).resolve().parents[1]
FIGURE_DIR = POST_DIR / "figures"
DATA_DIR = POST_DIR / "data"

PAPER = "#FBF8F1"
INK = "#24313A"
MUTED = "#626D70"
GUIDE = "#DFDED7"
TEAL = "#176B78"
RUST = "#B25739"
GREY = "#829093"

plt.rcParams.update(
    {
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": GUIDE,
        "grid.color": GUIDE,
        "grid.alpha": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


@dataclass(frozen=True)
class Parameters:
    y: float = 1.0
    beta: float = 0.60
    gamma: float = 5.0
    bond_payoff: float = 0.30
    stock_payoff_low: float = 0.17
    stock_payoff_high: float = 0.23
    probability_high: float = 0.5
    workers: float = 1.0


BASE = Parameters()


def bisect_increasing(func, low: float, high: float, iterations: int = 100) -> float:
    """Find a zero of an increasing function bracketed by low and high."""
    if not (func(low) <= 0 <= func(high)):
        raise ValueError("The increasing root is not bracketed")
    for _ in range(iterations):
        mid = (low + high) / 2
        if func(mid) > 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2


def utility(c: float | np.ndarray, gamma: float) -> float | np.ndarray:
    if gamma == 1:
        return np.log(c)
    return np.power(c, 1 - gamma) / (1 - gamma)


def riskless_choice(r: float, *, y: float, beta: float, gamma: float) -> dict:
    """Exact two-date CRRA choice with no income in retirement."""
    a = beta ** (1 / gamma) * r ** (1 / gamma - 1)
    s = y * a / (1 + a)
    c0 = y - s
    c1 = r * s
    u = float(utility(c0, gamma) + beta * utility(c1, gamma))
    return {"saving": s, "c0": c0, "c1": c1, "utility": u}


def hicks_choice(r_new: float, old_utility: float, *, beta: float, gamma: float) -> dict:
    """New-slope tangency on the original indifference curve."""
    q = (beta * r_new) ** (1 / gamma)  # c1/c0
    if gamma == 1:
        c0 = np.exp((old_utility - beta * np.log(q)) / (1 + beta))
    else:
        base = (1 - gamma) * old_utility / (1 + beta * q ** (1 - gamma))
        c0 = base ** (1 / (1 - gamma))
    c1 = q * c0
    return {"c0": c0, "c1": c1, "compensated_y": c0 + c1 / r_new}


def risky_choice(
    mean_stock_return: float,
    stock_return_spread: float,
    safe_return: float,
    *,
    y: float,
    beta: float,
    gamma: float,
) -> dict:
    """Partial-equilibrium saving and portfolio choice in two equal states.

    Stock returns are mean +/- spread. The no-short/no-leverage restriction is
    alpha in [0, 1]. The portfolio FOC is strictly decreasing in alpha.
    """
    stock_returns = np.array(
        [mean_stock_return - stock_return_spread, mean_stock_return + stock_return_spread]
    )

    def portfolio_foc(alpha: float) -> float:
        portfolio_returns = safe_return + alpha * (stock_returns - safe_return)
        return float(np.mean((stock_returns - safe_return) * portfolio_returns ** (-gamma)))

    if portfolio_foc(0) <= 0:
        alpha = 0.0
    elif portfolio_foc(1) >= 0:
        alpha = 1.0
    else:
        alpha = bisect_increasing(lambda a: -portfolio_foc(a), 0.0, 1.0)

    portfolio_returns = safe_return + alpha * (stock_returns - safe_return)
    a = (beta * np.mean(portfolio_returns ** (1 - gamma))) ** (1 / gamma)
    saving = y * a / (1 + a)
    return {"alpha": alpha, "saving": saving, "saving_rate": saving / y}


def exchange_equilibrium(p: Parameters, *, workers: float | None = None) -> dict:
    """Price one stock claim and one safe claim for a cohort of workers.

    Each worker buys 1/n of each aggregate claim. Thus retirement consumption
    in state j is (D_j+B)/n. The asset FOCs price the two claims, and the
    aggregate young budget sets P_stock+P_bond = n*(y-c0).
    """
    n = p.workers if workers is None else workers
    if n <= 0:
        raise ValueError("workers must be positive")
    d = np.array([p.stock_payoff_low, p.stock_payoff_high], dtype=float)
    weights = np.array([1 - p.probability_high, p.probability_high])
    total_payoff = d + p.bond_payoff
    if np.any(total_payoff <= 0) or p.bond_payoff <= 0 or np.any(d <= 0):
        raise ValueError("All terminal payoffs must be positive")

    payoff_moment = float(np.dot(weights, total_payoff ** (1 - p.gamma)))
    coefficient = p.beta * n ** (p.gamma - 1) * payoff_moment
    c0 = bisect_increasing(lambda c: c + coefficient * c ** p.gamma - p.y, 0, p.y)
    saving_each = p.y - c0
    c1 = total_payoff / n
    marginal_utility_0 = c0 ** (-p.gamma)
    discount = p.beta * c1 ** (-p.gamma) / marginal_utility_0
    p_stock = float(np.dot(weights, discount * d))
    p_bond = float(np.dot(weights, discount * p.bond_payoff))
    total_price = p_stock + p_bond
    expected_stock_return = float(np.dot(weights, d)) / p_stock
    safe_return = p.bond_payoff / p_bond
    alpha = p_stock / total_price

    # The FOCs and the aggregate flow budget must both hold, not just one.
    assert abs(total_price - n * saving_each) < 1e-10
    rp = alpha * d / p_stock + (1 - alpha) * p.bond_payoff / p_bond
    assert abs(float(np.dot(weights, (d / p_stock - p.bond_payoff / p_bond) * rp ** (-p.gamma)))) < 1e-9

    return {
        "workers": n,
        "c0_each": c0,
        "saving_each": saving_each,
        "worker_cohort_saving": n * saving_each,
        "c1_low_each": float(c1[0]),
        "c1_high_each": float(c1[1]),
        "stock_price": p_stock,
        "bond_price": p_bond,
        "total_price": total_price,
        "stock_value_share": alpha,
        "expected_stock_return": expected_stock_return,
        "safe_return": safe_return,
    }


def bundle_units_demand(total_price: float, p: Parameters, workers: float) -> float:
    """Aggregate demand for fixed-payoff asset bundles at a candidate price.

    Relative stock and bond prices stay at their equilibrium ratio. Scaling
    both prices changes the return on one fixed aggregate payoff bundle.
    """
    d = np.array([p.stock_payoff_low, p.stock_payoff_high])
    weights = np.array([1 - p.probability_high, p.probability_high])
    bundle_returns = (d + p.bond_payoff) / total_price
    a = (p.beta * np.dot(weights, bundle_returns ** (1 - p.gamma))) ** (1 / p.gamma)
    saving_each = p.y * a / (1 + a)
    return workers * saving_each / total_price


def finish_axis(ax: plt.Axes, *, grid: bool = True) -> None:
    if grid:
        ax.grid(axis="y", linewidth=0.7)
    ax.tick_params(length=0)


def save_figure(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIGURE_DIR / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_smoothing() -> dict:
    r0, r1 = 1.07, 1.30  # A large illustrative change keeps A, H, B legible.
    a = riskless_choice(r0, y=BASE.y, beta=BASE.beta, gamma=BASE.gamma)
    b = riskless_choice(r1, y=BASE.y, beta=BASE.beta, gamma=BASE.gamma)
    h = hicks_choice(r1, a["utility"], beta=BASE.beta, gamma=BASE.gamma)

    def curve(x: np.ndarray, u: float) -> np.ndarray:
        inside = ((1 - BASE.gamma) * u - x ** (1 - BASE.gamma)) / BASE.beta
        out = np.full_like(x, np.nan)
        valid = inside > 0
        out[valid] = inside[valid] ** (1 / (1 - BASE.gamma))
        return out

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2), gridspec_kw={"width_ratios": [1, 1.05]})
    x = np.linspace(0.10, 1.0, 600)
    axes[0].plot(x, r0 * (BASE.y - x), color=TEAL, lw=2.6, label="Initial budget")
    axes[0].plot(x, r1 * (BASE.y - x), color=RUST, lw=2.6, ls="--", label="Higher return")
    axes[0].plot(x, r1 * (h["compensated_y"] - x), color=GREY, lw=1.9, ls=":", label="Compensated")
    axes[0].plot(x, curve(x, a["utility"]), color=GREY, alpha=0.8, lw=1.1)
    axes[0].plot(x, curve(x, b["utility"]), color=GREY, alpha=0.8, lw=1.1)
    axes[0].scatter([a["c0"], h["c0"], b["c0"]], [a["c1"], h["c1"], b["c1"]],
                    color=[TEAL, GREY, RUST], s=36, zorder=5)
    axes[0].scatter([BASE.y], [0], color=INK, s=25)
    axes[0].annotate("Income endowment", (BASE.y, 0), xytext=(-100, 12),
                     textcoords="offset points", color=MUTED, fontsize=8)
    axes[0].set(xlim=(0.12, 1.04), ylim=(-0.03, 1.16), xlabel="Consumption now, c₀", ylabel="Consumption retired, c₁")
    axes[0].legend(frameon=False, loc="upper right", fontsize=8)
    finish_axis(axes[0], grid=False)

    axes[1].plot(x, r0 * (BASE.y - x), color=TEAL, lw=2.6)
    axes[1].plot(x, r1 * (BASE.y - x), color=RUST, lw=2.6, ls="--")
    axes[1].plot(x, r1 * (h["compensated_y"] - x), color=GREY, lw=1.9, ls=":")
    axes[1].plot(x, curve(x, a["utility"]), color=GREY, alpha=0.8, lw=1.1)
    axes[1].plot(x, curve(x, b["utility"]), color=GREY, alpha=0.8, lw=1.1)
    for label, point, color, offset in [
        ("A", a, TEAL, (7, -20)),
        ("H", h, GREY, (-16, -20)),
        ("B", b, RUST, (7, 7)),
    ]:
        axes[1].scatter([point["c0"]], [point["c1"]], color=color, s=55, zorder=6)
        axes[1].annotate(label, (point["c0"], point["c1"]), xytext=offset,
                         textcoords="offset points", weight="bold", color=color)
    axes[1].annotate("Substitution: c₀ falls", xy=(h["c0"], h["c1"]),
                     xytext=(0.405, 0.66), fontsize=8.5, color=MUTED,
                     arrowprops={"arrowstyle": "->", "color": GREY, "lw": 1})
    axes[1].annotate("Income: c₀ rises", xy=(b["c0"], b["c1"]),
                     xytext=(0.55, 0.64), fontsize=8.5, color=MUTED,
                     arrowprops={"arrowstyle": "->", "color": GREY, "lw": 1})
    axes[1].set(xlim=(0.39, 0.67), ylim=(0.39, 0.73), xlabel="Consumption now, c₀", ylabel="Consumption retired, c₁")
    finish_axis(axes[1], grid=False)
    fig.tight_layout(w_pad=2)
    save_figure(fig, "two_period_smoothing.png")
    return {"initial": a, "compensated": h, "new": b, "r_initial": r0, "r_new": r1}


def plot_return_sensitivity() -> None:
    returns = np.linspace(1.00, 1.30, 121)
    r0 = 1.07
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    for gamma, color, style, label in [
        (0.5, RUST, (0, (5, 3)), "γ = 0.5: substitution dominates"),
        (1.0, GREY, (0, (2, 2)), "γ = 1: exactly flat"),
        (5.0, TEAL, "-", "γ = 5: income dominates"),
    ]:
        base = riskless_choice(r0, y=BASE.y, beta=BASE.beta, gamma=gamma)["saving"] / BASE.y
        changes = np.array([riskless_choice(r, y=BASE.y, beta=BASE.beta, gamma=gamma)["saving"] / BASE.y - base for r in returns])
        ax.plot((returns - 1) * 100, changes * 100, color=color, lw=2.7, ls=style, label=label)
    ax.axhline(0, color=GUIDE, lw=1)
    ax.axvline((r0 - 1) * 100, color=GUIDE, lw=1)
    ax.set(xlabel="Safe net return per model period (%)", ylabel="Change in saving rate from R = 1.07 (pp)", xlim=(0, 30))
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    finish_axis(ax)
    fig.tight_layout()
    save_figure(fig, "two_period_return_sensitivity.png")


def plot_portfolio() -> dict:
    means = np.linspace(1.07, 1.16, 121)
    safe = 1.07
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.25))
    samples = {}
    for spread, color, style in [(0.16, TEAL, "-"), (0.22, RUST, "--")]:
        choices = [risky_choice(mu, spread, safe, y=BASE.y, beta=BASE.beta, gamma=BASE.gamma) for mu in means]
        samples[str(spread)] = risky_choice(1.12, spread, safe, y=BASE.y, beta=BASE.beta, gamma=BASE.gamma)
        x = (means - 1) * 100
        axes[0].plot(x, [c["alpha"] * 100 for c in choices], color=color, lw=2.7, ls=style,
                     label=f"Stock return spread ±{spread:.0%}")
        axes[1].plot(x, [c["saving_rate"] * 100 for c in choices], color=color, lw=2.7, ls=style)
    axes[0].set(xlabel="Expected stock net return (%)", ylabel="Share of saving in stock (%)", xlim=(7, 16), ylim=(-2, 95))
    axes[1].set(xlabel="Expected stock net return (%)", ylabel="Saving / earnings (%)", xlim=(7, 16), ylim=(44, 47))
    axes[0].legend(frameon=False, loc="upper left", fontsize=8.5)
    for ax in axes:
        ax.axvline(7, color=GUIDE, lw=1)
        finish_axis(ax)
    fig.tight_layout(w_pad=2.8)
    save_figure(fig, "two_period_portfolio.png")
    return samples


def plot_market_clearing() -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    prices = np.linspace(0.31, 0.62, 240)
    for n, color, style in [(0.9, RUST, "--"), (1.0, GREY, ":"), (1.1, TEAL, "-")]:
        demand = [bundle_units_demand(price, BASE, n) for price in prices]
        ax.plot(demand, prices, color=color, lw=2.6, ls=style, label=f"{n:.1f} workers")
        eq = exchange_equilibrium(BASE, workers=n)
        ax.scatter([1], [eq["total_price"]], color=color, s=42, zorder=6)
    ax.axvline(1, color=INK, lw=1.7, label="One fixed payoff bundle")
    ax.set(xlabel="Aggregate payoff bundles demanded", ylabel="Price of the fixed bundle", xlim=(0.72, 1.28), ylim=(0.30, 0.62))
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    finish_axis(ax)
    fig.tight_layout()
    save_figure(fig, "two_period_market_clearing.png")


def plot_demographic_shock() -> dict:
    workers = np.linspace(0.9, 1.1, 121)
    equilibria = [exchange_equilibrium(BASE, workers=float(n)) for n in workers]
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.25))
    x = (workers - 1) * 100
    axes[0].plot(x, [e["stock_price"] for e in equilibria], color=TEAL, lw=2.7, label="Stock")
    axes[0].plot(x, [e["bond_price"] for e in equilibria], color=RUST, lw=2.7, ls="--", label="Safe claim")
    axes[1].plot(x, [(e["expected_stock_return"] - 1) * 100 for e in equilibria], color=TEAL, lw=2.7, label="Expected stock")
    axes[1].plot(x, [(e["safe_return"] - 1) * 100 for e in equilibria], color=RUST, lw=2.7, ls="--", label="Safe claim")
    axes[0].set(xlabel="Change in number of workers (%)", ylabel="Aggregate claim price", xlim=(-10, 10))
    axes[1].set(xlabel="Change in number of workers (%)", ylabel="Expected net return per model period (%)", xlim=(-10, 10))
    for i, ax in enumerate(axes):
        ax.axvline(0, color=GUIDE, lw=1)
        ax.legend(frameon=False, loc="upper left" if i == 0 else "upper right", fontsize=8.5)
        finish_axis(ax)
    fig.tight_layout(w_pad=2.7)
    save_figure(fig, "two_period_demographic_shock.png")
    return {str(n): exchange_equilibrium(BASE, workers=n) for n in (0.9, 1.0, 1.1)}


def choice_at_candidate_stock_return(
    mu: float, p: Parameters, safe_return: float
) -> tuple[dict, float]:
    """Household choice at an offered expected stock return.

    The physical stock payoff distribution is fixed within a demand curve.
    Its candidate price is E[D]/mu, so both state returns move with price.
    The demand figures use equal-probability states as in the calibration.
    """
    if p.probability_high != 0.5:
        raise ValueError("The return-demand figures require equal state probabilities")
    mean_d = (p.stock_payoff_low + p.stock_payoff_high) / 2
    stock_price = mean_d / mu
    stock_return_spread = (p.stock_payoff_high - p.stock_payoff_low) / (2 * stock_price)
    choice = risky_choice(
        mu, stock_return_spread, safe_return, y=p.y, beta=p.beta, gamma=p.gamma
    )
    return choice, stock_price


def bond_cleared_stock_schedule(mu: float, p: Parameters) -> dict:
    """Clear the safe market at candidate mu; report stock excess demand.

    Only the point with stock_units_demanded == 1 clears both asset markets.
    Other points define a conditional demand schedule, not equilibria.
    """
    def bond_excess(rb: float) -> float:
        choice, _ = choice_at_candidate_stock_return(mu, p, rb)
        desired_bond_spending = p.workers * (1 - choice["alpha"]) * choice["saving"]
        bond_supply_value = p.bond_payoff / rb
        return desired_bond_spending - bond_supply_value

    rb = bisect_increasing(bond_excess, 0.2, 3.0, iterations=55)
    choice, ps = choice_at_candidate_stock_return(mu, p, rb)
    pb = p.bond_payoff / rb
    stock_units = p.workers * choice["alpha"] * choice["saving"] / ps
    bond_units = p.workers * (1 - choice["alpha"]) * choice["saving"] / pb
    assert abs(bond_units - 1) < 1e-10
    expected_old_consumption = choice["saving"] * (
        choice["alpha"] * mu + (1 - choice["alpha"]) * rb
    )
    return {
        "expected_stock_return": mu,
        "safe_return": rb,
        "stock_price": ps,
        "bond_price": pb,
        "stock_units_demanded": stock_units,
        "bond_units_demanded": bond_units,
        "saving_each": choice["saving"],
        "stock_value_share": choice["alpha"],
        "c0_each": p.y - choice["saving"],
        "expected_c1_each": expected_old_consumption,
    }


def stock_units_with_fixed_safe_return(mu: float, p: Parameters, rb: float) -> float:
    choice, ps = choice_at_candidate_stock_return(mu, p, rb)
    return p.workers * choice["alpha"] * choice["saving"] / ps


def safe_units_at_price(mu: float, safe_price: float, p: Parameters) -> float:
    rb = p.bond_payoff / safe_price
    choice, _ = choice_at_candidate_stock_return(mu, p, rb)
    return p.workers * (1 - choice["alpha"]) * choice["saving"] / safe_price


def local_stock_price_elasticity(
    mu: float, p: Parameters, *, fixed_safe_return: float | None = None
) -> float:
    """Finite-difference elasticity of desired stock units to its own price."""
    delta = 1e-4
    if fixed_safe_return is None:
        q_low = bond_cleared_stock_schedule(mu - delta, p)["stock_units_demanded"]
        q_high = bond_cleared_stock_schedule(mu + delta, p)["stock_units_demanded"]
    else:
        q_low = stock_units_with_fixed_safe_return(mu - delta, p, fixed_safe_return)
        q_high = stock_units_with_fixed_safe_return(mu + delta, p, fixed_safe_return)
    mean_d = (p.stock_payoff_low + p.stock_payoff_high) / 2
    p_low_mu = mean_d / (mu - delta)
    p_high_mu = mean_d / (mu + delta)
    return float((np.log(q_high) - np.log(q_low)) / (np.log(p_high_mu) - np.log(p_low_mu)))


def plot_lower_stock_return_demand() -> dict:
    baseline = exchange_equilibrium(BASE)
    lower_payoff_parameters = replace(
        BASE,
        stock_payoff_low=0.9 * BASE.stock_payoff_low,
        stock_payoff_high=0.9 * BASE.stock_payoff_high,
    )
    lower = exchange_equilibrium(lower_payoff_parameters)
    mu_high = baseline["expected_stock_return"]
    mu_low = lower["expected_stock_return"]
    rb_high = baseline["safe_return"]

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.5))
    mu_grid = np.linspace(1.01, 1.18, 80)
    for p, color, style, label in [
        (BASE, TEAL, "-", "Initial payoffs; safe market clears"),
        (lower_payoff_parameters, RUST, "--", "Stock payoff 10% lower; safe market clears"),
    ]:
        q = [bond_cleared_stock_schedule(float(mu), p)["stock_units_demanded"] for mu in mu_grid]
        axes[0].plot(q, (mu_grid - 1) * 100, color=color, lw=2.6, ls=style, label=label)
    fixed_q = [stock_units_with_fixed_safe_return(float(mu), BASE, rb_high) for mu in mu_grid]
    axes[0].plot(fixed_q, (mu_grid - 1) * 100, color=GREY, lw=2.0, ls=":",
                 label="Initial payoffs; safe return fixed")
    axes[0].axvline(1, color=INK, lw=1.5, label="One stock claim available")
    axes[0].scatter([1, 1], [(mu_high - 1) * 100, (mu_low - 1) * 100],
                    color=[TEAL, RUST], s=52, zorder=5)
    axes[0].set(xlabel="Stock claims desired", ylabel="Expected stock net return (%)",
                xlim=(0, 1.45), ylim=(0.5, 18.5))
    axes[0].legend(frameon=False, loc="upper left", fontsize=7.2)
    finish_axis(axes[0])

    safe_prices = np.linspace(0.25, 0.33, 90)
    for mu, p, color, style, label in [
        (mu_high, BASE, TEAL, "-", "Initial stock return"),
        (mu_low, lower_payoff_parameters, RUST, "--", "Lower stock return"),
    ]:
        q = [safe_units_at_price(mu, float(pb), p) for pb in safe_prices]
        axes[1].plot(q, safe_prices, color=color, lw=2.6, ls=style, label=label)
    axes[1].axvline(1, color=INK, lw=1.5, label="One safe claim available")
    axes[1].scatter([1, 1], [baseline["bond_price"], lower["bond_price"]],
                    color=[TEAL, RUST], s=52, zorder=5)
    axes[1].set(xlabel="Safe claims desired", ylabel="Price of safe claim",
                xlim=(0.72, 1.33), ylim=(0.248, 0.333))
    axes[1].legend(frameon=False, loc="upper right", fontsize=8)
    finish_axis(axes[1])
    fig.tight_layout(w_pad=2.5)
    save_figure(fig, "two_period_lower_stock_return_demand.png")

    fixed_elasticity = local_stock_price_elasticity(mu_high, BASE, fixed_safe_return=rb_high)
    cleared_elasticity = local_stock_price_elasticity(mu_high, BASE)
    assert abs(bond_cleared_stock_schedule(mu_high, BASE)["stock_units_demanded"] - 1) < 1e-9
    assert abs(bond_cleared_stock_schedule(mu_low, lower_payoff_parameters)["stock_units_demanded"] - 1) < 1e-9
    return {
        "lower_stock_payoff_factor": 0.9,
        "baseline": baseline,
        "lower_stock_payoff": lower,
        "stock_price_elasticity_fixed_safe_return": fixed_elasticity,
        "stock_price_elasticity_safe_market_clears": cleared_elasticity,
    }


def plot_lower_stock_return_comparison(shock: dict) -> None:
    base = shock["baseline"]
    low = shock["lower_stock_payoff"]
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    labels_left = ["Stock purchase", "Safe purchase", "Total saving"]
    base_left = [base["stock_price"], base["bond_price"], base["saving_each"]]
    low_left = [low["stock_price"], low["bond_price"], low["saving_each"]]
    labels_right = ["Now, c₀", "Retired, E[c₁]"]
    base_right = [base["c0_each"], (base["c1_low_each"] + base["c1_high_each"]) / 2]
    low_right = [low["c0_each"], (low["c1_low_each"] + low["c1_high_each"]) / 2]
    x = np.arange(len(labels_left))
    width = 0.34
    axes[0].bar(x - width / 2, base_left, width, color=TEAL, label="Baseline")
    axes[0].bar(x + width / 2, low_left, width, color=RUST, label="Stock payoff 10% lower")
    for positions, values in [(x - width / 2, base_left), (x + width / 2, low_left)]:
        for xpos, value in zip(positions, values):
            axes[0].text(xpos, value + 0.004, f"{value:.3f}", ha="center", va="bottom", fontsize=8)
    axes[0].set_xticks(x, labels_left)
    axes[0].set_ylim(0, 0.53)
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    finish_axis(axes[0])

    y = np.arange(len(labels_right))[::-1]
    axes[1].hlines(y, low_right, base_right, color=GUIDE, lw=2.5, zorder=1)
    axes[1].scatter(base_right, y, color=TEAL, s=85, label="Baseline", zorder=3)
    axes[1].scatter(low_right, y, color=RUST, s=85, label="Stock payoff 10% lower", zorder=3)
    for values, offset in [(base_right, 0.004), (low_right, -0.004)]:
        for value, ypos in zip(values, y):
            axes[1].text(value + offset, ypos + 0.13, f"{value:.3f}", ha="center", fontsize=8)
    axes[1].set_yticks(y, labels_right)
    axes[1].set_xlim(0.465, 0.55)
    axes[1].set_ylim(-0.45, 1.45)
    axes[1].legend(frameon=False, fontsize=8, loc="lower left")
    finish_axis(axes[1])
    axes[0].set_ylabel("Date-0 goods per worker")
    axes[1].set_xlabel("Consumption per worker")
    fig.tight_layout(w_pad=2.4)
    save_figure(fig, "two_period_lower_stock_return_comparison.png")


def main() -> None:
    FIGURE_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    smoothing = plot_smoothing()
    plot_return_sensitivity()
    portfolio = plot_portfolio()
    plot_market_clearing()
    demographic = plot_demographic_shock()
    stock_return_shock = plot_lower_stock_return_demand()
    plot_lower_stock_return_comparison(stock_return_shock)
    summary = {
        "description": "Illustrative two-period model; one period is not calibrated to one year.",
        "parameters": asdict(BASE),
        "smoothing": smoothing,
        "portfolio_at_mean_stock_return_1_12": portfolio,
        "demographic": demographic,
        "stock_return_shock": stock_return_shock,
    }
    path = DATA_DIR / "two_period_summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"Saved 7 figures to {FIGURE_DIR}")
    print(f"Saved numerical summary to {path}")
    for n, outcome in demographic.items():
        print(f"n={n}: P={outcome['total_price']:.3f}, "
              f"stock return={outcome['expected_stock_return']:.3f}, "
              f"safe return={outcome['safe_return']:.3f}")
    print("Local stock-demand elasticity to its own price: "
          f"{stock_return_shock['stock_price_elasticity_fixed_safe_return']:.2f} "
          "with fixed safe return; "
          f"{stock_return_shock['stock_price_elasticity_safe_market_clears']:.2f} "
          "with the safe market clearing")


if __name__ == "__main__":
    main()
