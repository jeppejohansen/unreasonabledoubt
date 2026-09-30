// ── Page & font setup ────────────────────────────────────────────────────────
#set page(margin: (x: 1.2in, y: 1.2in))
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.7em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 16pt)
#show heading.where(level: 2): set text(size: 13pt)
#show link: underline

// ── Title block ──────────────────────────────────────────────────────────────
#align(center)[
  #text(size: 22pt, weight: "bold")[Demand for Investment Is Inelastic]
  #v(0.3em)
  #text(size: 12pt, style: "italic")[Why savings don't fall when valuations rise]
  #v(0.3em)
  #text(size: 10pt)[Jeppe Johansen · Unreasonable Doubt · 2026]
]

#v(1em)

= Introduction

When stock valuations climb, a natural reaction is: "People will stop saving so much — expected returns are too low." But they won't. They _can't_.

The reason is simple. Most household saving is driven by retirement. You work for thirty-odd years, then you need to fund a decade or more of consumption with no labor income. That need doesn't shrink because the S&P 500 is expensive. If anything, lower expected returns mean you need to save _more_, not less, to hit the same retirement target.

What _does_ change is where the money goes. When stock valuations are high and expected returns are low, households shift their portfolios toward bonds. When stocks look cheap, they load up on equities. The margin of adjustment is _portfolio allocation_, not _total savings_.

This post builds a simple lifecycle model to make the argument precise. We then embed it in a market-clearing framework to show what happens when inelastic savings meets inelastic asset supply. The punchline: asset prices are far more sensitive to shifts in savings flows than standard intuition suggests, because neither the supply of savings nor the supply of assets adjusts much. Prices do all the work.

= The Supply Side: What Can Households Buy?

Before we get to the savings decision, it helps to understand what households are actually buying with their savings. There are two asset classes, each with its own supply constraint.

== Stocks: claims on earnings

A stock is a claim on a stream of future corporate earnings. @fig-stock-cashflows illustrates the idea: you pay a price $P$ today in exchange for a share of earnings $E$ each period going forward. The expected return is roughly the _earnings yield_ — the inverse of the price-to-earnings ratio:

$ E[R_s] approx E / P = 1 / ("P/E") $

The crucial point is that the _quantity_ of earnings is approximately fixed in the short run. The economy's capital stock $K$ doesn't change overnight. Firms are slow to build new capacity even when valuations are high — the Q-investment literature documents that real investment barely responds to market prices, especially since 2000 (Gutierrez & Philippon 2017). Firms increasingly prefer buybacks to building.

So stock supply is nearly _vertical_: the quantity of earnings claims is fixed, and the price (P/E ratio) adjusts to clear the market. @fig-stock-supply shows the supply curve.

#figure(
  image("figures/stock_cashflows.png", width: 85%),
  caption: [A stock is a claim on a stream of future earnings. You pay price $P$ today and receive earnings $E$ each period.],
) <fig-stock-cashflows>

#figure(
  image("figures/stock_supply.png", width: 85%),
  caption: [Stock supply is nearly vertical. The quantity of earnings claims is fixed; the P/E ratio adjusts to clear the market.],
) <fig-stock-supply>

== Bonds: government debt

A bond is simpler: you lend the government a fixed amount and receive a known return $R_f$ (@fig-bond-cashflows). Governments _can_ issue bonds at will, making supply mechanically elastic. But not all bonds are "safe." Only a handful of sovereigns — the US, Germany, Japan — issue debt that global investors treat as truly risk-free (He, Krishnamurthy & Milbradt 2016). And governments issue bonds to fund deficits, not to accommodate household savings demand.

The result is a "safe asset shortage" (Caballero, Farhi & Gourinchas 2017): global demand for safe stores of value has outstripped supply, driving a secular decline in real interest rates. Safe asset supply is more elastic than stock supply, but still largely exogenous to the savings market. @fig-bond-supply illustrates the constrained supply curve.

#figure(
  image("figures/bond_cashflows.png", width: 85%),
  caption: [A bond is a loan to the government at a known return $R_f$.],
) <fig-bond-cashflows>

#figure(
  image("figures/bond_supply.png", width: 85%),
  caption: [Bond supply is constrained by fiscal policy and sovereign credibility. The yield adjusts, but the quantity of safe assets is largely exogenous.],
) <fig-bond-supply>

= Market Clearing and Equilibrium

Now we can write down the equilibrium. Three quantities are approximately fixed in the short run:

