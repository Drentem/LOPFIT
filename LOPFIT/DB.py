from LOPFIT.ext import db


class Common():
    @classmethod
    def query_all(cls):
        return cls.query.all()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return True

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
    def query_setting(cls, setting):
        return cls.query.filter(cls.setting == setting).one().value

    @classmethod
    def init(cls):
        if not cls.query.filter(cls.setting == "execution_key").first():
            cls.add(Settings(
                setting="execution_key",
                value=0
            ))

    @classmethod
    def update(cls, setting, value):
        query = cls.query.filter(cls.setting == setting).one()
        query.value = value
        db.session.commit()


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
        return cls.query.filter(cls.phrase_id == phrase_id).one()

    @classmethod
    def get_phrases(cls):
        query = cls.query.order_by(cls.folder_id, cls.name).all()
        phrases_raw = {}
        for i in query:
            if i.folder_id not in phrases_raw.keys():
                phrases_raw[i.folder_id] = []
            phrases_raw[i.folder_id].append(
                {"id": i.phrase_id, "name": i.name})
        return phrases_raw

    @classmethod
    def get_phrase_list_html(cls):
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
                                "<li role='treeitem' class='doc' id='phrase-" +
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
        return ''.join(html_list)

    @ classmethod
    def get_cmds(cls):
        query = cls.query.all()
        cmds = []
        for item in query:
            i = item.phrase_id, item.cmd
            cmds.append(i)
        return cmds

    @ classmethod
    def get_phrase(cls, phrase_id):
        try:
            return cls.query.filter(cls.phrase_id == phrase_id).one().phrase
        except Exception:
            return False

    @ classmethod
    def check_cmd(cls, cmd):
        query = cls.query.filter(cls.cmd == cmd).first()
        if query:
            return True
        else:
            return False

    @ classmethod
    def remove(cls, phrase_id):
        query = cls.query.filter(cls.phrase_id == phrase_id).one()
        db.session.delete(query)
        db.session.commit()
        return True

    @ classmethod
    def update(cls, data):
        phrase = cls.query.filter(cls.id == data['id']).one()
        phrase.cmd = data['cmd']
        phrase.name = data['name']
        phrase.phrase = data['phrase']
        db.session.commit()
        return True


class Folders(db.Model, Common):
    __tablename__ = 'folders'
    folder_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255), nullable=False)
    parent_folder_id = db.Column(db.Integer, nullable=False)
    sqlite_autoincrement = True

    def __repr__(self):
        return '<Folder %r>' % self.folder_id

    @ classmethod
    def query_id(cls, folder_id):
        return cls.query.filter(cls.folder_id == folder_id).one()

    @ classmethod
    def remove(cls, id):
        def processing(folder_id):
            sub_folders = cls.query.filter(
                cls.parent_folder_id == folder_id).all()
            for folder in sub_folders:
                processing(folder.folder_id)
                phrases_affected = Phrases.get_phrases4folder(folder.folder_id)
                for phrase_folder in phrases_affected:
                    phrase = Phrases.query_id(phrase_folder.phrase_id)
                    db.session.delete(phrase)
                    db.session.delete(phrase_folder)
                    db.session.commit()
            folder = cls.query_id(folder_id)
            db.session.delete(folder)
            db.session.commit()
        processing(id)
        return True

    @ classmethod
    def get_folders(cls):
        query = cls.query.order_by(cls.parent_folder_id, cls.name).all()
        folders_raw = {}
        for i in query:
            if i.parent_folder_id not in folders_raw.keys():
                folders_raw[i.parent_folder_id] = []
            folders_raw[i.parent_folder_id].append(
                {"id": i.folder_id, "name": i.name})
        return folders_raw

    @ classmethod
    def get_folders_select_html(cls, exclude=False):
        if exclude:
            query = cls.query.filter(
                cls.parent_folder_id != exclude, cls.folder_id != exclude)\
                .order_by(cls.parent_folder_id, cls.name).all()
        else:
            query = cls.query.order_by(cls.parent_folder_id, cls.name).all()
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
        return ''.join(html_list)
