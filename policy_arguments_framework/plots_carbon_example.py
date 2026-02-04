"""Generate illustrative plots for the carbon-tax example."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


OUTPUT_DIR = Path("policy_arguments_framework/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Illustrative outcomes (higher = better emissions reduction)
Y_A_DUR = 100  # carbon tax, durable
Y_B_DUR = 70   # green investment fund, durable
Y_A_REV = 20   # carbon tax, reversed
Y_B_REV = 60   # green investment fund, reversed


def plot_2x2_table() -> None:
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.axis("off")

    cell_text = [
        [f"{Y_A_DUR}", f"{Y_B_DUR}"],
        [f"{Y_A_REV}", f"{Y_B_REV}"],
    ]
    row_labels = ["Durable policy (p)", "Reversal risk (1-p)"]
    col_labels = ["Carbon tax (A)", "Green investment fund (B)"]

    table = ax.table(
        cellText=cell_text,
        rowLabels=row_labels,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.1, 1.6)

    ax.set_title("Illustrative outcomes by policy and model", pad=14)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_2x2_table.png", dpi=200)
    plt.close(fig)


def plot_threshold() -> None:
    p = np.linspace(0, 1, 400)
    e_a = p * Y_A_DUR + (1 - p) * Y_A_REV
    e_b = p * Y_B_DUR + (1 - p) * Y_B_REV
    diff = e_a - e_b

    # Threshold where diff = 0
    # Avoid divide by zero; compute analytically
    denom = (Y_A_DUR - Y_A_REV) - (Y_B_DUR - Y_B_REV)
    if denom != 0:
        p_star = (Y_B_REV - Y_A_REV) / denom
    else:
        p_star = None

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(p, diff, color="#1f77b4", linewidth=2)
    ax.axhline(0, color="black", linewidth=1)
    if p_star is not None and 0 <= p_star <= 1:
        ax.axvline(p_star, color="#888888", linestyle="--", linewidth=1)
        ax.text(p_star + 0.02, 0.02 * (diff.max() - diff.min()), f"p*={p_star:.2f}")

    ax.set_xlabel("Probability of durable model (p)")
    ax.set_ylabel("E[Y(A)] - E[Y(B)]")
    ax.set_title("Policy choice threshold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_policy_threshold.png", dpi=200)
    plt.close(fig)


def plot_policy_map() -> None:
    # Fix the durable advantage and vary reversal outcomes
    durable_diff = Y_A_DUR - Y_B_DUR

    p_rev = np.linspace(0, 1, 300)
    rev_diff = np.linspace(-60, 60, 300)
    P, R = np.meshgrid(p_rev, rev_diff)

    # Expected advantage of A over B as a function of reversal probability and reversal payoff
    diff = (1 - P) * durable_diff + P * R

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    cmap = plt.get_cmap("RdYlGn")
    ax.contourf(P, R, diff, levels=[-1e9, 0, 1e9], colors=["#c62828", "#2e7d32"], alpha=0.85)
    ax.contour(P, R, diff, levels=[0], colors="black", linewidths=1)

    ax.text(0.75, 40, "A better", color="white", fontsize=10)
    ax.text(0.75, -40, "B better", color="white", fontsize=10)

    ax.set_xlabel("Probability of reversal (1-p)")
    ax.set_ylabel("Reversal model advantage: Y(A) - Y(B)")
    ax.set_title("When each policy is optimal")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_policy_map.png", dpi=200)
    plt.close(fig)


def plot_emissions_paths() -> None:
    # Illustrative emissions paths over time under two policies and two models
    years = np.arange(0, 51)

    # Baseline emissions level (index)
    baseline = 100.0

    # Carbon tax: faster initial decline, but vulnerable to reversal
    tax_durable = baseline * np.exp(-0.035 * years)
    tax_reversal = baseline * np.exp(-0.035 * np.minimum(years, 8))
    tax_reversal = np.where(
        years <= 8,
        tax_reversal,
        tax_reversal[8] + (baseline * 0.85 - tax_reversal[8]) * (1 - np.exp(-0.15 * (years - 8))),
    )

    # Green investment fund: slower start, more persistent reductions
    fund_durable = baseline * (0.85 * np.exp(-0.02 * years) + 0.15)
    # Green fund assumed irreversible in this illustrative version
    fund_reversal = fund_durable.copy()

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8), sharey=True)

    # Left: carbon tax
    axes[0].plot(years, tax_durable, label="Durable policy", color="#1f77b4", linewidth=2)
    axes[0].plot(years, tax_reversal, label="Reversal risk", color="#d62728", linewidth=2, linestyle="--")
    axes[0].set_title("Carbon tax (A)")
    axes[0].set_xlabel("Years")
    axes[0].set_ylabel("CO2 emissions (index)")
    axes[0].tick_params(axis="y", labelleft=False)
    axes[0].legend(frameon=False)

    # Right: green investment fund
    axes[1].plot(years, fund_durable, label="Durable policy", color="#1f77b4", linewidth=2)
    axes[1].plot(years, fund_reversal, label="Reversal risk", color="#d62728", linewidth=2, linestyle="--")
    axes[1].set_title("Green investment fund (B)")
    axes[1].set_xlabel("Years")
    axes[1].tick_params(axis="y", labelleft=False)
    axes[1].legend(frameon=False)

    fig.suptitle("Illustrative emissions paths by policy and model", y=1.02)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_emissions_paths.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_emissions_by_model() -> None:
    # Reuse the emissions paths to compare policies within each model
    years = np.arange(0, 51)
    baseline = 100.0

    tax_durable = baseline * np.exp(-0.035 * years)
    tax_reversal = baseline * np.exp(-0.035 * np.minimum(years, 8))
    tax_reversal = np.where(
        years <= 8,
        tax_reversal,
        tax_reversal[8] + (baseline * 0.85 - tax_reversal[8]) * (1 - np.exp(-0.15 * (years - 8))),
    )

    fund_durable = baseline * (0.85 * np.exp(-0.02 * years) + 0.15)
    # Green fund assumed irreversible in this illustrative version
    fund_reversal = fund_durable.copy()

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8), sharey=True)

    # Left: durable model
    axes[0].plot(years, tax_durable, label="Carbon tax (A)", color="#1f77b4", linewidth=2)
    axes[0].plot(years, fund_durable, label="Green fund (B)", color="#2e7d32", linewidth=2)
    axes[0].set_title("Durable model")
    axes[0].set_xlabel("Years")
    axes[0].set_ylabel("CO2 emissions (index)")
    axes[0].tick_params(axis="y", labelleft=False)
    axes[0].legend(frameon=False)

    # Right: reversal model
    axes[1].plot(years, tax_reversal, label="Carbon tax (A)", color="#1f77b4", linewidth=2, linestyle="--")
    axes[1].plot(years, fund_reversal, label="Green fund (B)", color="#2e7d32", linewidth=2, linestyle="--")
    axes[1].set_title("Reversal model")
    axes[1].set_xlabel("Years")
    axes[1].tick_params(axis="y", labelleft=False)
    axes[1].legend(frameon=False)

    fig.suptitle("Illustrative emissions paths by model", y=1.02)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_emissions_by_model.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_vs_probability() -> None:
    # Expected cumulative emissions as a function of model probability
    years = np.arange(0, 51)
    baseline = 100.0

    tax_durable = baseline * np.exp(-0.035 * years)
    tax_reversal = baseline * np.exp(-0.035 * np.minimum(years, 8))
    tax_reversal = np.where(
        years <= 8,
        tax_reversal,
        tax_reversal[8] + (baseline * 0.85 - tax_reversal[8]) * (1 - np.exp(-0.15 * (years - 8))),
    )

    fund_durable = baseline * (0.85 * np.exp(-0.02 * years) + 0.15)
    # Green fund assumed irreversible
    fund_reversal = fund_durable.copy()

    # Cumulative emissions over the horizon
    cum_tax_durable = tax_durable.sum()
    cum_tax_reversal = tax_reversal.sum()
    cum_fund_durable = fund_durable.sum()
    cum_fund_reversal = fund_reversal.sum()

    p = np.linspace(0, 1, 400)
    exp_cum_tax = p * cum_tax_durable + (1 - p) * cum_tax_reversal
    exp_cum_fund = p * cum_fund_durable + (1 - p) * cum_fund_reversal

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(p, exp_cum_tax, label="Carbon tax (A)", color="#1f77b4", linewidth=2)
    ax.plot(p, exp_cum_fund, label="Green fund (B)", color="#2e7d32", linewidth=2)

    ax.set_xlabel("Probability of durable model (p)")
    ax.set_ylabel("Expected cumulative CO2 (index·years)")
    ax.tick_params(axis="y", labelleft=False)
    ax.set_title("Cumulative emissions vs model probability")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "carbon_cumulative_vs_probability.png", dpi=200)
    plt.close(fig)


def main() -> None:
    plot_2x2_table()
    plot_threshold()
    plot_policy_map()
    plot_emissions_paths()
    plot_emissions_by_model()
    plot_cumulative_vs_probability()


if __name__ == "__main__":
    main()
