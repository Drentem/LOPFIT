# This module is shared code between OSs
import keyboard
from keyboard import KeyboardEvent
from pynput.mouse import Events as M_Events
from flask import _app_ctx_stack
from time import sleep
from threading import Thread
from sys import platform

if platform == "linux" or platform == "linux2":  # Linux
    print("This OS is not supported.")
    exit()
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
    # Required for integrating with Flask and the database
    def __init__(self, app=None, Phrases=None):
        self.app = app
        self.inGUI = False
        self.phrases = Phrases
        self.code = []
        self.CP = Clipboard()
        self.paused = False
        self.mouse_thread = Thread(target=self.__Mouse_Thread)
        self.mouse_thread.setDaemon(True)
        self.keyboard_thread = Thread(target=self.__Keyboard_Thread)
        self.keyboard_thread.setDaemon(True)
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

    # Code
    def __execute(self):
        self.paused = True
        with self.app.app_context():
            phrase = self.phrases.check_cmd(''.join(self.code))
            print(phrase)
        if phrase:
            clearing = []
            for i in range(len(self.code)+1):
                clearing.extend(backspace)
            keyboard.play(clearing)
            self.CP.borrow(
                html=phrase['html'],
                text=phrase['text'])
            self.kb.send(paste_keys)
            sleep(0.1)
            self.CP.giveBack()
        keyboard.unhook_all()
        self.__reset()
        self.paused = False

    def __Keyboard_Thread(self):
        while True:
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
