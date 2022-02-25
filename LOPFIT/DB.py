from LOPFIT.ext import db


class Common():
    @classmethod
    def query_all(cls):
        return cls.query.all()

    @classmethod
    def query_id(cls, id):
        return cls.query.filter(cls.id == id).one()

    def __repr__(self):
        return '<%r>' % self.id


class Phrases(db.Model):
    __tablename__ = 'phrases'
    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(length=255), nullable=False)
    name = db.Column(db.String(length=255), nullable=False)
    phrase = db.Column(db.BLOB, nullable=False)
    sqlite_autoincrement = True

    @classmethod
    def get_phrase_list(cls):
        query = cls.query.all()
        cmds = []
        for item in query:
            i = item.id, item.name
            cmds.append(i)
        return cmds

    @classmethod
    def get_cmds(cls):
        query = cls.query.all()
        cmds = []
        for item in query:
            i = item.id, item.cmd
            cmds.append(i)
        return cmds

    @classmethod
    def get_phrase(cls, id):
        try:
            return cls.query.filter(cls.id == id).one().phrase
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
    def add(cls, data):
        db.session.add(cls(
            cmd=data['cmd'],
            name=data['name'],
            phrase=data['phrase']
        ))
        db.session.commit()
        return True

    @classmethod
    def remove(cls, id):
        query = cls.query.filter(cls.id == id).one()
        db.session.delete(query)
        db.session.commit()
        return True

    @classmethod
    def update(cls, data):
        phrase = cls.query.filter(cls.id == id).one()
        phrase.cmd = data['cmd']
        phrase.name = data['name']
        phrase.phrase = data['phrase']
        db.session.commit()
        return True
