// Compact formal note for the market monetarist draft.
#set page(margin: (x: 0.8in, y: 0.8in))
#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true, leading: 0.45em)
#set list(spacing: 0.25em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 16pt)
#show heading.where(level: 2): set text(size: 13pt)

= A Market Monetarist Workhorse Model

This draft is deliberately only about primitives and assumptions. The aim is to state what the model takes as given before deriving anything from it. In particular, we do not yet derive velocity, aggregate demand, SRAS, the policy rule, or the behavior of nominal interest rates. Those belong in later sections.

The intended model is a compact market monetarist workhorse: forward-looking households, consumption smoothing, the quantity identity, endogenous short-run velocity, long-run monetary neutrality, some short-run nominal non-neutrality, and monetary policy understood as an expected nominal regime rather than as an interest-rate rule.

== Baseline Environment

Plain language. Time is discrete. There is one final good, a representative household, a nominal price level, real output, and a monetary asset used to settle transactions. To keep the first version clean, the baseline model abstracts from investment, government purchases, and net exports. Those can be added later, but they are not needed to state the core primitives.

The real object households care about is consumption. Nominal GDP is not in utility. It matters because it is the observable nominal value of economy-wide expenditure.

Math. Time is indexed by $t = 0, 1, 2, dots$. The main aggregate objects are:

$
  C_t, quad Y_t, quad Y_t^*, quad P_t, quad M_t.
$

Here $C_t$ is real consumption, $Y_t$ is realized real output, $Y_t^*$ is potential output, $P_t$ is the price level, and $M_t$ is the money stock. Nominal expenditure is

$
  X_t equiv P_t Y_t.
$

Velocity is defined by the quantity identity:

$
  M_t V_t = P_t Y_t = X_t,
  quad
  V_t equiv X_t / M_t.
$

Lowercase letters denote logs:

$
  x_t = p_t + y_t = m_t + v_t.
$

In the stripped-down closed-economy version, the aggregate resource constraint is simply

$
  C_t = Y_t.
$

This is not a theory of demand. It is only the resource constraint for the smallest useful version of the model.

== Rational Expectations

Plain language. Agents are forward-looking and use all available information when forming expectations. Rational expectations does not mean that everyone always forecasts correctly. It means forecast errors are not predictable using information already available at the time the forecast was made. If agents are surprised, the surprise must come from genuinely new information.

This matters because the model will rely on expectations about future real income and the future nominal regime. A household's current consumption choice depends on what it expects the future to look like. A central bank's current policy stance also depends on what markets expect future nominal expenditure to be.

Math. Let $I_t$ denote the information available at time $t$. For any future variable $Z_(t+j)$,

$
  E_t Z_(t+j) equiv E[Z_(t+j) | I_t].
$

The forecast error is

$
  epsilon_(t+j)^Z equiv Z_(t+j) - E_t Z_(t+j).
$

Rational expectations requires

$
  E_t epsilon_(t+j)^Z = 0.
$

Equivalently, forecast errors are orthogonal to information known at time $t$. If $W_t$ is any variable in $I_t$, then

$
  E[epsilon_(t+j)^Z W_t] = 0.
$

So when the model later speaks of expected future output, expected inflation, or expected NGDP, those expectations are conditional mathematical expectations, not ad hoc beliefs.

== Consumption Smoothing

Plain language. Households choose a path of consumption over time. They do not mechanically consume a fixed share of current income. Instead, they compare current consumption with future consumption and try to avoid unnecessary jumps in marginal utility.

This is the main behavioral primitive of aggregate demand in the model. If expected future real income rises, households feel richer today and want to spend more today. If expected future real income falls, households feel poorer today and want to spend less today. The model therefore has a direct channel from expected future real output to current expenditure.

Importantly, the household's utility is real. It values consumption, not nominal GDP. NGDP can become a signal and policy variable later, but it is not an argument of the utility function.

Math. Preferences are

$
  U_t = E_t sum_(j=0)^infinity beta^j u(C_(t+j)),
  quad
  0 < beta < 1,
  quad
  u' > 0,
  quad
  u'' < 0.
$

There is no direct utility term for nominal expenditure:

$
  U_t = U_t(C_t, C_(t+1), dots),
  quad
  partial U_t / partial X_t = 0.
$

Let $A_t$ be real financial wealth, $Y_t^n$ real disposable income, and $R_(t+1)^r$ the gross real return on the household's asset portfolio. The real budget constraint is

$
  A_(t+1) = R_(t+1)^r (A_t + Y_t^n - C_t).
$

For an interior optimum, consumption satisfies the Euler equation:

$
  u'(C_t) = beta E_t [R_(t+1)^r u'(C_(t+1))].
$

It is often useful to summarize future income by human wealth. Let $Q_(t,t+j)$ be the real discount factor. Then

$
  H_t = E_t sum_(j=0)^infinity Q_(t,t+j) Y_(t+j)^n.
