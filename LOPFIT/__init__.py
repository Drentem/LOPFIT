from flask import Flask, render_template, request, jsonify
import logging
from LOPFIT.DB import Phrases, Folders, Settings, db
from LOPFIT.inputHandler import Inputs
from LOPFIT.misc.logs import loggers


def create_app():
    loggers['backend'].info('Starting Flask...')
    app = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.disabled = True
    loggers['backend'].debug('...Configuring Database...')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///LOPFIT.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        Settings.init()
    loggers['backend'].debug('...Configuring Database COMPLETE')
    loggers['backend'].debug('...Loading Keyboard and Mouse event handlers...')
    kb = Inputs(app, Phrases, Settings)
    loggers['backend'].debug('...Loading Keyboard and Mouse event handlers'
                             ' COMPLETE')

    loggers['backend'].debug('...Loading Flask routes...')

    @app.route('/')
    def index():
        loggers['backend'].debug('Frontend Loaded')
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
            loggers['backend'].info(
                'New folder added:\n'
                f'   Folder ID: {folder.folder_id}\n'
                f'   Name: {folder.name}\n'
                f'   Parent Folder ID: {folder.parent_folder_id}')
        elif request.method == 'GET':
            folder_html = Folders.get_folders_select_html()
            ret = {"folders_HTML": folder_html}
            loggers['backend'].debug('List of folders retrieved')
        return jsonify(ret)

    @app.route('/folder/<ID>', methods=["GET", "POST", "DELETE"])
    def folder(ID):
        data = request.get_json()
        if request.method == 'POST':
            folder = Folders.query_id(ID)
            old_name = folder.name
            old_parent = folder.parent_folder_id
            if "name" in data:
                folder.name = data['name']
            if "parent_folder_id" in data:
                folder.parent_folder_id = data['parent_folder_id']
            folder.commit()
            ret = {"folder_updated": True}
            loggers['backend'].info(
                'Folder updated:\n'
                f'   Folder ID: {folder.folder_id}\n'
                f'   Name: {old_name} => {folder.name}\n'
                f'   Parent Folder ID: {old_parent} = > '
                f'{folder.parent_folder_id}')
        elif request.method == "DELETE":
            Folders.remove(ID)
            ret = {"folder_removed": True}
            loggers['backend'].info('Folder removed:\n'
                                    f'Folder ID: {ID}')
        elif request.method == 'GET':
            folder_html = Folders.get_folders_select_html(ID)
            ret = {"folders_HTML": folder_html}
            loggers['backend'].debug('List of folders retrieved')
        return jsonify(ret)

    @app.route('/phrase/', methods=["GET", "POST"])
    def phrase():
        data = request.get_json()
        if request.method == 'POST':
            num = ''
            if not Phrases.cmd_free(data['cmd']):
                num = 0
                while not Phrases.cmd_free(data['cmd']+str(num)):
                    num += 1
            phrase = Phrases(
                name=data['name'],
                cmd=data['cmd']+str(num),
                folder_id=data['folder_id']
            )
            Phrases.add(phrase)
            db.session.flush()
            ret = {
                "phrase_added": True,
                "cmd": phrase.cmd,
                "phrase_id": phrase.phrase_id}
            loggers['backend'].info(
                'New phrase added:\n'
                f'   Phrase ID: {phrase.phrase_id}\n'
                f'   Name: {phrase.name}\n'
                f'   Command: {phrase.cmd}\n'
                f'   Parent Folder ID: {phrase.folder_id}')
        elif request.method == 'GET':
            phrases = Phrases.get_phrase_list_html()
            ret = {"phraseList_HTML": phrases}
            loggers['backend'].debug('List of folders and phrases retrieved')
        return jsonify(ret)

    @app.route('/phrase/<ID>', methods=["GET", "POST", "DELETE"])
    def existing_phrase(ID):
        data = request.get_json()
        if request.method == 'POST':
            phrase = Phrases.query_id(ID)
            old_name = phrase.name
            old_cmd = phrase.cmd
            old_folder = phrase.folder_id
            old_text = phrase.phrase_text
            old_html = phrase.phrase_html
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
            loggers['backend'].info(
                'Phrase updated:\n'
                f'   Phrase ID: {phrase.phrase_id}\n'
                f'   Name: {old_name} => {phrase.name}\n'
                f'   Command: {old_cmd} => {phrase.cmd}\n'
                f'   Parent Folder ID: {old_folder} => {phrase.folder_id}')
            loggers['backend'].debug(
                'Phrase updated:\n'
                f'   Phrase ID: {phrase.phrase_id}\n'
                f'   Old Text:\n\n{old_text}\n\n'
                f'   New Text:\n\n{phrase.phrase_text}\n\n'
                f'   Old HTML:\n\n{old_html}\n'
                f'   New HTML:\n\n{phrase.phrase_html}\n\n'
            )
        elif request.method == "DELETE":
            Phrases.remove(ID)
            Phrases.commit()
            ret = {"phrase_removed": True}
            loggers['backend'].info('Phrase removed:\n'
                                    f'Phrase ID: {ID}')
        elif request.method == 'GET':
            phrase = Phrases.query_id(ID)
            ret = {
                "cmd": phrase.cmd,
                "name": phrase.name,
                "phrase_html": phrase.phrase_html.decode()
                if phrase.phrase_html else "",
                "folder_id": phrase.folder_id
            }
            loggers['backend'].info(
                'Phrase retrieved:\n'
                f'   Phrase ID: {phrase.phrase_id}\n'
                f'   Name:{phrase.name}\n'
                f'   Command: {phrase.cmd}\n'
                f'   Parent Folder ID: {phrase.folder_id}')
            loggers['backend'].debug(
                'Phrase updated:\n'
                f'   Phrase ID: {phrase.phrase_id}\n'
                f'   Text:\n\n{phrase.phrase_text}\n\n'
                f'   HTML:\n\n{phrase.phrase_html}\n\n'
            )
        return jsonify(ret)

    @app.route('/config/<SETTING>', methods=["GET", "POST"])
    def config(SETTING):
        if request.method == 'POST':
            data = request.get_json()
            old_value = Settings.query_setting(SETTING)
            Settings.update(SETTING, data['value'])
            value = Settings.query_setting(SETTING)
            ret = {"setting_updated": True}
            loggers['backend'].info('Setting updated:\n'
                                    f'Setting: {SETTING}'
                                    f'Value: {old_value} => {value}')
        elif request.method == 'GET':
            value = Settings.query_setting(SETTING)
            ret = {"value": value}
            loggers['backend'].info('Setting retrieved:\n'
                                    f'Setting: {SETTING}'
                                    f'Value: {value}')
        return jsonify(ret)

    @ app.route('/focus/', methods=["POST"])
    def focus():
        data = request.get_json()
        kb.guiStatus(data['focus'])
        if data['focus']:
            loggers['backend'].info(
                'Received GUI focus change: Active')
        else:
            loggers['backend'].info(
                'Received GUI focus change: Inactive')
        return {"focus": data['focus']}

    # @ app.route('/shutdown', methods=['POST'])
    # def shutdown():
    #     data = request.get_json()
    #     if data['are_you_sure']:
    #         shutdown_server()
    #         return 'Server shutting down...'
    #     else:
    #         return False

    loggers['backend'].debug('...Loading Flask routes COMPLETE')
    loggers['backend'].info('Flask startup COMPLETE')
    return app
