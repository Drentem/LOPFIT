from pynput.keyboard import Controller, Listener, Key, HotKey
from pynput.mouse import Listener as M_Listener
from flask import _app_ctx_stack
from time import sleep

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

# May need to replace the listener with this to give a proper
# with keyboard.Events() as events:
#     # Block at most one second
#     event = events.get(1.0)
#     if event is None:
#         print('You did not press a key within one second')
#     else:
#         print('Received event {}'.format(event))


class KB(object):
    def __init__(self, app=None, Phrases=None):
        self.app = app
        self.inGUI = False
        self.phrases = Phrases
        self.kb = Controller()
        self.code = []
        self.CP = Clipboard()
        self.listener = Listener(on_press=self.__Listener_Check)
        self.m_listener = M_Listener(on_click=self.__on_click)
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
        if not self.inGUI:
            with self.app.app_context():
                phrase = self.phrases.check_cmd(''.join(self.code))
                print(phrase)
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

    def __on_click(self, x, y, button, pressed):
        if pressed:
            self.__reset()

    def __reset(self):
        self.code.clear()

    def __start(self):
        while not self.m_listener.running and not self.listener.running:
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
            # self.listener.join()
            # except Exception:
            #     sleep(0.1)

    def __stop(self):
        self.listener.stop()
        self.listener = Listener(on_press=self.__Listener_Check)

    def guiStatus(self, status=False):
        self.inGUI = status
        print(self.inGUI)


if __name__ == '__main__':
    try:
        kb = KB()
    except KeyboardInterrupt:
        exit()
