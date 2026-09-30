# Asset Supply Elasticity: Thinking Through the "Demand" Side

Working document on how to think about the supply of assets — both risky (stocks) and safe (bonds) — that households can buy with their (inelastic) savings.

## The Setup

We've established that the **supply of savings is inelastic** — households save ~70% of income for retirement regardless of returns. Now the question is: what can they actually buy with those savings?

Two asset classes:
1. **Risky assets (stocks):** claims on the economy's capital stock
2. **Safe assets (bonds):** government debt

Each has its own supply curve. The interaction of inelastic savings with these supply curves determines equilibrium prices (P/E ratios, bond yields).

---

## Risky Asset Supply (Stocks)

### Short run: very inelastic

The supply of stocks is essentially the existing capital stock K. In the short run, K is fixed — you can't build factories overnight. So the supply of equity claims is vertical.

When households pour inelastic savings into a fixed supply of stocks:
- Price P gets bid up
- P/E rises (expected returns fall)
- Tobin's Q = P/K rises above 1

### Medium/long run: somewhat elastic, but sluggish

When Q > 1, it's profitable for firms to invest (market values capital above replacement cost). But the empirical evidence says this response is **weak and slow**:

- **Hayashi (1982)** established the Q-theory of investment. In theory, Q should be the sufficient statistic for investment.
- **The Q-investment puzzle:** Empirically, investment barely responds to Q. The regression coefficient is far too small — implying firms face enormous adjustment costs or simply don't respond to market signals.
- **Gutierrez & Philippon (2017):** Post-2000, the investment-Q relationship has *weakened further*. Even with historically high Q values, firms increasingly prefer buybacks over real investment. Rising market concentration and governance changes (short-termism, shareholder pressure) explain the gap.
- **Baker & Wurgler (2002):** Firms do time equity markets — they issue shares when valuations are high. But the response is slow (operates over years) and incomplete.
- **Peters & Taylor (2017):** The Q-investment link improves when you include intangible capital (R&D, organizational capital). But intangible investment doesn't expand the supply of *tradeable assets* the same way physical capital does.

**Bottom line:** The supply of risky assets is inelastic in the short run (fixed K) and only weakly elastic in the long run (firms are slow to invest even when Q is high). This has gotten worse since 2000.

### Implication for P/E

With inelastic savings meeting inelastic asset supply, the P/E ratio is highly sensitive to small changes in either:
- More savings (demographics, pension mandates) → P/E rises sharply
- Less asset supply (buybacks, delisting) → P/E rises sharply
- Neither savings nor asset supply adjusts much, so the *price* does all the work

---

## Safe Asset Supply (Bonds)

### Mechanically elastic, but effectively constrained

Governments *can* issue bonds at will. But not all bonds are "safe":

- **He, Krishnamurthy & Milbradt (2016):** Safety status depends on market depth and sovereign credibility. Only a handful of governments (US, Germany, Japan) can issue debt that's treated as truly risk-free. The supply of *safe* assets is concentrated.
- **Krishnamurthy & Vissing-Jorgensen (2012):** Treasuries carry a "convenience yield" — they trade at a premium over equivalent-risk corporate bonds because of their safety/liquidity. When Treasury supply increases, this convenience yield narrows (but doesn't disappear). When supply is scarce, it widens. Direct evidence that safe asset supply is constrained relative to demand.

### The safe asset shortage

**Caballero, Farhi & Gourinchas (2017)** — the definitive treatment:
- Global demand for safe assets has grown faster than supply because:
  1. High-saving emerging economies (China) demand safe stores of value
  2. Aging populations in advanced economies increase retirement savings demand
  3. Post-2008, private safe assets (AAA mortgage-backed securities) were destroyed
  4. Few sovereigns can credibly issue safe debt
- Result: secular decline in safe real interest rates since the 1980s
- When the shortage is severe enough, the economy can enter a "safety trap" — a recession where the natural safe rate is negative

### Implication

Safe asset supply is **more elastic than risky asset supply** (governments can issue bonds) but still **constrained** by credibility. And the direction of the constraint matters: governments issue bonds based on fiscal needs, not to accommodate savings demand. So safe asset supply is largely *exogenous* to the savings market.

---

## Putting It Together: Two Vertical Lines and a Price

Think of the equilibrium as:

```
                  Return
                    |
                    |   S_risky     S_safe      S_savings
                    |     |           |            |
                    |     |           |            |
                    |     |           |            |
                    |     |           |            |
                    |_____|___________|____________|______ Quantity
                         K_stocks   B_bonds    Total savings
```

All three curves are near-vertical:
1. **S_savings** (household savings): inelastic because of retirement (our model result)
2. **S_risky** (stock supply): inelastic because capital stock is fixed short-run, firms slow to invest
3. **S_safe** (bond supply): somewhat less inelastic, but constrained by fiscal policy and sovereign credibility

The **prices** (stock P/E, bond yields) adjust to make the accounting work:
- Total savings = value of stocks held + value of bonds held
- The *quantity* of real assets is basically fixed
- So the *prices* absorb all the adjustment

### When savings exceeds available assets at "reasonable" prices

This is the core of the story:
1. Households must save X for retirement (inelastic)
2. There are K units of productive capital and B units of government bonds
3. If X > K + B at historical P/E ratios, prices get bid up
4. P/E rises until the market value of stocks + bonds = X
5. Expected returns fall, but households keep saving because retirement is non-negotiable

This is how you get structurally elevated P/E ratios. It's not a bubble — it's the equilibrium outcome of inelastic savings meeting inelastic asset supply.

---

## Connection to Value Investing

Value investors identify when P/E is "too high" and expected returns are low. They're right about the expected returns. But the model explains *why* prices stay high:

- It's not that investors are irrational
- It's that they have no alternative — retirement savings must go somewhere
- The value investor who underweights stocks when P/E is high is making a bet that OTHER investors will eventually need to sell — but in aggregate, they won't, because savings is inelastic

The value investor's edge (if any) comes from being on the *margin* — they can shift between stocks and bonds. But the aggregate pool of savings doesn't shrink. So value investing redistributes returns across investors without changing the total.

---

## Key References

- Caballero, Farhi & Gourinchas (2017) "The Safe Assets Shortage Conundrum" *JEP*
- Krishnamurthy & Vissing-Jorgensen (2012) "The Aggregate Demand for Treasury Debt" *JPE*
- Gutierrez & Philippon (2017) "Investmentless Growth" *Brookings Papers*
- Baker & Wurgler (2002) "Market Timing and Capital Structure" *JF*
- Hayashi (1982) "Tobin's Marginal Q and Average Q" *Econometrica*
- Peters & Taylor (2017) "Intangible Capital and the Investment-q Relation" *JFE*
- He, Krishnamurthy & Milbradt (2016) "What Makes US Government Bonds Safe Assets?" *AER P&P*
- Gorton & Ordonez (2013) "The Supply and Demand for Safe Assets" *NBER*

---

## Open Questions

- Should we model the bond supply explicitly (as fiscal-policy-determined, exogenous) and show how the savings residual flows into stocks?
- Can we compute an implied equilibrium P/E from the model? (Given total savings and a fixed capital stock K, what P clears the market?)
- How does this connect to secular stagnation? (Summers' argument that excess savings depresses the natural rate)
- Is the safe asset shortage the same phenomenon viewed from the bond market side?
