from LOPFIT.ext import db


class Common():
    @classmethod
    def query_all(cls):
        return cls.query.all()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return True


class Settings(db.Model, Common):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.String(length=255), nullable=False)
    value = db.Column(db.String(length=255), nullable=False)

    @classmethod
    def query_id(cls, id):
        return cls.query.filter(cls.id == id).one()

    @classmethod
    def update(cls, id, value):
        query = cls.query_id(id)
        query.value = value
        db.session.commit()


class Phrases(db.Model, Common):
    __tablename__ = 'phrases'
    phrase_id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(length=255), nullable=False)
    name = db.Column(db.String(length=255), nullable=False)
    phrase = db.Column(db.BLOB, nullable=False)
    sqlite_autoincrement = True

    def __repr__(self):
        return '<Phrase %r>' % self.phrase_id

    @classmethod
    def query_id(cls, id):
        return cls.query.filter(cls.phrase_id == id).one()

    @classmethod
    def get_phrase_list_html(cls):
        folders_raw = Folders.get_folders()
        query = cls.query.join(
            Phrase_Folders, cls.phrase_id == Phrase_Folders.phrase_id)\
            .add_columns(Phrase_Folders.folder_id).order_by(cls.name)
        html_list = []

        def processing(folder_data):
            for item in folder_data:
                html_list.append("<li role='treeitem' aria-expanded='false' ")
                html_list.append("selected='no' id='folder-" + str(item['id']))
                html_list.append("'><span>"+item['name']+"</span>")
                html_list.append("<ul role='group'>")

                if item['id'] in folders_raw.keys():
                    processing(folders_raw[item['id']])
                for phrase in query.filter(
                        Phrase_Folders.folder_id == item['id']).all():
                    html_list.append(
                        "<li role='treeitem' class='doc' id='phrase-" +
                        str(item['id']) + "'>")
                    html_list.append(phrase.Phrases.name)
                    html_list.append('</li>')
                html_list.append('</ul>')
                html_list.append('</li>')

        if len(folders_raw) > 0:
            processing(folders_raw[0])

        return ''.join(html_list)

    @classmethod
    def get_cmds(cls):
        query = cls.query.all()
        cmds = []
        for item in query:
            i = item.phrase_id, item.cmd
            cmds.append(i)
        return cmds

    @classmethod
    def get_phrase(cls, phrase_id):
        try:
            return cls.query.filter(cls.phrase_id == phrase_id).one().phrase
        except Exception:
            return False

    @classmethod
    def check_cmd(cls, cmd):
        query = cls.query.filter(cls.id == id).first()
        if query:
            return True
        else:
            return False

    @classmethod
    def remove(cls, phrase_id):
        query = cls.query.filter(cls.phrase_id == phrase_id).one()
        db.session.delete(query)
        db.session.commit()
        return True

    @classmethod
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

    @classmethod
    def query_id(cls, id):
        return cls.query.filter(cls.folder_id == id).one()

    @classmethod
    def remove(cls, id):
        def processing(folder_id):
            sub_folders = cls.query.filter(
                cls.parent_folder_id == folder_id).all()
            for folder in sub_folders:
                processing(folder.folder_id)
                phrases_affected = Phrase_Folders.get_phrases(folder.folder_id)
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

    @classmethod
    def get_folders(cls):
        query = cls.query.order_by(cls.parent_folder_id, cls.name).all()
        folders_raw = {}
        for i in query:
            if i.parent_folder_id not in folders_raw.keys():
                folders_raw[i.parent_folder_id] = []
            folders_raw[i.parent_folder_id].append(
                {"id": i.folder_id, "name": i.name})
        return folders_raw

    @classmethod
    def get_folders_select_html(cls):
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


class Phrase_Folders(db.Model, Common):
    __tablename__ = 'phrases_folders'
    id = db.Column(db.Integer, primary_key=True)
    phrase_id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def update_id(cls, phrase_id, folder_id):
        query = cls.query.filter(cls.phrase_id == phrase_id).one()
        query.folder_id = folder_id
        query.commit()

    @classmethod
    def get_phrases(cls, folder_id):
        query = cls.query.filter(cls.folder_id == folder_id).all()
        return query

    @classmethod
    def remove(cls, id):
        query = cls.query.filter(cls.id == id).one()
        db.session.delete(query)
        db.session.commit()
        return True
