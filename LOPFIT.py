import sys
import os
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_path, "LOPFIT", "includes"))
from LOPFIT import create_app  # noqa: E402
from LOPFIT.misc.systemTray import create_icon  # noqa: E402


app = create_app()
icon = create_icon(root_path)

if __name__ == "__main__":
    icon.run_detached()
    app.run(host="localhost", port=5050, debug=False)
