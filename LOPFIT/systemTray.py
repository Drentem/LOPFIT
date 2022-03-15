from LOPFIT.logs import loggers
import webbrowser
from sys import platform
import os


def create_icon(root_path, STOP):
    icon_path = os.path.join(os.path.join(root_path, "LOPFIT",
                                          'static', "favicon.ico"))
    loggers['backend'].info('Initializing system tray icon...')
    if platform == "linux" or platform == "linux2":  # Linux
        print("This OS is not supported.")
        exit()
    elif platform in ['Mac', 'darwin', 'os2', 'os2emx']:  # MacOS
        import rumps

        class IconHandler(rumps.App):
            @rumps.clicked("Open LOPFIT")
            def __open_LOPFIT(self, _):
                loggers['backend'].debug('Loading GUI in browser...')
                webbrowser.open('http://localhost:5050', new=2)
                loggers['backend'].debug('Loaded GUI in browser.')

            @rumps.clicked("Exit")
            def __tray_Exit(self, _):
                loggers['backend'].info('Starting Exit process...')
                loggers['backend'].info('Exited')
                rumps.quit_application()

        icon = IconHandler('LOPFIT',
                           icon=icon_path,
                           menu=['Open LOPFIT', 'Exit'],
                           quit_button=None)

    elif platform in ['Windows', 'win32', 'cygwin']:  # Windows
        from pystray import Icon, Menu, MenuItem
        from PIL import Image

        def __open_LOPFIT():
            loggers['backend'].debug('Loading GUI in browser...')
            webbrowser.open('http://localhost:5050', new=2)
            loggers['backend'].debug('Loaded GUI in browser.')

        def __tray_Exit():
            loggers['backend'].info('Starting Exit process...')
            icon.stop()
            loggers['backend'].info('Exited')

        image = Image.open(icon_path)
        menu = Menu(
            MenuItem('Open LOPFIT', __open_LOPFIT),
            MenuItem('Exit', __tray_Exit)
        )
        icon = Icon('LOPFIT', image, menu=menu)

    loggers['backend'].info('System tray icon initialized.')
    return icon
