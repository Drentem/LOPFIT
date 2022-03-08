import sys
import os
import threading
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_path, "LOPFIT", "includes"))
from werkzeug.serving import make_server  # noqa: E402
from LOPFIT import create_app  # noqa: E402
from LOPFIT.misc.systemTray import create_icon  # noqa: E402
from LOPFIT.misc.logs import loggers  # noqa: E402


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('localhost', 5050, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        loggers['backend'].debug('Starting server thread...')
        self.server.serve_forever()

    def shutdown(self):
        loggers['backend'].debug('Exiting server thread...')
        self.server.shutdown()


def start_server(server):
    server.start()
    loggers['backend'].debug('Server thread started')


def stop_server(server):
    server.shutdown()
    loggers['backend'].debug('Server thread exited')


if __name__ == "__main__":
    loggers['backend'].info("Initializing app...")
    app = create_app()
    server = ServerThread(app)
    start_server(server)
    loggers['backend'].debug("Adding icon to system tray...")
    icon = create_icon(root_path, stop_server)
    loggers['backend'].debug("Adding icon to system tray COMPLETE")
    loggers['backend'].info("Initializing app COMPLETE")
    icon.run()
    stop_server(server)
