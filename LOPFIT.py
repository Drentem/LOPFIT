import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "LOPFIT", "includes"))
from LOPFIT import create_app  # noqa: E402


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5050, debug=True)
