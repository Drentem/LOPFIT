# import win32gui
import klembord


class Clipboard:
    def __init__(self):
        self.temp_clipboard = {}
        klembord.init()

    def __storeUserClipboard(self):
        self.temp_clipboard = klembord.get()

    def __restoreUserClipboard(self):
        klembord.get(self.temp_clipboard)
        self.temp_clipboard = None
        self.temp_clipboard = {}

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
