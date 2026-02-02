"""Module for configuring logging."""

import json
import logging
from datetime import datetime

from src.settings import Settings

logging.getLogger("pymongo").setLevel(logging.INFO)

logger = logging.getLogger("product_catalog_service")


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def config_logger(settings: Settings):
    stream = logging.StreamHandler()

    if settings.app.log_format == "json":
        formatter = JSONFormatter()
    else:
        fmt_string = "%(asctime)s - %(levelname)s %(filename)s:%(lineno)d -- %(message)s"
        formatter = logging.Formatter(fmt_string)

    stream.setFormatter(formatter)
    logger.addHandler(stream)

    if settings.app.debug:
        logger.setLevel(logging.DEBUG)
        logger.info("Logging level set to DEBUG")
    else:
        logger.setLevel(logging.INFO)
        logger.info("Logging level set to INFO")
