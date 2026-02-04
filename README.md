# Unreasonable Doubt

Drafts, models, and supporting material for Unreasonable Doubt blog posts.

## Repository layout
- `old_blogs_style/`: Prior published posts used as style references (PDFs) and locally extracted text for quick search.
- `policy_arguments_framework/`: Current draft work (e.g., `policy_blog.md`).
- `demand_for_investment_is_inelastic/`: Reserved space for a future post (currently empty).
- `src/`: Code and modules to support figures/simulations (currently empty).

## Writing voice (quick take)
- Analytical, model-driven, and accessible to non-specialists.
- Uses clear signposting (e.g., “Concretely,” “Intuitively,” “Summarizing,” “Put differently”).
- Builds from simple assumptions to implications; includes worked examples.
- Avoids jargon when possible; defines key terms when used.

For full guidance, see `STYLE_GUIDE.md` and `POST_TEMPLATE.md`.

## About code development

Uses `uv` for Python.

Run scripts:
- `uv run python path/to/script.py`

Install packages (project dependencies):
- `uv add <package>` (e.g. `uv add numpy matplotlib`)
- `uv sync` to align the environment with `pyproject.toml`

Install packages for a standalone script:
- `uv add --script path/to/script.py <package>`
