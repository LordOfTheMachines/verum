# Roadmap

Phases ship in order. A phase is done when its exit criteria hold **and** CI is
green on `main`. See [PROGRESS.md](PROGRESS.md) for current state.

---

## Phase 0 — Project setup ✅

Repository scaffolding, tooling, licence, CI, documentation.

**Exit criteria:** met (2026-07-20).

---

## Phase 1 — PDF viewing (MVP) 🎯 next

The first phase that produces a runnable application.

### Tasks

| # | Task | Notes |
| --- | --- | --- |
| 1.1 | Declare runtime dependencies: `PyQt6`, `PyMuPDF`; re-add `pytest-qt` to the dev group | it was removed in Phase 0 because a Qt-less install aborts collection |
| 1.2 | `core/errors.py` — exception hierarchy | see ARCHITECTURE.md |
| 1.3 | `backends/pdf.py` — PyMuPDF adapter: open, page count, page size, render at scale | no UI imports |
| 1.4 | `core/document.py` — format sniffing + backend registry | magic bytes, not extension alone |
| 1.5 | `core/renderer.py` + `core/cache.py` — scale maths and bounded LRU | pixel-budget eviction |
| 1.6 | `core/session.py` — open document, current page, zoom mode | |
| 1.7 | `ui/app.py` + `main()`; restore `[project.scripts] verum = "verum.app:main"` | removed in Phase 0 as it pointed at a non-existent module |
| 1.8 | `ui/main_window.py` — menu, toolbar, status bar, Open/Recent | |
| 1.9 | `ui/viewport.py` + `ui/page_item.py` — continuous scroll, placeholders | |
| 1.10 | Background render pool with cancellation | never rasterise on the GUI thread |
| 1.11 | Zoom: fit-width, fit-page, 25 %–800 %, Ctrl+scroll | |
| 1.12 | Navigation: next/prev page, go-to-page, Home/End, PgUp/PgDn | |
| 1.13 | Encrypted-PDF password prompt | `PasswordRequiredError` |
| 1.14 | Test fixtures: small/large/encrypted/corrupt PDFs in `tests/fixtures/` | keep them tiny, generate where possible |
| 1.15 | Headless UI tests via `QT_QPA_PLATFORM=offscreen`; enable them in CI | CI already exports the variable |
| 1.16 | Handle `verum <file.pdf>` CLI argument | |

### Exit criteria

- `uv run verum sample.pdf` opens a window and renders page 1.
- A 500-page PDF opens in under 1 s and scrolls without a visible stall.
- Zoom and page navigation work by keyboard and mouse.
- Corrupt, encrypted and non-PDF inputs produce a clear message, never a crash.
- `core` and `backends` remain importable without Qt installed.

---

## Phase 2 — Reading experience

Full-text search with hit highlighting and next/prev; text selection and
copy-to-clipboard; document outline (TOC) sidebar; page thumbnails; user
bookmarks; recent-files list; session restore (last page and zoom per file);
rotate view; continuous vs. single-page modes; dark/light theme.

**Exit criteria:** search across a 500-page document returns the first hit in
under 500 ms; reopening a file restores the previous position.

---

## Phase 3 — PDF editing

Merge, split, extract, reorder, rotate and delete pages via pikepdf; a
page-manipulation dialog with drag-to-reorder thumbnails; undo/redo; save and
save-as with an explicit dirty-state indicator.

**Exit criteria:** the source file is never modified in place without an
explicit save; a round-trip of open → reorder → save preserves bookmarks,
metadata and embedded fonts.

---

## Phase 4 — Image formats

PNG, JPEG, TIFF (incl. multi-page), WebP, BMP, GIF via an `image` backend;
EXIF-aware orientation; multi-page TIFF navigated with the same page model as
PDF; basic view transforms (rotate, flip).

**Exit criteria:** images open through the identical viewport code path as PDF;
no format-specific branches leak into `ui`.

---

## Phase 5 — Document formats

Plain text with encoding detection; Markdown with a rendered view; DOCX via
`python-docx` (read-only, layout approximated, explicitly not WYSIWYG).

**Exit criteria:** the format limitations are documented in-app, so DOCX
fidelity is never mistaken for a bug.

---

## Phase 6 — OCR

PaddleOCR integration as an **optional** extra (`verum[ocr]`); OCR a scanned
page into a searchable text layer; language selection; batch OCR with progress
and cancellation; write the text layer back into the PDF via pikepdf.

**Exit criteria:** Verum installs and runs fully without the OCR extra; OCR runs
off the GUI thread and is cancellable.

---

## Phase 7+ — Hardening and packaging

Windows installer and portable build (PyInstaller/Briefcase); Linux AppImage
and/or Flatpak; file-association handling; crash reporting; performance budget
tests in CI; accessibility pass (keyboard-only navigation, screen readers);
i18n scaffolding with Turkish and English; evaluation of a Rust core port for
the render pipeline.

---

## Explicit non-goals

- A full editing suite. Verum edits document *structure*, not page *content*.
- Form filling and digital signatures (revisit only after Phase 7).
- A web or mobile client.
- Cloud sync or accounts.
