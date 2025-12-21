"""Module for configuring logging."""

import logging

from src.settings import Settings

logging.getLogger("pymongo").setLevel(logging.INFO)

logger = logging.getLogger("product_catalog_service")


def config_logger(settings: Settings):
    stream = logging.StreamHandler()
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
