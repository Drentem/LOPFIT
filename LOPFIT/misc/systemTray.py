from pystray import Icon, Menu, MenuItem
from PIL import Image
from LOPFIT.misc.logs import loggers
import os
import webbrowser


def create_icon(root_path, STOP):
    def __open_LOPFIT():
        loggers['backend'].debug('Loading GUI in browser...')
        webbrowser.open('http://localhost:5050', new=2)
        loggers['backend'].debug('Loaded GUI in browser.')

    def __tray_Exit():
        loggers['backend'].info('Starting Exit process...')
        STOP()
        icon.stop()
        loggers['backend'].info('Exited')

    loggers['backend'].info('Initializing system tray icon...')
    image = Image.open(
        os.path.join(os.path.join(root_path, "LOPFIT", "favicon.ico")))
    menu = Menu(
        MenuItem('Open LOPFIT Window', __open_LOPFIT),
        MenuItem('Exit', __tray_Exit)
    )
    icon = Icon('LOPFIT', image, menu=menu)

    loggers['backend'].info('System tray icon initialized.')
    return icon
