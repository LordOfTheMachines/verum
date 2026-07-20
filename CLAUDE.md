# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this project is

Verum is a lightweight universal document viewer — PDF first, then images,
text and office formats. Python 3.12+ / PyQt6 / PyMuPDF / pikepdf, managed with
uv. GPL-3.0-or-later.

Read [PROGRESS.md](PROGRESS.md) before assuming anything exists: as of Phase 0
there is **no runnable application**, only package scaffolding.

## Commands

```bash
uv sync                        # install dev environment
uv run ruff check .            # lint
uv run ruff format .           # format
uv run mypy                    # type check (strict)
uv run pytest --cov            # tests with coverage
uv run pytest tests/unit/test_package.py::test_version_is_exposed  # single test
```

All four checks must pass before committing — CI runs the same set on Linux and
Windows across Python 3.12 and 3.13.

## Architecture rules

Layering is `ui → core → backends`, and the dependency arrow points down only.

- **`verum.core` and `verum.backends` must never import `verum.ui` or `PyQt6`.**
  This is the project's one hard rule; it keeps the core headless-testable and
  keeps a future Rust port viable.
- Rasterisation never runs on the Qt main thread.
- Opening a document never mutates it. Writes are explicit and opt-in.
- Backend exceptions are wrapped in `verum.core.errors` types at the core
  boundary — the UI must never see a `fitz.*` or `pikepdf.*` exception.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full design and the module map.

## Conventions

- Line length 100; ruff lint rules `E, F, W, I, N, UP, B, C4, SIM`.
- Full type annotations — mypy runs in `strict` mode over `src` and `tests`.
- Every module gets a docstring; public functions get one when the name is not
  self-evident. No commentary that restates the code.
- The version lives **only** in `src/verum/__init__.py`; hatchling reads it.
- Prose in docs and code is English. Conversation with the maintainer is
  Turkish.

## Git

- **Commits are authored solely by Mehmet Gilik.** Never add a
  `Co-Authored-By: Claude ...` trailer, and never add "Generated with Claude
  Code" to a commit message or PR body. This repository is public and its
  contributor list should reflect the maintainer only.
- Conventional-commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`,
  `test:`, `perf:`, `ci:`.
- `main` is the default branch. Work on a feature branch and open a PR when the
  change is non-trivial.
- `origin` is HTTPS (`https://github.com/LordOfTheMachines/verum.git`) and
  authenticates through the `gh` credential helper — do not switch it to SSH,
  there is no key on this machine.

## Where things go

| Adding... | Goes in |
| --- | --- |
| a file-format reader | `src/verum/backends/<format>.py` |
| document/render/cache logic | `src/verum/core/` |
| a window, widget or dialog | `src/verum/ui/` |
| a headless test | `tests/unit/` |
| a full-stack test | `tests/integration/` |
| an architectural decision | `docs/adr/NNNN-title.md` |
| a closed roadmap item | a line in `PROGRESS.md` |
