import sys
import os
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_path, "LOPFIT", "includes"))
from gevent.pywsgi import WSGIServer  # noqa: E402
from LOPFIT import create_app  # noqa: E402
from LOPFIT.misc.systemTray import create_icon  # noqa: E402
from LOPFIT.misc.logs import loggers  # noqa: E402


if __name__ == "__main__":
    loggers['backend'].info("Initializing app...")
    app = create_app()
    # app.run(host="localhost", port=5050, debug=True)  # For debuging
    http_server = WSGIServer(('localhost', 5050), app)
    loggers['backend'].debug("Adding icon to system tray...")
    icon = create_icon(root_path, http_server.stop)
    icon.run_detached()
    loggers['backend'].debug("Adding icon to system tray COMPLETE")
    loggers['backend'].info("Initializing app COMPLETE")
    http_server.serve_forever()
