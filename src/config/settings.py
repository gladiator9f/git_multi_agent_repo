import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    app_name: str = "multi-agent-repo"
    version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.environ.get("APP_NAME", cls.app_name),
            version=os.environ.get("APP_VERSION", cls.version),
            debug=os.environ.get("DEBUG", "").lower() in ("1", "true", "yes"),
            log_level=os.environ.get("LOG_LEVEL", cls.log_level).upper(),
        )


def load_settings() -> Settings:
    return Settings.from_env()
