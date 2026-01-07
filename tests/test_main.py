import importlib.util

import pytest


def test_create_app_has_root_route() -> None:
    if importlib.util.find_spec("fastapi") is None:
        pytest.skip("fastapi not installed")

    from app.main import create_app

    app = create_app()
    paths = {route.path for route in app.routes}

    assert "/" in paths
