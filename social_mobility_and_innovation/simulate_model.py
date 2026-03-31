"""First-pass simulation for the social mobility and innovation model.

This script implements the current Typst model draft in a computational form
with an optional talent-sorting extension and omega talent persistence:

- CES production in sectoral talent inputs (raw talent in the baseline; effective talent under eta_W/eta_B extension)
- talent-based earnings y_(s,t)(h) = w_(s,t) * h^eta_s
- ARUM occupation choice with a parental switching cost c_g and common phi
- technology accumulation A_(s,t+1) = A_(s,t) + H_(t,s)
- talent transmission with persistence parameter omega (default 0.7)

Implementation notes:
- We approximate the unit-mass population with N agents of equal mass 1/N.
- Within-period wages are solved from a fixed point using ARUM logit probabilities.
- We then sample realized occupations and compute H and N directly from those assignments.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import csv
from statistics import NormalDist

import matplotlib.pyplot as plt
import numpy as np


FIGURES_DIR = Path("social_mobility_and_innovation/figures")
RESULTS_DIR = Path("social_mobility_and_innovation/results")
TALENT_FAN_QUANTILES = np.array([0.10, 0.25, 0.50, 0.75, 0.90], dtype=float)
TALENT_FAN_LABELS = ("p10", "p25", "p50", "p75", "p90")


@dataclass
class ModelParams:
    periods: int = 80
    n_agents: int = 10_000
    seed: int = 0
    simulation_mode: str = "monte_carlo"
    grid_size: int = 401

    alpha: float = 0.5
    rho: float = 0.4

    phi: float = 0.35
    c_g: float = 0.15  # occupation-switching cost relative to parent's occupation
    omega: float = 0.7  # intergenerational talent correlation/persistence
    # Sector-specific returns to talent in earnings/effective talent.
    # If eta_w == eta_b == 1, talent cancels from choice margins and there is no talent sorting.
    eta_w: float = 1.0
    eta_b: float = 1.0

    a_w0: float = 1.25
    a_b0: float = 1.0

    init_parent_white_share: float = 0.5

    # Talent distribution (strictly positive so logs are well-defined)
    talent_dist: str = "uniform"
    talent_lognorm_mean: float = 0.0
    talent_lognorm_sigma: float = 0.35
    talent_uniform_low: float = 0.0
    talent_uniform_high: float = 1.0

    eq_tol: float = 1e-8
    eq_max_iter: int = 500
    eq_damping: float = 0.2

    mass_floor: float = 1e-8

    # Output file stem (kept here for convenience of CLI wiring)
    output_stem: str = "social_mobility_innovation_baseline"


@dataclass
class PeriodResult:
    n_w: float
    n_b: float
    h_w: float
    h_b: float
    w_w: float
    w_b: float
    y: float
    p_w_given_wparent: float
    p_w_given_bparent: float
    mobility_up_b_to_w: float
    mobility_down_w_to_b: float


def sigmoid(x: np.ndarray) -> np.ndarray:
    x_clipped = np.clip(x, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-x_clipped))


def weighted_quantiles(
    values: np.ndarray,
    quantiles: np.ndarray,
    weights: np.ndarray | None = None,
) -> np.ndarray:
    """Return weighted quantiles of `values` for quantiles in [0, 1]."""
    values_arr = np.asarray(values, dtype=float)
    q_arr = np.asarray(quantiles, dtype=float)

    if values_arr.size == 0:
        return np.full(q_arr.shape, np.nan, dtype=float)

    if weights is None:
        return np.quantile(values_arr, q_arr).astype(float)

    weights_arr = np.asarray(weights, dtype=float)
    valid = np.isfinite(values_arr) & np.isfinite(weights_arr) & (weights_arr > 0.0)
    if not np.any(valid):
        return np.full(q_arr.shape, np.nan, dtype=float)

    x = values_arr[valid]
    w = weights_arr[valid]
    order = np.argsort(x)
    x = x[order]
    w = w[order]

    cum_w = np.cumsum(w)
    total_w = float(cum_w[-1])
    if total_w <= 0.0:
        return np.full(q_arr.shape, np.nan, dtype=float)

    return np.interp(
        q_arr,
        np.concatenate(([0.0], cum_w / total_w)),
        np.concatenate(([x[0]], x)),
    ).astype(float)


def parameter_tag(params: ModelParams) -> str:
    return (
        f"rho={params.rho:.2f}, phi={params.phi:.2f}, c_g={params.c_g:.2f}, omega={params.omega:.2f}, "
        f"eta_W={params.eta_w:.2f}, eta_B={params.eta_b:.2f}"
    )


def add_parameter_tag(fig: plt.Figure, params: ModelParams) -> None:
    fig.text(
        0.99,
        0.006,
        parameter_tag(params),
        ha="right",
        va="bottom",
        fontsize=9,
        color="#444444",
    )


def draw_talents(
    params: ModelParams,
    rng: np.random.Generator,
    size: int,
) -> np.ndarray:
    if params.talent_dist == "lognormal":
        talents = rng.lognormal(
            mean=params.talent_lognorm_mean,
            sigma=params.talent_lognorm_sigma,
            size=size,
        )
    elif params.talent_dist == "uniform":
        talents = rng.uniform(
            low=params.talent_uniform_low,
            high=params.talent_uniform_high,
            size=size,
        )
    else:
        raise ValueError(f"Unsupported talent_dist={params.talent_dist!r}")

    return talents.astype(float)


def build_talents(params: ModelParams, rng: np.random.Generator) -> np.ndarray:
    return draw_talents(params, rng, params.n_agents)


def build_talent_grid(params: ModelParams) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic quadrature-style grid for the base talent distribution.

    Returns (nodes, weights) with weights summing to 1.
    """
    if params.grid_size < 2:
        raise ValueError("grid_size must be at least 2")

    u = (np.arange(params.grid_size, dtype=float) + 0.5) / params.grid_size

    if params.talent_dist == "uniform":
        low = params.talent_uniform_low
        high = params.talent_uniform_high
        nodes = low + (high - low) * u
    elif params.talent_dist == "lognormal":
        nd = NormalDist()
        z = np.array([nd.inv_cdf(float(ui)) for ui in u], dtype=float)
        nodes = np.exp(params.talent_lognorm_mean + params.talent_lognorm_sigma * z)
    else:
        raise ValueError(f"Unsupported talent_dist={params.talent_dist!r}")

    weights = np.full(params.grid_size, 1.0 / params.grid_size, dtype=float)
    return nodes.astype(float), weights


