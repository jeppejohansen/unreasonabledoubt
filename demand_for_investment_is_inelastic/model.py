"""
Lifecycle savings model with portfolio choice and retirement.

Solves a finite-horizon problem (T_work=30 working periods + T_ret=10 retirement
periods) where households choose consumption and portfolio allocation between a
risk-free bond and a risky stock. During working years, households receive
deterministic labor income. During retirement, income drops to zero.

The key result: total savings is nearly invariant to expected stock returns
(inelastic savings supply) because the retirement funding need is fixed,
while portfolio allocation shifts strongly with returns.
"""

import numpy as np
from scipy.optimize import minimize_scalar

# ── Parameters ───────────────────────────────────────────────────────────────

GAMMA = 5          # CRRA risk aversion
BETA = 0.96        # discount factor
R_F = 1.02         # risk-free gross return
E_RS = 1.06        # expected gross stock return (baseline)
SIGMA_S = 0.35     # stock return volatility (log-normal)
Y_BAR = 1.0        # labor income during working years
T_WORK = 30        # working periods (with income)
T_RET = 10         # retirement periods (no income)
T = T_WORK + T_RET # total periods

# Grid for wealth (cash-on-hand) — log-spaced for resolution at low wealth
W_MIN = 0.01
W_MAX = 40.0
N_W = 150
W_GRID = np.exp(np.linspace(np.log(W_MIN), np.log(W_MAX), N_W))

# ── Supply curve calibration ──────────────────────────────────────────────────
# See equilibrium_math.md for derivation.
# Stock market clearing: R_s = 1 + E/(α·S)  →  E/S = (R_s - 1)·α
# Bond market clearing:  R_f = 1 + B/((1-α)·S) → B/S = (R_f - 1)·(1-α)
# Calibrated at baseline: α=0.374, R_s=1.06, R_f=1.02
ALPHA_EQ = 0.374
E_OVER_S = (E_RS - 1) * ALPHA_EQ        # ≈ 0.02244
B_OVER_S = (R_F - 1) * (1 - ALPHA_EQ)   # ≈ 0.01252


def stock_supply_return(alpha):
    """Expected stock return implied by market clearing at portfolio share α."""
    return 1 + E_OVER_S / alpha


def bond_supply_return(alpha):
    """Bond yield implied by market clearing at portfolio share α."""
    return 1 + B_OVER_S / (1 - alpha)

# Quadrature points for stock return shocks
N_SHOCKS = 7


def crra(c, gamma):
    """CRRA utility."""
    if gamma == 1.0:
        return np.log(np.maximum(c, 1e-10))
    return np.maximum(c, 1e-10) ** (1 - gamma) / (1 - gamma)


def gauss_hermite_lognormal(mu_log, sigma_log, n):
    """Gauss-Hermite quadrature nodes/weights for lognormal expectations."""
    xi, wi = np.polynomial.hermite.hermgauss(n)
    nodes = np.exp(mu_log + np.sqrt(2) * sigma_log * xi)
    weights = wi / np.sqrt(np.pi)
    return nodes, weights


def build_return_quadrature(expected_stock_return, sigma_s, n):
    """Build quadrature grid for stock return shocks."""
    mu_rs = np.log(expected_stock_return) - sigma_s**2 / 2
    rs_nodes, rs_weights = gauss_hermite_lognormal(mu_rs, sigma_s, n)
    return rs_nodes, rs_weights


def income(t, y_bar=Y_BAR, t_work=T_WORK):
    """Labor income at period t: y_bar during working years, 0 in retirement."""
    if t < t_work:
        return y_bar
    return 0.0


