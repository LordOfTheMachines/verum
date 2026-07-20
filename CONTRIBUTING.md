# Contributing

Verum is in early development — Phase 0 (setup) is done, Phase 1 (a working PDF
viewer) has not started. The most useful contributions right now are Phase 1
tasks from [ROADMAP.md](ROADMAP.md).

Questions and half-formed ideas belong in
[Discussions](https://github.com/LordOfTheMachines/verum/discussions); issues are
for concrete bugs and scoped work. Participation is governed by our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Development setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/LordOfTheMachines/verum.git
cd verum
uv sync
```

## The quality gate

All four must pass locally before you open a PR; CI runs the same set on Linux
and Windows across Python 3.12 and 3.13.

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov
```

CI syncs with `uv sync --locked`, so if you change a dependency constraint in
`pyproject.toml` you must run `uv lock` and commit the updated `uv.lock` in the
same change.

## Ground rules

- **Layering:** `ui → core → backends`, downward only. `core` and `backends`
  must not import `verum.ui` or `PyQt6`. See [ARCHITECTURE.md](ARCHITECTURE.md).
- **Typing:** mypy runs in strict mode over `src` and `tests`. No bare `Any`
  without a comment explaining why.
- **Tests:** new behaviour needs a test. Prefer headless tests in
  `tests/unit/`; reach for `pytest-qt` only when the behaviour is genuinely a
  widget's.
- **Line endings:** enforced by `.gitattributes` (LF everywhere except `.bat`
  and `.ps1`). Do not fight it with editor settings.

## Commit messages

Conventional commits — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`,
`test:`, `perf:`, `ci:`. Imperative mood, no trailing period.

```
feat(backends): add PyMuPDF page rendering at arbitrary scale
```

## Pull requests

Branch off `main`, one logical change per PR, fill in the template. If your
change makes an architectural decision, add an ADR under [docs/adr/](docs/adr/)
in the same PR. If it closes a roadmap item, add a line to
[PROGRESS.md](PROGRESS.md).

## Licence

By contributing you agree that your work is licensed under GPL-3.0-or-later.
Note that PyMuPDF is AGPL — dependencies incompatible with a copyleft licence
cannot be added.
