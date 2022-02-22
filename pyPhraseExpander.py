from pynput.keyboard import Controller
from pynput import keyboard
from DB import Phrases

kb = Controller()
suffix = keyboard.Key.space
end = keyboard.Key.esc


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
