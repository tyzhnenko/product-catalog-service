# ruff: noqa: S101
"""Tests for logging configuration."""

import json
import logging

from src.core.logging import AccessLogFormatter, JSONFormatter, config_logger
from src.settings import App, Settings


def test_json_formatter_basic_log():
    """Test that JSONFormatter produces valid JSON output."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.module = "test_module"
    record.funcName = "test_function"

    result = formatter.format(record)

    # Should be valid JSON
    log_data = json.loads(result)

    # Should contain expected fields
    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "test_logger"
    assert log_data["message"] == "Test message"
    assert log_data["module"] == "test_module"
    assert log_data["function"] == "test_function"
    assert log_data["line"] == 42
    assert "timestamp" in log_data


def test_json_formatter_with_exception():
    """Test that JSONFormatter handles exceptions properly."""
    formatter = JSONFormatter()

    try:
        raise ValueError("Test exception")
    except ValueError:
        import sys

        exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="test.py",
            lineno=42,
            msg="Error occurred",
            args=(),
            exc_info=exc_info,
        )
        record.module = "test_module"
        record.funcName = "test_function"

        result = formatter.format(record)
        log_data = json.loads(result)

        # Should contain exception information
        assert log_data["level"] == "ERROR"
        assert log_data["message"] == "Error occurred"
        assert "exception" in log_data
        assert "ValueError: Test exception" in log_data["exception"]


def test_config_logger_text_format(caplog):
    """Test that config_logger configures text format correctly."""
    settings = Settings()
    settings.app = App(debug=True, log_format="text")

    # Clear any existing handlers
    from src.core.logging import logger

    logger.handlers.clear()

    config_logger(settings)

    # Logger should be configured
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0

    # Should use standard formatter, not JSONFormatter
    handler = logger.handlers[0]
    assert not isinstance(handler.formatter, JSONFormatter)


def test_config_logger_json_format(caplog):
    """Test that config_logger configures JSON format correctly."""
    settings = Settings()
    settings.app = App(debug=False, log_format="json")

    # Clear any existing handlers
    from src.core.logging import logger

    logger.handlers.clear()

    config_logger(settings)

    # Logger should be configured
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0

    # Should use JSONFormatter
    handler = logger.handlers[0]
    assert isinstance(handler.formatter, JSONFormatter)


def test_log_format_validation():
    """Test that log_format only accepts valid values."""
    import pytest
    from pydantic import ValidationError

    # Valid values should work
    App(log_format="text")
    App(log_format="json")

    # Invalid value should raise ValidationError
    with pytest.raises(ValidationError):
        App(log_format="invalid")


def test_access_log_formatter_basic():
    """Test that AccessLogFormatter produces valid JSON output for access logs."""
    formatter = AccessLogFormatter()
    record = logging.LogRecord(
        name="uvicorn.access",
        level=logging.INFO,
        pathname="access.py",
        lineno=10,
        msg='%s - "%s" %s',
        args=("127.0.0.1:8000", "GET /api/v1/stores/ HTTP/1.1", 200),
        exc_info=None,
    )
    record.client_addr = "127.0.0.1:8000"
    record.request_line = "GET /api/v1/stores/ HTTP/1.1"
    record.status_code = 200

    result = formatter.format(record)

    # Should be valid JSON
    log_data = json.loads(result)

    # Should contain expected fields
    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "uvicorn.access"
    assert log_data["client_addr"] == "127.0.0.1:8000"
    assert log_data["request_line"] == "GET /api/v1/stores/ HTTP/1.1"
    assert log_data["status_code"] == 200
    assert "timestamp" in log_data
    assert "message" in log_data


def test_config_logger_configures_uvicorn_loggers():
    """Test that config_logger also configures uvicorn access and error loggers."""
    settings = Settings()
    settings.app = App(debug=True, log_format="json")

    # Clear any existing handlers
    from src.core.logging import logger

    logger.handlers.clear()
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    error_logger = logging.getLogger("uvicorn.error")
    error_logger.handlers.clear()

    config_logger(settings)

    # Check uvicorn.access logger
    assert len(access_logger.handlers) > 0
    assert isinstance(access_logger.handlers[0].formatter, AccessLogFormatter)
    assert access_logger.propagate is False

    # Check uvicorn.error logger
    assert len(error_logger.handlers) > 0
    assert isinstance(error_logger.handlers[0].formatter, JSONFormatter)
    assert error_logger.propagate is False
