"""Verum — a lightweight universal document viewer.

The package is organised in three layers (see ``ARCHITECTURE.md``):

* :mod:`verum.backends` — format-specific document readers, no UI imports
* :mod:`verum.core` — document model, rendering pipeline, app services
* :mod:`verum.ui` — PyQt6 widgets and windows
"""

__all__ = ["__version__"]

#: Single source of truth for the project version; ``pyproject.toml`` reads it
#: from here via ``[tool.hatch.version]``.
__version__ = "0.0.1"