def solve_model(expected_stock_return=E_RS, gamma=GAMMA, beta=BETA, r_f=R_F,
                sigma_s=SIGMA_S, y_bar=Y_BAR, t_work=T_WORK, t_ret=T_RET,
                w_grid=None):
    """
    Solve the lifecycle model via backward induction.

    Uses nested 1D optimization: outer over consumption, inner over portfolio
    share. Stock returns are stochastic; income is deterministic (y_bar during
    working years, 0 in retirement).

    Returns dict with policy functions and value function arrays (T x N_W).
    """
    if w_grid is None:
        w_grid = W_GRID
    n_w = len(w_grid)
    t_total = t_work + t_ret

    rs_nodes, rs_weights = build_return_quadrature(
        expected_stock_return, sigma_s, N_SHOCKS
    )

    c_policy = np.zeros((t_total, n_w))
    alpha_policy = np.zeros((t_total, n_w))
    value = np.zeros((t_total, n_w))

    # Terminal period: consume everything
    c_policy[t_total - 1, :] = w_grid
    alpha_policy[t_total - 1, :] = 0.0
    value[t_total - 1, :] = crra(w_grid, gamma)

    for t in range(t_total - 2, -1, -1):
        v_next = value[t + 1, :]
        y_next = income(t + 1, y_bar, t_work)

        for i_w in range(n_w):
            w = w_grid[i_w]
            if w < 1e-8:
                c_policy[t, i_w] = w
                alpha_policy[t, i_w] = 0.0
                value[t, i_w] = crra(w, gamma)
                continue

            def _expected_value(savings, alpha):
                """Compute E[V(w')] for given savings and portfolio share."""
                R_p = alpha * rs_nodes + (1 - alpha) * r_f
                w_next = R_p * savings + y_next
                v_interp = np.interp(w_next, w_grid, v_next)
                return np.dot(rs_weights, v_interp)

            def _optimal_alpha(savings):
                """Find optimal portfolio share for given savings level."""
                if savings < 1e-10:
                    return 0.0, 0.0
                def neg_ev(alpha):
                    return -_expected_value(savings, alpha)
                res = minimize_scalar(neg_ev, bounds=(0.0, 1.0), method='bounded',
                                      options={'xatol': 1e-4})
                return res.x, -res.fun

            def _neg_total_value(c):
                """Negative of total value (utility + continuation) for given c."""
                if c <= 0 or c >= w:
                    return 1e10
                savings = w - c
                alpha_star, ev_star = _optimal_alpha(savings)
                return -(crra(c, gamma) + beta * ev_star)

            res_c = minimize_scalar(_neg_total_value,
                                    bounds=(0.01 * w, 0.99 * w),
                                    method='bounded',
                                    options={'xatol': 1e-5 * w})

            best_c = res_c.x
            best_savings = w - best_c
            best_alpha, best_ev = _optimal_alpha(best_savings)
            best_val = crra(best_c, gamma) + beta * best_ev

            c_policy[t, i_w] = best_c
            alpha_policy[t, i_w] = best_alpha
            value[t, i_w] = best_val

    return {
        "c_policy": c_policy,
        "alpha_policy": alpha_policy,
        "value": value,
        "w_grid": w_grid,
    }


