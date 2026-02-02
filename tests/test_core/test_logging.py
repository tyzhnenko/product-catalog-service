"""Tests for logging configuration."""

import json
import logging

import pytest

from src.core.logging import JSONFormatter, config_logger
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
