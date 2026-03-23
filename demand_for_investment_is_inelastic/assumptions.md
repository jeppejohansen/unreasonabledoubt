# Assumptions: Demand for Investment Is Inelastic

Working document laying out the model assumptions for the blog post.

## The Question

When expected returns on stocks fall, do households save less? How elastic is the supply of savings with respect to asset returns?

## Assets

1. **Risk-free asset: government bonds.** Fixed real return R_f (e.g., ~2%). The supply of government bonds is determined by fiscal policy — exogenous to household decisions.

2. **Risky asset: stocks (equity claims on firms).** Expected return E[R_s] > R_f (the equity premium). Returns are stochastic with volatility sigma_s.

3. **Stock of equities is (approximately) perfectly inelastic in the short run.** Firms have a fixed capital stock at any moment; new equity issuance responds slowly. So the supply of stocks is essentially vertical — the price (and hence expected return) adjusts to clear the market, not the quantity.

## Households (Supply of Savings)

- **Lifecycle model with retirement.** Households work for T_work periods earning deterministic labor income Y_bar, then retire for T_ret periods with zero income. The need to fund retirement consumption is the primary savings motive.

- **CRRA preferences.** Utility u(c) = c^(1-gamma)/(1-gamma). Risk aversion parameter gamma governs both the willingness to substitute consumption over time and aversion to risk.

- **Two choice margins each period:**
  1. How much to consume vs. save (total savings)
  2. How to allocate savings between bonds and stocks (portfolio choice)

- **No income uncertainty.** Labor income during working years is deterministic. This keeps the model simple and isolates the lifecycle/retirement motive as the driver of savings inelasticity. (Income shocks would add a precautionary motive that reinforces the result but is not necessary for it.)

- **Stochastic stock returns.** The risky asset return is drawn from a lognormal distribution each period. This is the only source of uncertainty in the model.

- **Borrowing constraint.** Households cannot borrow: savings S_t >= 0.

- **No short-selling.** Portfolio share in stocks alpha_t in [0, 1].

## Firms / Capital Demand (to be developed)

- **Neoclassical production.** Firms use capital and labor; marginal product of capital is decreasing (Cobb-Douglas or similar).

- **Capital demand is downward-sloping in the required return.** As the cost of capital rises, firms want less of it.

- **Key question: how elastic is capital demand?** If firms have good substitution possibilities between capital and labor, demand is more elastic. If production is more Leontief-like, demand is inelastic too.

## The Core Mechanism

When expected stock returns change, households have two margins of adjustment:

1. **Total savings (inelastic margin):** The retirement funding need is essentially fixed — you must accumulate enough wealth during working years to fund T_ret periods of consumption with zero income. Higher returns mean each dollar saved grows faster, but you still need the same consumption in retirement. With gamma > 1 (EIS < 1), the income and substitution effects on total savings roughly cancel.

2. **Portfolio allocation (elastic margin):** When expected stock returns rise, stocks become more attractive relative to bonds. Households shift their portfolio toward stocks. There is no offsetting force — higher expected returns unambiguously make stocks more attractive for a given level of risk.

The result: total savings barely moves with returns, but portfolio composition shifts strongly.

## Supply-Demand Framing

- **Supply of savings (from households):** Nearly vertical (inelastic). The lifecycle/retirement motive dominates the return incentive.

- **Demand for capital (from firms):** Downward-sloping. Lower cost of capital means firms want more.

- **Implication:** Because savings supply is inelastic, shifts in capital demand mostly move the return on capital (the price), not the quantity of investment. Policies that try to boost investment by making saving more attractive have limited effect on quantities.

## Parameters (Baseline Calibration)

| Parameter | Symbol | Value | Rationale |
|-----------|--------|-------|-----------|
| Risk aversion | gamma | 5 | Standard in portfolio choice literature |
| Discount factor | beta | 0.96 | Standard |
| Risk-free rate | R_f | 1.02 | ~2% real |
| Expected stock return | E[R_s] | ~6% real | Equity premium ~4% |
| Stock return volatility | sigma_s | 0.35 | Calibrated for interior portfolio solutions (accounts for underdiversification and human-capital effects) |
| Labor income (working years) | Y_bar | 1.0 | Normalized |
| Working periods | T_work | 30 | ~30 years of working life |
| Retirement periods | T_ret | 10 | ~10 years of retirement |

## Supply Side: What Can Households Buy?

Households save ~70% of lifetime income regardless of returns. But what do they actually buy with those savings? Two asset classes, each with its own supply constraint.

### Risky assets (stocks): nearly perfectly inelastic

Stocks are claims on the economy's capital stock K. In the short run, K is fixed — you cannot create more economy overnight.

- **P/E as the price variable.** If the total capital stock has aggregate earnings E and the stock market prices it at P, the P/E ratio is the "price per unit of earnings." Higher P/E means lower expected returns.
- **Why supply doesn't respond to high prices.** Even when P/E is high (Tobin's Q > 1), firms are slow to invest. The Q-investment literature (Hayashi 1982, Gutierrez & Philippon 2017) documents that real investment barely responds to market valuations, especially post-2000. Firms prefer buybacks over building new capacity.
- **Result:** The supply of tradeable equity claims is approximately vertical. The price (P/E) does all the adjusting.

### Safe assets (government bonds): constrained by credibility

Governments *can* issue bonds at will, making supply mechanically elastic. But not all bonds are "safe":

- **Only a few sovereigns qualify.** Safety depends on sovereign credibility and market depth (He, Krishnamurthy & Milbradt 2016). Only the US, Germany, Japan, and a handful of others issue debt that global investors treat as truly risk-free.
- **The safe asset shortage.** Global demand for safe assets has outstripped supply (Caballero, Farhi & Gourinchas 2017). Aging populations, high-saving emerging economies, and the destruction of private safe assets (AAA MBS) post-2008 have widened the gap. The signature: secular decline in safe real interest rates.
- **Supply is driven by fiscal needs, not savings demand.** Governments issue bonds to fund deficits, not to accommodate household savings. So safe asset supply is largely exogenous to the savings market.

### The equilibrium

When inelastic savings meets inelastic asset supply, the **price does all the work**:

1. Households must save X for retirement (inelastic — our model result)
2. There are K units of productive capital and B units of government bonds
3. If X exceeds the market value of K + B at historical P/E ratios, prices get bid up
4. P/E rises until market value of stocks + bonds = total savings
5. Expected returns fall, but households keep saving because retirement is non-negotiable

This is how you get structurally elevated P/E ratios. It is not a bubble — it is the equilibrium outcome of inelastic savings meeting inelastic asset supply.

## Open Questions

- How much detail on the firm side? Full partial equilibrium (solve for equilibrium return) or just overlay a conceptual demand curve on the household-derived supply curve?
- Should we vary risk aversion (gamma) to show how the elasticity depends on preferences?
- Do we want to show the two-period analytical result as a simple warm-up before the lifecycle simulation?
