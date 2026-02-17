# Assumptions: Demand for Investment Is Inelastic

Working document laying out the model assumptions for the blog post.

## The Question

When expected returns on stocks fall, do households save less? How elastic is the demand for savings/investment with respect to asset returns?

## Assets

1. **Risk-free asset: government bonds.** Fixed real return R_f (e.g., ~2%). The supply of government bonds is determined by fiscal policy — exogenous to household decisions.

2. **Risky asset: stocks (equity claims on firms).** Expected return E[R_s] > R_f (the equity premium). Returns are stochastic with volatility sigma_s.

3. **Stock of equities is (approximately) perfectly inelastic in the short run.** Firms have a fixed capital stock at any moment; new equity issuance responds slowly. So the supply of stocks is essentially vertical — the price (and hence expected return) adjusts to clear the market, not the quantity.

## Households (Supply of Savings)

- **Buffer stock model.** Households face uninsurable labor income risk and save both to smooth consumption and to self-insure against bad shocks (precautionary motive).

- **CRRA preferences.** Utility u(c) = c^(1-gamma)/(1-gamma). Risk aversion parameter gamma governs both the willingness to substitute consumption over time and aversion to risk.

- **Two choice margins each period:**
  1. How much to consume vs. save (total savings)
  2. How to allocate savings between bonds and stocks (portfolio choice)

- **Income uncertainty.** Labor income Y_t subject to transitory shocks: Y_t = Y_bar * xi_t, where log(xi_t) ~ N(-sigma_xi^2/2, sigma_xi^2).

- **Borrowing constraint.** Households cannot borrow: savings S_t >= 0.

- **No short-selling.** Portfolio share in stocks alpha_t in [0, 1].

## Firms / Capital Demand (to be developed)

- **Neoclassical production.** Firms use capital and labor; marginal product of capital is decreasing (Cobb-Douglas or similar).

- **Capital demand is downward-sloping in the required return.** As the cost of capital rises, firms want less of it.

- **Key question: how elastic is capital demand?** If firms have good substitution possibilities between capital and labor, demand is more elastic. If production is more Leontief-like, demand is inelastic too.

## The Core Mechanism

Two competing forces when expected stock returns fall:

1. **Substitution effect:** Saving is less rewarding, so consume more today. (Pushes savings down.)

2. **Precautionary / income effect:** Lower returns mean your wealth grows slower, so you need to save more to maintain the same buffer against bad shocks. (Pushes savings up.)

These roughly cancel for total savings. But portfolio allocation is highly elastic — households shift from stocks to bonds.

## Supply-Demand Framing

- **Supply of savings (from households):** Nearly vertical (inelastic). Precautionary motives dominate the return incentive.

- **Demand for capital (from firms):** Downward-sloping. Lower cost of capital means firms want more.

- **Implication:** Because savings supply is inelastic, shifts in capital demand mostly move the return on capital (the price), not the quantity of investment. Policies that try to boost investment by making saving more attractive have limited effect on quantities.

## Parameters (Baseline Calibration)

| Parameter | Symbol | Value | Rationale |
|-----------|--------|-------|-----------|
| Risk aversion | gamma | 5 | Standard in portfolio choice literature |
| Discount factor | beta | 0.96 | Standard |
| Risk-free rate | R_f | 1.02 | ~2% real |
| Expected stock return | E[R_s] | ~6% real | Equity premium ~4% |
| Stock return volatility | sigma_s | 0.18 | Typical annual equity vol |
| Labor income (normalized) | Y_bar | 1.0 | |
| Income shock volatility | sigma_xi | 0.15 | Moderate labor income risk |
| Periods | T | 40 | Working life |

## Open Questions

- How much detail on the firm side? Full partial equilibrium (solve for equilibrium return) or just overlay a conceptual demand curve on the household-derived supply curve?
- Should we vary risk aversion (gamma) to show how the elasticity depends on preferences?
- Do we want to show the two-period analytical result as a simple warm-up before the buffer stock simulation?
