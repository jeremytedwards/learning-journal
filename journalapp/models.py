import datetime

from sqlalchemy import Column, Index, Integer, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import desc


Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


def query_table():
    return DBSession.query(Entry).order_by(desc(Entry.created))


def query_post(post_id):
    return DBSession.query(Entry).get(post_id)


def new_entry(new_title=None, new_text=None):
    DBSession.add(Entry(title=new_title, text=new_text))
    DBSession.flush()
    new_id = DBSession.query(Entry).order_by(desc(Entry.created))[0].id
    return new_id


def edit_entry(pkey, new_title, new_text):
    update_dict = {"title": new_title, "text": new_text}
    DBSession.query(Entry).filter(Entry.id == pkey).update(update_dict)
    DBSession.flush()
    return pkey


class Entry(Base):
    """Class for creating database blog entries."""
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True)
    text = Column(Unicode())
    created = Column(DateTime, default=datetime.datetime.utcnow)


Index('my_index', Entry.title, unique=True)
