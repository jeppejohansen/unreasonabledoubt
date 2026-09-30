---
name: graphics-coder
description: Design or revise code-generated figures for Unreasonable Doubt posts, including chart choice, labels, colors, export, and visual inspection. Use when a figure or its generating script is the task.
---

Read [figure style](references/figure-style.md) for the default visual system. Follow a post's existing visual semantics when they are already established, and honor any specific user preference.

Start from the claim the figure must help the reader understand. Choose the simplest chart that shows the mechanism or comparison, and make model output, illustration, and observed data visibly distinguishable. Put the generating script in the post's `src/` for new work and write the figure to its `figures/`. Keep external images or data in `assets/` with attribution.

Run the script and inspect the exported figure at likely reading size. Check units, axes, legend, color contrast, line styles, annotation overlap, and whether the caption can explain the takeaway. Adjust the code and inspect again if a concrete problem remains. Report the output path and any assumption behind the plotted data.