$

Desired current consumption can then be written as an increasing function of total real wealth:

$
  C_t^d = c(A_t + H_t),
  quad
  c' > 0.
$

The primitive expectations channel is therefore

$
  E_t Y_(t+j)^n -> H_t -> C_t^d.
$

The model will later connect this desired consumption decision to nominal expenditure and velocity. That connection is not derived yet.

== Monetary Accounting and Velocity

Plain language. The quantity equation is an accounting identity. It says that the nominal value of transactions in final output equals the money stock times velocity. The identity itself does not say whether velocity is stable, unstable, exogenous, or endogenous.

The market monetarist move is to refuse to treat velocity as a constant. In this model, velocity is allowed to move because current expenditure is chosen by forward-looking households and because the monetary regime changes expectations about future nominal spending.

At this stage, however, velocity is only defined. We have not yet derived its short-run movements from the consumption problem.

Math. The identity is

$
  M_t V_t = P_t Y_t.
$

Equivalently,

$
  V_t = (P_t Y_t) / M_t = X_t / M_t.
$

At this stage, this is all we assume. Any claim that velocity has a stable long-run relation belongs in the derived model, not in the primitive accounting identity.

== Real Supply and Long-Run Neutrality

Plain language. Potential output is determined by real productive capacity: technology, labor, capital, institutions, and other real constraints. Monetary variables can affect realized output in the short run, but they do not create real productive capacity in the long run.

This is the classical long-run neutrality assumption. A permanent change in money may change the price level and nominal expenditure, but it does not permanently change potential output.

Math. Potential output is a real object:

$
  Y_t^* = F(A_t^r, K_t, N_t, z_t),
$

where $A_t^r$ is real technology, $K_t$ is capital, $N_t$ is labor input, and $z_t$ collects other real supply determinants. The important restriction is

$
  partial Y_t^* / partial M_s = 0
  quad "for monetary changes alone."
$

Long-run neutrality can be stated as

$
  lim_(j -> infinity) E_t (y_(t+j) - y_(t+j)^*) = 0.
$

For a permanent proportional increase in money, the long-run real effect is zero:

$
  lim_(j -> infinity) partial E_t y_(t+j) / partial m_t = 0.
$

In the same long-run comparison, the price level absorbs the nominal change:

$
  lim_(j -> infinity) partial E_t p_(t+j) / partial m_t = 1.
$

This is only a long-run restriction. It does not rule out short-run output effects from nominal disturbances.

== Minimal Short-Run Nominal Non-Neutrality

Plain language. The model assumes that nominal shocks can matter in the short run. Some nominal plans are made before all shocks are observed: wages, prices, debts, contracts, or coordination expectations. Because of that, unexpected changes in nominal expenditure need not be absorbed instantly and completely by the price level.

This is intentionally minimal. We are not yet committing to Calvo pricing, menu costs, fixed wages, debt-deflation, or a particular expectations-coordination mechanism. The primitive is only that short-run nominal expenditure surprises can move real output.

Math. Let $x_t = p_t + y_t$ be log nominal expenditure. The minimal non-neutrality condition is that, for short horizons, expected real output can respond to expected nominal expenditure:

$
  partial E_t (y_(t+h) - y_(t+h)^*) / partial E_t x_(t+h) > 0
  quad "for small" h.
$

Long-run neutrality requires this effect to disappear:

$
  lim_(h -> infinity)
  partial E_t (y_(t+h) - y_(t+h)^*) / partial E_t x_(t+h)
  = 0.
$

Later, this primitive can be given a specific microfoundation. For now it is only the assumption that gives the model room for an upward-sloping short-run aggregate supply curve.

== Monetary Policy as an Expected Nominal Regime

Plain language. Monetary policy is not defined by the current nominal interest rate. It is defined by the expected path of nominal expenditure that the central bank creates or permits. Open-market operations, communication, level targeting, futures-market convertibility, and interest-rate settings can all matter, but only because they change expectations about future nominal spending.

This is the market monetarist organizing assumption. The nominal interest rate is not the primitive policy variable. It is an equilibrium price of a nominal asset.

Math. Let the expected nominal regime at time $t$ be the expected path

$
  R_t^M equiv {E_t x_(t+j)}_(j=0)^infinity.
$

If the central bank has an NGDP-level target path, write it as

$
  x_(t+j)^T.
$

The policy-relevant object is the expected nominal expenditure gap:

$
  s_t(j) equiv E_t x_(t+j) - x_(t+j)^T.
$

This is a definition of the nominal stance, not yet a policy rule. A complete policy rule would specify how the central bank changes instruments when $s_t(j)$ differs from zero.

If we include a one-period nominal bond, let $q_t^n$ be its price in dollars today for one dollar tomorrow. The nominal interest rate is defined by

$
  1 + i_t = 1 / q_t^n.
$

