from flask import Flask, render_template, request, jsonify
from LOPFIT.DB import Phrases, Folders, Settings, db
from LOPFIT.keysHandler import KB

dbfile = 'sqlite:///LOPFIT.db'


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = dbfile
    db.init_app(app)
    kb = KB(app, Phrases)
    with app.app_context():
        db.create_all()
        Settings.init()

    @app.route('/')
    def index():
        return render_template('index.html.j2')

    @app.route('/folder/', methods=["GET", "POST"])
    def folders():
        data = request.get_json()
        if request.method == 'POST':
            folder = Folders(
                name=data['name'],
                parent_folder_id=data['parent_folder_id']
            )
            Folders.add(folder)
            ret = {"folder_added": True}
        elif request.method == 'GET':
            folder_html = Folders.get_folders_select_html()
            ret = {"folders_HTML": folder_html}
        return jsonify(ret)

    @app.route('/folder/<ID>', methods=["GET", "POST", "DELETE"])
    def folder(ID):
        data = request.get_json()
        if request.method == 'POST':
            folder = Folders.query_id(ID)
            if "name" in data:
                folder.name = data['name']
            if "parent_folder_id" in data:
                folder.parent_folder_id = data['parent_folder_id']
            folder.commit()
            ret = {"folder_updated": True}
        elif request.method == "DELETE":
            Folders.remove(ID)
            ret = {"folder_removed": True}
        elif request.method == 'GET':
            folder_html = Folders.get_folders_select_html(ID)
            ret = {"folders_HTML": folder_html}
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
            Phrases.add(phrase)
            ret = {
                "phrase_added": True,
                "cmd": data['cmd'],
                "phrase_id": phrase.phrase_id}
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
                phrase.phrase_html = ("<meta charset='utf-8'>"
                                      + data['phrase_html']).encode()
            phrase.commit()
            ret = {"phrase_updated": True}
        elif request.method == "DELETE":
            Phrases.remove(ID)
            Phrases.commit()
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

    @app.route('/focus/', methods=["POST"])
    def focus():
        data = request.get_json()
        kb.guiStatus(data['focus'])
        return {"focus": data['focus']}

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        data = request.get_json()
        if data['are_you_sure']:
            shutdown_server()
            return 'Server shutting down...'
        else:
            return False

    return app