def simulate_households(policy, n_households=5000, expected_stock_return=E_RS,
                        r_f=R_F, sigma_s=SIGMA_S, y_bar=Y_BAR,
                        t_work=T_WORK, t_ret=T_RET):
    """
    Simulate N households forward using the solved policy functions.
    Returns average savings rate and portfolio share over the lifecycle.
    """
    rng = np.random.default_rng(42)
    w_grid = policy["w_grid"]
    c_pol = policy["c_policy"]
    a_pol = policy["alpha_policy"]
    t_total = t_work + t_ret

    # Initial wealth = first period of income
    wealth = np.ones(n_households) * y_bar

    savings_rates = []
    portfolio_shares = []
    all_savings = []
    all_alpha = []

    for t in range(t_total - 1):
        c = np.interp(wealth, w_grid, c_pol[t])
        alpha = np.interp(wealth, w_grid, a_pol[t])

        c = np.clip(c, 0.01, wealth - 0.01)
        alpha = np.clip(alpha, 0.0, 1.0)

        savings = wealth - c
        savings_rate = savings / wealth
        savings_rates.append(np.mean(savings_rate))
        portfolio_shares.append(np.mean(alpha))
        all_savings.append(savings.copy())
        all_alpha.append(alpha.copy())

        # Stochastic stock returns
        mu_rs = np.log(expected_stock_return) - sigma_s**2 / 2
        stock_returns = rng.lognormal(mu_rs, sigma_s, n_households)

        R_p = alpha * stock_returns + (1 - alpha) * r_f
        y_next = income(t + 1, y_bar, t_work)
        wealth = R_p * savings + y_next
        wealth = np.maximum(wealth, 0.01)

    # Aggregate wealth and asset holdings across all periods
    # In a stationary OLG economy, averaging across periods ≈ averaging
    # across cohorts alive at the same time.
    all_savings = np.array(all_savings)         # (T-1, N)
    all_alpha = np.array(all_alpha)             # (T-1, N)
    avg_stock_holdings = np.mean(all_alpha * all_savings)
    avg_bond_holdings = np.mean((1 - all_alpha) * all_savings)
    avg_savings_amount = np.mean(all_savings)

    return {
        "avg_savings_rate": np.mean(savings_rates),
        "avg_portfolio_share": np.mean(portfolio_shares),
        "savings_rates_by_period": np.array(savings_rates),
        "portfolio_shares_by_period": np.array(portfolio_shares),
        "avg_stock_holdings": float(avg_stock_holdings),
        "avg_bond_holdings": float(avg_bond_holdings),
        "avg_savings_amount": float(avg_savings_amount),
    }


def sweep_expected_returns(return_range=None, **kwargs):
    """
    Vary expected stock return and record aggregate savings rate and
    portfolio share at each level.
    """
    if return_range is None:
        return_range = np.linspace(0.90, 1.10, 11)

    results = []
    for e_rs in return_range:
        print(f"  Solving for E[R_s] = {e_rs:.3f} ...")
        policy = solve_model(expected_stock_return=e_rs, **kwargs)
        sim = simulate_households(policy, expected_stock_return=e_rs, **kwargs)
        results.append({
            "expected_return": e_rs,
            "avg_savings_rate": sim["avg_savings_rate"],
            "avg_portfolio_share": sim["avg_portfolio_share"],
        })
        print(f"    savings rate = {sim['avg_savings_rate']:.4f}, "
              f"portfolio share = {sim['avg_portfolio_share']:.4f}")

    return results


