"""Smoke test: the package and every pipeline module import."""

import importlib

import pytest

MODULES = [
    "config",
    "geocode",
    "scope",
    "extract_acs",
    "extract_shapes",
    "cache",
    "transform",
    "validate",
    "join_geo",
    "pipeline",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name: str) -> None:
    """Each module under census_radius_explorer imports cleanly."""
    importlib.import_module(f"census_radius_explorer.{name}")
