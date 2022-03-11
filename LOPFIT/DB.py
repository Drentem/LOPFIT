from LOPFIT.ext import db
from LOPFIT.misc.logs import loggers


class Common():
    @classmethod
    def query_all(cls):
        object_type = type(cls)
        try:
            query = cls.query.all()
            loggers['database'].debug(
                f'Retrieved all {object_type}s from the database.')
            return query
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                f'Failed to add {object_type} to the database. Error details:'
            )

    def add(self):
        object_type = type(self)
        try:
            db.session.add(self)
            db.session.commit()
            return True
            loggers['database'].debug(
                f'Added {object_type} to the database.')
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                f'Failed to add {object_type} to the database. Error details:'
            )

    @classmethod
    def commit(cls):
        db.session.commit()


class Settings(db.Model, Common):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.String(length=255), nullable=False)
    value = db.Column(db.String(length=255), nullable=False)
    sqlite_autoincrement = True

    @classmethod
    def init(cls):
        try:
            loggers['database'].info('Initilizing database...')
            if not cls.query.filter(cls.setting == "execution_key").first():
                setting = "execution_key"
                value = "space"
                cls.add(Settings(
                    setting=setting,
                    value=value
                ))
                loggers['database'].debug('Adding initial setting:'
                                          f'     Setting: {setting}\n'
                                          f'     Value: {value}'
                                          )
            loggers['database'].info('Initilizing database COMPLETE')
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to initilize the database. Error details:'
            )

    @classmethod
    def query_setting(cls, setting):
        try:
            value = cls.query.filter(cls.setting == setting).one().value
            loggers['database'].debug('Retrieved setting from database:\n'
                                      f'     Setting: {setting}\n'
                                      f'     Value: {value}'
                                      )
            return value
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieve setting from database:\n'
                f'     Setting: {setting}\n'
                'Error details:'
            )

    @classmethod
    def update(cls, setting, value):
        try:
            query = cls.query.filter(cls.setting == setting).one()
            query.value = value
            db.session.commit()
            loggers['database'].debug('Updated setting in database:\n'
                                      f'     Setting: {setting}\n'
                                      f'     Value: {value}'
                                      )
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to update setting in database:\n'
                f'     Setting: {setting}\n'
                f'     Value: {value}\n'
                'Error details:'
            )


