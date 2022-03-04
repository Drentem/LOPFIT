from pynput.keyboard import Controller, Key, HotKey, Events as KB_Events
from pynput.mouse import Events as M_Events
from flask import _app_ctx_stack
from time import sleep
from threading import Thread

from sys import platform
if platform == "linux" or platform == "linux2":  # Linux
    this = "nothing yet"
    # from LOPFIT.OS_Specific import db
elif platform in ['Mac', 'darwin', 'os2', 'os2emx']:  # MacOS
    from LOPFIT.OS_Specific._MacOS import Clipboard  # , Window  (Macros)
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
    def __init__(self, app=None, Phrases=None):
        self.app = app
        self.inGUI = False
        self.phrases = Phrases
        self.kb = Controller()
        self.code = []
        self.CP = Clipboard()
        self.paused = False
        self.exit = False
        self.mouse_thread = Thread(target=self.__Mouse_Thread)
        self.keyboard_thread = Thread(target=self.__Keyboard_Thread)
        if app is not None:
            self.init_app(app, Phrases)
        self.__start()

    def init_app(self, app, phrases):
        self.phrases = phrases
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()

    def __execute(self):
        with self.app.app_context():
            phrase = self.phrases.check_cmd(''.join(self.code))
        if phrase:
            for i in range(0, len(self.code)+1):
                self.kb.tap(Key.backspace)
            self.CP.borrow(
                html=phrase['html'],
                text=phrase['text'])
            self.kb.press(paste_keys[0])
            self.kb.tap(paste_keys[1])
            self.kb.release(paste_keys[0])
            sleep(0.1)
            self.CP.giveBack()
        self.__reset()

    def __Keyboard_Thread(self):
        with KB_Events() as events:
            for event in events:
                if not self.inGUI and not self.paused:
                    self.code = list(filter(None, self.code))
                    if isinstance(event, KB_Events.Press):
                        if hasattr(event.key, 'char'):
                            if event.key.char in terminate_keys:
                                self.__execute()
                            else:
                                self.code.append(event.key.char)
                        else:
                            if event.key in terminate_keys:
                                self.__execute()
                            elif event.key == Key.backspace:
                                if len(self.code) > 0:
                                    self.code.pop()
                else:
                    self.__reset()
                if self.exit:
                    break

    def __Mouse_Thread(self):
        with M_Events() as events:
            for event in events:
                if not self.inGUI and not self.paused:
                    if isinstance(event, M_Events.Click):
                        self.__reset()

    def __reset(self):
        self.code.clear()

    def __start(self):
        self.mouse_thread.start()
        self.keyboard_thread.start()

    def guiStatus(self, status=False):
        self.inGUI = status


if __name__ == '__main__':
    try:
        kb = KB()
    except KeyboardInterrupt:
        exit()
