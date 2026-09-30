# Figure style for Unreasonable Doubt

Use the [five rendered trials](style_trials/comparison.png) when choosing a visual treatment. They plot the same saved lifecycle-model sweep, so differences in readability come from design rather than data. The [rendering script](../scripts/render_style_trials.py) regenerates them. These are directions for new figures, not a reason to restyle an established post without a request.

## Default: editorial paper

[View the full-size example](style_trials/01_editorial_paper.png). Use this for a new blog figure unless the subject or surrounding figures call for another treatment.

| Role | Hex |
| --- | --- |
| Canvas | `#FBF8F1` |
| Main text | `#24313A` |
| Secondary text | `#626D70` |
| Horizontal guides | `#DFDED7` |
| Main series | `#176B78` |
| Comparison series | `#B25739` |

At a roughly 9.6-inch export width, start with a 3-point solid main line and a 2.5-point dashed comparison line (`(5, 3)` dash pattern). Use end labels beside the lines when they fit, a marker at a value named in the label, and light horizontal guides. Keep text labels on the canvas; the two series colors have at least 4.5:1 contrast against it. Use DejaVu Sans for axes and labels; a restrained serif title can work when the chart needs its own headline. A blog caption may already supply the headline, in which case leave the title out of the image.

Colors name roles within a figure, not universal concepts: teal is not always “baseline,” and rust is not always “policy.” Keep a chosen meaning stable across related figures. Distinguish important series by dash pattern, marker, or direct label as well as hue. If a figure needs more than two prominent series, first consider highlighting one line and muting the rest, or using small multiples.

## Five trials and when to use them

| Trial | Treatment | Best use |
| --- | --- | --- |
| [01 Editorial paper](style_trials/01_editorial_paper.png) | Warm canvas, teal and rust, end labels, minimal framing | Default blog figure. |
| [02 Analytical white](style_trials/02_analytical_white.png) | White canvas, blue `#006A9F` and orange `#C66E2A`, distinct markers and dashes | Dense technical figures or a white page where the canvas should disappear. |
| [03 Focus ink](style_trials/03_focus_ink.png) | Graphite context line, brick red `#B64C42` for one focal claim, subtle band | One result deserves explicit emphasis; check that the highlight does not imply a threshold that the model has not established. |
| [04 Small multiples](style_trials/04_small_multiples.png) | Separate panels and endpoint changes | Two outcomes have different denominators or ranges. State when panel scales differ, and label the change in each panel. |
| [05 Night](style_trials/05_night.png) | Dark navy `#152636`, cyan `#62CFC8`, gold `#F0BC68` | Slides or a dark presentation surface; avoid as the routine blog export. |

The examples use one return sweep: stock portfolio share rises by about 37 percentage points while the saving rate rises by about 1.1 points. The plotted values are model output, not observed data. The comparative designs follow the Financial Times' [Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md) in choosing a chart for the claim, and Datawrapper's guidance to [label near the data](https://www.datawrapper.de/blog/text-in-data-visualizations) and [distinguish series beyond color](https://www.datawrapper.de/blog/colorblindness-part2). These examples are original treatments, not copies of either publisher's brand.

## Export checks

Label quantities and units, and state whether the values are model output, illustration, or observed data. Put external source details in the caption or a quiet source line. Prefer a focused chart with a short title or no title when the post supplies a caption. At likely reading size, check end labels, ticks, annotation overlap, and whether a low-movement series remains visible. Export a PNG at about 200 DPI for blog use; use vector output when the destination accepts it and fine type matters. Open the saved file before treating the figure as finished.
