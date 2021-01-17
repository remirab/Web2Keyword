import os
import settings
import logging
from logging.handlers import TimedRotatingFileHandler

web_drivers_dir_path = os.path.join(".", "cache", "drivers")

if not os.path.exists(web_drivers_dir_path):
    os.mkdir(web_drivers_dir_path)

drivers = {}
for _, _, _file in os.walk(web_drivers_dir_path):
    for f in sorted(_file):
        drivers.update({f: os.path.join(".", "cache", "drivers", f)})

logger = logging.getLogger('main_logger')
logger.setLevel(settings.LOG_LEVEL)
formatter = logging.Formatter(
    fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d-%y %H:%M:%S'
)

if not os.path.exists("./logs"):
    os.mkdir("./logs")

fh = TimedRotatingFileHandler('./logs/main_logger.log', when='D', interval=1)
fh.setFormatter(formatter)
logger.addHandler(fh)
LOGGER_HANDLER = logger
