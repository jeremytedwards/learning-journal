# -*- coding: utf-8 -*-
from journalapp.models import DBSession, Base, Entry
from pyramid import testing
from sqlalchemy import create_engine
from webob import multidict

import pytest
import os

# TEST_DATABASE_URL = 'postgresql+psycopg2://jackbot:@localhost:5432/'
# TEST_DATABASE_URL = 'postgresql+psycopg2://journalapp:journalapp@localhost:5432/'
TEST_DATABASE_URL = os.environ.get('JOURNAL_APP_TEST', 'sqlite://')
# TEST_DATABASE_URL = 'sqlite://'


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(scope='session')
def app(config_uri):
    """Create pretend app fixture of our main app."""
    from journalapp import main
    from webtest import TestApp
    from pyramid.paster import get_appsettings
    settings = get_appsettings(config_uri)
    settings['sqlalchemy.url'] = TEST_DATABASE_URL
    app = main({}, **settings)
    return TestApp(app)


# @pytest.fixture()
# def session(dbtransaction):
#     from journalapp.models import DBSession
#     return DBSession


@pytest.fixture()
def new_entry(request):
    """Return a fresh new Entry and flush to the database."""
    entry = Entry(title="Test Title", text="Test Text for an entry.")
    DBSession.add(entry)
    DBSession.flush()
    return entry


@pytest.fixture(scope='function')
def dummy_request():
    """Make a base generic dummy request to be used."""
    request = testing.DummyRequest()
    config = testing.setUp()
    config.add_route('home', '/')
    config.add_route('detail', '/entry/{pkey:\d+}')
    config.add_route('new', '/new/')
    config.add_route('edit', '/edit/{pkey:\d+}')
    return request


@pytest.fixture(scope='function')
def dummy_get_request(dummy_request):
    """Make a dummy GET request to test views."""
    dummy_request.method = 'GET'
    dummy_request.POST = multidict.NoVars()
    return dummy_request


@pytest.fixture(scope='function')
def dummy_post_request(request, dummy_request):
    """Make a dummy POST request to test views."""
    dummy_request.method = 'POST'
    dummy_request.POST = multidict.MultiDict([('title', 'TESTadd'),
                                              ('text', 'TESTadd')])
    return dummy_request