def transmit_talents(
    parent_talents: np.ndarray,
    params: ModelParams,
    rng: np.random.Generator,
) -> np.ndarray:
    """One-generation talent transmission with persistence omega.

    With probability omega, the child inherits the parent's talent exactly.
    Otherwise, talent is redrawn from the base talent distribution.
    """
    if not (0.0 <= params.omega <= 1.0):
        raise ValueError("omega must lie in [0, 1]")

    if params.omega == 1.0:
        return parent_talents.copy()
    if params.omega == 0.0:
        return draw_talents(params, rng, parent_talents.size)

    inherit = rng.random(parent_talents.size) < params.omega
    fresh = draw_talents(params, rng, parent_talents.size)
    return np.where(inherit, parent_talents, fresh)


def initial_parent_background(
    params: ModelParams,
    rng: np.random.Generator,
) -> np.ndarray:
    """Return boolean array: True if parent was white-collar."""
    return rng.random(params.n_agents) < params.init_parent_white_share


def sector_wage_rates(
    a_b: float,
    a_w: float,
    h_b: float,
    h_w: float,
    params: ModelParams,
) -> tuple[float, float, float]:
    """Return (w_b, w_w, y) from CES production using unit-mass normalized sector inputs."""
    h_b_eff = max(h_b, params.mass_floor)
    h_w_eff = max(h_w, params.mass_floor)

    if abs(params.rho) < 1e-12:
        # Cobb-Douglas limit of CES as rho -> 0
        x_b = a_b * h_b_eff
        x_w = a_w * h_w_eff
        y = (x_b ** params.alpha) * (x_w ** (1.0 - params.alpha))
        w_b = params.alpha * y / h_b_eff
        w_w = (1.0 - params.alpha) * y / h_w_eff
        return w_b, w_w, y

    z = (
        params.alpha * (a_b * h_b_eff) ** params.rho
        + (1.0 - params.alpha) * (a_w * h_w_eff) ** params.rho
    )
    y = z ** (1.0 / params.rho)

    w_b = params.alpha * (a_b ** params.rho) * (h_b_eff ** (params.rho - 1.0)) * (z ** (1.0 / params.rho - 1.0))
    w_w = (1.0 - params.alpha) * (a_w ** params.rho) * (h_w_eff ** (params.rho - 1.0)) * (z ** (1.0 / params.rho - 1.0))
    return w_b, w_w, y


def compute_choice_probabilities(
    talents: np.ndarray,
    parent_is_white: np.ndarray,
    w_b: float,
    w_w: float,
    params: ModelParams,
) -> np.ndarray:
    """Per-agent probability of choosing white-collar (ARUM logit)."""
    if params.phi <= 0:
        raise ValueError("phi must be strictly positive")

    # Optional sorting extension: sector-specific returns to talent.
    # If eta_w != eta_b, talent enters the occupation-choice margin.
    y_w = np.maximum(w_w * np.power(talents, params.eta_w), params.mass_floor)
    y_b = np.maximum(w_b * np.power(talents, params.eta_b), params.mass_floor)

    # Delta = V_W - V_B
    delta = np.log(y_w) - np.log(y_b)
    delta[parent_is_white] += params.c_g
    delta[~parent_is_white] -= params.c_g

    return sigmoid(delta / params.phi)


def solve_within_period(
    talents: np.ndarray,
    parent_is_white: np.ndarray,
    a_b: float,
    a_w: float,
    params: ModelParams,
    rng: np.random.Generator,
    wage_guess: tuple[float, float] | None = None,
) -> tuple[PeriodResult, np.ndarray, np.ndarray, tuple[float, float]]:
    """Solve within-period wages (expected fixed point), then sample occupations."""
    if wage_guess is None:
        # Start from equal sector talent allocation (unit-mass normalized)
        h_total = talents.mean()
        h_b0 = max(0.5 * h_total, params.mass_floor)
        h_w0 = max(0.5 * h_total, params.mass_floor)
        w_b, w_w, _ = sector_wage_rates(a_b, a_w, h_b0, h_w0, params)
    else:
        w_b, w_w = wage_guess

    # Effective talent supplied in each sector if chosen.
    eff_talent_if_b = np.power(talents, params.eta_b)
    eff_talent_if_w = np.power(talents, params.eta_w)

    # Fixed point in expected sectoral talent totals implied by logit probabilities.
    for _ in range(params.eq_max_iter):
        p_white = compute_choice_probabilities(talents, parent_is_white, w_b, w_w, params)

        q_w_exp = float(np.mean(p_white * eff_talent_if_w))
        q_b_exp = float(np.mean((1.0 - p_white) * eff_talent_if_b))
        w_b_new, w_w_new, _ = sector_wage_rates(a_b, a_w, q_b_exp, q_w_exp, params)

        rel_change = max(
            abs(w_b_new - w_b) / max(abs(w_b), params.mass_floor),
            abs(w_w_new - w_w) / max(abs(w_w), params.mass_floor),
        )
        w_b = (1.0 - params.eq_damping) * w_b + params.eq_damping * w_b_new
        w_w = (1.0 - params.eq_damping) * w_w + params.eq_damping * w_w_new
        if rel_change < params.eq_tol:
            break

    # Recompute probabilities at converged wages and sample realized assignments.
    p_white = compute_choice_probabilities(talents, parent_is_white, w_b, w_w, params)
    occ_is_white = rng.random(talents.size) < p_white

    n_w = float(np.mean(occ_is_white))
    n_b = 1.0 - n_w
    # Raw talent totals (used for technology accumulation in the current draft)
    h_w = float(np.mean(talents * occ_is_white))
    h_b = float(np.mean(talents * (~occ_is_white)))
    # Effective talent totals (used for production and wages when eta_w or eta_b != 1)
    q_w = float(np.mean(eff_talent_if_w * occ_is_white))
    q_b = float(np.mean(eff_talent_if_b * (~occ_is_white)))

    # Record realized outcomes using realized production inputs (effective talent if eta != 1).
    w_b_real, w_w_real, y_real = sector_wage_rates(a_b, a_w, q_b, q_w, params)

    if np.any(parent_is_white):
        p_w_wparent = float(np.mean(p_white[parent_is_white]))
        mobility_down = float(np.mean(~occ_is_white[parent_is_white]))
    else:
        p_w_wparent = float("nan")
        mobility_down = float("nan")

    if np.any(~parent_is_white):
        p_w_bparent = float(np.mean(p_white[~parent_is_white]))
        mobility_up = float(np.mean(occ_is_white[~parent_is_white]))
    else:
        p_w_bparent = float("nan")
        mobility_up = float("nan")

    result = PeriodResult(
        n_w=n_w,
        n_b=n_b,
        h_w=h_w,
        h_b=h_b,
        w_w=w_w_real,
        w_b=w_b_real,
        y=y_real,
        p_w_given_wparent=p_w_wparent,
        p_w_given_bparent=p_w_bparent,
        mobility_up_b_to_w=mobility_up,
        mobility_down_w_to_b=mobility_down,
    )
    return result, occ_is_white, p_white, (w_b, w_w)


