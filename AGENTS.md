# Repository Guidelines

## Project Structure & Module Organization
- `README.md`, `STYLE_GUIDE.md`, `POST_TEMPLATE.md`: overview, voice guidance, and post template.
- `COMMENTS.md`: editorial notes organized by blog directory (one heading per draft folder).
- `policy_arguments_framework/`: active draft work, including `policy_blog.md`, `plots_carbon_example.py`, and generated figures in `policy_arguments_framework/figures/`.
- `old_blogs_style/`: prior published posts in PDF plus extracted text for reference.
- `pyproject.toml`, `uv.lock`: Python environment and dependency lockfile.

## Build, Test, and Development Commands
- `uv sync`: align the local environment with `pyproject.toml`.
- `uv run python policy_arguments_framework/plots_carbon_example.py`: run the plotting script to regenerate figures.
- `uv add <package>`: add a project dependency (example: `uv add pandas`).
- `uv add --script path/to/script.py <package>`: add dependencies for a standalone script.

## Coding Style & Naming Conventions
- Writing: follow `STYLE_GUIDE.md` and start new drafts from `POST_TEMPLATE.md`. Keep sections short with clear headings and explicit signposts (e.g., “Concretely,” “Intuitively,”).
- Python: 4-space indentation; `snake_case` for variables/functions; `lowercase_with_underscores.py` for scripts.
- Figures: use descriptive filenames like `policy_arguments_framework/figures/carbon_emissions_paths.png`.

## Testing Guidelines
- No automated test suite is configured.
- Validate scripts by running them and visually checking outputs in `policy_arguments_framework/figures/`.

## Commit & Pull Request Guidelines
- Commit history favors short, direct summaries (e.g., “updated plots”, “Fix README title casing”). Keep messages brief and specific to the change.
- If using PRs, include a concise description, list updated drafts/figures, link any related issue or draft, and attach screenshots for figure changes.

## Security & Configuration Tips
- Manage dependencies via `uv`; update `uv.lock` whenever adding or upgrading packages.
