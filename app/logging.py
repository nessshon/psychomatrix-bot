import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup():
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.add('logs/bot-logs.log', rotation="1 MB")