- *$S$* — total household savings (driven by the retirement motive, as we'll show)
- *$E$* — aggregate corporate earnings (determined by the capital stock)
- *$B$* — aggregate government bond interest payments (set by fiscal policy)

Households split their savings between stocks (share $alpha$) and bonds (share $1 - alpha$). Market clearing pins down prices.

== Stock market clearing

$alpha dot S$ dollars chase $E$ units of earnings. The P/E ratio adjusts:

$ "P/E" = (alpha dot S) / E $

More money flowing into stocks means a higher P/E — and lower expected returns. The expected gross stock return is one plus the earnings yield:

$ R_s = 1 + E / (alpha dot S) $

== Bond market clearing

$(1 - alpha) dot S$ dollars chase bonds paying aggregate interest $B$. The gross bond return adjusts:

$ R_f = 1 + B / ((1 - alpha) dot S) $

More money in bonds pushes yields down.

== One equation in one unknown

Households choose $alpha$ based on the equity premium — the gap between expected stock returns and the bond yield. Call their portfolio choice function $alpha = h(E[R_s] - R_f)$, where $h$ is increasing (a higher premium makes stocks more attractive). Substituting the market-clearing conditions:

$ alpha = h lr(( E / (alpha dot S) - B / ((1 - alpha) dot S) )) $

where $E$ and $B$ enter as the earnings yield and interest yield respectively (the $1+$ cancels in the premium). This is one equation in one unknown ($alpha$). The left side is trivially increasing in $alpha$. The right side is _decreasing_ in $alpha$: pushing more money into stocks lowers stock returns and raises bond yields, shrinking the premium. Where they cross is the equilibrium. Everything else — P/E, bond yields, the equity premium — follows.

@fig-ge-equilibrium shows the equilibrium graphically: the intersection of the supply-implied premium curve (decreasing in $alpha$) with the demand curve (increasing in $alpha$).

#figure(
  image("figures/ge_equilibrium.png", width: 85%),
  caption: [Equilibrium as the intersection of supply-implied and demand-implied equity premium curves. The supply curve is decreasing in the portfolio share $alpha$ (more money in stocks compresses the premium); the demand curve is increasing (households require a higher premium to hold more risk).],
) <fig-ge-equilibrium>

#figure(
  image("figures/ge_returns.png", width: 85%),
  caption: [Equilibrium stock returns, bond yields, and the equity premium from the general equilibrium model.],
) <fig-ge-returns>

== A caveat: lifecycle covariance

The equations above use $alpha dot S$ for "total dollars in stocks." In practice, $alpha$ and savings are _negatively correlated_ across the lifecycle: young workers have high $alpha$ (long horizon, lots of human capital) but low accumulated savings, while older workers have low $alpha$ but large nest eggs. This means:

$ E[alpha dot s] eq.not E[alpha] dot E[s] $

The simple supply curves are useful for intuition, but the actual equilibrium must be computed from realized holdings across the lifecycle. The model below does this correctly.

= The Buffer-Stock Savings Model

The equilibrium framework above takes $S$ as given. Now we show _why_ savings is inelastic — and how elastic portfolio allocation really is.

== Setup

A household lives for 40 periods: 30 working years with deterministic income $Y = 1$, followed by 10 retirement years with zero income. Each period, the household chooses how much to consume (vs. save) and how to split savings between stocks and bonds.

Preferences are CRRA with risk aversion $gamma = 5$:

$ u(c) = c^(1 - gamma) / (1 - gamma) $

The only uncertainty is stock returns, drawn from a lognormal distribution with volatility $sigma = 0.35$. The household discounts future utility at rate $beta = 0.96$, cannot borrow, and cannot short-sell.

Concretely, the problem is solved backwards from retirement via dynamic programming. At each age, the household looks at its wealth, the available returns, and the years remaining — and chooses the consumption and portfolio split that maximizes expected lifetime utility. The model is solved numerically on a wealth grid for each combination of stock returns and risk-free rates.

== The core result: savings is inelastic

@fig-savings-supply shows the main finding. The left panel plots the average savings rate (share of cash-on-hand saved each period, averaged across the lifecycle) against the expected stock return, varying $R_s$ from 3% to 15%. The savings rate barely moves — it stays around 71%, with less than 2 percentage points of variation across a 12 percentage point range of stock returns.

The right panel tells the other half of the story: the average portfolio share in stocks ($alpha$) swings from about 23% to 60% over the same range. When stock returns are high, households eagerly load up on equities. When returns are low, they shift to bonds. But they _keep saving the same amount_.

#figure(
  image("figures/savings_supply.png", width: 100%),
  caption: [*The core result.* Left: the savings rate is nearly invariant to expected stock returns — roughly 71% regardless. Right: portfolio allocation swings widely (23%–60%). Savings is inelastic; portfolio choice is elastic.],
) <fig-savings-supply>

