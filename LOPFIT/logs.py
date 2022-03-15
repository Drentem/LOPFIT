import logging
import os
from sys import platform

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.exception('This is an error message with exception details')
# logging.critical('This is a critical message')

if platform in ['Mac', 'darwin', 'os2', 'os2emx']:  # MacOS
    log_root = os.path.join(
        os.path.expanduser('~/Documents/'),
        'LOPFIT_DATA')
elif platform in ['Windows', 'win32', 'cygwin']:  # Windows
    log_root = os.path.join(
        os.path.expanduser('~/AppData/local'),
        'LOPFIT_DATA')
else:
    print("This OS is not supported.")
    exit()

os.makedirs(log_root, exist_ok=True)

logs = {
    "inputHandler": {
        "path": os.path.join(log_root, "inputHandler.log"),
        "level": logging.WARNING
    },
    "gui":  {
        "path": os.path.join(log_root, "gui.log"),
        "level": logging.WARNING
    },
    "backend":  {
        "path": os.path.join(log_root, "backend.log"),
        "level": logging.WARNING
    },
    "database":  {
        "path": os.path.join(log_root, "database.log"),
        "level": logging.WARNING
    }
}
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s',
                              datefmt='%d-%b-%y %H:%M:%S')
loggers = {}

for log in logs.keys():
    handler = logging.FileHandler(logs[log]['path'])
    handler.setFormatter(formatter)
    loggers[log] = logging.getLogger(log)
    loggers[log].setLevel(logs[log]['level'])
    loggers[log].addHandler(handler)
    loggers[log].info('========== NEW INSTANCE STARTED ==========')
