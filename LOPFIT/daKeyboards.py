from pynput.keyboard import Controller
from pynput import keyboard
from flask import current_app
from LOPFIT.ext import db
from sys import platform
if platform == "linux" or platform == "linux2":  # Linux
    print("Linux")
elif platform == "darwin":  # MacOS
    from richxerox import copy, paste
elif platform == "win32":  # Windows
    print("Windows")

kb = Controller()


class KB(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)

    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == end:
            # Stop listener
            return False

    def start():
        code = []
        with keyboard.Events() as events:
            for event in events:
                if not isinstance(event, keyboard.Events.Press):
                    if isinstance(event.key, keyboard.Key):
                        if event.key == end:
                            exit()
                        if event.key == keyboard.Key.backspace:
                            if len(code) > 0:
                                code.pop()
                        elif event.key == suffix:
                            if len(code) > 0:
                                code = ''.join(code)
                                if ''.join(code) in Phrases.get_cmds():
                                    print(Phrases.get_phrase[code])
                            code = []
                    else:
                        code.append(event.key.char)