== Why? The retirement anchor

Intuitively, the retirement motive acts as an anchor. You need to accumulate enough wealth during 30 working years to fund 10 years of consumption with no income. When returns rise, each dollar saved grows faster — but with risk aversion $gamma > 1$ (elasticity of intertemporal substitution below 1), the _income effect_ dominates: households don't consume much more today because future consumption is already well-funded. They pocket the windfall rather than spend it. The substitution and income effects roughly cancel on total savings, leaving the savings rate flat.

Put differently, the retirement constraint is _quantity-based_: you need a certain level of consumption in retirement, not a certain rate of return. Higher returns make hitting that target easier, but don't change the target itself. The household adjusts _how_ it invests — not _how much_.

== Decomposition: what absorbs the changes?

@fig-decomposition breaks down the household's response to changing returns. The bond-only model (dashed line) shows what would happen if stocks didn't exist: the savings rate is essentially flat, confirming that the inelasticity comes from the retirement motive, not from portfolio effects. Adding stocks (solid line) introduces a bit more variation — because stochastic returns create a small precautionary savings motive — but the core flatness persists.

The gap between the two lines shows that portfolio rebalancing absorbs nearly all the adjustment. When stock returns rise, households shift from bonds to stocks rather than saving more or less.

#figure(
  image("figures/decomposition.png", width: 85%),
  caption: [Savings rate in the bonds-only model (dashed) vs. the full model with stocks (solid). The flatness comes from the retirement motive; adding stocks barely changes the picture.],
) <fig-decomposition>

= Comparative Statics: What Moves Prices?

We've established that savings is inelastic and asset supply is approximately fixed. What happens when we vary the _level_ of savings, holding asset supply constant?

@fig-comparative-statics shows the answer. As total savings rises (e.g., due to demographics, pension mandates, or a savings glut), both stock valuations and bond prices climb. The P/E ratio rises because $"P/E" = alpha S slash E$ and $S$ is larger. Bond yields fall because $R_f = 1 + B slash ((1 - alpha) S)$ and $S$ is larger. The portfolio share $alpha$ barely changes — the premium compresses, but both returns fall together.

This is how you get structurally elevated P/E ratios. It is not a bubble. It is the equilibrium outcome of inelastic savings meeting inelastic asset supply. The money _has to go somewhere_.

#figure(
  image("figures/savings_comparative_statics.png", width: 100%),
  caption: [More savings raises asset prices across the board. P/E rises, bond yields fall, and portfolio allocation barely changes. Prices do all the adjusting.],
) <fig-comparative-statics>

== Connection to Gabaix & Koijen (2021)

The _Inelastic Markets Hypothesis_ says that \$1 of inflows raises aggregate market cap by roughly \$5. In our framework, this follows directly. From the stock market-clearing equation:

$ d("P/E") / (d S) = alpha / E $

The "multiplier" is $alpha slash E$ — the share going to stocks divided by aggregate earnings. With inelastic savings (retirement flows coming in mechanically) and fixed $E$, small changes in savings flows generate large P/E swings. This is exactly Gabaix & Koijen's mechanism, derived here from a lifecycle model.

@fig-supply-demand provides another view of the same result: a supply-demand diagram where inelastic savings supply meets a downward-sloping demand curve from firms. Because supply is nearly vertical, shifts in demand mostly move the price (expected return), not the quantity of savings.

#figure(
  image("figures/supply_demand.png", width: 85%),
  caption: [Inelastic savings supply (nearly vertical) meets downward-sloping demand for capital. Shifts in demand mostly move returns, not savings quantities.],
) <fig-supply-demand>

= Conclusion

The demand for investment is inelastic. Households save for retirement, and that need is non-negotiable — it doesn't bend much with expected returns. What adjusts is portfolio composition: more stocks or more bonds, depending on the premium.

When this inelastic savings meets an approximately fixed supply of assets, prices do all the adjusting. More savings flowing into the market doesn't get absorbed by more investment or less saving — it shows up as higher P/E ratios and lower yields. This is not irrational exuberance. It is the mechanical consequence of retirement savings searching for a home in a world with limited assets to buy.

Three implications stand out:

- *Elevated P/E ratios can be structural, not speculative.* When savings outstrip asset supply at historical valuations, prices must rise to clear the market. Calling this a "bubble" misses the mechanism.

- *Policies aimed at boosting savings will mostly raise asset prices, not investment.* If the supply of productive assets doesn't expand — and the Q-investment literature says it mostly doesn't — then more savings just bids up prices.