def solve_within_period_grid(
    talent_grid: np.ndarray,
    mass_wparent: np.ndarray,
    mass_bparent: np.ndarray,
    a_b: float,
    a_w: float,
    params: ModelParams,
    wage_guess: tuple[float, float] | None = None,
) -> tuple[PeriodResult, np.ndarray, np.ndarray, tuple[float, float]]:
    """Deterministic within-period solution on a weighted talent/background grid."""
    if wage_guess is None:
        h_total = float(np.sum((mass_wparent + mass_bparent) * talent_grid))
        h_b0 = max(0.5 * h_total, params.mass_floor)
        h_w0 = max(0.5 * h_total, params.mass_floor)
        w_b, w_w, _ = sector_wage_rates(a_b, a_w, h_b0, h_w0, params)
    else:
        w_b, w_w = wage_guess

    parent_w_mask = np.ones(talent_grid.size, dtype=bool)
    parent_b_mask = np.zeros(talent_grid.size, dtype=bool)

    eff_talent_if_b = np.power(talent_grid, params.eta_b)
    eff_talent_if_w = np.power(talent_grid, params.eta_w)

    for _ in range(params.eq_max_iter):
        p_w_if_wparent = compute_choice_probabilities(talent_grid, parent_w_mask, w_b, w_w, params)
        p_w_if_bparent = compute_choice_probabilities(talent_grid, parent_b_mask, w_b, w_w, params)

        q_w_exp = float(
            np.sum(mass_wparent * p_w_if_wparent * eff_talent_if_w)
            + np.sum(mass_bparent * p_w_if_bparent * eff_talent_if_w)
        )
        q_b_exp = float(
            np.sum(mass_wparent * (1.0 - p_w_if_wparent) * eff_talent_if_b)
            + np.sum(mass_bparent * (1.0 - p_w_if_bparent) * eff_talent_if_b)
        )
        w_b_new, w_w_new, _ = sector_wage_rates(a_b, a_w, q_b_exp, q_w_exp, params)

        rel_change = max(
            abs(w_b_new - w_b) / max(abs(w_b), params.mass_floor),
            abs(w_w_new - w_w) / max(abs(w_w), params.mass_floor),
        )
        w_b = (1.0 - params.eq_damping) * w_b + params.eq_damping * w_b_new
        w_w = (1.0 - params.eq_damping) * w_w + params.eq_damping * w_w_new
        if rel_change < params.eq_tol:
            break

    p_w_if_wparent = compute_choice_probabilities(talent_grid, parent_w_mask, w_b, w_w, params)
    p_w_if_bparent = compute_choice_probabilities(talent_grid, parent_b_mask, w_b, w_w, params)

    mass_white_occ = mass_wparent * p_w_if_wparent + mass_bparent * p_w_if_bparent
    mass_blue_occ = mass_wparent * (1.0 - p_w_if_wparent) + mass_bparent * (1.0 - p_w_if_bparent)

    n_w = float(np.sum(mass_white_occ))
    n_b = float(np.sum(mass_blue_occ))
    h_w = float(np.sum(mass_white_occ * talent_grid))
    h_b = float(np.sum(mass_blue_occ * talent_grid))
    q_w = float(np.sum(mass_white_occ * eff_talent_if_w))
    q_b = float(np.sum(mass_blue_occ * eff_talent_if_b))

    w_b_real, w_w_real, y_real = sector_wage_rates(a_b, a_w, q_b, q_w, params)

    mass_w_total = float(np.sum(mass_wparent))
    mass_b_total = float(np.sum(mass_bparent))
    if mass_w_total > 0.0:
        p_w_wparent = float(np.sum(mass_wparent * p_w_if_wparent) / mass_w_total)
        mobility_down = float(np.sum(mass_wparent * (1.0 - p_w_if_wparent)) / mass_w_total)
    else:
        p_w_wparent = float("nan")
        mobility_down = float("nan")

    if mass_b_total > 0.0:
        p_w_bparent = float(np.sum(mass_bparent * p_w_if_bparent) / mass_b_total)
        mobility_up = float(np.sum(mass_bparent * p_w_if_bparent) / mass_b_total)
    else:
        p_w_bparent = float("nan")
        mobility_up = float("nan")

    result = PeriodResult(
        n_w=n_w,
        n_b=n_b,
        h_w=h_w,
        h_b=h_b,
        w_w=w_w_real,
        w_b=w_b_real,
        y=y_real,
        p_w_given_wparent=p_w_wparent,
        p_w_given_bparent=p_w_bparent,
        mobility_up_b_to_w=mobility_up,
        mobility_down_w_to_b=mobility_down,
    )
    return result, p_w_if_wparent, p_w_if_bparent, (w_b, w_w)


