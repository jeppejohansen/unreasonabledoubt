# Social Mobility and Innovation Model: Summary

This note summarizes what the model is trying to explain, what is written in the Typst document, and how the Python simulation implements it.

## What the model is trying to explain

The model studies how social mobility frictions affect:

- occupational choice (blue-collar vs white-collar),
- the allocation of talent across occupations,
- sector productivity growth (technology accumulation),
- and, in the dynamic version, persistence across generations.

The core idea is:

- people choose occupations based on wages plus social frictions,
- talent allocation affects production and wages,
- talent allocated to a sector drives future technology in that sector,
- and social mobility frictions can distort this allocation.

## Conceptual model (Typst document)

The formal write-up is in `social_mobility_and_innovation/model.typ`.

### Agents and state

- Time is discrete.
- Each person has:
  - parental occupation background `g in {W, B}`
  - talent `h in [0,1]`
- Each person chooses occupation `s in {W, B}`.

### Production and wages

The model distinguishes:

- `Q_(t,s)`: effective talent in sector `s` (used in production/wages)
- `H_(t,s)`: raw talent in sector `s` (used in technology accumulation)

Production is CES in effective talent:

- `Y_t = CES(A_(B,t) Q_(t,B), A_(W,t) Q_(t,W))`

with parameter `rho`.

Important interpretation:

- Higher `rho` means more substitutability (not more complementarity) in this CES parameterization.

Wages:

- `w_(s,t)` is the wage rate per unit of effective talent (marginal product of sectoral effective talent).
- Individual earnings are:
  - `y_(s,t)(h) = w_(s,t) h^(eta_s)`

where `eta_W` and `eta_B` govern returns to talent by occupation.

### Occupational choice (ARUM)

Workers choose occupations using a random utility model with:

- wage/earnings differences,
- switching cost `c_g` (same parameter for both directions, relative to parent occupation),
- noise/friction `phi`.

The ARUM/logit setup implies:

- lower `phi` => choices more wage-responsive / deterministic,
- higher `phi` => noisier choices.

### Why talent sorting may or may not appear

If `eta_W = eta_B = 1`, then talent cancels from the choice margin:

- `log y_W(h) - log y_B(h)` does not depend on `h`

So in that special case:

- there is no talent sorting in occupational choice,
- talent matters for earnings levels and aggregates, but not for who chooses which occupation.

If `eta_W > eta_B`, then higher-talent individuals are more likely to choose white-collar:

- this generates talent sorting.

### Technology accumulation

Technology evolves using raw talent sums:

- `A_(W,t+1) = A_(W,t) + H_(t,W)`
- `A_(B,t+1) = A_(B,t) + H_(t,B)`

This is a deliberate modeling choice in the current draft.

Implication:

- production/wages depend on effective talent `Q`,
- technology depends on raw talent `H`.

This can produce weaker technology divergence than the wage/choice sorting patterns might suggest.

### Talent transmission (`omega`)

The Typst document now includes an intergenerational talent process with persistence parameter `omega in [0,1]`:

- `omega = 0`: parent and child talents are uncorrelated
- `omega = 1`: perfect transmission

Construction:

- with probability `omega`, child inherits parent talent exactly
- with probability `1 - omega`, child talent is redrawn from `U(0,1)`

This preserves a `U(0,1)` marginal talent distribution every period (starting from `U(0,1)`).

## Python simulation (`simulate_model.py`)

The simulation implementation is in `social_mobility_and_innovation/simulate_model.py`.

It is a finite-agent Monte Carlo approximation of the model:

- unit mass of population is approximated by `n_agents` agents,
- each agent has equal mass `1 / n_agents`.

### Main implementation logic

For each period:

1. Solve a within-period wage fixed point (using expected choices)
   - guess wages,
   - compute logit choice probabilities,
   - aggregate expected effective talent by sector,
   - update sector wage rates from marginal products,
   - iterate to convergence.

2. Sample realized occupations from the logit probabilities
   - this gives realized occupation assignments and realized `N_(t,s)`.

3. Compute realized aggregates
   - raw talent by sector `H_(t,s)` for technology,
   - effective talent by sector `Q_(t,s)` for production/wages,
   - output and wage rates.

4. Update technology
   - add realized raw talent `H_(t,s)` to each sector's technology.

5. Update intergenerational state
   - parental occupation background for next period becomes current realized occupation,
   - talents are transmitted using `omega`.

### Why the code uses both raw and effective talent

This is the main modeling/implementation distinction:

- Raw talent `H`:
  - used for technology accumulation.
- Effective talent `Q`:
  - used for production and wage rates when `eta_W` or `eta_B` differ from 1.

This matches the current Typst document.

### Parameters and defaults (current code)

Key defaults in the current Python code:

- `alpha = 0.5`
- `rho = 0.4`
- `phi = 0.35`
- `c_g = 0.15`
- `omega = 0.7`
- `eta_W = 1.0`, `eta_B = 1.0` (no-sorting special case)
- `A_W(0) = 1.25`, `A_B(0) = 1.0`
- talent distribution defaults to `U(0,1)`

### Figures and diagnostics generated by the script

The script generates:

- simulation overview (`A`, wages, occupation shares, talent/output),
- talent allocation diagnostics (`H`, gaps, composition, average talent by occupation),
- `p_W` vs talent (period 1 and final period),
- `p_W` vs talent conditional on parental background,
- production isoquants (CES substitution pattern).

Each figure now includes a footer with the key parameters used to generate it:

- `rho`, `phi`, `c_g`, `omega`, `eta_W`, `eta_B`

This is meant to prevent figure-parameter mismatches.

## Document / figure workflow (important)

The Typst document embeds static PNGs. It does not run Python automatically.

So if you change parameters in the simulation, you must:

1. rerun the Python script to regenerate figures, and
2. recompile the Typst document.

The document currently reads the default figure stem:

- `social_mobility_innovation_baseline*`

So the simplest workflow is:

```bash
uv run python social_mobility_and_innovation/simulate_model.py --rho 0.9
typst compile social_mobility_and_innovation/model.typ social_mobility_and_innovation/model.pdf
```

If you use a custom `--output-stem`, the document will not update unless you also change the image paths in `model.typ`.

## Current modeling caveats / open choices

These are not bugs, but they matter for interpretation:

- `rho` interpretation:
  - higher `rho` = more substitutability in this CES setup.
- `eta_W = eta_B = 1` implies no talent sorting in occupation choice by construction.
- Technology uses raw talent `H`, not effective talent `Q`.
  - if stronger divergence is desired, the technology law may need to depend on `Q` or a convex function of `H`.
- The simulation uses stochastic assignment (sampling from logit probabilities), so there is Monte Carlo noise.

## Suggested reading order

If you are trying to understand or extend the model:

1. Read the equations in `social_mobility_and_innovation/model.typ`
2. Read `simulate_model.py` top-to-bottom once
3. Inspect the talent-allocation diagnostics figure first when something looks surprising
4. Check the parameter footer on each figure before interpreting differences
