from structlog import get_logger, stdlib

from .custom_logging import set_up_custom_logging

logger: stdlib.BoundLogger = get_logger()


def main() -> None:  # noqa: D103
    set_up_custom_logging()
    logger.info("Starting scanner")


if __name__ == "__main__":
    main()