class Phrases(db.Model, Common):
    __tablename__ = 'phrases'
    phrase_id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(length=255), nullable=False, unique=True)
    name = db.Column(db.String(length=255), nullable=False)
    folder_id = folder_id = db.Column(db.Integer)
    phrase_text = db.Column(db.BLOB)
    phrase_html = db.Column(db.BLOB)
    sqlite_autoincrement = True

    def __repr__(self):
        return '<Phrase %r>' % self.phrase_id

    @classmethod
    def query_id(cls, phrase_id):
        try:
            phrase = cls.query.filter(cls.phrase_id == phrase_id).one()
            loggers['database'].debug('Retrieved phrase from the database:\n'
                                      f'     Phrase ID: {phrase.phrase_id}\n'
                                      f'     Name: {phrase.name}'
                                      f'     Command: {phrase.cmd}'
                                      )
            return phrase
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieve a phrase from the database:\n'
                f'     Phrase ID: {phrase_id}\n'
                'Error details:'
            )

    @classmethod
    def get_phrases(cls):
        try:
            query = cls.query.order_by(cls.folder_id, cls.name).all()
            phrases_raw = {}
            for i in query:
                if i.folder_id not in phrases_raw.keys():
                    phrases_raw[i.folder_id] = []
                phrases_raw[i.folder_id].append(
                    {"id": i.phrase_id, "name": i.name})
            loggers['database'].debug(
                'Phrase information gathered from the database')
            return phrases_raw
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieve phrases from the database')

    @classmethod
    def get_phrase_list_html(cls):
        try:
            folders_raw = Folders.get_folders()
            phrases_raw = Phrases.get_phrases()
            html_list = []

            def processing(id):
                if id in folders_raw:
                    for item in folders_raw[id]:
                        html_list.append(
                            "<li role='treeitem' aria-expanded='false' " +
                            "selected='no' id='folder-" + str(item['id']) +
                            "'><span>" + item['name'] + "</span>")
                        html_list.append("<ul role='group'>")
                        if item['id'] in folders_raw:
                            processing(item['id'])
                        if item['id'] in phrases_raw:
                            for phrase in phrases_raw[item['id']]:
                                html_list.append(
                                    "<li role='treeitem' class='doc'"
                                    " id='phrase-" +
                                    str(phrase['id']) + "'>" +
                                    phrase['name'] + '</li>')
                        html_list.append('</ul>')
                        html_list.append('</li>')
                if id == 0 and id in phrases_raw:
                    for phrase in phrases_raw[id]:
                        html_list.append(
                            "<li role='treeitem' class='doc' id='phrase-" +
                            str(phrase['id']) + "'>" +
                            phrase['name'] + '</li>')

            if len(folders_raw) > 0:
                processing(0)
            loggers['database'].debug('Converted folders and phrases'
                                      ' from the database to HTML format')
            return ''.join(html_list)
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to convert folders and phrases'
                ' from the database to HTML format')

    @classmethod
    def get_phrase(cls, phrase_id):
        try:
            loggers['database'].debug(
                'Retrieved a phrase from the database:\n'
                f'     Phrase ID: {phrase_id}'
            )
            return cls.query.filter(cls.phrase_id == phrase_id).one().phrase
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieve a phrase from the database:\n'
                f'     Phrase ID: {phrase_id}\n'
                'Error details:'
            )
            return False

    @classmethod
    def check_cmd(cls, cmd):
        try:
            query = cls.query.filter(cls.cmd == cmd).first()
            if query:
                query = {
                    'text': query.phrase_text.decode(),
                    'html': query.phrase_html.decode()
                }
                loggers['database'].debug(
                    'Phrase command succeeded to retrieve a phrase'
                    'from the database:\n'
                    f'     Command: {cmd}'
                )
                return query
            else:
                loggers['database'].debug(
                    'Phrase command does not exist in the database:\n'
                    f'     Command: {cmd}'
                )
                return False
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieve a phrase from the database:\n'
                f'     Command: {cmd}\n'
                'Error details:'
            )
            return False

    @classmethod
    def cmd_free(cls, cmd):
        try:
            query = cls.query.filter(cls.cmd == cmd).first()
            if query:
                loggers['database'].debug('Phrase command exists:\n'
                                          f'     Command: {cmd}'
                                          )
                return False
            else:
                loggers['database'].debug(
                    'Phrase command does not exist in the database:\n'
                    f'     Command: {cmd}'
                )
                return True
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to to check command in the database:\n'
                f'     Command: {cmd}\n'
                'Error details:'
            )
            return False

    @classmethod
    def remove(cls, phrase_id):
        try:
            query = cls.query.filter(cls.phrase_id == phrase_id).one()
            db.session.delete(query)
            db.session.commit()
            loggers['database'].debug(
                'Removed a phrase from the database:\n'
                f'     Phrase ID: {phrase_id}'
            )
            return True
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to remove a phrase from the database:\n'
                f'     ID: {phrase_id}\n'
                'Error details:'
            )

    @classmethod
    def update(cls, data):
        try:
            phrase = cls.query.filter(cls.id == data['id']).one()
            phrase.cmd = data['cmd']
            phrase.name = data['name']
            phrase.phrase_text = data['phrase_text']
            phrase.phrase_html = data['phrase_html']
            db.session.commit()
            loggers['database'].info(
                'Updated a phrase from the database:\n'
                f'     ID: {phrase.phrase_id}\n'
                f'     Name: {phrase.name}\n'
                f'     Command: {phrase.cmd}\n')
            loggers['database'].debug(
                'Updated a phrase from the database:\n'
                f'     ID: {phrase.phrase_id}\n'
                f'     Phrase Text: {phrase.phrase_text}\n'
                f'     Phrase HTML: {phrase.phrase_html}\n'
                f'     Command: {phrase.cmd}\n')
            return True
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to update a phrase from the database:\n'
                f'     ID: {data["phrase_id"]}\n'
                f'     Name: {data["name"]}\n'
                f'     Command: {data["cmd"]}\n'
                f'     Phrase Text: {data["phrase_text"]}\n'
                f'     Phrase HTML: {data["phrase_html"]}\n'
                'Error details:'
            )