def solve_general_equilibrium(E_agg=None, B_agg=None,
                              r_s_init=E_RS, r_f_init=R_F,
                              tol=5e-4, max_iter=15, damping=0.5,
                              **kwargs):
    """
    Find equilibrium (R_s, R_f) where S = I:

        α · S = E_agg / (R_s - 1)     (stock market clears)
        (1-α) · S = B_agg / (R_f - 1) (bond market clears)

    where S (avg savings amount) and α (avg portfolio share) come from the
    lifecycle model solved at (R_s, R_f).

    E_agg and B_agg are aggregate earnings and bond supply, calibrated at the
    baseline so that the initial (R_s, R_f) is consistent.

    Uses dampened iteration: R_new = damping * R_implied + (1-damping) * R_old.
    """
    # Step 0: calibrate E_agg and B_agg at the initial point
    print(f"  Calibrating asset supply at R_s={r_s_init:.4f}, R_f={r_f_init:.4f}...")
    policy_0 = solve_model(expected_stock_return=r_s_init, r_f=r_f_init, **kwargs)
    sim_0 = simulate_households(policy_0, expected_stock_return=r_s_init,
                                r_f=r_f_init, **kwargs)

    S_0 = sim_0["avg_savings_amount"]
    alpha_0 = sim_0["avg_portfolio_share"]

    if E_agg is None:
        E_agg = alpha_0 * S_0 * (r_s_init - 1)
    if B_agg is None:
        B_agg = (1 - alpha_0) * S_0 * (r_f_init - 1)

    print(f"  Calibrated: E_agg={E_agg:.6f}, B_agg={B_agg:.6f}")
    print(f"  Baseline: S={S_0:.4f}, α={alpha_0:.4f}")

    r_s, r_f = r_s_init, r_f_init

    for iteration in range(max_iter):
        policy = solve_model(expected_stock_return=r_s, r_f=r_f, **kwargs)
        sim = simulate_households(policy, expected_stock_return=r_s, r_f=r_f,
                                  **kwargs)

        S = sim["avg_savings_amount"]
        alpha = sim["avg_portfolio_share"]
        stock_holdings = sim["avg_stock_holdings"]
        bond_holdings = sim["avg_bond_holdings"]

        # Implied returns from market clearing
        r_s_implied = 1 + E_agg / stock_holdings if stock_holdings > 1e-10 else 2.0
        r_f_implied = 1 + B_agg / bond_holdings if bond_holdings > 1e-10 else 1.5

        # Convergence check
        err_s = abs(r_s_implied - r_s)
        err_f = abs(r_f_implied - r_f)
        print(f"  iter {iteration+1}: R_s={r_s:.5f} R_f={r_f:.5f}  "
              f"S={S:.4f} α={alpha:.4f}  "
              f"R_s_impl={r_s_implied:.5f} R_f_impl={r_f_implied:.5f}  "
              f"err=({err_s:.5f}, {err_f:.5f})")

        if err_s < tol and err_f < tol:
            print(f"  Converged after {iteration+1} iterations.")
            break

        # Dampened update
        r_s = damping * r_s_implied + (1 - damping) * r_s
        r_f = damping * r_f_implied + (1 - damping) * r_f

        # Safety: keep returns positive
        r_s = max(r_s, 1.001)
        r_f = max(r_f, 1.001)
    else:
        print(f"  Warning: did not converge after {max_iter} iterations.")

    return {
        "r_s": float(r_s),
        "r_f": float(r_f),
        "premium": float(r_s - r_f),
        "avg_savings_rate": sim["avg_savings_rate"],
        "avg_portfolio_share": alpha,
        "avg_savings_amount": S,
        "avg_stock_holdings": stock_holdings,
        "avg_bond_holdings": bond_holdings,
        "E_agg": float(E_agg),
        "B_agg": float(B_agg),
        "converged": bool(err_s < tol and err_f < tol),
    }


def sweep_general_equilibrium(E_agg_range=None, B_agg_range=None,
                              baseline_ge=None, **kwargs):
    """
    Comparative statics around the GE equilibrium.

    Vary E_agg (earnings supply) and/or B_agg (bond supply) and find the
    new equilibrium each time. Shows how changes in asset supply move prices.
    """
    if baseline_ge is None:
        baseline_ge = solve_general_equilibrium(**kwargs)

    E_base = baseline_ge["E_agg"]
    B_base = baseline_ge["B_agg"]

    results = [baseline_ge]

    # Vary E_agg (stock supply) holding B fixed
    if E_agg_range is not None:
        for E_mult in E_agg_range:
            if E_mult == 1.0:
                continue
            print(f"\n  E_agg = {E_mult:.2f}x baseline...")
            ge = solve_general_equilibrium(
                E_agg=E_base * E_mult, B_agg=B_base,
                r_s_init=baseline_ge["r_s"], r_f_init=baseline_ge["r_f"],
                **kwargs
            )
            ge["E_multiplier"] = E_mult
            ge["B_multiplier"] = 1.0
            results.append(ge)

    # Vary B_agg (bond supply) holding E fixed
    if B_agg_range is not None:
        for B_mult in B_agg_range:
            if B_mult == 1.0:
                continue
            print(f"\n  B_agg = {B_mult:.2f}x baseline...")
            ge = solve_general_equilibrium(
                E_agg=E_base, B_agg=B_base * B_mult,
                r_s_init=baseline_ge["r_s"], r_f_init=baseline_ge["r_f"],
                **kwargs
            )
            ge["E_multiplier"] = 1.0
            ge["B_multiplier"] = B_mult
            results.append(ge)

    return results


