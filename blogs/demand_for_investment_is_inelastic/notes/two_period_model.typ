// Build from the post directory:
// typst compile --root . notes/two_period_model.typ notes/two_period_model.pdf

#set page(paper: "us-letter", margin: (x: 0.88in, y: 0.80in), numbering: "1")
#set text(font: "New Computer Modern", size: 10.5pt)
#set par(leading: 0.62em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 15pt)
#show heading.where(level: 2): set text(size: 12pt)
#set list(indent: 1.15em, body-indent: 0.45em, spacing: 0.40em)
#show figure.caption: set text(size: 9pt)

#align(center)[
  #text(size: 21pt, weight: "bold")[Retirement saving and asset prices]
  #v(0.35em)
  #text(size: 11pt, style: "italic")[A two-period model, read one step at a time]
]

#v(0.8em)

= Start with behavior

- *Consumption smoothing.* A worker earns while young and has no labor income when retired. They value consumption on both dates, so some current income is carried forward. This is a preference for a smoother path, not a literal fixed retirement spending target.
- *Two separate choices.* The worker chooses how much to save, then how to divide those savings between a risky claim and a safe claim. Changes in returns can move these two choices by different amounts.
- *Both return effects matter.* A higher return makes future consumption cheaper relative to present consumption (substitution). It also makes a given saving plan richer (income). The net change in saving depends on preferences and the initial position.
- *Prices clear claims.* The total date-1 payoffs of existing claims are fixed for the pricing exercise. More demand can therefore raise their date-0 prices and lower the returns earned by new buyers. This is a model of trading existing assets; there is no choice to build new capital.

== Three blocks to remember

- *1. Household:* choose current consumption and holdings of the two claims.
- *2. Payoffs:* one claim pays a risky amount; the other pays a safe amount at retirement.
- *3. Clearing:* all claims must be held, so their prices adjust until desired holdings equal the fixed units available.

= Primitives

- *Dates and people.* There are dates $0$ (working) and $1$ (retirement), and $n > 0$ identical workers. One aggregate unit of each claim is sold at date 0 by initial owners. The claims pay once at date 1 and then expire.
- *Endowments.* Each worker receives $y > 0$ units of date-0 goods and no date-1 labor income. Payoffs at date 1 come from an exogenous resource stream. The safe payoff can be thought of as externally backed; its fiscal backing is outside this model. Initial owners receive the date-0 sale proceeds. Their choices are outside the model.
- *Preferences.* Each worker maximizes $u(c_0) + beta E[u(c_1)]$, with $beta > 0$. For $gamma > 0$, marginal utility is $u'(c) = c^(-gamma)$. When $gamma != 1$, $u(c) = c^(1-gamma)/(1-gamma)$; when $gamma = 1$, $u(c) = ln c$.
- *Claims.* The stock pays $D^L$ in the low state and $D^H$ in the high state, with probabilities $1-p$ and $p$. The safe claim pays $B > 0$ in either state. Both stock payoffs are positive. Their date-0 prices are $P_s$ and $P_b$.
- *Holdings and budgets.* A worker buys $q_s$ stock units and $q_b$ safe units:
  $ c_0 + P_s q_s + P_b q_b = y, quad c_1^j = D^j q_s + B q_b, quad j in {L,H}. $
  We require $q_s, q_b >= 0$. Saving is the *worker's date-0 flow* $s = y-c_0 = P_s q_s + P_b q_b$. This is spending on assets, not net saving for the whole economy. Its stock share by market value is $alpha = P_s q_s/s$.
- *Returns.* The stock's state-dependent gross return is $R_s^j = D^j/P_s$; the safe gross return is $R_b = B/P_b$. Because each claim pays once and expires, these returns have no resale-price term.

= The full model

- *Household problem.* Taking $P_s$ and $P_b$ as given, choose $c_0,q_s,q_b$ to maximize utility subject to the two budgets and nonnegative holdings. Equivalently, choose $s$ and $alpha$ with $c_1^j = s R_p^j$ and $R_p^j = alpha R_s^j + (1-alpha)R_b$.
- *Saving condition.* At an interior optimum, the marginal utility lost now equals expected discounted marginal utility gained from the portfolio payoff:
  $ c_0^(-gamma) = beta E[R_p^j (c_1^j)^(-gamma)]. $
- *Portfolio condition.* At an interior stock share, the extra risky payoff must have zero marginal-utility-weighted value:
  $ E[(R_s^j-R_b)(c_1^j)^(-gamma)] = 0. $
  If this expression is nonpositive at $alpha=0$, hold no stock; if nonnegative at $alpha=1$, put all saving in stock.