class Folders(db.Model, Common):
    __tablename__ = 'folders'
    folder_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255), nullable=False)
    parent_folder_id = db.Column(db.Integer, nullable=False)
    sqlite_autoincrement = True

    def __repr__(self):
        return '<Folder %r>' % self.folder_id

    @classmethod
    def query_id(cls, folder_id):
        try:
            folder = cls.query.filter(cls.folder_id == folder_id).one()
            loggers['database'].debug('Retrieved folder from the database:\n'
                                      f'     Folder ID: {folder.folder_id}\n'
                                      f'     Name: {folder.name}'
                                      )
            return folder
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieve a folder from the database:\n'
                f'     Folder ID: {folder_id}\n'
                'Error details:'
            )

    @classmethod
    def __remove(cls, folder_id):
        try:
            query = cls.query.filter(cls.folder_id == folder_id).one()
            db.session.delete(query)
            db.session.commit()
            loggers['database'].debug(
                'Removed a folder from the database:\n'
                f'     Folder ID: {folder_id}'
            )
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to remove a folder from the database:\n'
                f'     Folder ID: {folder_id}\n'
                'Error details:'
            )

    @classmethod
    def remove(cls, id):
        try:
            loggers['database'].debug(
                'Attempting to remove folder and contents from the database:\n'
                f'     Folder ID: {id}'
            )

            def processing(folder_id):
                sub_folders = cls.query.filter(
                    cls.parent_folder_id == folder_id).all()
                for folder in sub_folders:
                    processing(folder.folder_id)
                    phrases_affected = Phrases.get_phrases4folder(
                        folder.folder_id)
                    for phrase_folder in phrases_affected:
                        Phrases.remove(phrase_folder.phrase_id)
                        cls.__remove(phrase_folder.phrase_id)
                        db.session.commit()
                cls.__remove(folder_id)
                db.session.commit()
            processing(id)
            loggers['database'].debug(
                'Successfully removed folder and contents:\n'
                f'     Folder ID: {id}'
            )
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to remove folder and contents from the database:\n'
                f'     ID: {id}\n'
                'Error details:'
            )

    @classmethod
    def get_folders(cls):
        try:
            query = cls.query.order_by(cls.parent_folder_id, cls.name).all()
            folders_raw = {}
            for i in query:
                if i.parent_folder_id not in folders_raw.keys():
                    folders_raw[i.parent_folder_id] = []
                folders_raw[i.parent_folder_id].append(
                    {"id": i.folder_id, "name": i.name})
            loggers['database'].debug(
                'Successfully retrieved folders from the database'
            )
            return folders_raw
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieved folders from the database. Error details:'
            )

    @classmethod
    def get_folders_select_html(cls, exclude=False):
        try:
            if exclude:
                query = cls.query.filter(
                    cls.parent_folder_id != exclude, cls.folder_id != exclude)\
                    .order_by(cls.parent_folder_id, cls.name).all()
            else:
                query = cls.query.order_by(
                    cls.parent_folder_id, cls.name).all()
            folders_raw = {}
            for i in query:
                if i.parent_folder_id not in folders_raw.keys():
                    folders_raw[i.parent_folder_id] = []
                folders_raw[i.parent_folder_id].append(
                    {"id": i.folder_id, "name": i.name})
            folders = [{"id": 0, "name": "Root Folder"}]

            def processing(folder_data, depth=0):
                for item in folder_data:
                    folder = {"id": item["id"], "name": item["name"].rjust(
                        len(item["name"])+depth*2, "-")}
                    folders.append(folder)
                    if item['id'] in folders_raw.keys():
                        depth += 1
                        depth = processing(folders_raw[item['id']], depth)
                return depth - 1

            if len(folders_raw) > 0:
                processing(folders_raw[0])
            html_list = []
            for folder in folders:
                html_list.append('<option value=' + str(folder['id']) + ">")
                html_list.append(folder['name'])
                html_list.append('</option>')
            loggers['database'].debug(
                'Successfully retrieved folders from the database as HTML.'
            )
            return ''.join(html_list)
        except Exception as e:  # noqa: F841
            loggers['database'].exception(
                'Failed to retrieved folders from the database as HTML.'
                ' Error details:'
            )
