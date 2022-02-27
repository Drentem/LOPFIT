try:
    from flask import Flask, render_template, requst
except Exception:
    import subprocess
    import sys

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'flask'])
    from flask import Flask, render_template
finally:
    from LOPFIT.daKeyboards import KB
    from LOPFIT.DB import Phrases, Folders, db

    dbfile = 'sqlite:///LOPFIT.db'
    # dbfile = 'sqlite:////' + str(os.path.join(
    #     os.path.expanduser("~/Documents"), "LOPFIT.db"))

    def create_app():
        app = Flask(__name__)
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = dbfile
        db.init_app(app)
        with app.app_context():
            db.create_all()

        @app.route('/')
        def index():
            phrase_folders = Folders.get_folders_select()
            phrase_list = Phrases.get_phrase_list_html()
            return render_template('index.html.j2',
                                   folders=phrase_folders,
                                   phrase_list=phrase_list)

        @ app.route('/phrases')
        def phrases():
            phrase_list = Phrases.get_phrase_list()
            return render_template('phrases.html.j2',
                                   phrases=phrase_list)

        @ app.route('/phrase/', methods=["POST"])
        def phrase_new():
            data = {
                "cmd": ""
            }
            Phrases.add(data)
            return render_template('phrase.html.j2')

        @ app.route('/phrase/<ID>')
        def phrase_edit(ID):
            return render_template('phrases.html.j2')

        return app
