from pynput.keyboard import Controller, Listener, Key, HotKey
from pynput.mouse import Listener as M_Listener
from time import sleep

# from LOPFIT.ext import db
from sys import platform
if platform == "linux" or platform == "linux2":  # Linux
    this = "nothing yet"
    # from LOPFIT.OS_Specific import db
elif platform in ['Mac', 'darwin', 'os2', 'os2emx']:  # MacOS
    # from LOPFIT.OS_Specific._MacOS import Clipboard, Window
    from OS_Specific._MacOS import Clipboard  # , Window  Need Window later
    terminate_keys = [
        '\x03',  # MacOS Numpad return
    ]
    paste_keys = [Key.cmd, 'v']
elif platform in ['Windows', 'win32', 'cygwin']:  # Windows
    import win32gui
    hwnd = win32gui.GetForegroundWindow()
    omniboxHwnd = win32gui.FindWindowEx(hwnd, 0, 'Chrome_OmniboxView', None)
    terminate_keys = []
    paste_keys = HotKey.parse('<ctrl>+v')

terminate_keys.extend([Key.space, Key.tab, Key.enter])


class KB(object):
    def __init__(self, app=None):
        self.app = app
        self.kb = Controller()
        self.code = []
        self.CP = Clipboard()
        self.listener = Listener(on_press=self.__Listener_Check)
        self.m_listener = M_Listener(on_click=self.__on_click)
        if app is not None:
            self.init_app(app)
        self.__start()

    def init_app(self, app):
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)

    def __execute(self):
        if ''.join(self.code) == "test":
            for i in range(0, len(self.code)+1):
                self.kb.tap(Key.backspace)
            self.CP.borrow(html="<strong>Bold</strong>", text="Bold")
            self.kb.press(paste_keys[0])
            self.kb.tap(paste_keys[1])
            self.kb.release(paste_keys[0])
            sleep(0.1)
            self.CP.giveBack()
        self.__reset()

    def __Listener_Check(self, key):
        self.code = list(filter(None, self.code))
        if hasattr(key, 'char'):
            if key.char in terminate_keys:
                self.__execute()
            else:
                self.code.append(key.char)
        else:
            if key in terminate_keys:
                self.__execute()
            elif key == Key.backspace:
                if len(self.code) > 0:
                    self.code.pop()
        print(self.code)

    def __on_click(self, x, y, button, pressed):
        if pressed:
            self.__reset()

    def __reset(self):
        self.code.clear()
        print('reset')

    def __start(self):
        while True:
            # try:
            if not self.m_listener.running:
                try:
                    self.m_listener.start()
                except Exception:
                    print("Keyboard bad start")
            if not self.listener.running:
                try:
                    self.listener.start()
                except Exception:
                    print("Keyboard bad start")
            self.listener.join()
            # except Exception:
            #     sleep(0.1)

    def __stop(self):
        self.listener.stop()
        self.listener = Listener(on_press=self.__Listener_Check)


if __name__ == '__main__':
    try:
        kb = KB()
    except KeyboardInterrupt:
        exit()
