# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Drafts, models, and supporting material for the **Unreasonable Doubt** blog. Each post lives in its own directory containing a markdown draft, Python scripts for generating figures/simulations, and a `figures/` output folder. The `old_blogs_style/` directory holds previously published posts (PDF + text) used as style references.

## Commands

```bash
# Run a Python script
uv run python path/to/script.py

# Add a project dependency
uv add <package>

# Sync environment with pyproject.toml
uv sync

# Add a dependency scoped to a standalone script
uv add --script path/to/script.py <package>
```

There is no test suite or linter configured.

## Architecture

- Each blog post gets its own top-level directory (e.g., `policy_arguments_framework/`, `demand_for_investment_is_inelastic/`).
- Within a post directory: `*.md` for the draft, `*.py` for figure/simulation scripts, `figures/` for generated PNGs.
- `src/modules/` is reserved for shared reusable code (currently empty).
- Python 3.12+, managed with `uv`. Dependencies: matplotlib, numpy, pypdf2.

## Writing Voice & Post Structure

Follow `STYLE_GUIDE.md` and `POST_TEMPLATE.md`. Key points:

- **Model-first reasoning:** Start from assumptions, build a mechanism, derive implications.
- **Accessible to non-specialists:** Define terms early, avoid unexplained jargon.
- **Post structure:** Hook → Setup → Model/Framework → Mechanism Walkthrough → Results/Implications → Conclusion → Notes/References.
- Use signpost phrases: "Concretely," "Intuitively," "Put differently," "Summarizing."
- Include at least one worked example per post.
- Distinguish between competing intuitions before resolving them.
- When using equations, keep them simple and explain each parameter in plain language.

## Figure Scripts

Plot scripts use matplotlib, save to `figures/` at 200 DPI as PNG. Figures should clearly label axes and describe the causal chain being illustrated.