- *Small flows move prices a lot.* Because both savings supply and asset supply are inelastic, the equilibrium is fragile. Demographic shifts, pension mandates, or savings gluts can generate large swings in valuations, even without changes in fundamentals.

This is not a prediction about where markets are headed. It is a disciplined way to reason about why valuations are where they are — and why the common intuition ("just save less when returns are low") fundamentally misunderstands how household savings works.

#v(1.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)

== Notes and References

The lifecycle model uses standard parameters from the portfolio choice literature: $gamma = 5$, $beta = 0.96$, $sigma = 0.35$, with 30 working years and 10 retirement years. The model is solved via backward induction on a 150-point wealth grid with 5,000 Monte Carlo paths. General equilibrium is computed by iterating on market-clearing conditions until convergence. Full code is available in the companion repository.

We use $R$ for gross returns throughout, following the convention in Cochrane (2005) and Campbell & Viceira (2002). The stock return formula $R_s = 1 + E slash P$ is the zero-growth Gordon model (a perpetuity paying $E$ with price $P$). The market-clearing substitution $P = alpha dot S$ — so that $R_s = 1 + E slash (alpha dot S)$ — follows the Gabaix & Koijen (2021) framing where aggregate prices are determined by savings flows into each asset class.

*Key references:*

- Cagetti (2003). "Interest Elasticity in a Life-Cycle Model with Precautionary Savings." _AER P&P._ Directly estimates savings elasticity at approximately zero.

- Cocco, Gomes & Maenhout (2005). "Consumption and Portfolio Choice over the Life Cycle." _Review of Financial Studies._ The canonical lifecycle portfolio model.

- Gabaix & Koijen (2021). "In Search of the Origins of Financial Fluctuations: The Inelastic Markets Hypothesis." _NBER WP._ \$1 of inflows raises market cap by ~\$5.

- Caballero, Farhi & Gourinchas (2017). "The Safe Assets Shortage Conundrum." _JEP._ The definitive treatment of the safe asset shortage.

- Gutierrez & Philippon (2017). "Investmentless Growth." _Brookings Papers._ Documents weak investment response to high valuations.

- Kopecky & Taylor (2022). "The Savings Glut of the Old." _NBER WP._ Aging populations create a savings glut that depresses returns and elevates prices.

== Model Summary

*Primitives*

- Household lives $T = 40$ periods: 30 working years ($Y = 1$), 10 retirement years ($Y = 0$)
- CRRA utility: $u(c) = c^(1 - gamma) slash (1 - gamma)$, $space gamma = 5$, $space beta = 0.96$
- Stock returns: lognormal, volatility $sigma = 0.35$
- Constraints: no borrowing, no short-selling

*Asset supply (approximately fixed)*

- $E$ — aggregate corporate earnings (pinned by the capital stock)
- $B$ — aggregate government bond interest payments (set by fiscal policy)
- $S$ — total household savings (driven by the retirement motive)

*Market clearing*

- Households allocate share $alpha$ to stocks, $1 - alpha$ to bonds
- Stock market: $"P/E" = (alpha dot S) / E$, so $R_s = 1 + E / (alpha dot S)$
- Bond market: $R_f = 1 + B / ((1 - alpha) dot S)$
- Equity premium: $pi = R_s - R_f = E / (alpha dot S) - B / ((1 - alpha) dot S)$

*Portfolio choice*

- Households choose $alpha = h(pi)$, with $h$ increasing in the premium
- Equilibrium condition (one equation, one unknown):
$ alpha = h lr(( E / (alpha dot S) - B / ((1 - alpha) dot S) )) $
- LHS is increasing in $alpha$; RHS is decreasing (more money in stocks compresses the premium). Unique intersection determines equilibrium $alpha^*$.

*Comparative statics*

- Sensitivity of P/E to savings: $d("P/E") / (d S) = alpha / E$
- With $E$ fixed and $alpha$ roughly stable, small $Delta S$ generates large $Delta "P/E"$ (the Gabaix--Koijen multiplier)
- Higher $S$ raises P/E and lowers $R_f$ roughly in proportion; $alpha$ barely moves

*Key quantitative results*

- Savings rate $approx 71%$ of cash-on-hand (averaged across the lifecycle), varying less than 2 pp across $R_s in [3%, 15%]$
- Portfolio share $alpha$ swings from $approx 23%$ to $approx 60%$ over the same range
- Adjustment margin is portfolio allocation, not total savings

#v(1em)
#text(size: 9pt, style: "italic")[Jeppe Johansen is a writer at Unreasonable Doubt, covering economics, institutions, and ideas.]
