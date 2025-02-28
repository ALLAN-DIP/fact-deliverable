"""A collection of various utilities."""

import logging


def return_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Returns a properly set up logger.
    Args:
        name: Name of logger.
        log_level: Verbosity level of logger.
    Returns:
        An initialized logger.
    """
    # Monkey patch module to show milliseconds
    logging.Formatter.default_msec_format = "%s.%03d"

    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        # Fall back to `WARNING`, the default level of the root logger, if `log_level` is `NOTSET`
        level=log_level or logging.WARNING,
    )
    new_logger = logging.getLogger(name)
    new_logger.setLevel(log_level)
    return new_logger