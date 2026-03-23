"""
Introductory figures for the blog post: what are you buying when you buy
a bond vs a stock?

1. bond_cashflows.png — deterministic cash flows from a bond
2. stock_cashflows.png — uncertain cash flows from a stock (with error bars)
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (9, 5),
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
})


def plot_bond_cashflows():
    """Bond: pay P today, receive fixed coupons + face value at maturity."""
    T = 10
    periods = np.arange(0, T + 1)
    coupon = 3.0
    face_value = 100.0
    price = 95.0

    fig, ax = plt.subplots()

    # Price paid (negative cash flow at t=0)
    ax.bar(0, -price, color="#d62728", width=0.6, zorder=3)
    ax.annotate(f"Pay ${price:.0f}", xy=(0, -price),
                xytext=(-1.5, -price + 10), fontsize=11, color="#d62728",
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5))

    # Coupons (positive cash flows at t=1..T-1)
    for t in range(1, T):
        ax.bar(t, coupon, color="#2c7fb8", width=0.6, zorder=3)

    # Label coupons with arrow from above
    ax.annotate(f"${coupon:.0f} coupon each year", xy=(5, coupon),
                xytext=(5, coupon + 18), fontsize=11, color="#2c7fb8",
                ha="center",
                arrowprops=dict(arrowstyle="->", color="#2c7fb8", lw=1.5))

    # Final payment: coupon + face value
    final = coupon + face_value
    ax.bar(T, final, color="#2c7fb8", width=0.6, zorder=3)
    ax.annotate(f"Coupon + face value = ${final:.0f}", xy=(T, final),
                xytext=(T - 2.5, final + 12), fontsize=11, color="#2c7fb8",
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#2c7fb8", lw=1.5))

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Cash flow ($)")
    ax.set_title("Bond: fixed, known cash flows")
    ax.set_xticks(periods)
    ax.set_xlim(-0.8, T + 0.8)
    ax.set_ylim(-price - 15, final + 30)
    ax.grid(True, alpha=0.2, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "bond_cashflows.png", dpi=200)
    plt.close(fig)
    print("Saved bond_cashflows.png")


def plot_stock_cashflows():
    """Stock: pay P today, receive uncertain dividends + uncertain terminal value."""
    T = 10
    periods = np.arange(0, T + 1)
    price = 100.0

    # Expected dividends: growing at ~3% per year
    g = 0.03
    d0 = 4.0
    expected_divs = np.array([d0 * (1 + g)**t for t in range(1, T + 1)])

    # Uncertainty grows over time
    vol = 0.25
    std_divs = np.array([d0 * vol * np.sqrt(t) for t in range(1, T + 1)])

    # Terminal value (uncertain)
    terminal_expected = price * (1 + g)**T
    terminal_std = terminal_expected * 0.35

    fig, ax = plt.subplots()

    # Price paid
    ax.bar(0, -price, color="#d62728", width=0.6, zorder=3)
    ax.annotate(f"Pay ${price:.0f}", xy=(0, -price),
                xytext=(-1.5, -price + 10), fontsize=11, color="#d62728",
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5))

    # Dividends with growing error bars
    div_periods = np.arange(1, T)
    ax.bar(div_periods, expected_divs[:T-1], color="#2ca02c", width=0.6,
           alpha=0.7, zorder=3)
    ax.errorbar(div_periods, expected_divs[:T-1], yerr=1.5 * std_divs[:T-1],
                fmt="none", ecolor="#2ca02c", elinewidth=2, capsize=4,
                capthick=1.5, zorder=4, alpha=0.7)

    ax.annotate("Dividends (uncertain,\nerror bars widen over time)",
                xy=(5, expected_divs[4] + 1.5 * std_divs[4]),
                xytext=(4, 35), fontsize=11, color="#2ca02c", ha="center",
                arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    # Terminal period: dividend + terminal value
    total_final = expected_divs[T - 1] + terminal_expected
    total_final_std = np.sqrt(std_divs[T - 1]**2 + terminal_std**2)

    ax.bar(T, total_final, color="#2ca02c", width=0.6, alpha=0.7, zorder=3)
    ax.errorbar(T, total_final, yerr=1.5 * total_final_std,
                fmt="none", ecolor="#2ca02c", elinewidth=3, capsize=7,
                capthick=2.5, zorder=4, alpha=0.7)

    ax.annotate("Dividend + sale price\n(very uncertain)",
                xy=(T, total_final + 1.5 * total_final_std),
                xytext=(T - 2.5, total_final + 1.5 * total_final_std + 15),
                fontsize=11, color="#2ca02c", fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.5))

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Cash flow ($)")
    ax.set_title("Stock: uncertain, growing cash flows")
    ax.set_xticks(periods)
    ax.set_xlim(-0.8, T + 0.8)
    ymax = total_final + 1.5 * total_final_std + 40
    ax.set_ylim(-price - 15, ymax)
    ax.grid(True, alpha=0.2, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "stock_cashflows.png", dpi=200)
    plt.close(fig)
    print("Saved stock_cashflows.png")


if __name__ == "__main__":
    plot_bond_cashflows()
    plot_stock_cashflows()
    print(f"\nFigures saved to {OUTPUT_DIR}/")
