# try:
#
#     from sys import platform
# except Exception:
#     import subprocess
#     import sys
#
#     subprocess.check_call(
#         [sys.executable, "-m", "pip", "install", 'flask-sqlalchemy'])
#     from flask_sqlalchemy import SQLAlchemy
#     from sys import platform
# finally:
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
