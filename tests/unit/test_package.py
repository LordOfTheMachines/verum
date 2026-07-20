"""Smoke tests for the package itself.

These keep the quality gate honest while Phase 1 is still empty: they fail if
the package stops importing or the version metadata drifts.
"""

import re

import verum

_PEP440_RELEASE = re.compile(r"^\d+\.\d+\.\d+")


def test_version_is_exposed() -> None:
    assert isinstance(verum.__version__, str)
    assert _PEP440_RELEASE.match(verum.__version__), verum.__version__


def test_layers_import_cleanly() -> None:
    import verum.backends
    import verum.core
    import verum.ui

    for layer in (verum.backends, verum.core, verum.ui):
        assert layer.__doc__, f"{layer.__name__} is missing its module docstring"
