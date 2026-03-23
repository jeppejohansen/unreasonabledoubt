# Equilibrium: Inelastic Savings Meets Inelastic Supply

Mathematical framework for the interaction of household portfolio demand with stock and bond supply.

## Setup

Three things are fixed (or nearly so) in the short run:

| Quantity | Symbol | Why fixed |
|----------|--------|-----------|
| Total savings | S | Retirement motive — households save ~70% of income regardless of returns |
| Aggregate earnings | E | Capital stock K is fixed short-run; earnings = f(K) |
| Government bonds outstanding | B | Determined by fiscal policy, not savings demand |

Households must allocate their savings between two assets:
- Stocks: share α
- Bonds: share (1 - α)

## Market Clearing

### Stock market

α · S dollars chase a fixed quantity of earnings E. The P/E ratio adjusts:

    P/E = α · S / E                ... (1)

Higher α (more money flowing to stocks) → higher P/E → lower expected returns.

The expected stock return (earnings yield in a stationary economy):

    E[R_s] = E / (P · K) ≈ 1 / (P/E)       ... (2)

So equations (1) and (2) together: E[R_s] = E / (α · S). More savings chasing stocks → lower returns.

### Bond market

(1 - α) · S dollars chase B bonds. The bond yield adjusts:

    y = B / ((1 - α) · S)          ... (3)

More money flowing to bonds → bond prices rise → yields fall.

## Portfolio Choice (Demand)

Households choose α based on the equity premium (E[R_s] - R_f). The standard mean-variance result:

    α = (E[R_s] - R_f) / (γ · σ²)         ... (4)

where γ is risk aversion and σ² is stock return variance. This says households are fairly elastic between stocks and bonds — when the premium rises, they shift strongly toward stocks.

**Note:** The simple CAPM formula (4) understates the lifecycle model's α because it ignores human capital. Working households have a large implicit bond (future labor income), so their optimal *financial* portfolio tilts more heavily toward stocks. The lifecycle model gives α ≈ 37% at a 4% premium, vs ~7% from naive mean-variance with γ=5, σ=0.35. The shape is similar (increasing, roughly linear), but the level is shifted up.

For the equilibrium analysis, what matters is that α is an **increasing function** of the equity premium. Call it:

    α = h(E[R_s] - y)              ... (4')

where h is increasing and h(0) ≈ 0 (no premium → no reason to hold risky assets).

## Equilibrium

Substitute market clearing (2) and (3) into portfolio choice (4'):

    α = h( E/(α·S) - B/((1-α)·S) )

This is **one equation in one unknown** (α). Everything else follows:
- P/E from (1)
- y from (3)
- E[R_s] from (2)

### Intuition for the solution

The equation has a unique solution because:
- **Left side** (α) is increasing in α (trivially)
- **Right side** (h(·)) is *decreasing* in α: higher α raises stock prices (lowering E[R_s]) and lowers bond prices (raising y), both of which shrink the premium → h(·) falls

Where these cross is the equilibrium.

## Comparative Statics: What Happens When...

### More savings (S rises — demographics, pension mandates)

From the equilibrium equation: higher S lowers both E/(αS) and B/((1-α)S). The equity premium falls. But α doesn't change much (it's pinned by the portfolio choice function). So:

- **P/E rises** (equation 1: P/E = αS/E, and S is larger)
- **Bond yields fall** (equation 3: y = B/((1-α)S), and S is larger)
- **Portfolio share α barely changes** — the premium shrinks, but both returns fall together

This is the key result: **more savings raises asset prices across the board without much change in portfolio allocation.** The money has to go somewhere.

### Less stock supply (buybacks, delisting — E falls)

From (1): P/E = αS/E. Lower E → higher P/E. From (2): E[R_s] = E/(αS) falls.

Stocks get expensive. Households shift toward bonds (α falls somewhat). Bond yields fall too as money flows in. But total savings is unchanged — the same pool of money is now chasing fewer earnings claims.

### More bond supply (fiscal expansion — B rises)

From (3): y = B/((1-α)S). Higher B → higher yields. Bonds become more attractive → α falls → some money shifts from stocks to bonds → P/E falls.

But the effect is muted: total savings S is fixed, so a larger B just means bonds absorb more of the same savings pool. Yields rise, P/E falls, but the magnitudes depend on how elastic h(·) is.

### Higher stock volatility (σ rises)

From (4): h(·) becomes less responsive — for a given premium, households want less in stocks. α falls → P/E falls, y falls (more money in bonds). The equity premium must rise to coax households into holding the fixed supply of stocks.

## The Three Curves in One Diagram

We can plot everything in (α, return) space:

**X-axis:** α (share of savings in stocks)
**Y-axis:** Expected return

Three curves:
1. **Stock supply** (from equation 2): E[R_s] = E/(α·S). Downward-sloping hyperbola — as more money flows into stocks, expected returns fall.
2. **Bond supply** (from equation 3): y = B/((1-α)·S). Upward-sloping in α — as money leaves bonds, bond yields rise.
3. **Demand** (from equation 4'): α = h(E[R_s] - y). This is the portfolio choice — households want the α where the premium justifies the risk.

Equilibrium: where the demand curve is consistent with both supply curves simultaneously.

Alternatively, we can plot the **equity premium** (E[R_s] - y) against α:
- The premium implied by supply is: π(α) = E/(α·S) - B/((1-α)·S) — decreasing in α
- The premium demanded by households is: α = h(π), or equivalently π = h⁻¹(α) — increasing in α
- Intersection = equilibrium

## Important caveat: lifecycle covariance

The simple equations above use α·S for "total dollars in stocks." In practice, α and savings are **negatively correlated across the lifecycle**: young workers have high α (long horizon, lots of human capital) but low accumulated savings, while older workers have low α but large savings. This means:

    E[α · s] ≠ E[α] · E[s]

In the model: avg_stock_holdings = 0.94, but avg_portfolio_share × avg_savings_amount = 0.46 × 3.58 = 1.66. The gap is large (~43% overestimate).

**Implication:** The supply curves R_s = E/(α·S) and y = B/((1-α)·S) are useful for intuition, but the actual equilibrium must be computed from the model's realized stock and bond holdings across the lifecycle — not from aggregate averages. The GE solver in model.py does this correctly.

## Calibration (from GE solver)

From the converged general equilibrium:
- R_s = 7.9%, R_f = 1.6%, equity premium = 6.3pp
- Average savings rate = 71.2% (nearly invariant to returns)
- Average portfolio share α = 46.4%
- Average stock holdings = 0.94, bond holdings = 2.63 (per household per period)
- E_agg = 0.074, B_agg = 0.042

The savings rate varies by only ~1.1pp across a 12pp range of stock returns (3% to 15%), while the portfolio share swings from 23% to 60%. This confirms the core thesis: savings is nearly inelastic, portfolio allocation does all the adjusting.

## Connection to Gabaix & Koijen (2021)

The Inelastic Markets Hypothesis says $1 of inflows raises market cap by ~$5 (a "multiplier" of 5). In our framework:

    d(P/E)/dS = α/E

So the multiplier is α/E — the share going to stocks divided by aggregate earnings. With inelastic S (retirement savings flowing in mechanically) and fixed E, small changes in savings flows generate large P/E swings. This is exactly Gabaix & Koijen's mechanism, derived here from the lifecycle model.
