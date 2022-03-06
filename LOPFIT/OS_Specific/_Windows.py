import win32gui
from win32clipboard import (
    OpenClipboard as Open, EmptyClipboard as Empty,
    GetClipboardData as Get, SetClipboardData as Set,
    CloseClipboard as Close, EnumClipboardFormats as Enum)


class Clipboard:
    def __init__(self):
        self.temp_clipboard = []

    def __storeUserClipboard(self):
        Open()
        cb = {}
        format = 0
        try:
            while True:
                format = Enum(format)
                if format == 0:
                    break
                else:
                    try:
                        RawData = Get(format)
                    except Exception:
                        continue
                    else:
                        cb[format] = RawData
        finally:
            Empty()
            Close()
        self.temp_clipboard.append(cb)

    def __restoreUserClipboard(self):
        Empty()
        if self.temp_clipboard != []:
            Open()
            try:
                Empty()
                cb = self.temp_clipboard.pop()
                for format in cb:
                    Set(format, cb[format])
            finally:
                Close()
        self.temp_clipboard.clear()

    def borrow(self, html="", text=""):
        self.__storeUserClipboard()
        # TODO: Add Macro Handling
        Set()

    def giveBack(self):
        self.__restoreUserClipboard()


class Window:
    hwnd = win32gui.GetForegroundWindow()
    omniboxHwnd = win32gui.FindWindowEx(hwnd, 0, 'Chrome_OmniboxView', None)
    # def check_secure():
    #     input = check_output(commands['secure_input']).decode()
    #     secure_input_enabled = re.search('kCGSSessionSecureInputPID', input)
    #     if secure_input_enabled:
    #         return True
    #     else:
    #         return False
    #
    # def get():
    #     # TODO: This will be used for getting the window to var. (Macros)
    #     test = NSWorkspace
    #     print(test)
    #
    # def set():
    #     # TODO: This will be used for setting the window from var. (Macros)
    #     test = NSWorkspace
    #     print(test)