def sweep_supply_curve(alpha_range=None, E_agg=None, B_agg=None,
                       S_agg=None, **kwargs):
    """
    Sweep along the supply curve: for each candidate α, compute the
    (R_s, R_f) pair implied by market clearing, solve the model at those
    returns, and record what α the model actually produces.

    Where model_α ≈ input_α = general equilibrium.

    If E_agg, B_agg, S_agg are provided, uses those for the supply curves
    instead of the module-level constants.
    """
    if alpha_range is None:
        alpha_range = np.linspace(0.10, 0.60, 11)

    results = []
    for alpha_in in alpha_range:
        if E_agg is not None and S_agg is not None:
            r_s = 1 + E_agg / (alpha_in * S_agg)
        else:
            r_s = stock_supply_return(alpha_in)

        if B_agg is not None and S_agg is not None:
            r_f = 1 + B_agg / ((1 - alpha_in) * S_agg)
        else:
            r_f = bond_supply_return(alpha_in)

        premium = r_s - r_f

        print(f"  α_input={alpha_in:.3f}  R_s={r_s:.4f}  R_f={r_f:.4f}  "
              f"premium={premium:.4f}")
        policy = solve_model(expected_stock_return=r_s, r_f=r_f, **kwargs)
        sim = simulate_households(policy, expected_stock_return=r_s, r_f=r_f,
                                  **kwargs)

        results.append({
            "alpha_input": float(alpha_in),
            "expected_stock_return": float(r_s),
            "risk_free_rate": float(r_f),
            "premium": float(premium),
            "avg_savings_rate": sim["avg_savings_rate"],
            "avg_portfolio_share": sim["avg_portfolio_share"],
            "avg_stock_holdings": sim["avg_stock_holdings"],
            "avg_bond_holdings": sim["avg_bond_holdings"],
            "avg_savings_amount": sim["avg_savings_amount"],
        })
        print(f"    model α = {sim['avg_portfolio_share']:.4f}  "
              f"savings = {sim['avg_savings_rate']:.4f}  "
              f"stock_hold = {sim['avg_stock_holdings']:.4f}  "
              f"bond_hold = {sim['avg_bond_holdings']:.4f}")

    return results


def sweep_savings_level(s_multipliers=None, baseline_ge=None, **kwargs):
    """
    Comparative statics: what happens when total savings S changes,
    holding asset supply (E, B) fixed?

    Varying S up by factor k is equivalent to scaling E_agg and B_agg
    down by 1/k (more savers chasing the same assets).

    Returns a list of GE results, one per savings multiplier.
    """
    if s_multipliers is None:
        s_multipliers = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5]

    if baseline_ge is None:
        baseline_ge = solve_general_equilibrium(**kwargs)

    E_base = baseline_ge["E_agg"]
    B_base = baseline_ge["B_agg"]
    S_base = baseline_ge["avg_savings_amount"]

    results = []
    for k in s_multipliers:
        print(f"\n  S = {k:.1f}x baseline (E_agg/k={E_base/k:.6f}, B_agg/k={B_base/k:.6f})...")
        if k == 1.0:
            ge = baseline_ge.copy()
        else:
            ge = solve_general_equilibrium(
                E_agg=E_base / k, B_agg=B_base / k,
                r_s_init=baseline_ge["r_s"], r_f_init=baseline_ge["r_f"],
                **kwargs
            )
        ge["s_multiplier"] = k
        ge["total_savings_index"] = k * S_base
        # P/E = price / earnings = stock_holdings / (E_agg/k)
        # But more intuitive: P/E = 1 / (R_s - 1)
        ge["pe_ratio"] = 1.0 / (ge["r_s"] - 1)
        results.append(ge)

    return results


