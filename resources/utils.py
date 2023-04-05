import logging
import time


def setup_logging(debug: bool = False) -> None:
    """
    Sets up logging with ISO8601 timestamps and UTC times.
    Args:
        debug: Whether to do verbose logging at the DEBUG level
    """
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        level=logging.DEBUG if debug else logging.INFO,
    )
    logging.debug("Logger object configured. Debug mode enabled.")
