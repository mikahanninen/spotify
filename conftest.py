"""Root pytest configuration.

This file adds the --skip-integration option for skipping integration tests in CI.
"""

import pytest


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--skip-integration",
        action="store_true",
        default=False,
        help="Skip integration tests (tests marked with @pytest.mark.integration)"
    )


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (requires real Spotify)"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if config.getoption("--skip-integration"):
        skip_integration = pytest.mark.skip(reason="--skip-integration flag set")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
