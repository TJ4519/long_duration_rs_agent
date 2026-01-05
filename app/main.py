"""FastAPI application entrypoint."""

from fastapi import FastAPI

from .config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "environment": settings.environment,
            "status": "ok",
        }

    return app


app = create_app()
