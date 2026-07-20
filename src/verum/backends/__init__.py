"""Format-specific document backends.

Each backend adapts one file format (PDF, image, plain text, ...) to the
document protocol defined in :mod:`verum.core`. Backends must never import
from :mod:`verum.ui`.
"""
