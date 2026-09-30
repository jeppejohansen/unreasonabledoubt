= Model of social mobility and innovation

This note presents a simple dynamic Roy-style model of how social mobility frictions can affect occupational sorting and innovation over time. Individuals choose between blue-collar and white-collar work, and those choices shape the allocation of talent across sectors.

The model is intentionally compact. It keeps the choice problem, production side, and intergenerational transmission process simple enough to analyze and simulate, while still making the main mechanisms explicit: social frictions affect sorting, sorting affects sectoral talent, and sectoral talent affects future technology.

*Big-picture summary (what this model is trying to explain)*

At a high level, the model asks a dynamic allocation question: if social mobility is imperfect, how much does that matter not only for who gets which jobs today, but for the economy's future path of innovation? The central idea is that occupational choice is not just a distributional outcome. It also determines where talent is deployed, and where talent is deployed affects which sector's technology improves over time. In that sense, mobility frictions can create a compounding effect: a small distortion in who enters white-collar work today can change wages, technology, and incentives tomorrow, which then feeds back into later generations' choices.

The model is designed to separate several mechanisms that are often conflated. First, there is a *social friction* channel: people may prefer (or find it easier) to remain in the occupation associated with their parents, represented here as a switching cost. Second, there is a *market incentive* channel: workers respond to wage differences across occupations. Third, there is a *talent sorting* channel: if the return to talent is higher in one occupation than the other, high-talent individuals have stronger incentives to sort into that occupation. Finally, there is a *dynamic technology* channel: sectoral technology evolves as a function of the talent working in that sector, so allocation decisions today affect productivity tomorrow.

The occupation-choice block is the model's behavioral core. Each person chooses between blue-collar and white-collar work based on expected earnings and a background-dependent friction. The random-utility (ARUM/logit) specification makes this choice probabilistic rather than perfectly deterministic, which is useful for two reasons. Substantively, it allows the model to represent noise, unobserved preferences, or institutional frictions not fully captured by wages. Computationally, it produces smooth choice probabilities that make the within-period equilibrium easier to solve. The parameter $phi$ controls how responsive choices are to wage differences, while $c_g$ governs how strongly parental background tilts individuals toward their inherited occupation.

Talent enters through two related but conceptually distinct objects. On the individual side, talent affects earnings within each occupation. This is where the parameters $(eta_W, eta_B)$ matter: they determine how much additional talent translates into earnings in white-collar versus blue-collar work. If these returns are the same, talent may have little or no effect on the occupational margin; if white-collar returns rise more steeply with talent, higher-talent individuals sort disproportionately into white-collar work. This lets the model cleanly toggle between a no-sorting benchmark and specifications with strong sorting, without changing the rest of the structure.

On the production side, the model aggregates workers into sectoral talent inputs and combines them using a CES production function. This is the main place where the parameter $rho$ matters. Intuitively, $rho$ governs how easily the economy can substitute between blue-collar and white-collar talent when one sector becomes relatively scarce. If substitution is easier, distortions in one sector's talent allocation are less costly in the short run; if substitution is harder, those distortions bite more sharply. This production block determines sectoral wage rates, so it closes the feedback loop back to occupational choice: wages affect choices, and choices determine the talent inputs that generate wages.

The technology block makes the model dynamic in a substantive way rather than just repeating a static occupational-choice problem over time. Sector-specific technologies evolve as functions of sectoral talent, so current allocation affects future productivity. In the current version, the law of motion depends on raw talent totals by sector, while production and wages can depend on effective talent. This distinction is deliberate: it allows the model to represent a case where sorting can strongly affect earnings and current output even if the long-run innovation consequences are more muted (or vice versa, depending on the calibration). It also makes diagnostics more informative, because one can separately inspect who is choosing each occupation, how much raw talent is allocated, and how much effective talent is used in production.

The intergenerational transmission block is what turns mobility frictions into persistent social dynamics rather than a one-period wedge. Children inherit both a social background (through parental occupation) and, probabilistically, talent (through the parameter $omega$). When $omega$ is high, talent persistence reinforces occupational persistence: if high-talent parents are more likely to be in one occupation, their children are both socially and economically more likely to remain there. When $omega$ is low, the social background channel remains, but the talent channel resets more quickly. This lets the model ask whether observed persistence comes mostly from social frictions, talent inheritance, or the interaction of the two.

Putting the pieces together, the model is meant to answer questions like: When do mobility frictions mostly change *who earns what* versus when do they also change *how fast sectors innovate*? How much does talent sorting amplify or dampen those effects? Does greater substitutability across sectors reduce the long-run cost of misallocation, or can dynamic technology accumulation still produce large path dependence? And how do these answers change when talent is highly persistent across generations versus rapidly reshuffled?

