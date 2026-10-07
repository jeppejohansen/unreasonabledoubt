"""Render the post's sourced comparisons and institutional sketch.

Run from the repository root with:
    uv run python blogs/jiu_jitsu_and_monopsony/src/make_figures.py

The chart inputs and their source URLs live in the CSV files under ../assets/.
The comparison charts reproduce or derive published figures; the final diagram is a proposal.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


POST = Path(__file__).resolve().parents[1]
INPUT = POST / "assets" / "figure_values.csv"
OUTPUT = POST / "figures"

PAPER = "#FBF8F1"
INK = "#24313A"
MUTED = "#626D70"
GUIDE = "#DFDED7"
TEAL = "#176B78"
RUST = "#B25739"


def values() -> dict[str, dict[str, str]]:
    with INPUT.open(newline="", encoding="utf-8") as source:
        return {row["key"]: row for row in csv.DictReader(source)}


def number(rows: dict[str, dict[str, str]], key: str) -> float:
    return float(rows[key]["value"])


def setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": INK,
            "savefig.facecolor": PAPER,
        }
    )
    OUTPUT.mkdir(exist_ok=True)


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(OUTPUT / filename, dpi=220, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)


def appearance_offers(rows: dict[str, dict[str, str]]) -> None:
    cji = number(rows, "cji_appearance")
    adcc = number(rows, "adcc_appearance")
    fig, ax = plt.subplots(figsize=(9.6, 3.7))
    fig.subplots_adjust(left=0.27, right=0.96, top=0.83, bottom=0.27)
    ax.barh(1, cji, height=0.46, color=TEAL)
    ax.barh(0, adcc, height=0.46, facecolor=PAPER, edgecolor=RUST, hatch="///", linewidth=1.8)
    ax.set_yticks([1, 0], ["CJI announced minimum", "Reported ADCC proposal"])
    ax.tick_params(axis="y", length=0, pad=12)
    ax.set_xlim(0, 11_500)
    ax.set_xticks([0, 2_500, 5_000, 7_500, 10_000])
    ax.set_xticklabels(["$0", "$2,500", "$5,000", "$7,500", "$10,000"])
    ax.set_xlabel("US dollars per entrant", labelpad=12)
    ax.grid(axis="x", color=GUIDE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(cji + 170, 1, "$10,001", va="center", color=TEAL, weight="bold")
    ax.text(adcc + 170, 0, "$2,500", va="center", color=RUST, weight="bold")
    ax.set_title("2024 appearance-pay offers", loc="left", fontsize=15, weight="bold", pad=17)
    fig.text(
        0.27,
        0.07,
        "CJI advertised its floor; an unverified memo attributed to an ADCC organizer proposed $2,500.",
        color=MUTED,
        fontsize=8.5,
    )
    save(fig, "appearance_pay_offers_2024.png")


def athlete_revenue_shares(rows: dict[str, dict[str, str]]) -> None:
    entries = [
        ("UFC", "ufc_share", TEAL),
        ("Bellator", "bellator_share", TEAL),
        ("Strikeforce", "strikeforce_share", TEAL),
        ("Premier League", "premier_league_share", RUST),
    ]
    fig, (pay_ax, margin_ax) = plt.subplots(
        2, 1, figsize=(9.6, 7.5), gridspec_kw={"height_ratios": [2, 1]}
    )
    fig.subplots_adjust(left=0.27, right=0.95, top=0.87, bottom=0.15, hspace=0.5)
    fig.suptitle("Pay shares and operating margins", x=0.27, y=0.97, ha="left", fontsize=16, weight="bold")
    for index, (label, key, color) in enumerate(entries):
        y = 3 - index
        value = number(rows, key)
        pay_ax.barh(y, value, height=0.47, color=color, alpha=0.92)
        pay_ax.text(value + 1.1, y, f"{value:g}%", va="center", color=color, weight="bold")
    pay_ax.set_yticks([3, 2, 1, 0], [label for label, _, _ in entries])
    pay_ax.set_title("Athlete compensation / revenue", loc="left", fontsize=12, weight="bold", pad=12)

    margins = [
        ("UFC", "ufc_operating_margin", TEAL),
        ("Premier League", "premier_league_operating_margin", RUST),
    ]
    for index, (label, key, color) in enumerate(margins):
        y = 1 - index
        value = number(rows, key)
        margin_ax.barh(y, value, height=0.47, color=color, alpha=0.92)
        margin_ax.text(value + 1.1, y, f"{value:g}%", va="center", color=color, weight="bold")
    margin_ax.set_yticks([1, 0], [label for label, _, _ in margins])
    margin_ax.set_title("Operating margin: UFC FY2025; football 2024/25", loc="left", fontsize=12, weight="bold", pad=12)

    for ax in (pay_ax, margin_ax):
        ax.tick_params(axis="y", length=0, pad=10)
        ax.set_xlim(0, 75)
        ax.set_xticks([0, 20, 40, 60], ["0%", "20%", "40%", "60%"])
        ax.grid(axis="x", color=GUIDE, linewidth=0.8)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
    pay_ax.tick_params(axis="x", labelbottom=False, length=0)
    margin_ax.set_xlabel("Percent of revenue", labelpad=10)
    fig.text(
        0.27,
        0.045,
        "Pay: historical court/UEFA data. Margin: UFC adjusted EBITDA; football operating result. Definitions differ.",
        color=MUTED,
        fontsize=8.5,
    )
    save(fig, "athlete_revenue_shares.png")


def labour_concentration(rows: dict[str, dict[str, str]]) -> None:
    ols = number(rows, "concentration_ols")
    iv = number(rows, "concentration_iv")
    fig, ax = plt.subplots(figsize=(9.6, 3.7))
    fig.subplots_adjust(left=0.17, right=0.95, top=0.82, bottom=0.28)
    ax.barh([1, 0], [ols, iv], height=0.44, color=["#8DAAB0", TEAL])
    ax.set_yticks([1, 0], ["OLS estimate", "IV estimate"])
    ax.tick_params(axis="y", length=0, pad=10)
    ax.set_xlim(0, 20)
    ax.set_xticks([0, 5, 10, 15, 20], ["0%", "5%", "10%", "15%", "20%"])
    ax.set_xlabel("Lower posted wages in more concentrated markets", labelpad=11)
    ax.grid(axis="x", color=GUIDE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(ols + 0.5, 1, "5%", va="center", color=INK, weight="bold")
    ax.text(iv + 0.5, 0, "17%", va="center", color=TEAL, weight="bold")
    ax.set_title("More concentrated hiring, lower advertised pay", loc="left", fontsize=15, weight="bold", pad=17)
    fig.text(
        0.17,
        0.07,
        "US job postings; 25th-to-75th percentile concentration change. Estimates are not about jiu jitsu.",
        color=MUTED,
        fontsize=8.5,
    )
    save(fig, "concentration_and_posted_wages.png")


def size_and_pay() -> None:
    with (POST / "assets" / "premier_league_2024_25_clubs.csv").open(newline="", encoding="utf-8") as source:
        clubs = list(csv.DictReader(source))
    with (POST / "assets" / "mma_promoter_size_bounds.csv").open(newline="", encoding="utf-8") as source:
        promoters = {row["promoter"]: row for row in csv.DictReader(source)}

    revenue = np.array([int(row["revenue_gbp_thousands"]) for row in clubs], dtype=float)
    staff_cost = np.array([int(row["total_staff_cost_gbp_thousands"]) for row in clubs], dtype=float)
    club_size = revenue / revenue.sum() * 100
    staff_share = staff_cost / revenue * 100
    log_size = np.log10(club_size)
    slope, intercept = np.polyfit(log_size, staff_share, 1)
    correlation = np.corrcoef(log_size, staff_share)[0, 1]
    ufc = promoters["UFC"]
    ufc_size = float(ufc["reported_revenue_share_percent"])
    ufc_pay = float(ufc["fighter_compensation_share_percent"])

    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    fig.subplots_adjust(left=0.12, right=0.96, top=0.83, bottom=0.24)
    ax.set_title("Organization size and compensation share", loc="left", fontsize=16, weight="bold", pad=22)

    ax.scatter(club_size, staff_share, s=58, color=RUST, alpha=0.88, zorder=3,
               label="Premier League clubs · all staff")
    grid = np.geomspace(club_size.min(), club_size.max(), 100)
    ax.plot(grid, slope * np.log10(grid) + intercept, color=RUST, linewidth=2,
            zorder=2, label=f"Club-only fit · R² = {correlation ** 2:.2f}")
    ax.scatter([ufc_size], [ufc_pay], marker="D", s=100, color=TEAL, zorder=4,
               label="UFC · fighters")
    ax.annotate("UFC", (ufc_size, ufc_pay), xytext=(-8, 9), textcoords="offset points",
                ha="right", fontsize=11, color=TEAL, weight="bold")
    ax.set_xscale("log")
    ax.set_xlabel("Share of each sport's comparison-market revenue (%) · log scale", labelpad=12)
    ax.set_ylabel("Compensation / organization revenue (%)", labelpad=10)
    ax.set_xlim(1.5, 115)
    ticks = [2, 5, 10, 20, 50, 100]
    ax.set_xticks(ticks, [f"{tick}%" for tick in ticks])
    ax.minorticks_off()
    ax.set_ylim(0, 102)
    ax.set_yticks([0, 20, 40, 60, 80, 100], ["0%", "20%", "40%", "60%", "80%", "100%"])
    label_offsets = {
        "Liverpool": (3, 9),
        "Arsenal": (3, -13),
        "Tottenham Hotspur": (4, -13),
        "Wolverhampton Wanderers": (4, 5),
        "Ipswich Town": (4, -12),
    }
    for index, row in enumerate(clubs):
        if row["club"] in label_offsets:
            label = row["club"].replace(" Hotspur", "").replace("Wolverhampton Wanderers", "Wolves")
            ax.annotate(label, (club_size[index], staff_share[index]), xytext=label_offsets[row["club"]],
                        textcoords="offset points", fontsize=7.5, color=INK)

    ax.legend(loc="upper right", frameon=False, fontsize=8.7, handlelength=1.8)
    ax.grid(color=GUIDE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(0.12, 0.09,
             "Football: 20 clubs, FY2024/25, total staff wages. UFC: historical US market-share high and 2010–17 fighter/event-revenue share.",
             color=MUTED, fontsize=8.2)
    save(fig, "size_and_athlete_pay.png")


def box(ax: plt.Axes, x: float, y: float, w: float, h: float, label: str, color: str) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        linewidth=1.5,
        edgecolor=color,
        facecolor=PAPER,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", color=color, weight="bold")


def arrow(ax: plt.Axes, a: tuple[float, float], b: tuple[float, float], color: str) -> None:
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=15, color=color, linewidth=1.5))


def organization_sketch() -> None:
    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.08)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.plot([0.5, 0.5], [0.09, 0.9], color=GUIDE, linewidth=1.4)
    ax.text(0.25, 0.91, "Rival promotions", ha="center", fontsize=14, weight="bold")
    ax.text(0.75, 0.91, "One league, rival clubs", ha="center", fontsize=14, weight="bold")

    box(ax, 0.07, 0.65, 0.17, 0.14, "Event A", RUST)
    box(ax, 0.28, 0.65, 0.17, 0.14, "Event B", RUST)
    box(ax, 0.07, 0.31, 0.17, 0.14, "Athlete pool A", RUST)
    box(ax, 0.28, 0.31, 0.17, 0.14, "Athlete pool B", RUST)
    arrow(ax, (0.155, 0.45), (0.155, 0.64), RUST)
    arrow(ax, (0.365, 0.45), (0.365, 0.64), RUST)
    ax.text(0.26, 0.14, "Better offers can split the field", ha="center", color=RUST)

    box(ax, 0.67, 0.66, 0.16, 0.14, "League", TEAL)
    for x, label in [(0.55, "Club A"), (0.70, "Club B"), (0.85, "Club C")]:
        box(ax, x, 0.35, 0.11, 0.13, label, TEAL)
        arrow(ax, (x + 0.055, 0.49), (0.75, 0.65), TEAL)
    ax.text(0.75, 0.23, "Clubs bid for talent", ha="center", color=TEAL)
    ax.text(0.75, 0.14, "Athletes meet in the same competition", ha="center", color=TEAL)
    fig.text(0.04, 0.02, "Proposed institutional structure; schematic, not observed data.", color=MUTED, fontsize=8.5)
    save(fig, "promotion_vs_club_league.png")


def main() -> None:
    setup()
    rows = values()
    appearance_offers(rows)
    athlete_revenue_shares(rows)
    size_and_pay()
    labour_concentration(rows)
    organization_sketch()


if __name__ == "__main__":
    main()