def simulate_grid(
    params: ModelParams,
) -> tuple[dict[str, np.ndarray], dict[int, dict[str, np.ndarray | float]]]:
    if not (0.0 <= params.omega <= 1.0):
        raise ValueError("omega must lie in [0, 1]")

    talent_grid, base_weights = build_talent_grid(params)
    mass_wparent = params.init_parent_white_share * base_weights
    mass_bparent = (1.0 - params.init_parent_white_share) * base_weights

    a_w_path = np.empty(params.periods + 1, dtype=float)
    a_b_path = np.empty(params.periods + 1, dtype=float)
    a_w_path[0] = params.a_w0
    a_b_path[0] = params.a_b0

    fields = [
        "n_w",
        "n_b",
        "h_w",
        "h_b",
        "w_w",
        "w_b",
        "y",
        "p_w_given_wparent",
        "p_w_given_bparent",
        "mobility_up_b_to_w",
        "mobility_down_w_to_b",
    ]
    history = {name: np.empty(params.periods, dtype=float) for name in fields}
    fan_history: dict[str, np.ndarray] = {}
    for label in TALENT_FAN_LABELS:
        fan_history[f"talent_w_{label}"] = np.empty(params.periods, dtype=float)
        fan_history[f"talent_b_{label}"] = np.empty(params.periods, dtype=float)

    wage_guess: tuple[float, float] | None = None
    snapshot_periods = {0, params.periods - 1}
    snapshots: dict[int, dict[str, np.ndarray | float]] = {}

    parent_flags = np.concatenate(
        [
            np.ones(talent_grid.size, dtype=bool),
            np.zeros(talent_grid.size, dtype=bool),
        ]
    )
    stacked_talents = np.concatenate([talent_grid, talent_grid])

    for t in range(params.periods):
        result, p_w_if_wparent, p_w_if_bparent, wage_guess = solve_within_period_grid(
            talent_grid=talent_grid,
            mass_wparent=mass_wparent,
            mass_bparent=mass_bparent,
            a_b=a_b_path[t],
            a_w=a_w_path[t],
            params=params,
            wage_guess=wage_guess,
        )

        for name in fields:
            history[name][t] = getattr(result, name)

        mass_white_occ = mass_wparent * p_w_if_wparent + mass_bparent * p_w_if_bparent
        mass_blue_occ = mass_wparent * (1.0 - p_w_if_wparent) + mass_bparent * (1.0 - p_w_if_bparent)

        q_w = weighted_quantiles(talent_grid, TALENT_FAN_QUANTILES, weights=mass_white_occ)
        q_b = weighted_quantiles(talent_grid, TALENT_FAN_QUANTILES, weights=mass_blue_occ)
        for label, val in zip(TALENT_FAN_LABELS, q_w):
            fan_history[f"talent_w_{label}"][t] = float(val)
        for label, val in zip(TALENT_FAN_LABELS, q_b):
            fan_history[f"talent_b_{label}"][t] = float(val)

        if t in snapshot_periods:
            snapshots[t] = {
                "t": float(t),
                "a_w": float(a_w_path[t]),
                "a_b": float(a_b_path[t]),
                "w_w": float(result.w_w),
                "w_b": float(result.w_b),
                "talents": stacked_talents.copy(),
                "parent_is_white": parent_flags.copy(),
                # In grid mode we store expected occupation shares at each node.
                "occ_is_white": np.concatenate([p_w_if_wparent, p_w_if_bparent]),
                "p_white": np.concatenate([p_w_if_wparent, p_w_if_bparent]),
                "weights": np.concatenate([mass_wparent, mass_bparent]),
            }

        a_w_path[t + 1] = a_w_path[t] + result.h_w
        a_b_path[t + 1] = a_b_path[t] + result.h_b

        mass_wparent = params.omega * mass_white_occ + (1.0 - params.omega) * result.n_w * base_weights
        mass_bparent = params.omega * mass_blue_occ + (1.0 - params.omega) * result.n_b * base_weights

    out: dict[str, np.ndarray] = {
        "t": np.arange(params.periods, dtype=int),
        "a_w": a_w_path[:-1],
        "a_b": a_b_path[:-1],
        "a_w_next": a_w_path[1:],
        "a_b_next": a_b_path[1:],
        "a_w_terminal": np.array([a_w_path[-1]]),
        "a_b_terminal": np.array([a_b_path[-1]]),
    }
    out.update(history)
    out.update(fan_history)
    final_masses = mass_wparent + mass_bparent
    out["mean_talent"] = np.array([float(np.sum(final_masses * talent_grid))])
    return out, snapshots


def simulate(params: ModelParams) -> tuple[dict[str, np.ndarray], dict[int, dict[str, np.ndarray | float]]]:
    if params.simulation_mode == "grid":
        return simulate_grid(params)
    if params.simulation_mode != "monte_carlo":
        raise ValueError(f"Unsupported simulation_mode={params.simulation_mode!r}")

    rng = np.random.default_rng(params.seed)
    talents = build_talents(params, rng)
    parent_is_white = initial_parent_background(params, rng)

    a_w_path = np.empty(params.periods + 1, dtype=float)
    a_b_path = np.empty(params.periods + 1, dtype=float)
    a_w_path[0] = params.a_w0
    a_b_path[0] = params.a_b0

    fields = [
        "n_w",
        "n_b",
        "h_w",
        "h_b",
        "w_w",
        "w_b",
        "y",
        "p_w_given_wparent",
        "p_w_given_bparent",
        "mobility_up_b_to_w",
        "mobility_down_w_to_b",
    ]
    history = {name: np.empty(params.periods, dtype=float) for name in fields}
    fan_history: dict[str, np.ndarray] = {}
    for label in TALENT_FAN_LABELS:
        fan_history[f"talent_w_{label}"] = np.empty(params.periods, dtype=float)
        fan_history[f"talent_b_{label}"] = np.empty(params.periods, dtype=float)

    wage_guess: tuple[float, float] | None = None
    snapshot_periods = {0, params.periods - 1}
    snapshots: dict[int, dict[str, np.ndarray | float]] = {}

    for t in range(params.periods):
        result, occ_is_white, p_white, wage_guess = solve_within_period(
            talents=talents,
            parent_is_white=parent_is_white,
            a_b=a_b_path[t],
            a_w=a_w_path[t],
            params=params,
            rng=rng,
            wage_guess=wage_guess,
        )

        for name in fields:
            history[name][t] = getattr(result, name)

        q_w = weighted_quantiles(talents[occ_is_white], TALENT_FAN_QUANTILES)
        q_b = weighted_quantiles(talents[~occ_is_white], TALENT_FAN_QUANTILES)
        for label, val in zip(TALENT_FAN_LABELS, q_w):
            fan_history[f"talent_w_{label}"][t] = float(val)
        for label, val in zip(TALENT_FAN_LABELS, q_b):
            fan_history[f"talent_b_{label}"][t] = float(val)

        if t in snapshot_periods:
            snapshots[t] = {
                "t": float(t),
                "a_w": float(a_w_path[t]),
                "a_b": float(a_b_path[t]),
                "w_w": float(result.w_w),
                "w_b": float(result.w_b),
                "talents": talents.copy(),
                "parent_is_white": parent_is_white.astype(bool, copy=True),
                "occ_is_white": occ_is_white.astype(bool, copy=True),
                "p_white": p_white.copy(),
            }

        # Technology update using realized sector talent sums H_(t,s).
        a_w_path[t + 1] = a_w_path[t] + result.h_w
        a_b_path[t + 1] = a_b_path[t] + result.h_b

        # One child per parent: parental occupation updates, and talents evolve via omega transmission.
        parent_is_white = occ_is_white.copy()
        talents = transmit_talents(talents, params, rng)

    out: dict[str, np.ndarray] = {
        "t": np.arange(params.periods, dtype=int),
        "a_w": a_w_path[:-1],
        "a_b": a_b_path[:-1],
        "a_w_next": a_w_path[1:],
        "a_b_next": a_b_path[1:],
        "a_w_terminal": np.array([a_w_path[-1]]),
        "a_b_terminal": np.array([a_b_path[-1]]),
    }
    out.update(history)
    out.update(fan_history)
    out["mean_talent"] = np.array([talents.mean()])
    return out, snapshots