The simulation results are therefore best interpreted as a set of mechanism checks rather than a full quantitative calibration. The key outputs track occupation shares, mobility rates, sectoral wage rates, sectoral talent allocation, and technology paths over time. Looking at these objects together helps distinguish different stories that can look similar in one statistic alone. For example, a widening wage gap could reflect technology divergence, stronger talent sorting, or simply lower substitution; likewise, weak technology divergence can coexist with sharp sorting if the technology law of motion depends on raw rather than effective talent. The value of the model is that it puts these channels in one coherent dynamic framework and makes their interaction transparent.

*Environment*

Time is discrete, indexed by $t = 0, 1, 2, dots$. There is a unit mass of individuals. Each individual is characterized by:

- a parental occupation background $g in {W, B}$
- a talent level $h$ inherited from their parent

Each person chooses one occupation $s in {B, W}$ (blue-collar or white-collar).

In the baseline version, occupation choice depends on:

- wages in each occupation
- social background, through a switching cost $c_g$
- a common noise/friction parameter $phi$
- sector-specific returns to talent $(eta_W, eta_B)$ through earnings $y_s(h) = w_s h^(eta_s)$

Talent affects earnings through sector-specific returns to talent. When $eta_W = eta_B = 1$, talent cancels out of the occupation-choice margin, so there is no talent sorting in occupational choice.

*Production function and wages*

Let $Q_(t,s)$ denote effective talent allocated to sector $s$ at time $t$:

$
  Q_(t,s) = sum_(i: s_(i,t) = s) h_(i,t)^(eta_s)
$

Aggregate output is produced with a CES technology that combines effective talent allocated to blue- and white-collar work:

$
  Y_t = [alpha (A_(B,t) Q_(t,B))^rho + (1 - alpha) (A_(W,t) Q_(t,W))^rho]^(1 / rho)
$

with $rho < 1$. We also track occupation shares $(N_(B,t), N_(W,t))$ separately for mobility dynamics.

Define

$
  Z_t = alpha (A_(B,t) Q_(t,B))^rho + (1 - alpha) (A_(W,t) Q_(t,W))^rho
$

so $Y_t = Z_t^(1 / rho)$.

Let $w_(s,t)$ denote the wage rate per unit of effective talent in sector $s$. This is the marginal product of sectoral effective talent:

$
  w_(B,t) = alpha A_(B,t)^rho Q_(t,B)^(rho - 1) Z_t^(1 / rho - 1)
$

$
  w_(W,t) = (1 - alpha) A_(W,t)^rho Q_(t,W)^(rho - 1) Z_t^(1 / rho - 1)
$

An individual with talent $h_i$ who works in sector $s$ earns:

$
  y_(s,t)(h_i) = w_(s,t) h_(i,t)^(eta_s)
$

*Choosing sector to work in (ARUM with parental switching costs)*

Occupation choice is modeled as a random-utility problem (ARUM). A worker's background is their parent's occupation $g in {W, B}$.

Let $c_g$ be the cost of switching away from the parent's occupation.

Systematic utility is background-dependent:

$
  V_(W|W,t)(h_i) = log y_(W,t)(h_i), quad V_(B|W,t)(h_i) = log y_(B,t)(h_i) - c_g
$

$
  V_(W|B,t)(h_i) = log y_(W,t)(h_i) - c_g, quad V_(B|B,t)(h_i) = log y_(B,t)(h_i)
$

Add idiosyncratic shocks:

$
  U_(s|g,t) = V_(s|g,t) + phi epsilon_s
$

with iid Type-I extreme value shocks $epsilon_s$. The parameter $phi > 0$ is a common noise (or friction) scale.

- As $phi -> 0$, choices become nearly deterministic (within each background).
- As $phi$ increases, choices become less wage-responsive / more noisy.

Under this specification,

$
  log y_(W,t)(h_i) - log y_(B,t)(h_i) = log w_(W,t) - log w_(B,t) + (eta_W - eta_B) log h_(i,t)
$

So $eta_W > eta_B$ generates talent sorting into white-collar occupations. The no-sorting special case is $eta_W = eta_B = 1$, where talent cancels from the choice margin and $p_(W|g,t)$ is independent of $h_i$.

Choice probabilities are logit within each background:

$
  p_(W|g,t) = exp(V_(W|g,t) / phi) / (exp(V_(W|g,t) / phi) + exp(V_(B|g,t) / phi))
$

and $p_(B|g,t) = 1 - p_(W|g,t)$.

