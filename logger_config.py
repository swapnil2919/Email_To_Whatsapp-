import logging
import logging.config
import os
from pathlib import Path


def setup_logging() -> None:
    """Configure console + rotating file logging."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "standard",
                },
                "file_app": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "level": log_level,
                    "formatter": "standard",
                    "filename": str(logs_dir / "app.log"),
                    "when": "midnight",
                    "backupCount": 14,
                    "encoding": "utf-8",
                },
                "file_error": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "ERROR",
                    "formatter": "standard",
                    "filename": str(logs_dir / "error.log"),
                    "maxBytes": 1048576,
                    "backupCount": 10,
                    "encoding": "utf-8",
                },
            },
            "root": {
                "level": log_level,
                "handlers": ["console", "file_app", "file_error"],
            },
        }
    )
