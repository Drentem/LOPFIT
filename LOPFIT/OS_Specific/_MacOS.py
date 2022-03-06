from AppKit import NSWorkspace
from richxerox import copy, pasteall
from subprocess import check_output
import re

commands = {
    'secure_input': ['ioreg', '-alw', '0']
}


class Clipboard:
    def __init__(self):
        self.temp_clipboard = {}

    def __storeUserClipboard(self):
        self.temp_clipboard = pasteall()

    def __restoreUserClipboard(self):
        copy(**self.temp_clipboard)
        self.temp_clipboard = None
        self.temp_clipboard = {}

    def borrow(self, html="", text=""):
        self.__storeUserClipboard()
        # TODO: Add Macro Handling
        copy(text=text, html=html)

    def giveBack(self):
        self.__restoreUserClipboard()


class Window:
    def check_secure():
        input = check_output(commands['secure_input']).decode()
        secure_input_enabled = re.search('kCGSSessionSecureInputPID', input)
        if secure_input_enabled:
            return True
        else:
            return False

    def get():
        # TODO: This will be used for getting the window to var. (Macros)
        test = NSWorkspace
        print(test)

    def set():
        # TODO: This will be used for setting the window from var. (Macros)
        test = NSWorkspace
        print(test)