if __name__ == "__main__":
    import json
    from pathlib import Path

    print("Solving lifecycle model with retirement...")
    print(f"  gamma={GAMMA}, beta={BETA}, R_f={R_F}, sigma_s={SIGMA_S}")
    print(f"  T_work={T_WORK}, T_ret={T_RET}, Y_bar={Y_BAR}")

    # ── Sweep 1: vary E[R_s] with R_f fixed (partial equilibrium) ──
    print("\n── Sweep 1: Partial equilibrium (R_f fixed) ─────────")
    results = sweep_expected_returns()

    print(f"\n{'E[R_s]':>8s}  {'Savings Rate':>13s}  {'Stock Share':>12s}")
    for r in results:
        print(f"{r['expected_return']:8.3f}  {r['avg_savings_rate']:13.4f}  "
              f"{r['avg_portfolio_share']:12.4f}")

    out_path = Path(__file__).parent / "sweep_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {out_path}")

    # ── Sweep 2: General equilibrium (S = I) ──
    print("\n── Sweep 2: General equilibrium (S = I) ──")
    print("Finding baseline equilibrium...")
    baseline_ge = solve_general_equilibrium()

    print(f"\nBaseline GE:")
    print(f"  R_s = {baseline_ge['r_s']:.4f}  ({(baseline_ge['r_s']-1)*100:.2f}%)")
    print(f"  R_f = {baseline_ge['r_f']:.4f}  ({(baseline_ge['r_f']-1)*100:.2f}%)")
    print(f"  Premium = {baseline_ge['premium']*100:.2f}pp")
    print(f"  α = {baseline_ge['avg_portfolio_share']:.4f}")
    print(f"  Savings rate = {baseline_ge['avg_savings_rate']:.4f}")

    ge_path = Path(__file__).parent / "ge_results.json"
    with open(ge_path, "w") as f:
        json.dump(baseline_ge, f, indent=2)
    print(f"Saved to {ge_path}")

    # ── Sweep 3: vary R_s with endogenous R_f ──
    print("\n── Sweep 3: R_s sweep with endogenous R_f ──")
    E_agg = baseline_ge["E_agg"]
    B_agg = baseline_ge["B_agg"]
    ge_sweep = []
    for r_s_input in np.arange(1.03, 1.16, 0.02):
        print(f"\nSweeping expected stock returns with endogenous R_f...")
        # At each R_s, iterate R_f to clear the bond market
        r_f = baseline_ge["r_f"]
        for _ in range(10):
            policy = solve_model(expected_stock_return=r_s_input, r_f=r_f)
            sim = simulate_households(policy, expected_stock_return=r_s_input, r_f=r_f)
            r_f_implied = 1 + B_agg / sim["avg_bond_holdings"]
            if abs(r_f_implied - r_f) < 1e-4:
                break
            r_f = 0.5 * r_f_implied + 0.5 * r_f
            r_f = max(r_f, 1.001)

        r_s_implied = 1 + E_agg / sim["avg_stock_holdings"]
        ge_sweep.append({
            "r_s_input": float(r_s_input),
            "r_f": float(r_f),
            "r_s_implied": float(r_s_implied),
            "avg_savings_rate": sim["avg_savings_rate"],
            "avg_portfolio_share": sim["avg_portfolio_share"],
            "avg_stock_holdings": sim["avg_stock_holdings"],
            "avg_bond_holdings": sim["avg_bond_holdings"],
            "avg_savings_amount": sim["avg_savings_amount"],
        })
        print(f"  R_s={r_s_input:.4f}  R_f={r_f:.4f}  R_s_impl={r_s_implied:.4f}  "
              f"alpha={sim['avg_portfolio_share']:.4f}  savings={sim['avg_savings_rate']:.4f}  "
              f"stock_hold={sim['avg_stock_holdings']:.4f}")

    ge_sweep_path = Path(__file__).parent / "ge_sweep_results.json"
    with open(ge_sweep_path, "w") as f:
        json.dump(ge_sweep, f, indent=2)
    print(f"Saved to {ge_sweep_path}")

    # ── Sweep 4: vary total savings level ──
    print("\n── Sweep 4: Savings level comparative statics ──")
    s_sweep = sweep_savings_level(
        s_multipliers=[0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5],
        baseline_ge=baseline_ge,
    )

    s_sweep_path = Path(__file__).parent / "savings_sweep_results.json"
    with open(s_sweep_path, "w") as f:
        json.dump(s_sweep, f, indent=2)
    print(f"Saved to {s_sweep_path}")
