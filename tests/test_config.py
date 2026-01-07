from app.config import get_settings


def test_get_settings_defaults() -> None:
    settings = get_settings()

    assert settings.app_name == "Project Alexandria"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
