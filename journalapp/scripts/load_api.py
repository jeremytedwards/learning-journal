# coding=utf-8
import os
import requests

from journalapp.models import Entry
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


def load_with_key():
    """
    Opens a DB session
    Collects and processes a JSON into a DB session
    Closes the session
    """
    # Get API key
    api_key = os.environ.get('API_KEY', None)

    # Get DB Session
    database_url = os.environ.get('DATABASE_URL', None)
    print(database_url)
    engine = engine_from_config({'sqlalchemy.url': database_url})
    DBSession.configure(bind=engine)

    json_payload = {}
    r = requests.get('https://sea401d2.crisewing.com/api/export?apikey=' + api_key)
    if r.status_code == requests.codes.ok:
        json_payload = r.json()
    if json_payload:
        """post to journal"""
        for entry in json_payload:
            load_entry(entry["title"], entry["text"], entry["created"])

    # Flush DB Session
    print("Before:\n", DBSession.new)
    DBSession.flush()
    print("After:\n", DBSession.new)


def load_entry(update_title, update_text, update_created=None):
    """
    ADDs or UPDATEs an entry in the DB session
    """
    try:
        """ Try to find an item in the DB, if found update """
        existing_entry = DBSession.query(Entry).filter(Entry.title == update_title)
        update_dict = {
            "title": update_title,
            "text": update_text,
            "created": update_created
        }
        DBSession.query(Entry).filter(Entry.id == existing_entry.id).update(update_dict)
        print("Updated item:\n{}\n{}\n{}\n\n".format(**update_dict))
    except AttributeError:
        """ Item was not found in the DB, create new item """
        add_item = (
            Entry(title=update_title, text=update_text, created=update_created)
        )
        DBSession.add(add_item)
        # print(
        #     "Add item:\n{}\n{}\n\n "
        #     .format(add_item.title, add_item.text, add_item.created)
        # )

    """
    docs.python-requests.org/en/master/user/quickstart/

    Requests' simple API means that all forms of HTTP request are as obvious.
    For example, this is how you make an HTTP POST request:
        r = requests.get('https://api.github.com/events')
        r = requests.post('http://httpbin.org/post', data={'key': 'value'})
        r = requests.put('http://httpbin.org/put', data={'key': 'value'})
        r = requests.delete('http://httpbin.org/delete')
        r = requests.head('http://httpbin.org/get')
        r = requests.options('http://httpbin.org/get')
    Passing arguments:
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.get('http://httpbin.org/get', params=payload)
        So the resulting r would be:
        http://httpbin.org/get?key2=value2&key1=value1
    Built in JSON decoding:
        json_payload = r.json()
        In case the JSON decoding fails, r.json raises an exception. For
        example, if the response gets a 204 (No Content), or if the response
        contains invalid JSON, attempting r.json raises ValueError: No JSON
        object could be decoded.
        To check that a request is successful, use
        r.raise_for_status() will return None if ok
        or check
        r.status_code == requests.codes.ok
        is what you expect.

        You can Inspect the headers as well...
        r.headers
        {
            'content-encoding': 'gzip',
            'transfer-encoding': 'chunked',
            'connection': 'close',
            'server': 'nginx/1.0.4',
            'x-runtime': '148ms',
            'etag': '"e1ca502697e5c9317743dc078f67693f"',
            'content-type': 'application/json'
        }
    """

