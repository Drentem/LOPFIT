from flask import Flask, render_template
from flask_talisman import Talisman
from LOPFIT.daKeyboards import KB
from LOPFIT.DB import Phrases, db

dbfile = 'sqlite:///LOPFIT.db'
# dbfile = 'sqlite:////' + str(os.path.join(
#     os.path.expanduser("~/Documents"), "LOPFIT.db"))


def create_app():
    app = Flask(__name__)
    tal = Talisman(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = dbfile
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html.j2')

    @app.route('/phrases')
    @tal(
        frame_options='ALLOW-FROM',
        frame_options_allow_from='http://localhost:5050/',
    )
    def phrases():
        phrase_list = Phrases.get_phrase_list()
        return render_template('phrases.html.j2',
                               phrases=phrase_list)

    @app.route('/phrase')
    @tal(
        frame_options='ALLOW-FROM',
        frame_options_allow_from='http://localhost:5050/',
    )
    def phrase_new():
        return render_template('phrases.html.j2')

    @app.route('/phrase/<ID>')
    @tal(
        frame_options='ALLOW-FROM',
        frame_options_allow_from='http://localhost:5050/',
    )
    def phrase_edit(ID):
        return render_template('phrases.html.j2')

    return app
