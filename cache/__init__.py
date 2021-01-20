import os
import settings
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('main_logger')
logger.setLevel(settings.LOG_LEVEL)
formatter = logging.Formatter(
    fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d-%y %H:%M:%S'
)

fh = TimedRotatingFileHandler('./logs/main_logger.log', when='D', interval=1)
fh.setFormatter(formatter)
logger.addHandler(fh)
LOGGER_HANDLER = logger
