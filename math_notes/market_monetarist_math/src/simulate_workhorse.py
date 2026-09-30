"""Simulate a candidate market monetarist workhorse model.

This script is intentionally a *candidate closure* of the primitives in
``math_notes/market_monetarist_math/note.typ``. The current Typst note states assumptions;
it does not yet derive the full equilibrium. The goal here is therefore modest:

1. make the proposed mechanisms explicit enough to simulate,
2. compare impulse responses to a standard linear New Keynesian benchmark, and
3. save figures/tables that show where the closure behaves well or badly.

The market monetarist block has:

- consumption-smoothing pressure from expected future real income,
- endogenous velocity pressure from desired spending and money-demand shocks,
- an NGDP-regime policy parameter that offsets velocity pressure through money,
- a short-run nominal non-neutrality closure that maps NGDP gaps into output gaps,
- an endogenous nominal rate proxy from expected inflation and real consumption growth.

The New Keynesian block is the standard three-equation linear model:

- dynamic IS curve,
- New Keynesian Phillips curve,
- Taylor rule.

Run:
    uv run python math_notes/market_monetarist_math/src/simulate_workhorse.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT_DIR / "figures"
DATA_DIR = ROOT_DIR / "data"

COLOR_MM = "#2563eb"
COLOR_PASSIVE = "#6b7280"
COLOR_NK = "#c2410c"
COLOR_ZERO = "#111827"


@dataclass(frozen=True)
class Params:
    periods: int = 48
    shock_date: int = 4

    # Market monetarist closure.
    human_wealth_discount: float = 0.94
    velocity_from_human_wealth: float = 0.85
    velocity_from_money_demand: float = 1.0
    ngdp_regime_offset: float = 0.90
    sras_lambda: float = 0.55
    output_gap_persistence: float = 0.35
    real_rate_sensitivity: float = 0.35
    nominal_rate_smoothing: float = 0.35

    # New Keynesian benchmark.
    nk_beta: float = 0.99
    nk_sigma: float = 1.0
    nk_kappa: float = 0.15
    nk_phi_pi: float = 1.50
    nk_phi_y: float = 0.50


@dataclass(frozen=True)
class Scenario:
    name: str
    title: str
    potential: np.ndarray
    income_news: np.ndarray
    velocity_shock: np.ndarray
    nominal_regime_shock: np.ndarray
    nk_natural_rate: np.ndarray
    nk_cost_push: np.ndarray
    nk_policy_shock: np.ndarray


@dataclass(frozen=True)
class ModelResult:
    label: str
    t: np.ndarray
    ngdp_gap: np.ndarray
    output_gap: np.ndarray
    output: np.ndarray
    price_level: np.ndarray
    inflation: np.ndarray
    velocity: np.ndarray | None
    money: np.ndarray | None
    nominal_rate: np.ndarray


def ar_shock(periods: int, start: int, size: float, rho: float) -> np.ndarray:
    """AR(1) impulse starting at `start`, in log-deviation units."""
    path = np.zeros(periods, dtype=float)
    if not 0 <= start < periods:
        return path
    path[start] = size
    for t in range(start + 1, periods):
        path[t] = rho * path[t - 1]
    return path


def build_scenarios(params: Params) -> list[Scenario]:
    """Create shock paths with rough cross-model analogues."""
    t = params.periods
    s = params.shock_date
    zero = np.zeros(t, dtype=float)

    def scenario(
        name: str,
        title: str,
        *,
        potential: np.ndarray | None = None,
        income_news: np.ndarray | None = None,
        velocity_shock: np.ndarray | None = None,
        nominal_regime_shock: np.ndarray | None = None,
        nk_natural_rate: np.ndarray | None = None,
        nk_cost_push: np.ndarray | None = None,
        nk_policy_shock: np.ndarray | None = None,
    ) -> Scenario:
        return Scenario(
            name=name,
            title=title,
            potential=zero.copy() if potential is None else potential,
            income_news=zero.copy() if income_news is None else income_news,
            velocity_shock=zero.copy() if velocity_shock is None else velocity_shock,
            nominal_regime_shock=zero.copy()
            if nominal_regime_shock is None
            else nominal_regime_shock,
            nk_natural_rate=zero.copy() if nk_natural_rate is None else nk_natural_rate,
            nk_cost_push=zero.copy() if nk_cost_push is None else nk_cost_push,
            nk_policy_shock=zero.copy() if nk_policy_shock is None else nk_policy_shock,
        )

    return [
        scenario(
            "expected_income_slump",
            "Negative Expected-Income Shock",
            income_news=ar_shock(t, s, -0.030, 0.82),
            nk_natural_rate=ar_shock(t, s, -0.018, 0.82),
        ),
        scenario(
            "velocity_crash",
            "Velocity / Money-Demand Shock",
            velocity_shock=ar_shock(t, s, -0.040, 0.70),
            nk_natural_rate=ar_shock(t, s, -0.022, 0.70),
        ),
        scenario(
            "negative_supply",
            "Negative Real Supply Shock",
            potential=ar_shock(t, s, -0.030, 0.90),
            nk_cost_push=ar_shock(t, s, 0.014, 0.75),
        ),
        scenario(
            "monetary_contraction",
            "Contractionary Nominal-Regime Shock",
            nominal_regime_shock=ar_shock(t, s, -0.040, 0.80),
            nk_policy_shock=ar_shock(t, s, 0.024, 0.65),
        ),
    ]


def expected_human_wealth(real_income: np.ndarray, discount: float) -> np.ndarray:
    """Discounted expected future real income, normalized to income units.

    In these deterministic impulse responses, rational expectations means the
    whole future shock path is known after the shock arrives.
    """
    periods = len(real_income)
    wealth = np.zeros(periods, dtype=float)
    for t in range(periods):
        weights = discount ** np.arange(periods - t)
        denom = float(np.sum(weights))
        wealth[t] = float(np.dot(weights, real_income[t:]) / denom)
    return wealth


def simulate_market_monetarist(
    scenario: Scenario,
    params: Params,
    *,
    label: str,
    ngdp_regime_offset: float,
) -> ModelResult:
    """Simulate the market monetarist candidate closure."""
    periods = params.periods
    time = np.arange(periods)

    real_income = scenario.potential + scenario.income_news
    human_wealth = expected_human_wealth(real_income, params.human_wealth_discount)
    human_wealth[: params.shock_date] = 0.0

    velocity_pressure = (
        params.velocity_from_human_wealth * human_wealth
        + params.velocity_from_money_demand * scenario.velocity_shock
    )

    # The central bank offsets velocity pressure by changing money. A value of
    # 1.0 is a fully credible NGDP-level regime; 0.0 is passive money.
    ngdp_gap = scenario.nominal_regime_shock + (1.0 - ngdp_regime_offset) * velocity_pressure
    velocity = velocity_pressure
    money = ngdp_gap - velocity

    output_gap = np.zeros(periods, dtype=float)
    for t in range(periods):
        lagged_gap = output_gap[t - 1] if t > 0 else 0.0
        output_gap[t] = (
            params.output_gap_persistence * lagged_gap
            + params.sras_lambda * ngdp_gap[t]
        )

    output = scenario.potential + output_gap
    price_level = ngdp_gap - output
    inflation = np.diff(np.r_[0.0, price_level])

    expected_inflation = np.r_[inflation[1:], 0.0]
    expected_consumption_growth = np.r_[np.diff(output), 0.0]
    raw_nominal_rate = (
        params.real_rate_sensitivity * expected_consumption_growth
        + expected_inflation
    )
    nominal_rate = np.zeros(periods, dtype=float)
    for t in range(periods):
        lagged_rate = nominal_rate[t - 1] if t > 0 else 0.0
        nominal_rate[t] = (
            params.nominal_rate_smoothing * lagged_rate
            + (1.0 - params.nominal_rate_smoothing) * raw_nominal_rate[t]
        )

    return ModelResult(
        label=label,
        t=time,
        ngdp_gap=ngdp_gap,
        output_gap=output_gap,
        output=output,
        price_level=price_level,
        inflation=inflation,
        velocity=velocity,
        money=money,
        nominal_rate=nominal_rate,
    )


def simulate_new_keynesian(scenario: Scenario, params: Params) -> ModelResult:
    """Solve a standard linear New Keynesian model by backward induction."""
    periods = params.periods
    time = np.arange(periods)
    output_gap = np.zeros(periods + 1, dtype=float)
    inflation = np.zeros(periods + 1, dtype=float)

    beta = params.nk_beta
    sigma = params.nk_sigma
    kappa = params.nk_kappa
    phi_pi = params.nk_phi_pi
    phi_y = params.nk_phi_y

    lhs = np.array(
        [
            [1.0 + phi_y / sigma, phi_pi / sigma],
            [-kappa, 1.0],
        ],
        dtype=float,
    )

    # The shock is unanticipated until `shock_date`. From that date forward,
    # agents know the deterministic shock path and solve under perfect foresight.
    for t in range(periods - 1, params.shock_date - 1, -1):
        rhs = np.array(
            [
                output_gap[t + 1]
                + inflation[t + 1] / sigma
                + scenario.nk_natural_rate[t] / sigma
                - scenario.nk_policy_shock[t] / sigma,
                beta * inflation[t + 1] + scenario.nk_cost_push[t],
            ],
            dtype=float,
        )
        output_gap[t], inflation[t] = np.linalg.solve(lhs, rhs)

    output_gap = output_gap[:periods]
    inflation = inflation[:periods]
    price_level = np.cumsum(inflation)
    output = scenario.potential + output_gap
    ngdp_gap = price_level + output
    nominal_rate = (
        phi_pi * inflation
        + phi_y * output_gap
        + scenario.nk_policy_shock
    )

    return ModelResult(
        label="New Keynesian Taylor rule",
        t=time,
        ngdp_gap=ngdp_gap,
        output_gap=output_gap,
        output=output,
        price_level=price_level,
        inflation=inflation,
        velocity=None,
        money=None,
        nominal_rate=nominal_rate,
    )


def simulate_new_keynesian_rate_peg(params: Params, step: float = 0.010) -> ModelResult:
    """Simulate the NK model under a permanent higher nominal-rate peg.

    This is the simple neo-Fisherian/Cochrane-style diagnostic. If the nominal
    interest rate is treated as the permanent nominal regime, the terminal
    Fisher condition implies higher long-run inflation rather than a permanent
    contraction. That is the point of the plot: the meaning of a rate increase
    depends on the monetary/fiscal regime closing the model.
    """
    periods = params.periods
    time = np.arange(periods)
    nominal_rate = np.zeros(periods, dtype=float)
    nominal_rate[params.shock_date :] = step

    output_gap = np.zeros(periods + 1, dtype=float)
    inflation = np.zeros(periods + 1, dtype=float)

    steady_inflation = step
    steady_output_gap = (1.0 - params.nk_beta) * steady_inflation / params.nk_kappa
    output_gap[periods] = steady_output_gap
    inflation[periods] = steady_inflation

    for t in range(periods - 1, params.shock_date - 1, -1):
        output_gap[t] = (
            output_gap[t + 1]
            - (nominal_rate[t] - inflation[t + 1]) / params.nk_sigma
        )
        inflation[t] = params.nk_beta * inflation[t + 1] + params.nk_kappa * output_gap[t]

    output_gap = output_gap[:periods]
    inflation = inflation[:periods]
    price_level = np.cumsum(inflation)
    output = output_gap.copy()
    ngdp_gap = price_level + output

    return ModelResult(
        label="NK rate peg / Fisher terminal",
        t=time,
        ngdp_gap=ngdp_gap,
        output_gap=output_gap,
        output=output,
        price_level=price_level,
        inflation=inflation,
        velocity=None,
        money=None,
        nominal_rate=nominal_rate,
    )


def percent(path: np.ndarray) -> np.ndarray:
    return 100.0 * path


def style_axis(ax: plt.Axes, title: str, ylabel: str) -> None:
    ax.axhline(0.0, color=COLOR_ZERO, linewidth=0.8, alpha=0.65)
    ax.set_title(title, pad=8)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_scenario(
    scenario: Scenario,
    mm: ModelResult,
    passive: ModelResult,
    nk: ModelResult,
    output_dir: Path,
) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(12.0, 9.0), sharex=True)
    fig.suptitle(scenario.title, fontsize=16, fontweight="bold", y=0.98)

    series = [
        (mm, COLOR_MM, 2.5, "-"),
        (passive, COLOR_PASSIVE, 2.0, "--"),
        (nk, COLOR_NK, 2.2, "-"),
    ]

    ax = axes[0, 0]
    style_axis(ax, "Nominal Expenditure / NGDP Gap", "percent")
    for result, color, lw, ls in series:
        ax.plot(result.t, percent(result.ngdp_gap), color=color, linewidth=lw, linestyle=ls, label=result.label)
    ax.legend(frameon=False, fontsize=9, loc="best")

    ax = axes[0, 1]
    style_axis(ax, "Real Output vs Potential", "percent")
    ax.plot(
        mm.t,
        percent(scenario.potential),
        color=COLOR_ZERO,
        linewidth=1.8,
        linestyle=":",
        label="Potential output",
    )
    for result, color, lw, ls in series:
        ax.plot(result.t, percent(result.output), color=color, linewidth=lw, linestyle=ls, label=result.label)
    ax.legend(frameon=False, fontsize=8.5, loc="best")

    ax = axes[1, 0]
    style_axis(ax, "Inflation", "percentage points")
    for result, color, lw, ls in series:
        ax.plot(result.t, percent(result.inflation), color=color, linewidth=lw, linestyle=ls)

    ax = axes[1, 1]
    style_axis(ax, "Price Level", "percent")
    for result, color, lw, ls in series:
        ax.plot(result.t, percent(result.price_level), color=color, linewidth=lw, linestyle=ls)

    ax = axes[2, 0]
    style_axis(ax, "MM Velocity And Money", "percent")
    ax.plot(mm.t, percent(mm.velocity), color="#16a34a", linewidth=2.3, label="Velocity pressure")
    ax.plot(mm.t, percent(mm.money), color="#7c3aed", linewidth=2.3, label="Implied money")
    ax.plot(passive.t, percent(passive.money), color=COLOR_PASSIVE, linewidth=1.8, linestyle="--", label="Passive money")
    ax.legend(frameon=False, fontsize=9, loc="best")

    ax = axes[2, 1]
    style_axis(ax, "Nominal Interest Rate", "percentage points")
    ax.plot(mm.t, percent(mm.nominal_rate), color=COLOR_MM, linewidth=2.5, label=mm.label)
    ax.plot(nk.t, percent(nk.nominal_rate), color=COLOR_NK, linewidth=2.2, label=nk.label)
    ax.legend(frameon=False, fontsize=9, loc="best")

    for ax in axes[-1, :]:
        ax.set_xlabel("period")

    fig.tight_layout()
    fig.savefig(output_dir / f"{scenario.name}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_interest_rate_source_test(params: Params, output_dir: Path) -> None:
    """Show that the sign of an interest-rate move is not a stance measure."""
    zero = np.zeros(params.periods, dtype=float)

    def scenario(
        name: str,
        title: str,
        *,
        nominal_regime_shock: np.ndarray | None = None,
        nk_policy_shock: np.ndarray | None = None,
    ) -> Scenario:
        return Scenario(
            name=name,
            title=title,
            potential=zero.copy(),
            income_news=zero.copy(),
            velocity_shock=zero.copy(),
            nominal_regime_shock=zero.copy()
            if nominal_regime_shock is None
            else nominal_regime_shock,
            nk_natural_rate=zero.copy(),
            nk_cost_push=zero.copy(),
            nk_policy_shock=zero.copy() if nk_policy_shock is None else nk_policy_shock,
        )

    mm_easy_scenario = scenario(
        "mm_easy_regime",
        "MM Easy NGDP Regime",
        nominal_regime_shock=ar_shock(params.periods, params.shock_date, 0.040, 0.80),
    )
    mm_tight_scenario = scenario(
        "mm_tight_regime",
        "MM Tight NGDP Regime",
        nominal_regime_shock=ar_shock(params.periods, params.shock_date, -0.040, 0.80),
    )
    nk_hike_scenario = scenario(
        "nk_policy_rate_hike",
        "NK Policy-Rate Hike",
        nk_policy_shock=ar_shock(params.periods, params.shock_date, 0.024, 0.65),
    )

    mm_easy = simulate_market_monetarist(
        mm_easy_scenario,
        params,
        label="MM: easy NGDP regime",
        ngdp_regime_offset=params.ngdp_regime_offset,
    )
    mm_tight = simulate_market_monetarist(
        mm_tight_scenario,
        params,
        label="MM: tight NGDP regime",
        ngdp_regime_offset=params.ngdp_regime_offset,
    )
    nk_hike = simulate_new_keynesian(nk_hike_scenario, params)

    experiments = [
        (
            "MM: higher rates with faster growth",
            mm_easy,
            COLOR_MM,
            "easy nominal regime",
        ),
        (
            "MM: lower rates with weaker growth",
            mm_tight,
            COLOR_MM,
            "tight nominal regime",
        ),
        (
            "NK: policy-rate hike is contractionary",
            nk_hike,
            COLOR_NK,
            "Taylor-rule shock",
        ),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.1), sharex=True)
    fig.suptitle("Interest Rates Are Not the Monetary Stance", fontsize=15, fontweight="bold")

    for ax, (title, result, color, label) in zip(axes, experiments, strict=True):
        real_growth = np.diff(np.r_[0.0, result.output])
        style_axis(ax, title, "percentage points")
        ax.plot(
            result.t,
            percent(result.nominal_rate),
            color=color,
            linewidth=2.4,
            label="nominal interest rate",
        )
        ax.plot(
            result.t,
            percent(real_growth),
            color="#16a34a",
            linewidth=2.2,
            linestyle="--",
            label="real output growth",
        )
        ax.set_xlabel("period")
        ax.text(
            0.02,
            0.93,
            label,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9,
            color="#374151",
        )
        ax.legend(frameon=False, fontsize=8.5, loc="lower right")

    fig.tight_layout()
    fig.savefig(output_dir / "interest_rate_source_test.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_classic_nk_diagnostics(params: Params, output_dir: Path) -> None:
    """Plot textbook NK IRFs plus the rate-peg diagnostic."""
    zero = np.zeros(params.periods, dtype=float)

    def scenario(
        name: str,
        title: str,
        *,
        nk_natural_rate: np.ndarray | None = None,
        nk_cost_push: np.ndarray | None = None,
        nk_policy_shock: np.ndarray | None = None,
    ) -> Scenario:
        return Scenario(
            name=name,
            title=title,
            potential=zero.copy(),
            income_news=zero.copy(),
            velocity_shock=zero.copy(),
            nominal_regime_shock=zero.copy(),
            nk_natural_rate=zero.copy() if nk_natural_rate is None else nk_natural_rate,
            nk_cost_push=zero.copy() if nk_cost_push is None else nk_cost_push,
            nk_policy_shock=zero.copy() if nk_policy_shock is None else nk_policy_shock,
        )

    natural_rate = simulate_new_keynesian(
        scenario(
            "nk_natural_rate_slump",
            "Natural-rate shock",
            nk_natural_rate=ar_shock(params.periods, params.shock_date, -0.018, 0.82),
        ),
        params,
    )
    policy_hike = simulate_new_keynesian(
        scenario(
            "nk_policy_hike",
            "Policy-rate shock",
            nk_policy_shock=ar_shock(params.periods, params.shock_date, 0.024, 0.65),
        ),
        params,
    )
    cost_push = simulate_new_keynesian(
        scenario(
            "nk_cost_push",
            "Cost-push shock",
            nk_cost_push=ar_shock(params.periods, params.shock_date, 0.014, 0.75),
        ),
        params,
    )
    rate_peg = simulate_new_keynesian_rate_peg(params)

    columns = [
        ("Negative natural-rate shock", natural_rate, "Demand shock under Taylor rule"),
        ("Policy-rate hike", policy_hike, "Textbook monetary tightening"),
        ("Cost-push shock", cost_push, "Inflation-output tradeoff"),
        ("Permanent higher rate peg", rate_peg, "Fisher terminal condition"),
    ]
    rows = [
        ("Output gap", "percent", lambda result: result.output_gap, COLOR_MM),
        ("Inflation", "percentage points", lambda result: result.inflation, COLOR_NK),
        ("Nominal interest rate", "percentage points", lambda result: result.nominal_rate, COLOR_ZERO),
    ]

    fig, axes = plt.subplots(3, 4, figsize=(15.0, 8.2), sharex=True)
    fig.suptitle("Classic New Keynesian Diagnostics", fontsize=16, fontweight="bold", y=0.99)

    for col, (title, result, note) in enumerate(columns):
        for row, (label, ylabel, getter, color) in enumerate(rows):
            ax = axes[row, col]
            style_axis(ax, "", ylabel if col == 0 else "")
            ax.plot(result.t, percent(getter(result)), color=color, linewidth=2.4)
            if row == 0:
                ax.set_title(title, pad=8)
                ax.text(
                    0.02,
                    0.92,
                    note,
                    transform=ax.transAxes,
                    ha="left",
                    va="top",
                    fontsize=8.5,
                    color="#374151",
                )
            if col > 0:
                ax.set_ylabel("")
            if row == len(rows) - 1:
                ax.set_xlabel("period")

    fig.tight_layout()
    fig.savefig(output_dir / "nk_classic_diagnostics.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def summary_row(scenario: Scenario, result: ModelResult) -> dict[str, str | float]:
    loss = float(
        np.sum(result.output_gap**2)
        + np.sum(result.inflation**2)
        + 0.25 * np.sum(result.ngdp_gap**2)
    )
    return {
        "scenario": scenario.name,
        "model": result.label,
        "min_output_gap_pct": float(np.min(percent(result.output_gap))),
        "max_output_gap_pct": float(np.max(percent(result.output_gap))),
        "min_output_pct": float(np.min(percent(result.output))),
        "min_potential_pct": float(np.min(percent(scenario.potential))),
        "max_output_growth_pct": float(np.max(percent(np.diff(np.r_[0.0, result.output])))),
        "cum_abs_ngdp_gap_pct": float(np.sum(np.abs(percent(result.ngdp_gap)))),
        "max_abs_inflation_pp": float(np.max(np.abs(percent(result.inflation)))),
        "min_nominal_rate_pp": float(np.min(percent(result.nominal_rate))),
        "max_nominal_rate_pp": float(np.max(percent(result.nominal_rate))),
        "quadratic_loss": loss,
    }


def write_summary(rows: list[dict[str, str | float]], output_path: Path) -> None:
    fieldnames = [
        "scenario",
        "model",
        "min_output_gap_pct",
        "max_output_gap_pct",
        "min_output_pct",
        "min_potential_pct",
        "max_output_growth_pct",
        "cum_abs_ngdp_gap_pct",
        "max_abs_inflation_pp",
        "min_nominal_rate_pp",
        "max_nominal_rate_pp",
        "quadratic_loss",
    ]
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, str | float]]) -> None:
    print("\nStabilization summary")
    print("-" * 79)
    print(
        f"{'scenario':<28} {'model':<28} {'loss':>10} "
        f"{'min ygap':>9} {'min y':>8} {'max |pi|':>9}"
    )
    for row in rows:
        print(
            f"{str(row['scenario']):<28} "
            f"{str(row['model']):<28} "
            f"{float(row['quadratic_loss']):>10.5f} "
            f"{float(row['min_output_gap_pct']):>9.2f} "
            f"{float(row['min_output_pct']):>8.2f} "
            f"{float(row['max_abs_inflation_pp']):>9.2f}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--periods", type=int, default=Params.periods)
    parser.add_argument("--shock-date", type=int, default=Params.shock_date)
    parser.add_argument(
        "--scenario",
        choices=[
            "all",
            "expected_income_slump",
            "velocity_crash",
            "negative_supply",
            "monetary_contraction",
        ],
        default="all",
    )
    parser.add_argument(
        "--ngdp-regime-offset",
        type=float,
        default=Params.ngdp_regime_offset,
        help="Share of velocity pressure offset by the MM nominal regime.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    params = Params(
        periods=args.periods,
        shock_date=args.shock_date,
        ngdp_regime_offset=args.ngdp_regime_offset,
    )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    scenarios = build_scenarios(params)
    if args.scenario != "all":
        scenarios = [scenario for scenario in scenarios if scenario.name == args.scenario]

    rows: list[dict[str, str | float]] = []
    for scenario in scenarios:
        mm = simulate_market_monetarist(
            scenario,
            params,
            label="Market monetarist NGDP regime",
            ngdp_regime_offset=params.ngdp_regime_offset,
        )
        passive = simulate_market_monetarist(
            scenario,
            params,
            label="Passive money",
            ngdp_regime_offset=0.0,
        )
        nk = simulate_new_keynesian(scenario, params)

        plot_scenario(scenario, mm, passive, nk, FIGURES_DIR)
        rows.extend(
            [
                summary_row(scenario, mm),
                summary_row(scenario, passive),
                summary_row(scenario, nk),
            ]
        )

    plot_interest_rate_source_test(params, FIGURES_DIR)
    plot_classic_nk_diagnostics(params, FIGURES_DIR)

    summary_path = DATA_DIR / "workhorse_summary.csv"
    write_summary(rows, summary_path)
    print_summary(rows)
    print(f"\nSaved figures to {FIGURES_DIR}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()
