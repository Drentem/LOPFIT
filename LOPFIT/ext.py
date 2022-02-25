try:
    from flask_sqlalchemy import SQLAlchemy
except Exception:
    import subprocess
    import sys

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'flask-sqlalchemy'])
    from flask_sqlalchemy import SQLAlchemy
finally:
    db = SQLAlchemy()
