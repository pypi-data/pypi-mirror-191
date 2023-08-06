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


class DuplicateFilter(logging.Filter):
    """
    If the message that is passed to the logger is the same as previous one, skip it
    Helps to reduce mess in terminal window
    To add the filter:  logger.addFilter(DuplicateFilter())
    """

    def filter(self, record):
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False
