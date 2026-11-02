import json
import logging
import logging.config
from pathlib import Path

_LOGGING_CONFIGURED = False


def setup_logging() -> None:
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    config_path = Path(__file__).resolve().parents[2] / "logging_config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            "Cannot find logging_config.json. Ensure the file exists at the repository root."
        )

    with config_path.open("rt", encoding="utf-8") as file:
        config = json.load(file)

    logging.config.dictConfig(config)

    # Avoid duplicate SQL statement logs by relying on configured root handlers only.
    sqlalchemy_parent_logger = logging.getLogger("sqlalchemy.engine")
    # Set SQL logging to WARNING or ERROR in production.
    sqlalchemy_parent_logger.setLevel(logging.INFO)
    sqlalchemy_parent_logger.handlers.clear()
    sqlalchemy_parent_logger.propagate = True

    sqlalchemy_engine_logger = logging.getLogger("sqlalchemy.engine.Engine")
    sqlalchemy_engine_logger.handlers.clear()
    sqlalchemy_engine_logger.propagate = True

    _LOGGING_CONFIGURED = True
