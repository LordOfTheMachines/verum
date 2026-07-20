# Progress

A running log of what actually exists, as opposed to what is planned. Update
this file whenever a roadmap item closes.

**Current phase:** Phase 0 complete → Phase 1 (PDF viewing MVP) not started.
**Runnable application:** no.

---

## Status by phase

| Phase | State | Notes |
| --- | --- | --- |
| 0 — Project setup | ✅ complete | tooling, licence, CI, docs |
| 1 — PDF viewing (MVP) | ⬜ not started | 16 tasks, see ROADMAP.md |
| 2 — Reading experience | ⬜ not started | |
| 3 — PDF editing | ⬜ not started | |
| 4 — Image formats | ⬜ not started | |
| 5 — Document formats | ⬜ not started | |
| 6 — OCR | ⬜ not started | |
| 7+ — Hardening & packaging | ⬜ not started | |

## What exists on disk

```
src/verum/
├── __init__.py          # __version__ only — the version source of truth
├── py.typed             # PEP 561 marker
├── backends/__init__.py # docstring only, no backends yet
├── core/__init__.py     # docstring only, no core yet
└── ui/__init__.py       # docstring only, no widgets yet

tests/
├── unit/test_package.py # import + version smoke tests
└── integration/         # empty
```

Total production code: package metadata and layer docstrings. **No document is
openable yet.**

## Quality gate

Run before every commit; CI enforces the same four:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov
```

Last local run (2026-07-20): all green — 2 tests, 8 files type-checked,
100 % coverage of the 2 statements that exist.

---

## Log

### 2026-07-20 — Phase 0 closed out

Audit of the repository found it half-scaffolded and partly broken. Fixed:

- **`pytest-qt` broke the entire test suite.** It was in the dev group without
  any Qt binding installed, so pytest aborted during collection — the suite had
  never run. Removed until Phase 1 brings PyQt6 with it.
- **Broken console script.** `[project.scripts] verum = "verum.app:main"`
  pointed at a module that does not exist; `uv run verum` crashed. Removed with
  a note; it returns in task 1.7.
- **Missing `LICENSE`.** README linked to a file that was never committed,
  leaving a public repo with no licence text despite declaring GPL-3.0-or-later.
  Added the full GPL-3.0 text.
- **Empty `.github/` and `docs/adr/`.** The directories existed locally but git
  does not track empty directories, so the repository had no CI at all. Added a
  CI workflow (ruff, ruff-format, mypy strict, pytest on Linux + Windows ×
  Python 3.12/3.13), issue templates and a PR template.
- **Version declared twice.** Hardcoded in `pyproject.toml` with nothing in the
  package. Now `dynamic = ["version"]`, read from `verum.__version__`.
- **Dev dependencies in the wrong table.** `[project.optional-dependencies]` →
  `[dependency-groups]`, matching how uv manages them.
- **Stray `end` file.** 1.9 KB of `git diff` output accidentally redirected into
  the working tree. Deleted.
- **Regenerable caches.** Removed `.mypy_cache/` and `.ruff_cache/` (2.3 MB).
- **Remote used SSH without a key**, so `git push` failed. Switched `origin` to
  HTTPS to match the authenticated `gh` credential helper.

Added: `ARCHITECTURE.md`, `ROADMAP.md`, `PROGRESS.md`, `CONTRIBUTING.md`,
`CLAUDE.md`, ADR-0001/0002, `[project.urls]`, coverage config, and the first
real tests.

### 2026-05-16 — Initial scaffold

Project skeleton, `.gitattributes` line-ending policy, README with vision and
roadmap (PR #1).
