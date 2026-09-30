---
name: blog-coder
description: Write or revise Python scripts that generate models, figures, and tables for an Unreasonable Doubt post. Use for post-specific code and reproducible outputs, not prose editing.
---

Follow the repo's [README](../../../README.md) for the current workflow. New post code belongs in `blogs/<slug>/src/`; generated numerical data, figures, and tables go to sibling `data/`, `figures/`, and `tables/`. Resolve paths from `Path(__file__).resolve().parents[1]` so the script works from any caller directory. Put externally sourced inputs in `assets/` and note their origin.

Use the shared `uv` environment and add project dependencies with `uv add`, updating `uv.lock`. Give long simulations a clear command-line entry point and seed stochastic runs when reproducibility matters. Make output names descriptive and make it clear which inputs and parameters produced them. Keep existing post layouts workable rather than relocating code merely to match new conventions.

Run a changed script when practical and inspect the generated figure or table. For costly models, use a small meaningful case if it exercises the changed logic; tell the user when a full run remains necessary.
