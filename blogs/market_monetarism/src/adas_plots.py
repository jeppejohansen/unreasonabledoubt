"""Generate AD-AS diagrams for the market monetarism draft."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

Y_MIN = 55
Y_MAX = 145
P_MIN = 55
P_MAX = 125
Y_POTENTIAL = 100

COLOR_AD = "#2563eb"
COLOR_LRAS = "#262626"
COLOR_NEW = "#16a34a"
COLOR_EQUILIBRIUM = "#111827"
COLOR_FLEXIBLE = "#6b7280"
COLOR_GAP = "#c2410c"


def ad(y: np.ndarray | float, intercept: float = 150) -> np.ndarray | float:
    return intercept - 0.55 * y


def sticky_as(y: np.ndarray | float) -> np.ndarray | float:
    return 95 + 0.45 * (y - Y_POTENTIAL)


def equilibrium(y_eq: float = Y_POTENTIAL, ad_intercept: float = 150) -> tuple[float, float]:
    p_eq = ad(y_eq, ad_intercept)
    return y_eq, p_eq


def sticky_equilibrium(ad_intercept: float = 150) -> tuple[float, float]:
    y_eq = (ad_intercept - 50) / (0.55 + 0.45)
    p_eq = sticky_as(y_eq)
    return y_eq, p_eq


def style_axes(ax: plt.Axes, title: str) -> None:
    ax.set_xlim(Y_MIN, Y_MAX)
    ax.set_ylim(P_MIN, P_MAX)
    ax.set_xlabel("Real output (Y)")
    ax.set_ylabel("Price level (P)")
    ax.set_title(title, pad=12)
    ax.grid(True, alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


def plot_lras(
    ax: plt.Axes,
    y_potential: float = Y_POTENTIAL,
    label: str = "LRAS\n(Y*)",
    color: str = COLOR_LRAS,
    alpha: float = 1.0,
) -> None:
    ax.axvline(y_potential, color=color, linewidth=2.2, alpha=alpha)
    ax.text(y_potential + 1.8, P_MAX - 5, label, color=color, va="top", alpha=alpha)


def mark_equilibrium(ax: plt.Axes, y_eq: float, p_eq: float, label: str) -> None:
    ax.scatter([y_eq], [p_eq], s=36, color=COLOR_EQUILIBRIUM, zorder=5)
    ax.plot([y_eq, y_eq], [P_MIN, p_eq], color=COLOR_EQUILIBRIUM, linewidth=1, linestyle=":")
    ax.plot([Y_MIN, y_eq], [p_eq, p_eq], color=COLOR_EQUILIBRIUM, linewidth=1, linestyle=":")
    ax.text(y_eq + 2, p_eq + 2, label, color=COLOR_EQUILIBRIUM, fontweight="bold")


def save(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_baseline() -> None:
    y = np.linspace(Y_MIN, Y_MAX, 400)
    y_eq, p_eq = equilibrium()

    fig, ax = plt.subplots(figsize=(7, 4.6))
    style_axes(ax, "Long-Run AD-AS")

    ax.plot(y, ad(y), color=COLOR_AD, linewidth=2.6)
    plot_lras(ax)

    ax.text(127, ad(127) + 2, "AD", color=COLOR_AD, fontweight="bold")
    mark_equilibrium(ax, y_eq, p_eq, "E0")

    save(fig, "ad_as_baseline.png")


def plot_shocks() -> None:
    y = np.linspace(Y_MIN, Y_MAX, 400)
    y0, p0 = equilibrium()
    y_demand, p_demand = equilibrium(ad_intercept=165)
    y_supply, p_supply = equilibrium(y_eq=115)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), sharey=True)

    demand_ax, supply_ax = axes
    style_axes(demand_ax, "Positive Demand Shock")
    demand_ax.plot(y, ad(y), color=COLOR_AD, linewidth=2.4, alpha=0.45)
    demand_ax.plot(y, ad(y, 165), color=COLOR_NEW, linewidth=2.8)
    plot_lras(demand_ax)
    demand_ax.text(128, ad(128) + 2, "AD0", color=COLOR_AD, fontweight="bold", alpha=0.75)
    demand_ax.text(116, ad(116, 165) + 3, "AD1", color=COLOR_NEW, fontweight="bold")
    demand_ax.annotate(
        "",
        xy=(105, ad(105, 165)),
        xytext=(105, ad(105)),
        arrowprops={"arrowstyle": "->", "color": COLOR_NEW, "linewidth": 2},
    )
    mark_equilibrium(demand_ax, y0, p0, "E0")
    mark_equilibrium(demand_ax, y_demand, p_demand, "E1")

    style_axes(supply_ax, "Positive Long-Run Supply Shock")
    supply_ax.set_ylabel("")
    supply_ax.plot(y, ad(y), color=COLOR_AD, linewidth=2.6)
    plot_lras(supply_ax, y_potential=Y_POTENTIAL, label="LRAS0\n(Y0*)", color=COLOR_LRAS, alpha=0.45)
    plot_lras(supply_ax, y_potential=y_supply, label="LRAS1\n(Y1*)", color=COLOR_NEW)
    supply_ax.text(127, ad(127) + 2, "AD", color=COLOR_AD, fontweight="bold")
    supply_ax.annotate(
        "",
        xy=(y_supply, 72),
        xytext=(Y_POTENTIAL, 72),
        arrowprops={"arrowstyle": "->", "color": COLOR_NEW, "linewidth": 2},
    )
    mark_equilibrium(supply_ax, y0, p0, "E0")
    mark_equilibrium(supply_ax, y_supply, p_supply, "E1")

    save(fig, "ad_as_shocks.png")


def plot_sticky_price_cross() -> None:
    spending_surprise = np.linspace(-30, 30, 400)
    flexible_prices = spending_surprise
    sticky_prices = 0.42 * spending_surprise

    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.set_xlim(-32, 32)
    ax.set_ylim(-32, 32)
    ax.set_xlabel(r"Nominal spending surprise: $MV - E[MV]$")
    ax.set_ylabel(r"Price adjustment: $P - P_{fixed}$")
    ax.set_title("Sticky-Price Cross", pad=12)
    ax.grid(True, alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axhline(0, color=COLOR_EQUILIBRIUM, linewidth=1)
    ax.axvline(0, color=COLOR_EQUILIBRIUM, linewidth=1)

    ax.plot(
        spending_surprise,
        flexible_prices,
        color=COLOR_FLEXIBLE,
        linewidth=2.4,
        linestyle="--",
    )
    ax.plot(spending_surprise, sticky_prices, color=COLOR_NEW, linewidth=2.8)

    ax.text(15, 19, "Flexible prices\n45-degree line", color=COLOR_FLEXIBLE)
    ax.text(12, 1.5, "Sticky prices", color=COLOR_NEW, fontweight="bold")
    ax.text(1.4, -3.7, "Expectations met", color=COLOR_EQUILIBRIUM)

    x_positive = 20
    y_flexible_positive = x_positive
    y_sticky_positive = 0.42 * x_positive
    ax.annotate(
        "",
        xy=(x_positive, y_flexible_positive),
        xytext=(x_positive, y_sticky_positive),
        arrowprops={"arrowstyle": "<->", "color": COLOR_EQUILIBRIUM, "linewidth": 1.7},
    )
    ax.text(
        x_positive + 2,
        (y_flexible_positive + y_sticky_positive) / 2,
        "Real output\nexpands",
        va="center",
        color=COLOR_EQUILIBRIUM,
    )

    x_negative = -20
    y_flexible_negative = x_negative
    y_sticky_negative = 0.42 * x_negative
    ax.annotate(
        "",
        xy=(x_negative, y_sticky_negative),
        xytext=(x_negative, y_flexible_negative),
        arrowprops={"arrowstyle": "<->", "color": COLOR_EQUILIBRIUM, "linewidth": 1.7},
    )
    ax.text(
        x_negative - 2,
        (y_flexible_negative + y_sticky_negative) / 2,
        "Real output\ncontracts",
        va="center",
        ha="right",
        color=COLOR_EQUILIBRIUM,
    )

    save(fig, "sticky_price_cross.png")


def plot_sticky_price_ad_as() -> None:
    y = np.linspace(Y_MIN, Y_MAX, 400)
    y0, p0 = sticky_equilibrium()
    y1, p1 = sticky_equilibrium(ad_intercept=165)

    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    style_axes(ax, "AD-AS With Sticky Prices")

    ax.plot(y, ad(y), color=COLOR_AD, linewidth=2.4, alpha=0.45)
    ax.plot(y, ad(y, 165), color=COLOR_NEW, linewidth=2.8)
    ax.plot(y, sticky_as(y), color="#c2410c", linewidth=2.8)
    plot_lras(ax, color=COLOR_FLEXIBLE, alpha=0.65)

    ax.text(128, ad(128) + 2, "AD0", color=COLOR_AD, fontweight="bold", alpha=0.75)
    ax.text(128, ad(128, 165) - 8, "AD1", color=COLOR_NEW, fontweight="bold")
    ax.text(126, sticky_as(126) + 2, "Sticky-price AS", color="#c2410c", fontweight="bold")

    ax.annotate(
        "",
        xy=(106, ad(106, 165)),
        xytext=(106, ad(106)),
        arrowprops={"arrowstyle": "->", "color": COLOR_NEW, "linewidth": 2},
    )
    mark_equilibrium(ax, y0, p0, "E0")
    mark_equilibrium(ax, y1, p1, "E1")
    ax.annotate(
        "",
        xy=(y1, P_MIN + 6),
        xytext=(y0, P_MIN + 6),
        arrowprops={"arrowstyle": "->", "color": COLOR_EQUILIBRIUM, "linewidth": 1.7},
    )
    ax.text((y0 + y1) / 2, P_MIN + 8, "Y rises", ha="center", color=COLOR_EQUILIBRIUM)

    save(fig, "sticky_price_ad_as.png")


def plot_interest_rate_single_schedule() -> None:
    rates = np.linspace(2.0, 6.2, 400)
    target = 100.0
    f0 = 112.5 - 2.5 * rates
    i0 = 5.0
    point_a = (i0, target)

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.set_xlim(1.9, 6.3)
    ax.set_ylim(91.5, 108.5)
    ax.set_xlabel(r"Policy interest rate: $i_t$")
    ax.set_ylabel(r"Expected NGDP: $E_t[NGDP_T]$")
    ax.set_title("The NGDP Forecast Schedule", pad=12)
    ax.grid(True, alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.axhline(target, color=COLOR_EQUILIBRIUM, linewidth=2.2)
    ax.text(6.0, target + 0.45, r"$NGDP_T^*$", color=COLOR_EQUILIBRIUM, ha="right")

    ax.plot(rates, f0, color=COLOR_AD, linewidth=2.8)
    ax.text(
        5.18,
        98.4,
        r"$F_0:\ E_t[NGDP_T]=A_0-bi_t$",
        color=COLOR_AD,
        fontweight="bold",
    )

    ax.plot([i0, i0], [91.5, target], color=COLOR_EQUILIBRIUM, linewidth=1, linestyle=":")
    ax.text(i0, 91.95, r"$i_0$", ha="center", va="bottom", color=COLOR_EQUILIBRIUM)
    ax.scatter([point_a[0]], [point_a[1]], s=48, color=COLOR_EQUILIBRIUM, zorder=5)
    ax.text(point_a[0] + 0.08, point_a[1] + 0.65, "A", color=COLOR_EQUILIBRIUM, fontweight="bold")

    save(fig, "interest_rate_ngdp_single_schedule.png")


def plot_interest_rate_ngdp_forecast() -> None:
    rates = np.linspace(2.0, 6.2, 400)
    target = 100.0
    f0 = 112.5 - 2.5 * rates
    f1 = 107.5 - 2.5 * rates

    i0 = 5.0
    i1 = 3.0
    i2 = 4.0
    point_a = (i0, target)
    point_b = (i2, 107.5 - 2.5 * i2)
    point_c = (i1, target)

    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.set_xlim(1.9, 6.3)
    ax.set_ylim(91.5, 108.5)
    ax.set_xlabel(r"Policy interest rate: $i_t$")
    ax.set_ylabel(r"Expected NGDP: $E_t[NGDP_T]$")
    ax.set_title("Lower Rates Can Still Be Tight Money", pad=12)
    ax.grid(True, alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.axhline(target, color=COLOR_EQUILIBRIUM, linewidth=2.2)
    ax.text(6.0, target + 0.45, r"$NGDP_T^*$", color=COLOR_EQUILIBRIUM, ha="right")

    ax.plot(rates, f0, color=COLOR_AD, linewidth=2.7, alpha=0.45)
    ax.plot(rates, f1, color=COLOR_NEW, linewidth=2.9)
    ax.text(5.65, 98.6, r"$F_0$", color=COLOR_AD, fontweight="bold", alpha=0.8)
    ax.text(5.1, 94.8, r"$F_1$", color=COLOR_NEW, fontweight="bold")

    ax.annotate(
        "",
        xy=(3.8, 107.5 - 2.5 * 3.8),
        xytext=(3.8, 112.5 - 2.5 * 3.8),
        arrowprops={"arrowstyle": "->", "color": COLOR_NEW, "linewidth": 2},
    )

    for rate, label in [(i1, r"$i_1$"), (i2, r"$i_2$"), (i0, r"$i_0$")]:
        ax.plot([rate, rate], [91.5, 100], color=COLOR_EQUILIBRIUM, linewidth=1, linestyle=":")
        ax.text(rate, 91.95, label, ha="center", va="bottom", color=COLOR_EQUILIBRIUM)

    for (x, y), label, offset in [
        (point_a, "A", (0.08, 0.65)),
        (point_b, "B", (0.08, -1.0)),
        (point_c, "C", (-0.24, 0.65)),
    ]:
        ax.scatter([x], [y], s=44, color=COLOR_EQUILIBRIUM, zorder=5)
        ax.text(
            x + offset[0],
            y + offset[1],
            label,
            color=COLOR_EQUILIBRIUM,
            fontweight="bold",
        )

    ax.annotate(
        "",
        xy=(i2, 92.8),
        xytext=(i0, 92.8),
        arrowprops={"arrowstyle": "->", "color": COLOR_EQUILIBRIUM, "linewidth": 1.8},
    )
    ax.text((i0 + i2) / 2, 93.25, "rate cut", ha="center")

    ax.annotate(
        "",
        xy=(i2, target),
        xytext=point_b,
        arrowprops={"arrowstyle": "<->", "color": "#c2410c", "linewidth": 1.8},
    )
    ax.text(i2 + 0.12, (target + point_b[1]) / 2, "forecast gap", va="center", color="#c2410c")

    ax.text(2.35, 92.5, r"$i_1<i_2<i_0$", color=COLOR_EQUILIBRIUM)

    save(fig, "interest_rate_ngdp_forecast.png")


def plot_ngdp_level_targeting() -> None:
    time = np.arange(0, 8)
    target_growth = 0.04
    pre_shock_target = target_growth * time

    level_target_actual = np.array([0.00, 0.04, 0.08, 0.06, 0.12, 0.18, 0.24, 0.28])
    non_level_actual = np.array([0.00, 0.04, 0.08, 0.06, 0.10, 0.14, 0.18, 0.22])
    reset_target = np.array([np.nan, np.nan, np.nan, 0.06, 0.10, 0.14, 0.18, 0.22])

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8), sharey=True)

    for ax, title in zip(
        axes,
        [
            "NGDP Level Targeting",
            "Non-Level NGDP Growth Target",
        ],
    ):
        ax.set_xlim(-0.1, 7.1)
        ax.set_ylim(-0.01, 0.31)
        ax.set_xlabel("Time")
        ax.set_title(title, pad=12)
        ax.grid(True, alpha=0.18)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.plot(
            time,
            pre_shock_target,
            color=COLOR_EQUILIBRIUM,
            linewidth=2.2,
            linestyle="--",
        )
        ax.axvline(3, color=COLOR_FLEXIBLE, linewidth=1.4, linestyle=":", alpha=0.85)
        ax.text(3.08, 0.015, "miss", color=COLOR_FLEXIBLE)

    axes[0].set_ylabel("Log nominal GDP")

    axes[0].plot(time, level_target_actual, color=COLOR_AD, linewidth=3.0)
    axes[0].fill_between(
        time[3:6],
        level_target_actual[3:6],
        pre_shock_target[3:6],
        color=COLOR_GAP,
        alpha=0.16,
    )
    axes[0].annotate(
        "make-up growth",
        xy=(5, level_target_actual[5]),
        xytext=(4.05, 0.235),
        color=COLOR_NEW,
        arrowprops={"arrowstyle": "->", "color": COLOR_NEW, "linewidth": 1.8},
    )
    axes[0].text(5.15, pre_shock_target[5] + 0.008, "original path", color=COLOR_EQUILIBRIUM)
    axes[0].text(5.7, level_target_actual[5] - 0.018, "actual", color=COLOR_AD, fontweight="bold")

    axes[1].plot(time, non_level_actual, color=COLOR_AD, linewidth=3.0)
    axes[1].plot(time, reset_target, color=COLOR_NEW, linewidth=2.4, linestyle="--")
    axes[1].fill_between(
        time[3:],
        non_level_actual[3:],
        pre_shock_target[3:],
        color=COLOR_GAP,
        alpha=0.16,
    )
    axes[1].annotate(
        "target resets\nfrom lower base",
        xy=(4, reset_target[4]),
        xytext=(3.55, 0.205),
        color=COLOR_NEW,
        arrowprops={"arrowstyle": "->", "color": COLOR_NEW, "linewidth": 1.8},
    )
    axes[1].text(5.05, pre_shock_target[5] + 0.008, "old path", color=COLOR_EQUILIBRIUM)
    axes[1].text(5.0, non_level_actual[5] - 0.025, "actual", color=COLOR_AD, fontweight="bold")
    axes[1].text(5.2, 0.158, "permanent gap", color=COLOR_GAP)

    save(fig, "ngdp_level_targeting.png")


if __name__ == "__main__":
    plot_baseline()
    plot_shocks()
    plot_sticky_price_cross()
    plot_sticky_price_ad_as()
    plot_interest_rate_single_schedule()
    plot_interest_rate_ngdp_forecast()
    plot_ngdp_level_targeting()
    print(f"Saved figures to {OUTPUT_DIR}")
