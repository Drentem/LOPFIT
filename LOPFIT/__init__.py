# try:
#     from flask import Flask, render_template, request, jsonify
# except Exception:
#     import subprocess
#     import sys
#
#     subprocess.check_call(
#         [sys.executable, "-m", "pip", "install", 'flask'])
#     from flask import Flask, render_template, request, jsonify
#     from richxerox import paste
# finally:
from flask import Flask, render_template, request, jsonify
from LOPFIT.daKeyboards import KB
from LOPFIT.DB import Phrases, Folders, Settings, db

dbfile = 'sqlite:///LOPFIT.db'


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = dbfile
    db.init_app(app)
    with app.app_context():
        db.create_all()
        Settings.init()

    @app.route('/')
    def index():
        return render_template('index.html.j2')

    @app.route('/folder/', methods=["GET", "POST", "DELETE"])
    def folder():
        data = request.get_json()
        if request.method == 'POST':
            if "folder_id" in data:
                folder = Folders.query_id(data['folder_id'])
                if "name" in data:
                    folder.name = data['name']
                if "parent_folder_id" in data:
                    folder.parent_folder_id = data['parent_folder_id']
                folder.commit()
            else:
                folder = Folders(
                    name=data['name'],
                    parent_folder_id=data['parent_folder_id']
                )
                Folders.add(folder)
                ret = {"folder_added": True}
        elif request.method == "DELETE":
            Folders.remove(data['id'])
            ret = {"folder_removed": True}
        elif request.method == 'GET':
            ret = {"folders_HTML": Folders.get_folders_select_html()}
        return jsonify(ret)

    @app.route('/phrase/', methods=["GET", "POST"])
    def phrase():
        data = request.get_json()
        if request.method == 'POST':
            while Phrases.check_cmd(data['cmd']):
                data['cmd'] += "0"
            phrase = Phrases(
                name=data['name'],
                cmd=data['cmd'],
                folder_id=data['folder_id']
            )
            db.session.add(phrase)
            db.session.commit()
            ret = {
                "phrase_added": True,
                "cmd": data['cmd']}
        elif request.method == 'GET':
            phrases = Phrases.get_phrase_list_html()
            ret = {"phraseList_HTML": phrases}
        return jsonify(ret)

    @app.route('/phrase/<ID>', methods=["GET", "POST", "DELETE"])
    def existing_phrase(ID):
        data = request.get_json()
        if request.method == 'POST':
            phrase = Phrases.query_id(ID)
            if 'cmd' in data:
                phrase.cmd = data['cmd']
            if 'name' in data:
                phrase.name = data['name']
            if 'folder_id' in data:
                phrase.folder_id = data['folder_id']
            if 'phrase_text' in data:
                phrase.phrase_text = data['phrase_text'].encode()
                phrase.phrase_html = data['phrase_html'].encode()
            phrase.commit()
            ret = {"phrase_updated": True}
        elif request.method == "DELETE":
            Phrases.remove(ID)
            db.session.commit()
            ret = {"folder_removed": True}
        elif request.method == 'GET':
            phrase = Phrases.query_id(ID)
            ret = {
                "cmd": phrase.cmd,
                "name": phrase.name,
                "phrase_html": phrase.phrase_html.decode()
                if phrase.phrase_html else "",
                "folder_id": phrase.folder_id
            }
        return jsonify(ret)

    @app.route('/config/<SETTING>', methods=["GET", "POST"])
    def config(SETTING):
        if request.method == 'POST':
            data = request.get_json()
            Settings.update(SETTING, data['value'])
            value = Settings.query_setting(SETTING)
            ret = {"setting_updated": True}
        elif request.method == 'GET':
            value = Settings.query_setting(SETTING)
            ret = {"value": value}
        return jsonify(ret)

    return app
