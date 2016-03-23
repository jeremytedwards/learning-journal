# coding=utf-8
from .models import DBSession, Entry
from .form_new import NewBlogEntryForm
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from webob.multidict import NoVars


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
    update_dict = {
        "title": new_title,
        "text": new_text,
    }
    DBSession.query(Entry).filter(Entry.id==pkey).update(update_dict)
    DBSession.flush()
    return pkey


@view_config(route_name='home', renderer='templates/blog_home.jinja2')
def home(request):
    all_posts = query_table()
    return dict(blog_posts=all_posts)


@view_config(route_name='detail', renderer='templates/blog_detail.jinja2')
def detail(request):
    pkey = request.matchdict.get("pkey")
    one_post = query_post(pkey)
    if one_post is None:
        raise HTTPNotFound
    return dict(post=one_post)


@view_config(route_name='new', renderer='templates/blog_new.jinja2')
def new(request):
    form = NewBlogEntryForm(request.POST or NoVars())
    if request.method == "POST":
        new_pkey = new_entry(form.title.data, form.text.data)
        next_url = request.route_url('detail', pkey=new_pkey)
        return HTTPFound(location=next_url)
    return {'form': form}


@view_config(route_name='edit', renderer='templates/blog_edit.jinja2')
def edit(request):
    pkey = request.matchdict.get("pkey")
    entry = DBSession.query(Entry).get(pkey)
    if entry is None:
        raise HTTPNotFound
    form = NewBlogEntryForm(request.POST, entry)
    if request.method == "POST":
        try:
            form.populate_obj(entry)
            current_pkey = edit_entry(pkey, form.title.data, form.text.data)
            next_url = request.route_url('detail', pkey=current_pkey)
            return HTTPFound(location=next_url)
        except IntegrityError:
            form.errors.setdefault('error', []).append("Ah oh something "
                                                       "went wrong")
    return {'form': form}