The model will later price $q_t^n$ using the household Euler equation. At the primitive stage, the key point is simply that $i_t$ is an asset price, not the object that defines monetary ease or tightness.

== End Notes

The following pieces are intentionally not derived yet.

*Long-run velocity relation.* The model probably needs a meaningful long-run velocity relation, but it should not be imposed inside the quantity identity. A candidate object is

$
  v_t = bar(v) + tilde(v)_t,
  quad
  lim_(j -> infinity) E_t tilde(v)_(t+j) = 0.
$

The open question is what generates this: preferences, payment technology, banking institutions, portfolio choice, or some combination. Until that is specified, $V_t -> bar(V)$ should be treated as a target derivation rather than a primitive.

*Shock taxonomy.* The model should later distinguish three types of shocks.

First, real supply shocks change potential output. These are shocks to technology, labor supply, productivity, taxes, regulation, or other real productive constraints.

Second, nominal-demand or velocity shocks change nominal expenditure for a given real supply environment. These may come from money, payment technology, financial stress, or shifts in desired spending relative to money balances.

Third, expectation shocks change current behavior by changing expected future real income or the expected future nominal regime. Under rational expectations, these are not arbitrary beliefs; they are news about fundamentals, policy, or future states.

A later version can write these as:

$
  y_t^* = f(A_t^r, K_t, N_t, z_t) + a_t,
$

$
  mu_t: R_t^M -> {E_t x_(t+j)}_(j=0)^infinity,
$

$
  v_t = x_t - m_t,
$

and

$
  n_t^Z:
  E_t Z_(t+j) != E_(t-1) Z_(t+j).
$

The most important news shocks are news about future real income,

$
  n_t^Y:
  E_t Y_(t+j)^n != E_(t-1) Y_(t+j)^n,
$

and news about the future nominal regime,

$
  n_t^X:
  E_t x_(t+j) != E_(t-1) x_(t+j).
$

Their propagation through consumption, velocity, output, prices, and interest rates is derived later.

*Other missing derivations.*

- How the household consumption problem maps into aggregate nominal expenditure.

- How the velocity expression $V_t = P_t Y_t / M_t$ becomes an endogenous short-run object rather than merely an identity.

- What extra money-holding or settlement friction is needed, if any, to make the velocity microfoundation fully explicit.

- How a particular short-run aggregate supply curve is generated from wage contracts, sticky prices, debt contracts, or expectations-based coordination.

- Why the long-run aggregate supply curve is vertical in the full equilibrium.

- How NGDP becomes a useful signal and policy target without entering household utility.

- How to define monetary expansions and contractions by their effect on expected nominal expenditure.

- How the nominal interest rate is priced from the Euler equation.

- Why falling nominal rates can coexist with tight money, and rising nominal rates can coexist with easy money.

== Simulation Figures

These figures are generated by `math_notes/market_monetarist_math/src/simulate_workhorse.py`. They should be read as a test of one candidate closure of the primitives above, not as derivations already established in the text.

#figure(
  image("figures/expected_income_slump.png", width: 80%),
  caption: [Negative expected-income shock. The market monetarist closure offsets most of the consumption-smoothing pressure through the expected NGDP regime, while passive money and the Taylor-rule benchmark allow larger output gaps.],
)

#figure(
  image("figures/velocity_crash.png", width: 80%),
  caption: [Velocity or money-demand shock. A credible NGDP regime expands money enough to offset the fall in velocity pressure; passive money lets nominal expenditure fall.],
)

#figure(
  image("figures/negative_supply.png", width: 80%),
  caption: [Negative real supply shock. The shock lowers potential output, so actual output falls even when the output gap is stabilized. The useful comparison is whether the nominal regime avoids adding a demand shortfall on top of the real supply loss.],
)

#figure(
  image("figures/monetary_contraction.png", width: 80%),
  caption: [Contractionary nominal-regime shock. Both the market monetarist closure and passive-money case show that expected nominal expenditure is the object doing the work; interest rates are an equilibrium response.],
)

#figure(
  image("figures/interest_rate_source_test.png", width: 88%),
  caption: [Interest-rate source test. In the market monetarist closure, higher rates can coincide with faster growth when both are caused by an easier expected NGDP regime. A Taylor-rule policy-rate hike is contractionary in the New Keynesian benchmark. The point is not that rates mechanically cause growth; the point is that rates are an equilibrium price whose interpretation depends on the underlying shock.],
)

#figure(
  image("figures/nk_classic_diagnostics.png", width: 88%),
  caption: [Classic New Keynesian diagnostics. The first three columns show the textbook Taylor-rule responses to a natural-rate shock, a policy-rate shock, and a cost-push shock. The final column shows the rate-peg/Fisher terminal case: if the nominal interest rate is treated as the permanent nominal regime, a higher rate is associated with higher long-run inflation rather than a permanent contraction. This is the Cochrane-style warning about making the interest rate the primitive policy object.],
)
