# Architecture

> Status: **design intent**. Phase 1 has not been implemented yet, so most of
> the modules below do not exist on disk. This document is the contract new
> code is expected to follow — see [ROADMAP.md](ROADMAP.md) for what is built
> when, and [PROGRESS.md](PROGRESS.md) for what exists today.

## Guiding principles

1. **Viewer first, editor never-by-default.** Opening a document must never
   mutate it. Write paths are explicit, separate, and opt-in (Phase 3).
2. **The UI is a thin shell.** Anything that can be tested without a running
   Qt event loop lives outside `verum.ui`.
3. **One backend per format, one protocol for all of them.** Adding TIFF
   support must not require touching the viewport, and vice versa.
4. **Render lazily, cache deliberately.** A 2000-page PDF must open as fast as
   a 2-page one. Only visible pages are rasterised.
5. **No global state.** Dependencies are passed in; this is what keeps the core
   testable.

## Layers

```
┌─────────────────────────────────────────────────┐
│ verum.ui           PyQt6 windows, widgets,      │  imports: core, Qt
│                    actions, shortcuts           │
├─────────────────────────────────────────────────┤
│ verum.core         document model, render       │  imports: backends
│                    pipeline, page cache,        │  never: Qt, ui
│                    session/app services         │
├─────────────────────────────────────────────────┤
│ verum.backends     PDF / image / text readers   │  imports: 3rd-party libs
│                    behind one protocol          │  never: core, ui, Qt
└─────────────────────────────────────────────────┘
```

The dependency arrow points **down only**. `core` and `backends` must not
import `verum.ui` or `PyQt6` — this is checked in review (see the PR
checklist) and is the single rule that keeps the eventual Rust port (Phase 7+)
and headless testing possible.

### `verum.backends`

Each module adapts one format to a common protocol, roughly:

```python
class DocumentBackend(Protocol):
    @classmethod
    def can_open(cls, path: Path) -> bool: ...
    def page_count(self) -> int: ...
    def page_size(self, index: int) -> Size: ...          # points, pre-zoom
    def render(self, index: int, scale: float) -> Bitmap: ...
    def close(self) -> None: ...
```

Planned modules:

| Module | Format | Library | Phase |
| --- | --- | --- | --- |
| `pdf.py` | PDF, XPS, EPUB | PyMuPDF | 1 |
| `pdf_writer.py` | PDF mutation (merge/split/rotate) | pikepdf | 3 |
| `image.py` | PNG, JPEG, TIFF, WebP | Pillow / Qt | 4 |
| `text.py` | TXT, Markdown | stdlib + markdown-it | 5 |
| `office.py` | DOCX | python-docx | 5 |
| `ocr.py` | text layer extraction | PaddleOCR | 6 |

**Why two PDF libraries:** PyMuPDF (AGPL) is a fast rasteriser and text
extractor; pikepdf (MPL, libqpdf) does lossless structural edits without
re-encoding page content. Using PyMuPDF for writes would risk degrading the
source document. Note PyMuPDF's AGPL licence is compatible with Verum's
GPL-3.0-or-later, and is a reason the project cannot relicense to permissive
terms.

### `verum.core`

| Module | Responsibility | Phase |
| --- | --- | --- |
| `document.py` | Backend-agnostic open/close, format sniffing, backend registry | 1 |
| `renderer.py` | Page → bitmap at a given zoom; the only place scale maths lives | 1 |
| `cache.py` | Bounded LRU of rendered pages, keyed by `(page, scale)` | 1 |
| `session.py` | Open document, current page, zoom mode, recent files | 1 |
| `search.py` | Text search across pages, hit model | 2 |
| `bookmarks.py` | Outline/TOC model and user bookmarks | 2 |
| `errors.py` | Verum exception hierarchy | 1 |

### `verum.ui`

| Module | Responsibility | Phase |
| --- | --- | --- |
| `app.py` (`verum/app.py`) | `main()` entry point, `QApplication` bootstrap, CLI args | 1 |
| `main_window.py` | Menu bar, toolbar, status bar, actions | 1 |
| `viewport.py` | Scrollable page area, continuous scroll, zoom gestures | 1 |
| `page_item.py` | One rendered page + its placeholder while rendering | 1 |
| `sidebar.py` | Thumbnails, outline, bookmarks | 2 |
| `dialogs/` | Open, page manipulation, preferences | 1+ |

## Rendering pipeline

```
scroll/zoom event
      └─> viewport computes the visible page range
            └─> core.session asks core.renderer for (page, scale)
                  └─> core.cache hit?  ──yes──> return bitmap
                          │no
                          └─> backend.render() on a worker thread
                                └─> bitmap into cache, signal the viewport
```

Rasterisation never runs on the Qt main thread. The viewport draws a
grey placeholder at the correct aspect ratio until the bitmap arrives, so
scrolling never blocks.

**Cache policy:** LRU bounded by total pixel budget rather than page count (a
page at 400 % zoom costs far more than the same page at 100 %). Entries for a
scale that is no longer current are evicted first.

## Threading

* Qt main thread: all widget access, all painting.
* Render pool: `QThreadPool` of N-1 workers; each job is one `(page, scale)`.
* Jobs are cancellable — scrolling past a page abandons its pending render.
* Backends are **not** assumed thread-safe; each worker gets its own handle, or
  access is serialised per document. This is decided per backend and documented
  in its module docstring.

## Error handling

`verum.core.errors` defines the hierarchy:

```
VerumError
├── DocumentError
│   ├── UnsupportedFormatError   # no backend claims the file
│   ├── CorruptDocumentError     # backend opened it, then failed
│   └── PasswordRequiredError    # encrypted PDF
└── RenderError
```

A failed render degrades to an error placeholder on that page; it never takes
down the window. Backend exceptions are wrapped at the `core` boundary so the
UI never sees a `fitz.FileDataError`.

## Testing strategy

| Layer | How it is tested | Needs Qt? |
| --- | --- | --- |
| `backends` | Real fixture files in `tests/fixtures/`, byte-level assertions | no |
| `core` | Fake backend implementing the protocol; cache/eviction unit tests | no |
| `ui` | `pytest-qt` with `QT_QPA_PLATFORM=offscreen` | yes |

Integration tests in `tests/integration/` open a real PDF through the full
stack. The bulk of the suite must stay in the two headless layers.

## Decisions

Architecture decisions are recorded in [docs/adr/](docs/adr/). Start with
[ADR-0001](docs/adr/0001-record-architecture-decisions.md).
