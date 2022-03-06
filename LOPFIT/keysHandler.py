# This module is shared code between OSs
import keyboard
from keyboard import KeyboardEvent
from pynput.mouse import Events as M_Events
from flask import _app_ctx_stack
from time import sleep
import threading
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
        # Flask related variables
        self.app = app
        self.phrases = Phrases

        # OS related variables
        self.CP = Clipboard()

        # Keyboard and mouse event monitoring
        self.mouse_thread = threading.Thread(target=self.__Mouse_Thread)
        self.mouse_thread.daemon = True
        self.keyboard_thread = threading.Thread(target=self.__Keyboard_Thread)
        self.keyboard_thread.daemon = True

        # Data gathering variable
        self.phrase_cmd = []
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
        with self.app.app_context():
            phrase = self.phrases.check_cmd(''.join(self.phrase_cmd))
        if phrase:
            clearing = []
            for i in range(len(self.phrase_cmd)+1):
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

    def __Keyboard_Thread(self):
        t = threading.current_thread()
        while getattr(t, "exit", False):
            # self.phrase_cmd = list(filter(None, self.phrase_cmd))
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                print(getattr(t, "exit", False))
                if event.name in terminate_keys:
                    self.__execute()
                elif event.name == 'backspace':
                    if len(self.phrase_cmd) > 0:
                        self.phrase_cmd.pop()
                else:
                    self.phrase_cmd.append(event.name)
                print(self.phrase_cmd)

    def __Mouse_Thread(self):
        t = threading.current_thread()
        with M_Events() as events:
            for event in events:
                while getattr(t, "exit", False):
                    if isinstance(event, M_Events.Click):
                        self.__reset()

    def __reset(self):
        keyboard.unhook_all()
        self.phrase_cmd.clear()

    def __start(self):
        self.mouse_thread.start()
        self.keyboard_thread.start()

    def guiStatus(self, inGUI=False):
        if inGUI:
            keyboard.unhook_all()
            self.mouse_thread.exit = True
            self.keyboard_thread.exit = True
            self.__reset()
        else:
            try:
                self.mouse_thread.start()
            except Exception:
                print("Mouse thread still running")
            try:
                self.keyboard_thread.start()
            except Exception:
                print("Keyboard thread still running")


if __name__ == '__main__':
    try:
        kb = KB()
    except KeyboardInterrupt:
        exit()
