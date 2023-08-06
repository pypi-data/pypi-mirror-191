import logging


def setup_logging(requested_level: int) -> None:
    logging.basicConfig(
        level=requested_level,
        format="%(asctime)s,%(msecs)d %(levelname)s <%(threadName)s> [%(filename)s:%(lineno)d] %(message)s",
    )


def setup_logging_adv(requested_level: int) -> None:
    logging.basicConfig(
        level=requested_level,
        format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
    )