- *Market clearing.* There is one unit of each claim, so $n q_s = 1$ and $n q_b = 1$. Equivalently, $n alpha s = P_s$ and $n(1-alpha)s = P_b$. Thus each worker's retirement consumption is $c_1^j = (D^j+B)/n$.
- *Prices.* Let $c_0=y-s$. The two asset-pricing conditions become
  $ P_s = beta c_0^gamma E[D^j (c_1^j)^(-gamma)], quad P_b = beta c_0^gamma E[B(c_1^j)^(-gamma)]. $
  Together with $n y = n c_0 + P_s + P_b$, these determine consumption, saving, portfolio shares and prices.
- *A one-equation solution.* Substitute $c_1^j=(D^j+B)/n$ into the sum of the two price equations. The unique positive solution for $c_0$ satisfies
  $ y = c_0 + beta n^(gamma-1)c_0^gamma E[(D^j+B)^(1-gamma)]. $
  The code solves this monotone equation, then computes the two prices separately. This is the complete two-period market-clearing model used in the market-clearing figures.

== Illustrative values used below

- *Common behavior:* $y=1$, $beta=0.60$, $gamma=5$. These describe one stylized model period; the rates below are not annual estimates.
- *Full-model payoffs:* $D^L=0.17$, $D^H=0.23$, $p=0.5$, $B=0.30$, and initially $n=1$.
- *Baseline solution:* $s/y=45.9%$, $P_s=0.179$, $P_b=0.281$, and the stock receives $38.9%$ of saving. The expected stock gross return is $1.118$ and the safe gross return is $1.069$.

== Reproduce the figures

- *Code.* From the repository root run ` uv run python blogs/demand_for_investment_is_inelastic/src/two_period_model.py `. It writes seven figures to `figures/` and selected values to `data/two_period_summary.json`.
- *PDF.* From this post directory run ` typst compile --root . notes/two_period_model.typ notes/two_period_model.pdf `.

#pagebreak()

= Graph 1: a higher safe return

- *First take the return as given from the worker's point of view.* With a single safe asset paying gross return $R$, the budget line is $c_1=R(y-c_0)$. Comparing a higher $R$ rotates it around the income endowment $(y,0)$.
- *A to H: substitution.* The dotted compensated line is parallel to the new budget line and tangent to the original indifference curve. Current consumption falls from $0.539$ to $0.530$. If current income were held at its original level, this lower $c_0$ would mean more saving.
- *H to B: income.* On the actual new budget line, the worker can afford more consumption on both dates. Current consumption rises to $0.577$. This income effect is larger than the substitution effect, so saving falls from $0.461$ to $0.423$ when $R$ rises from $1.07$ to $1.30$.
- *The point of compensation.* At H, the hypothetical income endowment has been reduced to $0.918$. The arrows decompose the change in $c_0$; H is not a second saving outcome at the original income.

#figure(
  image("../figures/two_period_smoothing.png", width: 100%),
  caption: [Model illustration. Left: the full budget-line rotation. Right: a close view of the initial choice A, compensated choice H, and new choice B. The larger return change is used so the three points can be seen.],
)

= Graph 2: preferences decide the sign

- *Exact safe-asset solution.* Let $a(R)=beta^(1/gamma) R^(1/gamma-1)$. Then
  $ s/y = a(R)/(1+a(R)), quad (d ln(s/y))/(d ln R) = (1-s/y)(1/gamma-1). $
- *Three cases.* For $gamma < 1$, substitution dominates and saving rises with $R$. For $gamma = 1$, the two effects cancel exactly and $s/y=beta/(1+beta)$. For $gamma > 1$, income dominates and saving falls with $R$.
- *What this does and does not show.* A small change in the *saving rate* over a given return range can be useful to report, but retirement itself does not make saving fixed. The sign and elasticity follow from $gamma$ in this benchmark.

#figure(
  image("../figures/two_period_return_sensitivity.png", width: 100%),
  caption: [Model result. Each line shows the change in saving divided by income relative to $R=1.07$, with $y=1$ and $beta=0.60$. The vertical axis is in percentage points.],
)

= Graph 3: a better stock return

- *Now hold the safe return at $1.07$.* In this partial-equilibrium exercise, the stock pays a gross return of $mu-sigma$ or $mu+sigma$ with equal probability. Move $mu$ while holding the absolute two-state spread $sigma$ fixed.
- *Portfolio margin.* A higher $mu$ raises the stock share $alpha$. At $mu=1.12$, the share is $44.1%$ when $sigma=0.16$. Raising risk to $sigma=0.22$ lowers that share to $22.7%$.
- *Saving margin.* With $sigma=0.16$, saving changes from $46.1%$ to about $45.4%$ of earnings as $mu$ moves from $1.07$ to $1.16$. This comparison holds $R_b$ fixed. It is not a general theorem that saving always moves less than the stock share.
- *Important boundary.* At $mu=R_b$ the stock share is zero. Other model-period return ranges or preferences can give a different comparison. In this figure $mu$ is offered to the worker; it is not being set by market clearing.

