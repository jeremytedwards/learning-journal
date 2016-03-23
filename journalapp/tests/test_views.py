# coding=utf-8
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.exc import IntegrityError
from webob.multidict import MultiDict
from journalapp.form_new import NewBlogEntryForm
from journalapp.models import DBSession, Entry

import pytest


def test_home_view(dbtransaction, new_entry, dummy_get_request):
    """Test that the home view returns a Query of Entries."""
    from journalapp.views import home
    response_dict = home(dummy_get_request)
    entries = response_dict['blog_posts']
    assert entries[0] == new_entry


def test_detail_view(dbtransaction, new_entry, dummy_get_request):
    """Test that detail view returns the correct Entry page."""
    from journalapp.views import detail
    dummy_get_request.matchdict = {'pkey': new_entry.id}
    response_dict = detail(dummy_get_request)
    assert response_dict['post'] == new_entry


def test_new_view(dbtransaction, dummy_get_request):
    """Test that the new view returns a dict containing the proper form."""
    from journalapp.views import new
    response_dict = new(dummy_get_request)
    form = response_dict.get('form', None)
    assert isinstance(form, NewBlogEntryForm)


def test_edit_view(dbtransaction, new_entry, dummy_get_request):
    """Test that the edit view returns a dict containing the proper form."""
    from journalapp.views import edit
    dummy_get_request.matchdict = {'pkey': new_entry.id}
    response_dict = edit(dummy_get_request)
    print(response_dict)
    form = response_dict.get('form', None)
    print(form)
    assert isinstance(form, NewBlogEntryForm)


def test_edit_view_post(dbtransaction, new_entry, dummy_post_request):
    """Test that the edit view returns a dict containing the proper form."""
    from journalapp.views import edit
    dummy_post_request.path = '/edit'
    dummy_post_request.method = "POST"
    dummy_post_request.POST = MultiDict([
        ('title', "test post title"),
        ('text', "test post text")
    ])
    dummy_post_request.matchdict = {'pkey': new_entry.id}
    response = edit(dummy_post_request)
    assert response.status_code == 302 and response.title == 'Found'
    created_entry = DBSession.query(Entry).filter(
        Entry.title == "test post title"
    ).first()
    assert created_entry is not None
    expected_url = dummy_post_request.route_url('detail',
                                                pkey=created_entry.id)
    assert response.location.endswith(expected_url)


def test_new_view_post(dbtransaction, dummy_post_request):
    """Test that the new view returns a dict containing the proper form."""
    from journalapp.views import new
    dummy_post_request.path = '/new'
    dummy_post_request.method = "POST"
    dummy_post_request.POST = MultiDict([
        ('title', "test post title"),
        ('text', "test post text")
    ])
    response = new(dummy_post_request)
    assert response.status_code == 302 and response.title == 'Found'
    created_entry = DBSession.query(Entry).filter(
        Entry.title == "test post title"
    ).first()
    assert created_entry is not None
    expected_url = dummy_post_request.route_url('detail',
                                                pkey=created_entry.id)
    assert response.location.endswith(expected_url)


def test_new_view_dupe(dbtransaction, dummy_post_request):
    """Test that the new view returns a dict containing the proper form."""
    from journalapp.views import new
    dummy_post_request.path = '/new'
    response1 = new(dummy_post_request)
    assert response1.status_code == 302 and response1.title == 'Found'
    with pytest.raises(IntegrityError):
        new(dummy_post_request)


def test_detail_error(dbtransaction, dummy_get_request):
    """Test that detail page gives a HTTPNotFound when entry
    ID does not exist."""
    from journalapp.views import detail
    dummy_get_request.matchdict = {'pkey': 9999}
    with pytest.raises(HTTPNotFound):
        detail(dummy_get_request)


def test_edit_error(dbtransaction, dummy_get_request):
    """Test that edit page gives a HTTPNotFound when entry
    ID does not exist."""
    from journalapp.views import edit
    dummy_get_request.matchdict = {'pkey': 9999}
    with pytest.raises(HTTPNotFound):
        edit(dummy_get_request)
