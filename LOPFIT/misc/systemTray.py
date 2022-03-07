from pystray import Icon, Menu, MenuItem
from PIL import Image
import requests
import os
import webbrowser


def create_icon(root_path, STOP):
    def __open_LOPFIT():
        webbrowser.open('http://localhost:5050', new=2)

    def __tray_Exit():
        STOP()
        icon.stop()

    image = Image.open(
        os.path.join(os.path.join(root_path, "LOPFIT", "favicon.ico")))
    menu = Menu(
        MenuItem('Open LOPFIT Window', __open_LOPFIT),
        MenuItem('Exit', __tray_Exit)
    )
    icon = Icon('LOPFIT', image, menu=menu)

    return icon
