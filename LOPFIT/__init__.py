try:
    from flask import Flask, render_template, request, jsonify
except Exception:
    import subprocess
    import sys

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'flask'])
    from flask import Flask, render_template, request, jsonify
finally:
    # from LOPFIT.daKeyboards import KB
    from LOPFIT.DB import Phrases, Folders, Phrase_Folders, db

    dbfile = 'sqlite:///LOPFIT.db'

    def create_app():
        app = Flask(__name__)
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = dbfile
        db.init_app(app)
        with app.app_context():
            db.create_all()

        @app.route('/')
        def index():
            phrase_folders = Folders.get_folders_select_html()
            phrase_list = Phrases.get_phrase_list_html()
            return render_template('index.html.j2',
                                   folders=phrase_folders,
                                   phrase_list=phrase_list)

        @ app.route('/folder/', methods=["GET", "POST", "DELETE"])
        def folder():
            data = request.get_json()
            if request.method == 'POST':
                folder = Folders(
                    name=data['name'],
                    parent_folder_id=data['parent_folder_id']
                )
                Folders.add(folder)
                ret = {"folder_added": True}
            elif request.method == "DELETE":
                folder = Folders.query_id(data['id'])
                remove_phrases = data['remove']
                Folders.remove(folder, remove_phrases)
            elif request.method == 'GET':
                ret = {"folders": Folders.get_folders_select_html()}
            return jsonify(ret)

        @ app.route('/phrase/', methods=["GET", "POST", "DELETE"])
        def phrase():
            data = request.get_json()
            if request.method == 'POST':
                if id in data:
                    phrase = Phrases.query_id(data['id'])
                    phrase.cmd = data['cmd']
                    phrase.name = data['name']
                    phrase.phrase = data['phrase']
                    phrase.commit()
                    Phrase_Folders.update_id(data['id'], data['folder_id'])
                else:
                    phrase = Phrases(
                        name=data['name'],
                        parent_folder_id=data['parent_folder_id']
                    )
                    Phrases.add(phrase)
                ret = {"folder_added": True}
            elif request.method == "DELETE":
                phrase = Phrases.query_id(data['id'])
                # remove_phrases = data['remove']
                # Phrases.remove(folder, remove_phrases)
            elif request.method == 'GET':
                phrases = Phrases.get_phrase_list_html()
                ret = {"phrase_list": phrases}
            return jsonify(ret)

        @ app.route('/phrase/<ID>', methods=["GET", "POST", "DELETE"])
        def phrase_edit(ID):
            return render_template('phrases.html.j2')

        return app
