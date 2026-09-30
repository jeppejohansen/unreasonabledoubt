"""Render five chart-style studies from the saved demand-model sweep.

Run from the repository root with:
    uv run python .agents/skills/graphics-coder/scripts/render_style_trials.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image, ImageDraw


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_DATA = (
    REPO_ROOT
    / "blogs/demand_for_investment_is_inelastic/data/ge_sweep_results.json"
)
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "references/style_trials"


type StyleData = tuple[list[float], list[float], list[float], list[float], list[float]]


def load_series(path: Path) -> StyleData:
    rows = sorted(json.loads(path.read_text()), key=lambda row: row["r_s_input"])
    if len(rows) < 2:
        raise ValueError("The style study needs at least two sweep observations")

    returns = [100 * (row["r_s_input"] - 1) for row in rows]
    savings = [100 * (row["avg_savings_rate"] - rows[0]["avg_savings_rate"]) for row in rows]
    allocation = [
        100 * (row["avg_portfolio_share"] - rows[0]["avg_portfolio_share"])
        for row in rows
    ]
    saving_levels = [100 * row["avg_savings_rate"] for row in rows]
    stock_levels = [100 * row["avg_portfolio_share"] for row in rows]
    return returns, savings, allocation, saving_levels, stock_levels


def base_figure(
    *,
    background: str,
    ink: str,
    muted: str,
    title: str,
    subtitle: str,
    serif_title: bool = False,
) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(9.6, 5.45), facecolor=background)
    ax.set_facecolor(background)
    ax.set_position((0.105, 0.20, 0.68, 0.54))
    fig.text(
        0.105,
        0.92,
        title,
        fontsize=19,
        fontweight="semibold",
        fontfamily="DejaVu Serif" if serif_title else "DejaVu Sans",
        color=ink,
        va="top",
    )
    fig.text(0.105, 0.83, subtitle, fontsize=10.5, color=muted, va="top")
    fig.text(
        0.105,
        0.065,
        "Source: lifecycle model sweep · model output, not observed data",
        fontsize=8.7,
        color=muted,
    )
    return fig, ax


def setup_axes(
    ax: plt.Axes,
    *,
    ink: str,
    muted: str,
    grid: str,
    show_spines: bool = False,
    show_grid: bool = True,
) -> None:
    ax.set_xlim(2.7, 18.5)
    ax.set_ylim(-1.5, 42)
    ax.set_xticks([3, 5, 7, 9, 11, 13, 15])
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    ax.set_xlabel("Expected stock return", color=ink, fontsize=10.5, labelpad=13)
    ax.set_ylabel("Change from 3% case · percentage points", color=ink, fontsize=10.5, labelpad=11)
    ax.tick_params(axis="both", colors=muted, labelsize=9.5, length=0, pad=8)
    ax.set_axisbelow(True)
    if show_grid:
        ax.grid(axis="y", color=grid, linewidth=0.8)
    for name, spine in ax.spines.items():
        spine.set_visible(show_spines and name in ("left", "bottom"))
        spine.set_color(grid)
        spine.set_linewidth(0.9)


def label_ends(
    ax: plt.Axes,
    returns: list[float],
    savings: list[float],
    allocation: list[float],
    *,
    primary: str,
    secondary: str,
    saving_y: float = 4.3,
) -> None:
    ax.text(
        returns[-1] + 0.4,
        allocation[-1] - 0.4,
        f"Stock share\n+{allocation[-1]:.1f} pp",
        color=primary,
        fontsize=10,
        fontweight="semibold",
        va="center",
    )
    ax.annotate(
        f"Saving rate\n+{savings[-1]:.1f} pp",
        xy=(returns[-1], savings[-1]),
        xytext=(returns[-1] + 0.4, saving_y),
        color=secondary,
        fontsize=10,
        fontweight="semibold",
        va="center",
        arrowprops={"arrowstyle": "-", "color": secondary, "lw": 0.9},
    )


def editorial_paper(series: StyleData) -> plt.Figure:
    x, saving, stock, _, _ = series
    bg, ink, muted, grid = "#FBF8F1", "#24313A", "#626D70", "#DFDED7"
    primary, secondary = "#176B78", "#B25739"
    fig, ax = base_figure(
        background=bg,
        ink=ink,
        muted=muted,
        title="Two margins of adjustment",
        subtitle="Portfolio choice responds; total saving barely moves",
        serif_title=True,
    )
    setup_axes(ax, ink=ink, muted=muted, grid=grid)
    ax.plot(x, stock, color=primary, linewidth=3.1, solid_capstyle="round")
    ax.plot(x, saving, color=secondary, linewidth=2.5, linestyle=(0, (5, 3)))
    ax.scatter([x[-1]], [stock[-1]], color=primary, s=42, zorder=4)
    ax.scatter([x[-1]], [saving[-1]], color=secondary, s=38, zorder=4)
    label_ends(ax, x, saving, stock, primary=primary, secondary=secondary)
    return fig


def analytical_white(series: StyleData) -> plt.Figure:
    x, saving, stock, _, _ = series
    bg, ink, muted, grid = "#FFFFFF", "#152E44", "#5D6A75", "#E1E8ED"
    primary, secondary = "#006A9F", "#C66E2A"
    fig, ax = base_figure(
        background=bg,
        ink=ink,
        muted=muted,
        title="Saving stays almost flat",
        subtitle=f"Change from the {x[0]:.0f}% return case across {len(x)} model runs",
    )
    setup_axes(ax, ink=ink, muted=muted, grid=grid, show_spines=True)
    ax.plot(x, stock, color=primary, linewidth=2.9, marker="o", markersize=4.8)
    ax.plot(
        x, saving, color=secondary, linewidth=2.4, linestyle="--", marker="s", markersize=4
    )
    label_ends(ax, x, saving, stock, primary=primary, secondary=secondary)
    return fig


def focus_ink(series: StyleData) -> plt.Figure:
    x, saving, stock, _, _ = series
    bg, ink, muted, grid = "#FAFAF8", "#252B2F", "#686D70", "#E5E5E1"
    primary, secondary = "#626C73", "#B64C42"
    fig, ax = base_figure(
        background=bg,
        ink=ink,
        muted=muted,
        title=f"The saving rate moves by just {saving[-1]:.1f} points",
        subtitle=f"Even while the stock allocation moves by {stock[-1]:.0f} points",
    )
    setup_axes(ax, ink=ink, muted=muted, grid=grid, show_grid=False)
    ax.axhspan(0, 2.2, color="#F6E7E2", zorder=0)
    for y in (0, 20, 40):
        ax.axhline(y, color=grid, linewidth=0.8, zorder=0)
    ax.plot(x, stock, color=primary, linewidth=2.5, solid_capstyle="round")
    ax.plot(x, saving, color=secondary, linewidth=3.4, solid_capstyle="round")
    ax.scatter(x, saving, facecolor=bg, edgecolor=secondary, linewidth=1.5, s=35, zorder=4)
    label_ends(ax, x, saving, stock, primary=primary, secondary=secondary)
    return fig


def small_multiples(series: StyleData) -> plt.Figure:
    x, saving, stock, saving_levels, stock_levels = series
    bg, ink, muted, grid = "#F5F8F8", "#20343C", "#607179", "#DCE6E7"
    primary, secondary = "#166D83", "#AA6338"
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.45), facecolor=bg)
    fig.text(0.09, 0.92, "One return sweep, two responses", fontsize=19, weight="semibold", color=ink, va="top")
    fig.text(0.09, 0.83, f"Candidate expected stock returns range from {x[0]:.0f}% to {x[-1]:.0f}%", fontsize=10.5, color=muted, va="top")
    fig.text(0.09, 0.066, "Panel scales differ · Source: lifecycle model sweep, not observed data", fontsize=8.7, color=muted)
    panels = (
        (axes[0], saving_levels, secondary, "Total saving", "of income", f"+{saving[-1]:.1f} pp", (70.5, 72.5), [71, 72]),
        (axes[1], stock_levels, primary, "Stock allocation", "of portfolio", f"+{stock[-1]:.1f} pp", (20, 65), [20, 40, 60]),
    )
    for ax, values, color, name, unit, delta, ylim, yticks in panels:
        ax.set_facecolor(bg)
        ax.set_xlim(2.5, 15.8)
        ax.set_ylim(*ylim)
        ax.set_xticks([3, 7, 11, 15])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
        ax.set_yticks(yticks)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
        ax.tick_params(axis="both", colors=muted, labelsize=9.5, length=0, pad=7)
        ax.grid(axis="y", color=grid, linewidth=0.8)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.plot(x, values, color=color, linewidth=3.0, marker="o", markersize=4.5)
        ax.text(0.0, 1.17, name, transform=ax.transAxes, color=ink, fontsize=12, weight="semibold")
        ax.text(0.0, 1.06, unit, transform=ax.transAxes, color=muted, fontsize=9.5)
        ax.text(1.0, 1.11, delta, transform=ax.transAxes, color=color, fontsize=12, weight="semibold", ha="right")
    axes[0].set_position((0.09, 0.19, 0.36, 0.46))
    axes[1].set_position((0.55, 0.19, 0.36, 0.46))
    return fig


def night_figure(series: StyleData) -> plt.Figure:
    x, saving, stock, _, _ = series
    bg, ink, muted, grid = "#152636", "#F3F6F5", "#B7C4CB", "#385063"
    primary, secondary = "#62CFC8", "#F0BC68"
    fig, ax = base_figure(
        background=bg,
        ink=ink,
        muted=muted,
        title="Portfolio shifts, saving holds steady",
        subtitle="Model response to rising expected stock returns",
    )
    setup_axes(ax, ink=ink, muted=muted, grid=grid)
    ax.grid(axis="y", color=grid, linewidth=0.8, linestyle=(0, (2, 4)))
    ax.plot(x, stock, color=primary, linewidth=3.2, solid_capstyle="round")
    ax.plot(x, saving, color=secondary, linewidth=2.7, linestyle=(0, (2, 2)))
    ax.scatter([x[-1]], [stock[-1]], color=primary, s=50, zorder=4)
    ax.scatter([x[-1]], [saving[-1]], color=secondary, s=44, zorder=4)
    label_ends(ax, x, saving, stock, primary=primary, secondary=secondary)
    return fig


def comparison_sheet(files: list[Path], output: Path) -> None:
    width, height, gutter = 860, 490, 24
    sheet = Image.new("RGB", (2 * width + 3 * gutter, 3 * height + 4 * gutter), "#E9ECEB")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB")
        image.thumbnail((width, height - 22), Image.Resampling.LANCZOS)
        x = gutter + (index % 2) * (width + gutter)
        y = gutter + (index // 2) * (height + gutter)
        sheet.paste(image, (x, y + 22))
        draw.text((x + 4, y + 2), path.stem.replace("_", " "), fill="#25333A")
    sheet.save(output, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    series = load_series(args.data)
    trials = (
        ("01_editorial_paper", editorial_paper),
        ("02_analytical_white", analytical_white),
        ("03_focus_ink", focus_ink),
        ("04_small_multiples", small_multiples),
        ("05_night", night_figure),
    )
    files: list[Path] = []
    for name, render in trials:
        figure = render(series)
        output = args.output_dir / f"{name}.png"
        figure.savefig(output, dpi=200, facecolor=figure.get_facecolor())
        plt.close(figure)
        files.append(output)
        print(output)
    comparison_sheet(files, args.output_dir / "comparison.png")
    print(args.output_dir / "comparison.png")


if __name__ == "__main__":
    main()
