# from pynput.keyboard import Controller, Key, HotKey, Events as KB_Events
import keyboard
from keyboard import KeyboardEvent
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
    paste_keys = "cmd+v"
elif platform in ['Windows', 'win32', 'cygwin']:  # Windows
    from LOPFIT.OS_Specific._Windows import Clipboard  # , Window  (Macros)
    paste_keys = "ctrl+v"

terminate_keys = ['enter', 'space', 'tab']
backspace = [KeyboardEvent(event_type='down', name='backspace', scan_code=14),
             KeyboardEvent(event_type='up', name='backspace', scan_code=14)]


class KB(object):
    def __init__(self, app=None, Phrases=None):
        self.app = app
        self.inGUI = False
        self.phrases = Phrases
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
            clearing = []
            for i in range(len(self.code)+1):
                clearing.extend(backspace)
            keyboard.play(clearing)
            self.CP.borrow(
                html=phrase['html'],
                text=phrase['text'])
            self.kb.press(paste_keys[0])
            self.kb.tap(paste_keys[1])
            self.kb.release(paste_keys[0])
            sleep(0.1)
            self.CP.giveBack()
        keyboard.unhook_all()
        self.__reset()

    def __Keyboard_Thread(self):
        while True:
            if self.exit:
                break
            # self.code = list(filter(None, self.code))
            if not self.inGUI and not self.paused:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name in terminate_keys:
                        self.__execute()
                    elif event.name == 'backspace':
                        if len(self.code) > 0:
                            self.code.pop()
                    else:
                        self.code.append(event.name)
            else:
                self.__reset()

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