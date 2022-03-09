# import win32gui
import klembord
from collections import OrderedDict


class Clipboard:
    def __init__(self):
        self.temp_clipboard = OrderedDict()
        klembord.init()

    def __storeUserClipboard(self):
        pre_content = OrderedDict()
        for i in klembord.get(['TARGETS'])['TARGETS']:
            try:
                pre_content[i] = klembord.get([i])
            except Exception:
                pass

        for i in pre_content:
            print(pre_content[i][i])
            try:
                test = {i: pre_content[i][i]}
                klembord.set(test)
                self.temp_clipboard[i] = pre_content[i][i]
            except Exception:
                pass

    def __restoreUserClipboard(self):
        self.temp_clipboard.clear()
        klembord.set(self.temp_clipboard)
        self.temp_clipboard.clear()

    def borrow(self, html="", text=""):
        self.__storeUserClipboard()
        # TODO: Add Macro Handling
        klembord.set_with_rich_text(text, html)

    def giveBack(self):
        self.__restoreUserClipboard()

# class Window:
#     hwnd = win32gui.GetForegroundWindow()
#     omniboxHwnd = win32gui.FindWindowEx(hwnd, 0, 'Chrome_OmniboxView', None)
#     def get():
#         # TODO: This will be used for getting the window to var. (Macros)
#         test = NSWorkspace
#         print(test)
#
#     def set():
#         # TODO: This will be used for setting the window from var. (Macros)
#         test = NSWorkspace
#         print(test)
