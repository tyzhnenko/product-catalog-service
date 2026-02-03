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


class AccessLogFormatter(logging.Formatter):
    """Custom JSON formatter for uvicorn access logs."""

    def format(self, record: logging.LogRecord) -> str:
        # Extract uvicorn-specific attributes
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
        }

        # Uvicorn access logs have special attributes
        if hasattr(record, "client_addr"):
            log_data["client_addr"] = record.client_addr
        if hasattr(record, "request_line"):
            log_data["request_line"] = record.request_line
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code

        # Add the formatted message
        log_data["message"] = record.getMessage()

        return json.dumps(log_data)


def config_logger(settings: Settings):
    """Configure logging for the application and uvicorn.

    Args:
        settings: Application settings containing log format configuration.

    """
    # Configure application logger
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

    # Configure uvicorn access logger
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    access_stream = logging.StreamHandler()

    if settings.app.log_format == "json":
        access_formatter = AccessLogFormatter()
    else:
        # Use uvicorn's default access log format
        access_fmt = '%(client_addr)s - "%(request_line)s" %(status_code)s'
        access_formatter = logging.Formatter(access_fmt)

    access_stream.setFormatter(access_formatter)
    access_logger.addHandler(access_stream)
    access_logger.setLevel(logging.INFO)
    access_logger.propagate = False

    # Configure uvicorn error logger
    error_logger = logging.getLogger("uvicorn.error")
    error_logger.handlers.clear()
    error_stream = logging.StreamHandler()

    if settings.app.log_format == "json":
        error_formatter = JSONFormatter()
    else:
        error_fmt = "%(asctime)s - %(levelname)s %(name)s -- %(message)s"
        error_formatter = logging.Formatter(error_fmt)

    error_stream.setFormatter(error_formatter)
    error_logger.addHandler(error_stream)
    error_logger.setLevel(logging.INFO)
    error_logger.propagate = False
