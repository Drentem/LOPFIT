from sqlalchemy import Column, Integer, String, BLOB, create_engine
from sqlalchemy.ext.declarative import declarative_base
# import os

dbfile = 'sqlite:///pyPhraseExpander.db'
# dbfile = 'sqlite:////' + str(os.path.join(
#     os.path.expanduser("~/Documents"), "pyPhraseExpander.db"))
print(dbfile)
engine = create_engine(dbfile)
Base = declarative_base()


class Phrases(Base):
    __tablename__ = 'phrases'
    id = Column(Integer, primary_key=True)
    cmd = Column(String(length=255), nullable=False)
    name = Column(String(length=255), nullable=False)
    phrase = Column("phrase", BLOB, nullable=False)
    sqlite_autoincrement = True

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
        engine.add(cls(
            cmd=data['cmd'],
            name=data['name'],
            phrase=data['phrase']
        ))
        engine.commit()
        return True

    @classmethod
    def remove(cls, id):
        return True

    @classmethod
    def update(cls, data):
        phrase = cls.query.filter(cls.id == id).one()
        phrase.cmd = data['cmd']
        phrase.name = data['name']
        phrase.phrase = data['phrase']
        engine.commit()
        return True


Base.metadata.create_all(engine)
