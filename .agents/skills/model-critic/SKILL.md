---
name: model-critic
description: Critique a blog model's assumptions, equations, simulations, and conclusions, looking for unsupported leaps and sensitive parameters. Use for substantive model review, not general copy editing.
---

Read the draft or note alongside the equations, code, figures, and saved results relevant to the claim. Reconstruct the mechanism before judging it. Check that definitions and units stay consistent, the result follows from the assumptions, and the prose describes what was actually computed or plotted.

Probe the assumptions most likely to change the conclusion with a counterexample, limiting case, or targeted parameter variation. Use a small reproducible run when it materially resolves a question; avoid launching long simulations by default. Distinguish a flaw in logic or implementation from a contestable assumption and from a missing empirical basis.

Return the few highest-impact findings with file locations, why they matter, and a concrete way to test or revise them. State when a conclusion is robust under the checks performed and where the check was limited.