Occupation shares are summary statistics (useful for reporting and diagnostics), computed directly from realized assignments:

$
  N_(t,s) = sum_(i: s_(i,t) = s) 1
$

In particular, $N_(t,W) + N_(t,B) = 1$ (unit mass population).

== Law of motion.

Technology evolves with sectoral talent allocation, while talent itself follows the intergenerational transmission process below.

*Technology development*

Let $H_(t,s)$ denote raw talent (the sum of $h$) working in sector $s$ at time $t$:

$
  H_(t,s) = sum_(i: s_(i,t) = s) h_(i,t)
$

Technology accumulation is proportional to the raw talent working in each sector:

$
  A_(W,t+1) =  A_(W,t) + H_(t, W)
$

$
  A_(B,t+1) =  A_(B,t) + H_(t, B)
$

*Transmission of talent*

Let $omega in [0,1]$ index intergenerational persistence of talent. We want:

- $omega = 0$: parent and child talents are uncorrelated
- $omega = 1$: perfect transmission
- talent remains $U(0,1)$ in every period

An exact construction is:

$
  b_(i,t+1) in {0,1}, quad Pr(b_(i,t+1) = 1) = omega, quad u_(i,t+1) ~ U(0,1)
$

with $b_(i,t+1)$ and $u_(i,t+1)$ independent of each other and of $h_(i,t)$. Define

$
  h_(i,t+1) = b_(i,t+1) h_(i,t) + (1 - b_(i,t+1)) u_(i,t+1)
$

Interpretation: with probability $omega$, the child inherits the parent's talent exactly; with probability $1 - omega$, talent is redrawn independently from $U(0,1)$.

This does *not* rely on the false claim that an arbitrary mixture of uniforms is uniform. The relevant fact here is narrower: if $h_(i,t)$ already has marginal distribution $U(0,1)$, then $h_(i,t+1)$ is a mixture of two *identical marginals* ($h_(i,t)$ and $u_(i,t+1)$, both $U(0,1)$), so it is again $U(0,1)$.

Equivalently, for any $x in [0,1]$,

$
  Pr(h_(i,t+1) <= x) = omega Pr(h_(i,t) <= x) + (1 - omega) Pr(u_(i,t+1) <= x) = omega x + (1 - omega) x = x
$

Hence, starting from $h_(i,0) ~ U(0,1)$, talent is uniformly distributed in every period.

Moreover, under this construction the parent-child talent correlation is exactly $omega$, so $omega$ directly controls intergenerational talent persistence.

== Clarifying illustrations and intuition

*Talent transmission geometry (goal: visualize how $omega$ changes parent-child persistence)*

The next figure isolates the talent transmission rule itself using synthetic draws from the model's inheritance/redraw mechanism. The panels show parent talent on the x-axis and child talent on the y-axis for three values of $omega$. As $omega$ rises, more mass lies on the 45-degree line (exact inheritance), while the redraw component continues to fill the unit square.

#figure(
  image("figures/talent_transmission_omega_comparison.png", width: 100%),
  caption: [Talent transmission illustration: parent-child talent mappings for $omega in {0.00, 0.50, 1.00}$ under the inherit-or-redraw rule with $U(0,1)$ parent talent and redraws.],
)

*CES substitution geometry diagnostic (goal: build intuition for $rho$ before comparative statics)*

The original single-panel isoquant plot was hard to compare across values of $rho$. The next figure shows five isoquant panels in a common layout, with one factor on each axis, holding technology fixed and varying only $rho$ so the substitution geometry is directly visible (including near-Leontief and near-linear cases).

#figure(
  image("figures/social_mobility_innovation_final_production_isoquants.png", width: 100%),
  caption: [CES production isoquants in $(Q_B, Q_W)$ space for $rho in {0.05, 0.25, 0.50, 0.75, 0.95}$, shown in a common-layout comparison with shared contour levels. Higher $rho$ corresponds to greater substitutability in this parameterization.],
)

== Simulations

This final section collects all simulation-based figures in one place.

*Baseline dynamic benchmark (goal: establish the joint paths of technology, wages, mobility, sorting, and talent allocation)*

The figures in this block are all generated from the same simulation run (same DGP) and read from files with stem `social_mobility_innovation_final` (the output stem used by the `just simulate` command). The goal is to show, in one place, the joint behavior of technology, wages, mobility, sorting, and talent allocation before moving to comparative exercises.

#figure(
  image("figures/social_mobility_innovation_final.png", width: 95%),
  caption: [Simulation overview (single DGP): technology, wage rates, occupation shares/mobility, and occupation-specific talent distributions (fan plots).],
)

