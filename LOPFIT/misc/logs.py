import logging
import os

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.exception('This is an error message with exception details')
# logging.critical('This is a critical message')

root_path = os.path.dirname(os.path.abspath(__file__))
log_root = os.path.join(root_path, "..", "logs")
logs = {
    "keyboard": {
        "path": os.path.join(log_root, "keyboard.log"),
        "level": logging.DEBUG
    },
    "mouse":  {
        "path": os.path.join(log_root, "mouse.log"),
        "level": logging.DEBUG
    },
    "gui":  {
        "path": os.path.join(log_root, "gui.log"),
        "level": logging.DEBUG
    },
    "backend":  {
        "path": os.path.join(log_root, "backend.log"),
        "level": logging.DEBUG
    },
    "systemtray":  {
        "path": os.path.join(log_root, "systemtray.log"),
        "level": logging.DEBUG
    },
    "database":  {
        "path": os.path.join(log_root, "database.log"),
        "level": logging.DEBUG
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
