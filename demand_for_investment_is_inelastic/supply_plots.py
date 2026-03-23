"""
Supply curves for risky assets (stocks) and safe assets (bonds).

Conceptual/illustrative figures showing:
1. stock_supply.png — nearly vertical short-run, weakly elastic long-run
2. bond_supply.png — more elastic but constrained by sovereign credibility
"""

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


def plot_stock_supply():
    """
    Supply of risky assets (stocks).

    Y-axis: P/E ratio (price per unit of earnings)
    X-axis: Number of shares / claims on the economy

    Vertical line — you can't create more economy.
    """
    fig, ax = plt.subplots()

    K_current = 50

    ax.plot([K_current, K_current], [5, 45], color="#2c7fb8",
            linewidth=3, zorder=3)

    # Label
    ax.annotate("Fixed supply of stocks",
                xy=(K_current, 30), xytext=(K_current + 10, 32),
                fontsize=11, ha="left", color="#2c7fb8", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2c7fb8", lw=1.5))

    # Plain-language annotations
    ax.text(32, 40, "Expensive\n(low expected returns)", fontsize=9,
            color="gray", style="italic")
    ax.text(32, 10, "Cheap\n(high expected returns)", fontsize=9,
            color="gray", style="italic")

    ax.set_xlabel("Quantity of stocks (claims on the economy)")
    ax.set_ylabel("P/E ratio")
    ax.set_title("Supply of risky assets (stocks)")
    ax.set_xlim(28, 75)
    ax.set_ylim(3, 48)
    ax.set_xticks([])
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "stock_supply.png", dpi=200)
    plt.close(fig)
    print("Saved stock_supply.png")


def plot_bond_supply():
    """
    Supply of safe assets (government bonds).

    Y-axis: Bond yield (%)
    X-axis: Quantity of bonds outstanding

    Steep supply line with green/red shading for safe vs credibility-eroded zones.
    """
    fig, ax = plt.subplots()

    b_supply = np.linspace(20, 90, 100)
    yield_supply = 0.5 + 0.06 * (b_supply - 40)

    # Shade zones
    credibility_threshold = 72
    ax.axvspan(credibility_threshold, 92, alpha=0.08, color="#d62728", zorder=1)
    ax.axvspan(18, credibility_threshold, alpha=0.05, color="#2ca02c", zorder=1)

    ax.text(48, 5.5, '"Safe" asset zone', fontsize=11, color="#2ca02c",
            ha="center", style="italic")
    ax.text(80, 5.5, "Credibility\nerodes", fontsize=11, color="#d62728",
            ha="center", style="italic")

    # Credibility threshold
    ax.axvline(credibility_threshold, color="#d62728", linewidth=1.5,
               linestyle="--", alpha=0.5)

    # Supply line
    ax.plot(b_supply, yield_supply, color="#2c7fb8", linewidth=3, zorder=3)

    # Label
    ax.annotate("Government bond supply",
                xy=(55, 0.5 + 0.06 * (55 - 40)),
                xytext=(30, 3.0),
                fontsize=11, ha="center", color="#2c7fb8", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2c7fb8", lw=1.5))

    ax.set_xlabel("Quantity of government bonds outstanding")
    ax.set_ylabel("Bond yield (%)")
    ax.set_title("Supply of safe assets (government bonds)")
    ax.set_xlim(18, 92)
    ax.set_ylim(-0.5, 6.5)
    ax.set_xticks([])
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "bond_supply.png", dpi=200)
    plt.close(fig)
    print("Saved bond_supply.png")


if __name__ == "__main__":
    plot_stock_supply()
    plot_bond_supply()
    print(f"\nFigures saved to {OUTPUT_DIR}/")
