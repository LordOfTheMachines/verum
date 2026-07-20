# Verum

[![CI](https://github.com/LordOfTheMachines/verum/actions/workflows/ci.yml/badge.svg)](https://github.com/LordOfTheMachines/verum/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Licence: GPL-3.0-or-later](https://img.shields.io/badge/licence-GPL--3.0--or--later-green)](LICENSE)

A lightweight universal document viewer.

## Vision

Verum aims to be a focused, fast, and minimal viewer for any document or
image format — PDF, images (PNG, JPEG, TIFF), text, Markdown, Office formats,
and more — without the bloat of full editing suites.

## Status

🚧 **Phase 0 complete — Phase 1 not started.** The repository has its tooling,
licence, CI and architecture in place, but **no runnable application yet**: no
document can be opened. See [PROGRESS.md](PROGRESS.md) for exactly what exists
and [ROADMAP.md](ROADMAP.md) for what comes next.

## Roadmap

- **Phase 1 (MVP):** PDF viewing — open, render, navigate, zoom
- **Phase 2:** Reading experience — search, text selection, bookmarks
- **Phase 3:** PDF editing — merge, split, reorder, rotate pages
- **Phase 4:** Image formats — PNG, JPEG, TIFF, WebP
- **Phase 5:** Document formats — TXT, Markdown, DOCX
- **Phase 6:** OCR integration via PaddleOCR
- **Phase 7+:** Hardening, packaging, possible Rust port

Detailed task breakdown and exit criteria: [ROADMAP.md](ROADMAP.md).

## Tech Stack

- **Language:** Python 3.12+
- **GUI:** PyQt6
- **PDF rendering & text:** PyMuPDF
- **PDF manipulation:** pikepdf
- **Package manager:** uv

The reasoning behind these choices is recorded in
[ADR-0002](docs/adr/0002-tech-stack.md). Note that PyMuPDF and PyQt6 are the
reason Verum is copyleft.

## Building from Source

There is nothing to run yet — these steps set up the development environment.
Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/LordOfTheMachines/verum.git
cd verum
uv sync

uv run ruff check .          # lint
uv run ruff format --check . # formatting
uv run mypy                  # types (strict)
uv run pytest --cov          # tests
```

End-user build and packaging instructions arrive with the Phase 1 release.

## Documentation

| Document | Contents |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Layering, render pipeline, threading, module map |
| [ROADMAP.md](ROADMAP.md) | Phase-by-phase tasks and exit criteria |
| [PROGRESS.md](PROGRESS.md) | What is actually built, and the change log |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Dev setup, quality gate, ground rules |
| [docs/adr/](docs/adr/) | Architecture decision records |

## Contributing

Contributions are welcome — start with an open Phase 1 issue and read
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