*Baseline choice diagnostics (goal: show how talent and parental background shape occupational choice)*

#figure(
  image("figures/social_mobility_innovation_final_p_w_talent_snapshots.png", width: 95%),
  caption: [Period 1 and period T (same DGP): talent vs occupation choice (overall), shown as empirical white-collar shares by talent bin and model-implied $p_W$.],
)

#figure(
  image("figures/social_mobility_innovation_final_p_w_talent_by_background_snapshots.png", width: 95%),
  caption: [Period 1 and period T (same DGP): talent vs occupation choice conditional on parental background ($W$-parent vs $B$-parent), with model-implied conditional $p_W$.],
)

The two $p_W$ plots above show conditional choice probabilities by talent bin (and empirical white-collar rates by bin). They do *not* directly show total talent allocated to each sector.

*Baseline allocation diagnostics (goal: connect sorting patterns to the technology law of motion)*

The next figure shows the actual raw talent sums $H_W$ and $H_B$ over time (the objects that drive technology in the current law of motion), together with the implied technology gap and composition diagnostics, for the same DGP.

#figure(
  image("figures/social_mobility_innovation_final_talent_allocation_diagnostics.png", width: 95%),
  caption: [Same DGP: raw talent sums by sector over time, talent-gap vs technology-gap, worker earnings by occupation (fan plots), and average talent by occupation with headcount shares.],
)


*Comparative $rho$ sweep with fixed sorting (goal: isolate substitution effects while holding sorting incentives fixed)*

The figures below compare three deterministic grid simulations with $eta_W = 1.25$, $eta_B = 1.0$, and $rho in {0.25, 0.50, 0.75}$. They are generated by the `just simulate-rho025`, `just simulate-rho050`, and `just simulate-rho075` commands.

*Case A: lower substitutability ($rho = 0.25$)*

#figure(
  image("figures/social_mobility_innovation_eta125_rho025.png", width: 95%),
  caption: [Simulation overview with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.25$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho025_p_w_talent_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent (overall) with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.25$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho025_p_w_talent_by_background_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent by parental background with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.25$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho025_talent_allocation_diagnostics.png", width: 95%),
  caption: [Talent allocation diagnostics with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.25$.],
)

*Case B: intermediate substitutability ($rho = 0.50$)*

#figure(
  image("figures/social_mobility_innovation_eta125_rho050.png", width: 95%),
  caption: [Simulation overview with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.50$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho050_p_w_talent_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent (overall) with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.50$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho050_p_w_talent_by_background_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent by parental background with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.50$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho050_talent_allocation_diagnostics.png", width: 95%),
  caption: [Talent allocation diagnostics with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.50$.],
)

*Case C: higher substitutability ($rho = 0.75$)*

#figure(
  image("figures/social_mobility_innovation_eta125_rho075.png", width: 95%),
  caption: [Simulation overview with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.75$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho075_p_w_talent_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent (overall) with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.75$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho075_p_w_talent_by_background_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent by parental background with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.75$.],
)

#figure(
  image("figures/social_mobility_innovation_eta125_rho075_talent_allocation_diagnostics.png", width: 95%),
  caption: [Talent allocation diagnostics with $eta_W = 1.25$, $eta_B = 1.0$, and $rho = 0.75$.],
)

*High-sorting low-$rho$ stress test (goal: show how strong sorting and low noise can amplify dynamics)*

The figures below show a deterministic grid simulation with strong talent sorting at low substitutability: $rho = 0.25$, $eta_W = 2.0$, $eta_B = 1.0$, $phi = 0.05$, $c_g = 0.15$, and $omega = 0.70$. This run is generated by `just simulate-rho025-highsorting`.

#figure(
  image("figures/social_mobility_innovation_eta200_rho025_highsorting.png", width: 95%),
  caption: [Simulation overview for a high-sorting specification with $rho = 0.25$, $eta_W = 2.0$, and low noise ($phi = 0.05$).],
)

#figure(
  image("figures/social_mobility_innovation_eta200_rho025_highsorting_p_w_talent_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent (overall) for the high-sorting low-$rho$ specification.],
)

#figure(
  image("figures/social_mobility_innovation_eta200_rho025_highsorting_p_w_talent_by_background_snapshots.png", width: 95%),
  caption: [Occupation choice vs talent by parental background for the high-sorting low-$rho$ specification.],
)

#figure(
  image("figures/social_mobility_innovation_eta200_rho025_highsorting_talent_allocation_diagnostics.png", width: 95%),
  caption: [Talent allocation diagnostics for the high-sorting low-$rho$ specification.],
)
