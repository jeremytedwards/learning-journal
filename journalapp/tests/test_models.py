# coding=utf-8

from journalapp.models import Entry, DBSession


def test_create_entry(session):
    new_model = Entry(title="Blog Post", text="my entry goes here")
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None


def test_entry_date(session):
    new_model = Entry(title="Blog Post", text="my entry goes here")
    assert new_model.created is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.created is not None


def test_title(session):
    new_model = Entry(title="Blog Post", text="my entry goes here")
    DBSession.add(new_model)
    DBSession.flush()
    assert DBSession.query(Entry).all()[0].title == "Blog Post"


def test_text(session):
    new_model = Entry(title="Blog Post", text="my entry goes here")
    DBSession.add(new_model)
    DBSession.flush()
    assert DBSession.query(Entry).all()[0].text == "my entry goes here"