#figure(
  image("../figures/two_period_portfolio.png", width: 100%),
  caption: [Model result. Expected stock return varies with the safe return fixed at $7%$ per model period. Solid and dashed lines have different two-state stock-return spreads. The right panel uses a close vertical scale.],
)

#pagebreak()

= Graph 4: more buyers, same total payoff

- *Return to full market clearing.* Fix the total stock payoff $D^j$ and safe payoff $B$. More identical workers now bid for the same one unit of each claim. This is a buyer-cohort shock, not new saving appearing from outside the model.
- *One-bundle view.* Treat one stock unit plus one safe unit as a bundle with payoff $T^j=D^j+B$ and total price $P=P_s+P_b$. At a candidate price $P$, desired saving and aggregate demand are
  $ a(P) = [beta E[(T^j/P)^(1-gamma)]]^(1/gamma), $
  $ s_d(P) = y a(P)/(1+a(P)), quad Q_d(P;n) = n s_d(P)/P. $
- *Graphical clearing.* Supply is one bundle. A larger $n$ shifts the demand curve right. The intersection moves up in price. The relative stock/bond price within the bundle is held at its optimal equilibrium ratio while drawing these curves; homothetic preferences keep that ratio unchanged under this cohort shock.

#figure(
  image("../figures/two_period_market_clearing.png", width: 100%),
  caption: [Model result. Each dot is the full-model equilibrium for a different mass of workers. The supply of the existing payoff bundle is fixed at one.],
)

#pagebreak()

= Graph 5: trace both asset prices and returns

- *Prices.* Moving from $n=0.9$ to $n=1.1$ raises the stock price from $0.148$ to $0.211$ and the safe-claim price from $0.232$ to $0.331$. More workers buy the same total future cash flows.
- *Returns.* Because total payoffs have not changed, the expected stock gross return falls from $1.353$ to $0.949$ and the safe gross return from $1.294$ to $0.907$. A gross return below one is possible in this one-period asset market when claims become expensive relative to their terminal payoffs.
- *Worker saving also responds.* Saving per worker rises from $0.422$ to $0.492$ across that same shock. Total saving by the worker cohort rises from $0.380$ to $0.541$, exactly matching the value of the claims at each equilibrium. Asset sellers receive this spending, so it is not net saving for the whole economy. The model does not hold worker saving fixed by assumption.
- *Composition.* The stock value share stays at $38.9%$ under this particular shock because all workers have the same homothetic preferences and both claims' aggregate payoffs remain fixed. That invariance would not generally survive different preferences, existing wealth, or payoff changes.

#figure(
  image("../figures/two_period_demographic_shock.png", width: 100%),
  caption: [Model result. The horizontal axis varies the number of identical workers relative to the baseline. Both asset prices rise and both expected net returns fall; the two panels use different vertical units.],
)

= What the model establishes, and what it leaves open

- *It establishes a conditional saving response.* A retirement motive creates demand for future consumption. The return elasticity of saving still depends on preferences, risk, and the shock under study. The safe-asset benchmark supplies an exact counterexample to a claim that saving must be fixed.
- *It establishes a pricing channel.* More buyers for a fixed stream of payoffs raise existing-claim prices in this two-period economy. The full model solves both saving and portfolio choice; it does not assume a constant aggregate saving pool.
- *It does not establish a real-investment result.* No firm chooses new capital, issues new claims, or changes future output in response to price. To make a claim about investment quantity, add a firm that can produce new capital at a specified marginal or adjustment cost and clear the market for *new* claims separately from trading old ones.
- *It does not reproduce a stock-market flow multiplier or a conventional P/E ratio.* A terminal claim has $E[D]/P_s$ as its expected gross return. A perpetuity with resale has a different return equation. Dollar flows, market capitalization, and payout multiples need separate definitions before comparing them with empirical estimates.

#pagebreak()

= The question: what if the expected stock return falls?

