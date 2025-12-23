from app.main import create_app


def test_create_app_has_root_route() -> None:
    app = create_app()
    paths = {route.path for route in app.routes}

    assert "/" in paths
