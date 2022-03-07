# This module is shared code between OSs
from LOPFIT.misc.logs import loggers
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
        loggers['keyboard'].debug('Registered clipboard handler')

        # Keyboard and mouse event monitoring
        self.mouse_thread.daemon = True
        self.mouse_thread = threading.Thread(target=self.__Mouse_Thread)
        loggers['mouse'].debug('Registered mouse thread')
        self.keyboard_thread = threading.Thread(target=self.__Keyboard_Thread)
        self.keyboard_thread.daemon = True
        loggers['keyboard'].debug('Registered keyboard thread')

        # Data gathering variable
        self.phrase_cmd = []
        if app is not None:
            self.init_app(app, Phrases)
        self.__start()

    def init_app(self, app, Phrases):
        self.phrases = Phrases
        loggers['keyboard'].debug('Registered Phrase database access')
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()

    # Code
    def __execute(self):
        command = ''.join(self.phrase_cmd)
        with self.app.app_context():
            try:
                loggers['keyboard'].debug(
                    f'Checking if command exists: {command}')
                phrase = self.phrases.check_cmd(command)
            except Exception:
                loggers['keyboard'].exception(
                    'Failed to check if command exists. Error details:')
        if phrase:
            loggers['keyboard'].debug('Command exists')
            loggers['keyboard'].debug(
                f'Command phrase retrieved:\n{phrase.name}')
            try:
                length = len(command) + 1
                loggers['keyboard'].debug(
                    'Attempting to clear the command from where it was'
                    f' entered. Total characters: {length}')
                clearing = []
                for i in range(length):
                    clearing.extend(backspace)
                keyboard.play(clearing)
                loggers['keyboard'].debug(
                    'Successfully cleared the command from where it was'
                    ' entered.')
            except Exception:
                loggers['keyboard'].exception(
                    'Failed to clear the command from where it was entered.'
                    ' Error details:')
            try:
                loggers['keyboard'].debug(
                    'Attempting to borrow the clipboard...')
                self.CP.borrow(
                    html=phrase['html'],
                    text=phrase['text'])
            except Exception:
                loggers['keyboard'].exception(
                    'Failed to borrow the clipboard. Error details:')
            try:
                loggers['keyboard'].debug(
                    'Attempting to paste the phrase from the clipboard'
                    f' using {paste_keys}...')
                self.kb.send(paste_keys)
                sleep(0.1)
            except Exception:
                loggers['keyboard'].exception(
                    'Failed to paste the phrase from the clipboard.'
                    ' Error details:')
            try:
                loggers['keyboard'].debug(
                    'Attempting to give the clipboard back...')
                self.CP.giveBack()
            except Exception:
                loggers['keyboard'].exception(
                    'Failed to give the clipboard back. Error details:')
            self.__reset()
            return True
        else:
            self.__reset()
            return True

    def __Keyboard_Thread(self):
        try:
            loggers['keyboard'].info('Getting current thread information...')
            t = threading.current_thread()
            current_status = getattr(t, "exit", False)
            loggers['keyboard'].debug(f'Thread exit status: {current_status}')
        except Exception:
            loggers['keyboard'].exception(
                'Failed to retrieve current thread information')
        while getattr(t, "exit", False):
            # self.phrase_cmd = list(filter(None, self.phrase_cmd))
            current_status = getattr(t, "exit", False)
            loggers['keyboard'].debug(f'Thread exit status: {current_status}')
            event = keyboard.read_event()
            loggers['keyboard'].debug('Checking if the event is "Key Down":\n'
                                      f'     Event Info: {event}')
            if event.event_type == keyboard.KEY_DOWN:
                loggers['keyboard'].debug('Event is "Key Down".')
                loggers['keyboard'].debug('Checking if event is'
                                          ' a terminating key...')
                if event.name in terminate_keys:
                    loggers['keyboard'].debug('Event is terminating key.')
                    try:
                        loggers['keyboard'].info(
                            'Attempting to execute the command...')
                        if self.__execute():
                            loggers['keyboard'].info(
                                'Command executed.')
                        else:
                            loggers['keyboard'].info(
                                'Not a command')
                    except Exception:
                        loggers['keyboard'].exception(
                            'Failed to attepmt execution. Error details:')
                elif event.name == 'backspace':
                    loggers['keyboard'].debug(
                        'Attempting to remove a character from the command...')
                    try:
                        if len(self.phrase_cmd) > 0:
                            self.phrase_cmd.pop()
                            loggers['keyboard'].debug(
                                'Successfully removed a character'
                                ' from the command...')
                        else:
                            loggers['keyboard'].debug(
                                'No character to remove from the command...')
                    except Exception:
                        loggers['keyboard'].exception(
                            'Failed to remove a character from the command.'
                            ' Error details:')
                else:
                    self.phrase_cmd.append(event.name)
                loggers['keyboard'].debug('Currently stored command:'
                                          f' {"".join(self.phrase_cmd)}')
            loggers['keyboard'].debug('Sleeping for next cycle.')
            sleep(0.1)

    def __Mouse_Thread(self):
        try:
            loggers['mouse'].info('Getting current thread information...')
            t = threading.current_thread()
            current_status = getattr(t, "exit", False)
            loggers['mouse'].debug(f'Thread exit status: {current_status}')
        except Exception:
            loggers['mouse'].exception(
                'Failed to retrieve current thread information')
        with M_Events() as events:
            for event in events:
                while getattr(t, "exit", False):
                    current_status = getattr(t, "exit", False)
                    loggers['keyboard'].debug(
                        f'Thread exit status: {current_status}')
                    if isinstance(event, M_Events.Click):
                        loggers['mouse'].debug('Mouse clicked.')
                        loggers['mouse'].debug(
                            'Attempting to reset stored command...')
                        self.__reset('Mouse click')
                        loggers['mouse'].debug(
                            'Successfully reset stored command.')
                loggers['mouse'].debug('Sleeping for next cycle.')
                sleep(0.1)

    def __reset(self, reason):
        keyboard.unhook_all()
        self.phrase_cmd.clear()
        loggers['keyboard'].debug('Reset the stored command:\n'
                                  f'     Reason for reset: {reason}')

    def __start(self):
        try:
            loggers['mouse'].info('Initilizing mouse thread...')
            self.mouse_thread.start()
            loggers['mouse'].info('Mouse thread initialized.')
        except Exception:
            loggers['mouse'].exception(
                'Failed to initilize mouse thread. Error details:')
        try:
            loggers['keyboard'].info('Initilizing keyboard thread...')
            self.mouse_thread.start()
            loggers['keyboard'].info('Mouse thread initialized.')
        except Exception:
            loggers['keyboard'].exception(
                'Failed to initilize keyboard thread. Error details:')
        print("Not loading yet")

    def guiStatus(self, inGUI=False):
        if inGUI:
            keyboard.unhook_all()
            self.mouse_thread.exit = True
            loggers['mouse'].info('Stopping mouse thread while in the GUI')
            self.keyboard_thread.exit = True
            loggers['keyboard'].info(
                'Stopping keyboard thread while in the GUI')
            self.__reset('GUI Access')
        else:
            try:
                loggers['mouse'].info(
                    'Restarting mouse thread after the GUI lost focus...')
                self.mouse_thread.start()
                loggers['mouse'].info(
                    'Mouse thread restarted.')
            except Exception:
                loggers['mouse'].critical(
                    'Failed to restart the mouse thread. Error details:')
            try:
                loggers['keyboard'].info(
                    'Restarting keyboard thread after the GUI lost focus...')
                self.keyboard_thread.start()
                loggers['keyboard'].info(
                    'Keyboard thread restarted.')
            except Exception:
                loggers['keyboard'].critical(
                    'Failed to restart the keyboard thread. Error details:')