def save_csv(results: dict[str, np.ndarray], path: Path) -> None:
    field_order = [
        "t",
        "a_w",
        "a_b",
        "a_w_next",
        "a_b_next",
        "y",
        "w_w",
        "w_b",
        "n_w",
        "n_b",
        "h_w",
        "h_b",
        "p_w_given_wparent",
        "p_w_given_bparent",
        "mobility_up_b_to_w",
        "mobility_down_w_to_b",
    ]

    n_rows = len(results["t"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(field_order)
        for i in range(n_rows):
            writer.writerow([results[k][i] for k in field_order])


def plot_results(results: dict[str, np.ndarray], path: Path, params: ModelParams) -> None:
    t = results["t"]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    ax.plot(t, results["a_w"], label="A_W", color="#1f77b4", linewidth=2)
    ax.plot(t, results["a_b"], label="A_B", color="#d62728", linewidth=2)
    ax.set_title("Technology")
    ax.set_xlabel("t")
    ax.legend(frameon=False)

    ax = axes[0, 1]
    ax.plot(t, results["w_w"], label="w_W (per talent)", color="#1f77b4", linewidth=2)
    ax.plot(t, results["w_b"], label="w_B (per talent)", color="#d62728", linewidth=2)
    ax.set_title("Wage Rates")
    ax.set_xlabel("t")
    ax.legend(frameon=False)

    ax = axes[1, 0]
    ax.plot(t, results["n_w"], label="N_W", color="#1f77b4", linewidth=2)
    ax.plot(t, results["n_b"], label="N_B", color="#d62728", linewidth=2)
    ax.plot(t, results["mobility_up_b_to_w"], label="B→W", color="#2ca02c", linewidth=1.5, linestyle="--")
    ax.plot(t, results["mobility_down_w_to_b"], label="W→B", color="#9467bd", linewidth=1.5, linestyle="--")
    ax.set_title("Occupation Shares and Mobility")
    ax.set_xlabel("t")
    ax.set_ylim(0.0, 1.0)
    ax.legend(frameon=False, ncol=2)

    ax = axes[1, 1]
    def _plot_talent_fan(prefix: str, color: str, label: str) -> None:
        q10 = results[f"{prefix}_p10"]
        q25 = results[f"{prefix}_p25"]
        q50 = results[f"{prefix}_p50"]
        q75 = results[f"{prefix}_p75"]
        q90 = results[f"{prefix}_p90"]
        ax.fill_between(t, q10, q90, color=color, alpha=0.10)
        ax.fill_between(t, q25, q75, color=color, alpha=0.20)
        ax.plot(t, q50, color=color, linewidth=2.0, label=f"{label} median talent")

    _plot_talent_fan("talent_w", "#1f77b4", "W")
    _plot_talent_fan("talent_b", "#d62728", "B")

    ax.set_title("Talent Distribution by Occupation (fan plot)")
    ax.set_xlabel("t")
    ax.set_ylabel("Talent h")
    ax.grid(alpha=0.12)
    ax.legend(frameon=False)

    fig.suptitle("Social Mobility and Innovation Model (first-pass simulation)", y=0.995)
    add_parameter_tag(fig, params)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_talent_allocation_diagnostics(
    results: dict[str, np.ndarray],
    path: Path,
    params: ModelParams,
) -> None:
    """Plot raw talent allocation and related diagnostics over time."""
    t = results["t"]
    h_w = results["h_w"]
    h_b = results["h_b"]
    n_w = results["n_w"]
    n_b = results["n_b"]
    a_gap = results["a_w"] - results["a_b"]
    h_gap = h_w - h_b

    avg_h_w = h_w / np.maximum(n_w, 1e-12)
    avg_h_b = h_b / np.maximum(n_b, 1e-12)

    # Fan chart for worker earnings y_s(h) = w_s * h^eta_s, using occupation-specific talent quantiles.
    earnings_w = {
        label: results["w_w"] * np.power(np.maximum(results[f"talent_w_{label}"], params.mass_floor), params.eta_w)
        for label in TALENT_FAN_LABELS
    }
    earnings_b = {
        label: results["w_b"] * np.power(np.maximum(results[f"talent_b_{label}"], params.mass_floor), params.eta_b)
        for label in TALENT_FAN_LABELS
    }

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.6))

    ax = axes[0, 0]
    ax.plot(t, h_w, label="H_W (raw talent sum)", color="#1f77b4", linewidth=2)
    ax.plot(t, h_b, label="H_B (raw talent sum)", color="#d62728", linewidth=2)
    ax.set_title("Raw Talent by Sector")
    ax.set_xlabel("t")
    ax.legend(frameon=False)

    ax = axes[0, 1]
    ax.plot(t, h_gap, color="#2ca02c", linewidth=2, label="H_W - H_B")
    ax.axhline(0, color="#444444", linewidth=1)
    ax.set_title("Talent Gap and Technology Gap")
    ax.set_xlabel("t")
    ax.set_ylabel("H gap")
    ax.grid(alpha=0.12)
    ax2 = ax.twinx()
    ax2.plot(t, a_gap, color="#111111", linewidth=1.8, linestyle="--", label="A_W - A_B")
    ax2.set_ylabel("A gap")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")

    ax = axes[1, 0]
    def _plot_earnings_fan(series: dict[str, np.ndarray], color: str, label: str) -> None:
        ax.fill_between(t, series["p10"], series["p90"], color=color, alpha=0.10)
        ax.fill_between(t, series["p25"], series["p75"], color=color, alpha=0.20)
        ax.plot(t, series["p50"], color=color, linewidth=2.0, label=f"{label} median earnings")

    _plot_earnings_fan(earnings_w, "#1f77b4", "W")
    _plot_earnings_fan(earnings_b, "#d62728", "B")
    ax.set_title("Worker Earnings by Occupation (fan plot)")
    ax.set_xlabel("t")
    ax.set_ylabel(r"Earnings $y_s(h)$")
    ax.grid(alpha=0.12)
    ax.legend(frameon=False, fontsize=9)

    ax = axes[1, 1]
    ax.plot(t, avg_h_w, label="Avg talent in W = H_W / N_W", color="#1f77b4", linewidth=2)
    ax.plot(t, avg_h_b, label="Avg talent in B = H_B / N_B", color="#d62728", linewidth=2)
    ax.axhline(1.0, color="#666666", linewidth=1, linestyle=":")
    ax.set_title("Average Talent by Occupation + Headcount")
    ax.set_xlabel("t")
    ax.set_ylabel("Average talent")
    ax.grid(alpha=0.12)
    ax2 = ax.twinx()
    ax2.plot(t, n_w, label="N_W", color="#1f77b4", linewidth=1.6, linestyle="--", alpha=0.9)
    ax2.plot(t, n_b, label="N_B", color="#d62728", linewidth=1.6, linestyle="--", alpha=0.9)
    ax2.set_ylabel("Headcount share")
    ax2.set_ylim(0.0, 1.0)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=9, loc="best")

    fig.suptitle("Talent Allocation and Earnings Diagnostics", y=0.995)
    add_parameter_tag(fig, params)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def _snapshot_items(
    snapshots: dict[int, dict[str, np.ndarray | float]],
) -> list[tuple[int, str, dict[str, np.ndarray | float]]]:
    keys = sorted(snapshots.keys())
    if not keys:
        return []
    items: list[tuple[int, str, dict[str, np.ndarray | float]]] = []
    for idx, key in enumerate(keys):
        label = "Period 1" if idx == 0 else ("Period T" if idx == len(keys) - 1 else f"Period {idx + 1}")
        items.append((key, label, snapshots[key]))
    return items


