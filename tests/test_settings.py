import os
from src.config.settings import Settings, load_settings


class TestSettings:
    def test_defaults(self):
        s = Settings()
        assert s.app_name == "multi-agent-repo"
        assert s.version == "0.1.0"
        assert s.debug is False
        assert s.log_level == "INFO"

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("APP_NAME", "test-app")
        monkeypatch.setenv("APP_VERSION", "2.0.0")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        s = Settings.from_env()
        assert s.app_name == "test-app"
        assert s.version == "2.0.0"
        assert s.debug is True
        assert s.log_level == "DEBUG"

    def test_debug_false_values(self, monkeypatch):
        monkeypatch.setenv("DEBUG", "no")
        s = Settings.from_env()
        assert s.debug is False

    def test_load_settings_returns_settings(self):
        s = load_settings()
        assert isinstance(s, Settings)
