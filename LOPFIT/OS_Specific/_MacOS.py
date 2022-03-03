from AppKit import NSWorkspace
from richxerox import copy as cp, paste as ps, available
from subprocess import check_output
import re

commands = {
    'rtf': ['/usr/bin/textutil', '-convert', 'rtf', '-stdin', '-stdout'],
    'secure_input': ['ioreg', '-alw', '0']
}


class Clipboard:

    def __init__(self):
        self.temp_clipboard = {}
        self.types = 0

    def __storeUserClipboard(self):
        for i in available():
            self.temp_clipboard[i] = ps(format=i)
            if i == 'text':
                self.types += 1
            elif i == 'html':
                self.types += 2
            elif i == 'rtf':
                self.types += 4

    def __restoreUserClipboard(self):
        if self.types == 1:
            cp(text=self.temp_clipboard['text'])
        elif self.types == 2:
            cp(text=self.temp_clipboard['html'])
        elif self.types == 3:
            cp(
                text=self.temp_clipboard['text'],
                html=self.temp_clipboard['html']
            )
        elif self.types == 4:
            cp(text=self.temp_clipboard['rtf'])
        elif self.types == 5:
            cp(
                text=self.temp_clipboard['text'],
                rtf=self.temp_clipboard['rtf']
            )
        elif self.types == 6:
            cp(
                html=self.temp_clipboard['html'],
                rtf=self.temp_clipboard['rtf']
            )
        elif self.types == 7:
            cp(
                text=self.temp_clipboard['text'],
                rtf=self.temp_clipboard['rtf'],
                html=self.temp_clipboard['html']
            )
        self.types = 0
        self.temp_clipboard = None
        self.temp_clipboard = {}

    def borrow(self, html="", text=""):
        self.__storeUserClipboard()
        # TODO: Add Macro Handling
        rtf = check_output(
            commands['rtf'],
            input=html, text=True)
        cp(text=text, rtf=rtf, html=html)

    def giveBack(self):
        self.__restoreUserClipboard()


class Window:
    def check():
        input = check_output(commands['secure_input']).decode()
        secure_input_enabled = re.search('kCGSSessionSecureInputPID', input)
        if secure_input_enabled:
            return True
        else:
            return False
