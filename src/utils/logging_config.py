"""Logging helpers shared by project modules."""

from __future__ import annotations

import logging
import sys


DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure application logging once.

    Args:
        level: Minimum log level emitted to standard output.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.setLevel(level)
        return

    logging.basicConfig(
        level=level,
        format=DEFAULT_LOG_FORMAT,
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with the project default format.

    Args:
        name: Logger name, normally ``__name__``.

    Returns:
        Configured logger instance.
    """
    configure_logging()
    return logging.getLogger(name)
