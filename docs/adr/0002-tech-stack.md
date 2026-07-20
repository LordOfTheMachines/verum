# ADR-0002: Python + PyQt6 + PyMuPDF + pikepdf

- **Status:** accepted
- **Date:** 2026-07-20 (recorded retroactively; the choice was made 2026-05-16)

## Context

Verum needs to render PDF pages fast, run on Windows and Linux desktops, and
eventually manipulate PDF structure without degrading the source file. The
maintainer works primarily in Python.

## Decision

**Language: Python 3.12+.** Fast enough given that rasterisation happens in C
inside the PDF library, and by far the maintainer's most productive stack.
3.12 is the floor for the modern typing syntax used throughout.

**GUI: PyQt6.** Mature, native-feeling on both target platforms, has the
scroll-area and graphics-view primitives a viewport needs, and `pytest-qt`
makes widgets testable headlessly. GPL-3.0 licensing for Verum is what makes
PyQt6's GPL terms unproblematic. Alternatives: Tkinter (too primitive for a
viewport), GTK via PyGObject (weaker Windows story), a web stack in Electron
(rejected — contradicts "lightweight").

**PDF rendering and text: PyMuPDF.** The fastest Python rasteriser available,
with text extraction and search in the same package. Its AGPL licence is
compatible with GPL-3.0-or-later.

**PDF manipulation: pikepdf.** Wraps libqpdf for lossless structural edits —
merge, split, reorder, rotate — without re-encoding page content streams.
PyMuPDF can also write, but round-tripping through it risks degrading the
source; a viewer must not do that.

**Package manager: uv.** Fast, lockfile-based, handles Python-version pinning
and dependency groups in one tool.

## Consequences

- **Verum cannot be relicensed permissively.** PyMuPDF (AGPL) and PyQt6 (GPL)
  bind the project to copyleft. Any proposed dependency must be compatible.
- Two PDF libraries means two sets of PDF semantics to keep straight; the
  read/write split is drawn at the backend boundary
  (`backends/pdf.py` vs `backends/pdf_writer.py`) to keep it legible.
- PyQt6 and PyMuPDF ship large binary wheels — packaging (Phase 7) will need
  attention to installer size.
- CI must run Qt headless (`QT_QPA_PLATFORM=offscreen`).
- A future Rust port (Phase 7+) would target the core and rendering pipeline,
  which is why `core` and `backends` are forbidden from importing Qt.