def _binned_means(
    x: np.ndarray,
    y: np.ndarray,
    n_bins: int = 20,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    if x.size == 0:
        return np.array([]), np.array([])
    if x.size == 1:
        return x.copy(), y.copy()

    if weights is None:
        weights_arr = np.ones_like(x, dtype=float)
    else:
        weights_arr = np.asarray(weights, dtype=float)

    valid = np.isfinite(x) & np.isfinite(y) & np.isfinite(weights_arr) & (weights_arr > 0.0)
    if not np.any(valid):
        return np.array([]), np.array([])

    x = np.asarray(x[valid], dtype=float)
    y = np.asarray(y[valid], dtype=float)
    weights_arr = np.asarray(weights_arr[valid], dtype=float)

    if x.size == 1:
        return x.copy(), y.copy()

    order = np.argsort(x)
    x = x[order]
    y = y[order]
    weights_arr = weights_arr[order]

    if np.allclose(weights_arr, weights_arr[0]):
        edges = np.quantile(x, np.linspace(0.0, 1.0, n_bins + 1))
    else:
        cum_w = np.cumsum(weights_arr)
        total_w = float(cum_w[-1])
        if total_w <= 0.0:
            return np.array([]), np.array([])
        quantiles = np.linspace(0.0, 1.0, n_bins + 1)
        edges = np.interp(
            quantiles,
            np.concatenate(([0.0], cum_w / total_w)),
            np.concatenate(([x[0]], x)),
        )
    edges = np.unique(edges)
    if edges.size < 2:
        wsum = float(np.sum(weights_arr))
        return (
            np.array([float(np.sum(weights_arr * x) / wsum)]),
            np.array([float(np.sum(weights_arr * y) / wsum)]),
        )

    centers: list[float] = []
    means: list[float] = []
    for i in range(edges.size - 1):
        left, right = edges[i], edges[i + 1]
        if i < edges.size - 2:
            mask = (x >= left) & (x < right)
        else:
            mask = (x >= left) & (x <= right)
        if np.any(mask):
            w = weights_arr[mask]
            wsum = float(np.sum(w))
            centers.append(float(np.sum(w * x[mask]) / wsum))
            means.append(float(np.sum(w * y[mask]) / wsum))

    return np.asarray(centers), np.asarray(means)


def plot_p_w_vs_talent_snapshots(
    snapshots: dict[int, dict[str, np.ndarray | float]],
    path: Path,
    params: ModelParams,
) -> None:
    items = _snapshot_items(snapshots)
    if not items:
        return

    fig, axes = plt.subplots(1, len(items), figsize=(5.4 * len(items), 4.0), sharey=True)
    axes_arr = np.atleast_1d(axes)

    for ax, (t_idx, label, snap) in zip(axes_arr, items):
        talents = np.asarray(snap["talents"])
        occ_is_white = np.asarray(snap["occ_is_white"]).astype(float)
        p_white = np.asarray(snap["p_white"])
        weights = np.asarray(snap["weights"]) if "weights" in snap else None

        x_emp, y_emp = _binned_means(talents, occ_is_white, n_bins=18, weights=weights)
        x_mod, y_mod = _binned_means(talents, p_white, n_bins=18, weights=weights)

        ax.plot(x_emp, y_emp, color="#1f77b4", marker="o", markersize=3.5, linewidth=1.8, label="Empirical P(W|talent)")
        ax.plot(x_mod, y_mod, color="#d62728", linestyle="--", linewidth=2.0, label="Model p_W(talent)")

        ax.set_title(f"{label} (t={t_idx})")
        ax.set_xlabel("Talent")
        ax.set_ylim(0.0, 1.0)
        ax.grid(alpha=0.15)

    axes_arr[0].set_ylabel("White-collar probability / share")
    axes_arr[0].legend(frameon=False)

    fig.suptitle("Talent vs occupation choice (overall)", y=0.99)
    add_parameter_tag(fig, params)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_p_w_vs_talent_by_background_snapshots(
    snapshots: dict[int, dict[str, np.ndarray | float]],
    path: Path,
    params: ModelParams,
) -> None:
    items = _snapshot_items(snapshots)
    if not items:
        return

    fig, axes = plt.subplots(1, len(items), figsize=(5.8 * len(items), 4.2), sharey=True)
    axes_arr = np.atleast_1d(axes)

    colors = {"W_parent": "#1f77b4", "B_parent": "#d62728"}

    for ax, (t_idx, label, snap) in zip(axes_arr, items):
        talents = np.asarray(snap["talents"])
        parent_is_white = np.asarray(snap["parent_is_white"]).astype(bool)
        occ_is_white = np.asarray(snap["occ_is_white"]).astype(float)
        p_white = np.asarray(snap["p_white"])
        weights = np.asarray(snap["weights"]) if "weights" in snap else None

        for key, mask in [("W_parent", parent_is_white), ("B_parent", ~parent_is_white)]:
            if not np.any(mask):
                continue
            w_mask = weights[mask] if weights is not None else None
            x_emp, y_emp = _binned_means(talents[mask], occ_is_white[mask], n_bins=12, weights=w_mask)
            x_mod, y_mod = _binned_means(talents[mask], p_white[mask], n_bins=12, weights=w_mask)
            label_emp = "Empirical P(W|talent,parent=W)" if key == "W_parent" else "Empirical P(W|talent,parent=B)"
            label_mod = "Model p_W | parent=W" if key == "W_parent" else "Model p_W | parent=B"
            ax.plot(
                x_emp,
                y_emp,
                color=colors[key],
                marker="o",
                markersize=3.2,
                linewidth=1.6,
                alpha=0.95,
                label=label_emp,
            )
            ax.plot(
                x_mod,
                y_mod,
                color=colors[key],
                linestyle="--",
                linewidth=2.0,
                alpha=0.9,
                label=label_mod,
            )

        ax.set_title(f"{label} (t={t_idx})")
        ax.set_xlabel("Talent")
        ax.set_ylim(0.0, 1.0)
        ax.grid(alpha=0.15)

    axes_arr[0].set_ylabel("White-collar probability / share")

    # De-duplicate legend entries from both panels.
    handles, labels = axes_arr[0].get_legend_handles_labels()
    seen: set[str] = set()
    dedup_handles = []
    dedup_labels = []
    for h, l in zip(handles, labels):
        if l not in seen:
            dedup_handles.append(h)
            dedup_labels.append(l)
            seen.add(l)
    axes_arr[0].legend(dedup_handles, dedup_labels, frameon=False, fontsize=9)

    fig.suptitle("Talent vs occupation choice, conditional on parental background", y=0.99)
    add_parameter_tag(fig, params)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_production_substitution_pattern(params: ModelParams, path: Path) -> None:
    # Multi-panel isoquant comparison for different rho values (same alpha, same axes).
    rho_values = (0.05, 0.25, 0.50, 0.75, 0.95)
    q_b = np.linspace(0.03, 1.50, 240)
    q_w = np.linspace(0.03, 1.50, 240)
    qb_grid, qw_grid = np.meshgrid(q_b, q_w)

    def ces_output(rho: float) -> np.ndarray:
        if abs(rho) < 1e-12:
            return (qb_grid ** params.alpha) * (qw_grid ** (1.0 - params.alpha))
        z = params.alpha * qb_grid**rho + (1.0 - params.alpha) * qw_grid**rho
        return z ** (1.0 / rho)

    surfaces = [ces_output(rho) for rho in rho_values]
    common_min = max(float(np.min(s)) for s in surfaces)
    common_max = min(float(np.max(s)) for s in surfaces)
    span = max(common_max - common_min, 1e-6)
    levels = np.linspace(common_min + 0.18 * span, common_min + 0.90 * span, 6)
    levels = np.unique(levels)

    fig, axes = plt.subplots(2, 3, figsize=(13.8, 8.2), sharex=True, sharey=True)
    axes_arr = np.atleast_1d(axes).ravel()

    q_b_line = np.linspace(0.03, 0.97, 160)
    q_w_line = 1.0 - q_b_line

    for ax, rho, surface in zip(axes_arr, rho_values, surfaces):
        contour = ax.contour(qb_grid, qw_grid, surface, levels=levels, colors="#1f1f1f", linewidths=1.2)
        ax.clabel(contour, inline=True, fontsize=7, fmt="%.2f")
        ax.plot(
            q_b_line,
            q_w_line,
            color="#1f77b4",
            linestyle="--",
            linewidth=1.3,
            alpha=0.9,
        )

        sigma = 1.0 / (1.0 - rho) if abs(1.0 - rho) >= 1e-12 else float("inf")
        sigma_text = f"{sigma:.2f}" if np.isfinite(sigma) else "infty"
        ax.set_title(f"rho={rho:.2f}, sigma={sigma_text}")
        ax.grid(alpha=0.10)
        ax.set_xlim(q_b.min(), q_b.max())
        ax.set_ylim(q_w.min(), q_w.max())

    for ax in axes_arr[len(rho_values):]:
        ax.axis("off")

    axes_arr[0].set_ylabel(r"White-collar effective talent $Q_W$")
    axes_arr[3].set_ylabel(r"White-collar effective talent $Q_W$")
    for ax in axes_arr[: len(rho_values)]:
        ax.set_xlabel(r"Blue-collar effective talent $Q_B$")

    fig.suptitle("CES production isoquants by substitutability (higher rho = more substitutable)", y=0.97)
    fig.text(
        0.5,
        0.025,
        r"All panels use $A_B = A_W = 1$ and the same contour levels for comparability; dashed line shows $Q_B + Q_W = 1$.",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#444444",
    )
    fig.text(
        0.99,
        0.006,
        "alpha={:.2f}; rho panels = 0.05, 0.25, 0.50, 0.75, 0.95".format(params.alpha),
        ha="right",
        va="bottom",
        fontsize=9,
        color="#444444",
    )
    fig.tight_layout(rect=(0.0, 0.05, 1.0, 0.95))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_talent_transmission_omega_comparison(path: Path) -> None:
    """Illustrate the parent-child talent mapping for several omega values.

    This is a conceptual diagnostic for the transmission rule itself (not a full simulation run).
    """
    omegas = (0.00, 0.50, 1.00)
    n_points = 4_000
    rng = np.random.default_rng(12345)

    fig, axes = plt.subplots(1, len(omegas), figsize=(12.4, 4.2), sharex=True, sharey=True)
    axes_arr = np.atleast_1d(axes)

    x_line = np.array([0.0, 1.0], dtype=float)
    legend_handles = None
    legend_labels = None

    for ax, omega in zip(axes_arr, omegas):
        parent = rng.uniform(0.0, 1.0, size=n_points)
        inherit = rng.random(n_points) < omega
        redraw = rng.uniform(0.0, 1.0, size=n_points)
        child = np.where(inherit, parent, redraw)

        if np.any(~inherit):
            ax.scatter(
                parent[~inherit],
                child[~inherit],
                s=6,
                alpha=0.18,
                color="#6f6f6f",
                linewidths=0.0,
                label="Redrawn child talent",
            )
        if np.any(inherit):
            ax.scatter(
                parent[inherit],
                child[inherit],
                s=6,
                alpha=0.28,
                color="#1f77b4",
                linewidths=0.0,
                label="Inherited exactly",
            )

        ax.plot(x_line, x_line, color="#d62728", linestyle="--", linewidth=1.2, label=r"$h_{t+1}=h_t$")
        ax.set_title(f"omega={omega:.2f}")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.12)

        if legend_handles is None:
            legend_handles, legend_labels = ax.get_legend_handles_labels()

    axes_arr[0].set_ylabel(r"Child talent $h_{t+1}$")
    for ax in axes_arr:
        ax.set_xlabel(r"Parent talent $h_t$")

    fig.suptitle("Talent transmission rule: parent-child talent mapping for different omega", y=0.99)
    if legend_handles and legend_labels:
        fig.legend(legend_handles, legend_labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.95))
    fig.text(
        0.5,
        0.02,
        r"Synthetic draws from the transmission rule with parent talents and redraws from $U(0,1)$.",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#444444",
    )
    fig.tight_layout(rect=(0.0, 0.06, 1.0, 0.90))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def parse_args() -> ModelParams:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--periods", type=int, default=80)
    parser.add_argument("--n-agents", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--simulation-mode",
        choices=["monte_carlo", "grid"],
        default="monte_carlo",
        help="Monte Carlo agent simulation or deterministic weighted-grid approximation.",
    )
    parser.add_argument(
        "--grid-size",
        type=int,
        default=401,
        help="Number of quantile grid points for deterministic grid mode.",
    )

    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--rho", type=float, default=0.4)

    parser.add_argument("--phi", type=float, default=0.35)
    parser.add_argument("--c-g", type=float, default=0.15)
    parser.add_argument("--omega", type=float, default=0.7)
    parser.add_argument("--eta-w", type=float, default=1.0)
    parser.add_argument("--eta-b", type=float, default=1.0)

    parser.add_argument("--a-w0", type=float, default=1.25)
    parser.add_argument("--a-b0", type=float, default=1.0)
    parser.add_argument("--init-parent-white-share", type=float, default=0.5)

    parser.add_argument(
        "--talent-dist",
        choices=["lognormal", "uniform"],
        default="lognormal",
    )
    parser.add_argument("--talent-lognorm-mean", type=float, default=0.0)
    parser.add_argument("--talent-lognorm-sigma", type=float, default=0.35)
    parser.add_argument("--talent-uniform-low", type=float, default=0.5)
    parser.add_argument("--talent-uniform-high", type=float, default=1.5)

    parser.add_argument("--eq-tol", type=float, default=1e-8)
    parser.add_argument("--eq-max-iter", type=int, default=500)
    parser.add_argument("--eq-damping", type=float, default=0.2)
    parser.add_argument("--output-stem", type=str, default="social_mobility_innovation_baseline")

    args = parser.parse_args()
    return ModelParams(
        periods=args.periods,
        n_agents=args.n_agents,
        seed=args.seed,
        simulation_mode=args.simulation_mode,
        grid_size=args.grid_size,
        alpha=args.alpha,
        rho=args.rho,
        phi=args.phi,
        c_g=args.c_g,
        omega=args.omega,
        eta_w=args.eta_w,
        eta_b=args.eta_b,
        a_w0=args.a_w0,
        a_b0=args.a_b0,
        init_parent_white_share=args.init_parent_white_share,
        talent_dist=args.talent_dist,
        talent_lognorm_mean=args.talent_lognorm_mean,
        talent_lognorm_sigma=args.talent_lognorm_sigma,
        talent_uniform_low=args.talent_uniform_low,
        talent_uniform_high=args.talent_uniform_high,
        eq_tol=args.eq_tol,
        eq_max_iter=args.eq_max_iter,
        eq_damping=args.eq_damping,
        output_stem=args.output_stem,
    )


