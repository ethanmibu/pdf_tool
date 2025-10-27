## Repo: pdf_tool (pdf_toolkit)

This file gives focused, actionable guidance for AI coding agents working on this repository.

High-level goal
- Provide and maintain a small, well-tested CLI + optional GUI for merging/splitting PDFs locally.
- Keep changes simple and focused — this project avoids heavy dependencies and prefers small, readable functions.

Key entry points
- CLI: `pdf_toolkit.cli:main` (see `pdf_toolkit/cli.py`). The CLI uses argparse with subparsers for `merge`, `split`, and `gui`.
- Module runner: `python -m pdf_toolkit` triggers `pdf_toolkit.__main__` which calls `cli.main()`.
- GUI: `pdf_toolkit.gui.launch_gui()` (opt-in; importing GUI is guarded and only attempted with `--force`).

Important files to consult
- `pdf_toolkit/cli.py` — command parsing, `resolve_input_path()` behavior, and defaults from `config.load_config()`.
- `pdf_toolkit/config.py` — `load_config()` reads `config.json` from the repo root and merges with defaults `{input_dir: "input", output_dir: "output"}`.
- `pdf_toolkit/merge.py` — `merge_pdfs(input_paths, output_path)` uses pypdf to stream pages into a `PdfWriter` and ensures output dirs exist.
- `pdf_toolkit/split.py` — `split_pdf(input_path, output_dir, start_page=None, end_page=None)` supports per-page exports and inclusive ranges; it raises `ValueError` on invalid ranges.
- `pdf_toolkit/gui.py` — lightweight tkinter UI. Import guarded; use `can_launch_tkinter()` logic when adding GUI features.
- `tests/` — `test_merge.py`, `test_split.py` demonstrate test patterns and pypdf usage (tests create blank pages with `PdfWriter.add_blank_page`).

Project workflows / commands
- Local dev/test (preferred): create a venv and install `requirements.txt`.
  - Makefile provides helpers: `make install` (creates .venv + installs), `make test` (runs pytest under venv), `make run-merge`, `make run-split`.
- Quick test: `python -m pytest -q` (ensure venv active or dependencies installed).
- CLI examples (from README):
  - Merge: `python -m pdf_toolkit merge input1.pdf input2.pdf -o output/merged.pdf`
  - Split all pages: `python -m pdf_toolkit split input.pdf --all`

Repository-specific conventions
- Paths: CLI resolves input paths by checking (in order): given path, `input_dir/<path>`, `output_dir/<path>` (see `resolve_input_path`). When adding features that accept paths, mirror this resolution behavior.
- Config: prefer `config.json` for user-tunable defaults; `config.load_config()` silently falls back to defaults and tolerates malformed JSON.
- GUI import: importing tkinter and launching the GUI can crash some macOS Pythons — the project intentionally keeps GUI imports guarded and opt-in via `--force`. Preserve that opt-in pattern.
- Minimal dependencies: this project intentionally relies only on `pypdf` for PDF manipulation. Avoid adding heavy libraries without strong reason.

Testing and code style notes
- Tests use `pytest` and create temporary PDFs using `pypdf.PdfWriter.add_blank_page` — mimic this pattern in tests to avoid embedding binary fixtures.
- Functions return concrete Path-like objects: `merge_pdfs` returns the output Path, `split_pdf` returns a list of generated Paths. When changing signatures, update tests accordingly.

When adding features (how an AI should proceed)
1. Read `cli.py` and follow its argparse + subparser pattern if you add a new subcommand.
2. Use `resolve_input_path()` for any new path arguments to match UX expectations.
3. Add unit tests under `tests/` using `tmp_path` fixtures and the `pypdf` helper pattern from existing tests.
4. Keep GUI changes opt-in — don't import tkinter at module import time.
5. Update `pyproject.toml` if new runtime dependencies are needed and add them to `requirements.txt` for the test/dev flow.

Avoid
- Importing tkinter or other platform-sensitive modules at package import time.
- Changing the default config shape — `config.json` is intentionally simple.

Examples to reference in completions
- To add a `validate_pdf` helper: place it near `merge.py`/`split.py`, return Path objects, and write tests that create blank pages (see `tests/test_merge.py`).
- To add CLI flags: mirror naming and defaults in `cli.py`, include help text, and update README usage examples.

If anything above is ambiguous or you need examples for a specific change (new subcommand, refactor, or GUI tweak), ask and I'll provide a targeted snippet referencing the exact lines to edit.

---
Request for feedback: Is the level of detail correct? Tell me which areas you want expanded (tests, packaging, GUI behavior, or common refactors) and I will iterate.
