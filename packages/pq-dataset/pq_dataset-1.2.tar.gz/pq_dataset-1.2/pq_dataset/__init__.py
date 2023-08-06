import logging
import os
from pathlib import Path
from datetime import datetime
   
logger = logging.getLogger()

if (logger.hasHandlers()):
    logger.handlers.clear()

logger.setLevel(logging.DEBUG)

# our first handler is a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler_format = '%(asctime)s | %(name)s |  %(levelname)s: %(message)s'
console_handler.setFormatter(logging.Formatter(console_handler_format))
logger.addHandler(console_handler)

# the second handler is a file handler
output = os.path.expanduser('~')
log_path = f'{output}{os.path.sep}pqd_logging'

if not Path(log_path).exists():
    os.makedirs(log_path)

logfile_name = f'{log_path}{os.path.sep}{datetime.today().strftime("%Y-%m-%d")}_{__name__}.log'
file_handler = logging.FileHandler(logfile_name)
file_handler.setLevel(logging.DEBUG)
file_handler_format = '%(asctime)s | %(levelname)s | %(name)s | %(lineno)d: %(message)s'
file_handler.setFormatter(logging.Formatter(file_handler_format))
logger.addHandler(file_handler)

logger.info(f'Logging started - writing to: {log_path}')