def main() -> None:
    params = parse_args()
    results, snapshots = simulate(params)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    stem = params.output_stem
    fig_path = FIGURES_DIR / f"{stem}.png"
    talent_diag_fig_path = FIGURES_DIR / f"{stem}_talent_allocation_diagnostics.png"
    p_w_talent_fig_path = FIGURES_DIR / f"{stem}_p_w_talent_snapshots.png"
    p_w_bg_fig_path = FIGURES_DIR / f"{stem}_p_w_talent_by_background_snapshots.png"
    prod_fig_path = FIGURES_DIR / f"{stem}_production_isoquants.png"
    transmission_fig_path = FIGURES_DIR / "talent_transmission_omega_comparison.png"
    csv_path = RESULTS_DIR / f"{stem}.csv"

    plot_results(results, fig_path, params)
    plot_talent_allocation_diagnostics(results, talent_diag_fig_path, params)
    plot_p_w_vs_talent_snapshots(snapshots, p_w_talent_fig_path, params)
    plot_p_w_vs_talent_by_background_snapshots(snapshots, p_w_bg_fig_path, params)
    plot_production_substitution_pattern(params, prod_fig_path)
    plot_talent_transmission_omega_comparison(transmission_fig_path)
    save_csv(results, csv_path)

    t_last = -1
    print(f"Saved figure: {fig_path}")
    print(f"Saved figure: {talent_diag_fig_path}")
    print(f"Saved figure: {p_w_talent_fig_path}")
    print(f"Saved figure: {p_w_bg_fig_path}")
    print(f"Saved figure: {prod_fig_path}")
    print(f"Saved figure: {transmission_fig_path}")
    print(f"Saved csv:    {csv_path}")
    print(
        "Final period summary: "
        f"A_W={results['a_w_next'][t_last]:.3f}, "
        f"A_B={results['a_b_next'][t_last]:.3f}, "
        f"N_W={results['n_w'][t_last]:.3f}, "
        f"H_W={results['h_w'][t_last]:.3f}, "
        f"w_W={results['w_w'][t_last]:.3f}, "
        f"w_B={results['w_b'][t_last]:.3f}, "
        f"mode={params.simulation_mode}, "
        f"c_g={params.c_g:.2f}, "
        f"omega={params.omega:.2f}, "
        f"eta_W={params.eta_w:.2f}, "
        f"eta_B={params.eta_b:.2f}"
    )


if __name__ == "__main__":
    main()