- *Specify the cause.* In this model $mu = E[D]/P_s$ is the expected *gross* stock return. A lower $mu$ can come from weaker future payouts or from a higher price paid for unchanged payouts. Those shocks need not change consumption or saving in the same way. The Gordon perpetuity analogy adds resale value; here the stock is a terminal claim.
- *The experiment here.* Reduce both stock payouts by $10%$: $(D^L,D^H)=(0.17,0.23)$ becomes $(0.153,0.207)$. Keep current earnings, the safe payoff, preferences and the number of workers fixed. Re-solve *both* asset markets. Expected stock payout falls from $0.20$ to $0.18$; the stock price adjusts from $0.179$ to $0.173$. Thus its expected *net* return falls from $11.8%$ to $4.2%$ per model period.
- *Portfolio substitution and the safe price.* The stock is less attractive relative to the safe claim. Workers direct a smaller share of their asset spending to stock ($38.9%$ to $36.5%$). Competition for the one safe claim raises its price from $0.281$ to $0.300$, so its net return falls from $6.9%$ to about $-0.1%$. These are equilibrium prices; the safe return cannot be held fixed for this comparison.
- *Saving and consumption.* Stock spending falls from $0.179$ to $0.173$, while safe-claim spending rises from $0.281$ to $0.300$. Total worker saving rises from $0.459$ to $0.473$, or by $1.38$ percentage points of unchanged earnings. Current consumption falls from $0.541$ to $0.527$. Expected retirement consumption falls from $0.500$ to $0.480$ because total future payouts are lower. The weaker future resource stream makes workers poorer; they reduce present consumption to cushion retirement. Substitution away from lower-return future consumption works against that saving response.
- *An exact saving sign.* Write $T^j=D^j+B$. The full-model equation contains $E[(T^j)^(1-gamma)]$. When every $T^j$ falls, this expectation rises if $gamma>1$, so its unique solution has lower $c_0$ and higher $s=y-c_0$. At $gamma=1$ saving is unchanged; for $gamma<1$ it falls. Here $1/gamma$ is the elasticity of intertemporal substitution. Consumption smoothing alone does not fix the saving sign.
- *Limits to the conjecture.* A fall in $mu$ alone does not imply that both dates' consumption fall or that workers rotate into safe claims. If only $beta$ rises from $0.60$ to $0.75$, stock return falls from $11.8%$ to $7.3%$ and safe return from $6.9%$ to $2.6%$. Saving rises from $0.459$ to $0.479$, yet expected retirement consumption stays at $0.500$ and the stock spending share stays at $38.9%$. Future payoffs did not change.

== Graph 6: demand for the two claims

- *Read the stock panel.* Each point offers a candidate stock return $mu$ by setting $P_s=E[D]/mu$, then lets the safe price move until the safe market clears. The horizontal coordinate is the resulting number of stock claims workers would buy. The vertical black line is the one claim actually available. Only each colored intersection with that line clears *both* markets. The teal and rust curves hold different stock payout streams fixed, so they are two conditional demand schedules, not a path of equilibria.
- *Why show the dotted curve?* It repeats the initial stock payout schedule while holding the safe return at its initial value. Allowing the safe price to respond makes the stock-demand schedule much steeper in return-versus-quantity space. The safe panel shows its own demand at the two stock-return scenarios: lower stock return shifts demand for the safe claim toward a higher price at the one-unit supply.
- *Read the horizontal units carefully.* At the same offered $mu$, a claim with $10%$ less payout also costs $10%$ less. Its *number of units* demanded can therefore be larger, even though the stock spending share is smaller at the new equilibrium. The two dots and the spending comparison below show the combined equilibrium response; a horizontal shift of physical-unit demand alone does not isolate portfolio substitution.

#figure(
  image("../figures/two_period_lower_stock_return_demand.png", width: 80%),
  caption: [Conditional demand for risky and safe claims. Both black supply lines are one physical claim. The colored dots are the two full equilibria. Stock demand is traced against its expected net return; safe demand is traced against its price.],
)

== Graph 7: spending and consumption in the two equilibria

- *Where the extra saving goes.* The rise in safe-claim purchases more than offsets the fall in stock purchases. With one claim of each type, their purchase values are also their equilibrium prices. The right panel shows both consumption dates falling; its points compare levels without using a truncated bar axis.

#figure(
  image("../figures/two_period_lower_stock_return_comparison.png", width: 100%),
  caption: [Model result for a 10% cut in both stock payouts. Left: worker spending on each claim and total date-0 saving. Right: current and expected retirement consumption per worker.],
)

== Is risky-asset demand inelastic?

- *Define the elasticity first.* For one fixed stock payout stream, measure the local response of desired *physical stock units* to their own price near the initial equilibrium: $epsilon_(q_s,P_s) = d ln q_s / d ln P_s$. A price increase means a lower offered $mu=E[D]/P_s$. The dotted schedule in Graph 6, with the safe return held fixed, gives $epsilon approx -23.8$; the teal schedule, with the safe market clearing at each candidate stock price, gives $epsilon approx -1.42$.
- *Interpretation.* Safe-price adjustment sharply reduces the stock-demand response, so the cross-market effect matters. Yet $abs(epsilon) > 1$ in this calibration, so physical stock demand is still elastic by the usual own-price definition. These are local conditional-demand slopes, not an estimate of an empirical market-capitalization response to flows. The $10%$ payout cut also changes the demand schedule itself, so the two colored equilibrium dots should not be used as a single-curve elasticity calculation.
