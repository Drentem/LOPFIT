# This module is shared code between OSs
from LOPFIT.misc.logs import loggers
import keyboard
from keyboard import KeyboardEvent, send
from pynput.mouse import Listener
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
    backspace = "delete"
elif platform in ['Windows', 'win32', 'cygwin']:  # Windows
    from LOPFIT.OS_Specific._Windows import Clipboard  # , Window  (Macros)
    paste_keys = "ctrl+v"
    backspace = "backspace"

terminate_keys = ['enter', 'space', 'tab']

log = loggers['inputHandler']


class Inputs(object):
    # Required for integrating with Flask and the database
    def __init__(self, app=None, Phrases=None):
        # Flask related variables
        self.app = app
        self.phrases = Phrases

        # OS related variables
        log.debug('Registering clipboard handler...')
        self.CP = Clipboard()
        log.debug('Clipboard handler registered.')

        # Keyboard and mouse event monitoring
        log.debug('Registering mouse thread...')
        self.mouse_thread = threading.Thread(target=self.__Mouse_Thread)
        self.mouse_thread.daemon = True
        log.debug('Mouse thread registered.')
        log.debug('Registering keyboard thread...')
        self.keyboard_thread = threading.Thread(target=self.__Keyboard_Thread)
        self.keyboard_thread.daemon = True
        log.debug('Keyboard thread registered.')

        # Data gathering variable
        self.phrase_cmd = []
        if app is not None:
            self.init_app(app, Phrases)
        self.__start()

    def init_app(self, app, Phrases):
        self.phrases = Phrases
        log.info('Registered Phrase database access')

    # Code
    def __execute(self):
        command = ''.join(self.phrase_cmd)
        with self.app.app_context():
            try:
                log.debug(
                    f'Checking if command exists: {command}')
                phrase = self.phrases.check_cmd(command)
            except Exception as e:  # noqa: F841
                log.exception(
                    'Failed to check if command exists. Error details:')
        if phrase:
            log.debug('Command exists')
            try:
                length = len(command) + 1
                log.debug(
                    'Attempting to clear the command from where it was'
                    f' entered. Total characters: {length}')
                clearing = []
                for i in range(length):
                    send(backspace)
                keyboard.play(clearing)
                log.debug(
                    'Successfully cleared the command from where it was'
                    ' entered.')
            except Exception as e:  # noqa: F841
                log.exception(
                    'Failed to clear the command from where it was entered.'
                    ' Error details:')
            try:
                log.debug(
                    'Attempting to borrow the clipboard...')
                self.CP.borrow(
                    html=phrase['html'],
                    text=phrase['text'])
            except Exception as e:  # noqa: F841
                log.exception(
                    'Failed to borrow the clipboard. Error details:')
            try:
                log.debug(
                    'Attempting to paste the phrase from the clipboard'
                    f' using {paste_keys}...')
                send(paste_keys)
                sleep(0.1)
            except Exception as e:  # noqa: F841
                log.exception(
                    'Failed to paste the phrase from the clipboard.'
                    ' Error details:')
            try:
                log.debug(
                    'Attempting to give the clipboard back...')
                self.CP.giveBack()
            except Exception as e:  # noqa: F841
                log.exception(
                    'Failed to give the clipboard back. Error details:')
            self.__reset("Command executed")
            return True
        else:
            self.__reset("Command doesn't exist")
            return True

    def __Keyboard_Thread(self):
        log.info('Keyboard thread started.')
        try:
            log.info('Getting current thread information...')
            t = threading.current_thread()
        except Exception as e:  # noqa: F841
            log.exception(
                'Failed to retrieve current thread information')
        while not getattr(t, "pause", False):
            event = keyboard.read_event()
            log.debug('Checking if the event is "Key Down":\n'
                      f'     Event Info: {event}')
            if event.event_type == keyboard.KEY_DOWN:
                log.debug('Event is "Key Down".')
                log.debug('Checking if event is'
                          ' a terminating key...')
                if event.name in terminate_keys:
                    log.debug('Event is terminating key.')
                    try:
                        log.info(
                            'Attempting to execute the command...')
                        if self.__execute():
                            log.info(
                                'Command executed.')
                        else:
                            log.info(
                                'Not a command')
                    except Exception as e:  # noqa: F841
                        log.exception(
                            'Failed to attepmt execution. Error details:')
                elif event.name == backspace:
                    log.debug(
                        'Attempting to remove a character from the command...')
                    try:
                        if len(self.phrase_cmd) > 0:
                            self.phrase_cmd.pop()
                            log.debug(
                                'Successfully removed a character'
                                ' from the command...')
                        else:
                            log.debug(
                                'No character to remove from the command...')
                    except Exception as e:  # noqa: F841
                        log.exception(
                            'Failed to remove a character from the command.'
                            ' Error details:')
                elif len(event.name) == 1:
                    if keyboard.is_pressed('caps lock') or \
                            keyboard.is_pressed('shift') or \
                            keyboard.is_pressed('right shift'):
                        self.phrase_cmd.append(event.name.upper())
                    else:
                        self.phrase_cmd.append(event.name)
                elif not (event.name == 'caps lock' or
                          event.name == 'shift' or
                          event.name == 'right shift'):
                    self.__reset('Invalid key entered.'
                                 ' Clearing in case the cursor moved.')
                log.debug('Currently stored command:'
                          f' {"".join(self.phrase_cmd)}')

    def __Mouse_Thread(self):
        t = threading.current_thread()

        def on_click(x, y, button, pressed):
            if not getattr(t, "pause", False) and pressed:
                log.debug('Mouse clicked.')
                log.debug(
                    'Attempting to reset stored command...')
                self.__reset('Mouse click')
                log.debug(
                    'Successfully reset stored command.')

        with Listener(on_click=on_click) as listener:
            log.info('Mouse thread started.')
            listener.join()

    def __reset(self, reason):
        self.phrase_cmd.clear()
        log.debug('Reset the stored command:\n'
                  f'     Reason for reset: {reason}')

    def __start(self):
        try:
            log.info('Initilizing mouse thread...')
            self.mouse_thread.start()
            log.info('Mouse thread initialized.')
        except Exception as e:  # noqa: F841
            log.exception(
                'Failed to initilize mouse thread. Error details:')
        try:
            log.info('Initilizing keyboard thread...')
            self.keyboard_thread.start()
            log.info('Keyboard thread initialized.')
        except Exception as e:  # noqa: F841
            log.exception(
                'Failed to initilize keyboard thread. Error details:')

    def guiStatus(self, inGUI=False):
        if inGUI:
            self.mouse_thread.pause = True
            log.info('Pausing mouse thread while in the GUI')
            self.keyboard_thread.pause = True
            log.info(
                'Pausing keyboard thread while in the GUI')
            self.__reset('GUI Access')
        else:
            try:
                log.info(
                    'Resuming mouse thread after the GUI lost focus...')
                self.mouse_thread.pause = False
                log.info(
                    'Mouse thread restarted.')
            except Exception as e:  # noqa: F841
                log.critical(
                    'Failed to resume the mouse thread. Error details:',
                    exc_inc=True)
            try:
                log.info(
                    'Resuming keyboard thread after the GUI lost focus...')
                self.keyboard_thread.pause = False
                log.info(
                    'Keyboard thread resumed.')
            except Exception as e:  # noqa: F841
                log.critical(
                    'Failed to resume the keyboard thread. Error details:',
                    exc_inc=True)
