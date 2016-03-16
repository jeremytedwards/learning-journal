# from pyramid.response import Response
from pyramid.view import view_config

# from sqlalchemy.exc import DBAPIError
#
# from .models import (
#     DBSession,
#     Entry,
#     )


@view_config(route_name='blog_post', renderer='templates/blog_base.jinja2', match_param='blog=somevalue')
def blog_view_somevalue(request):
    return request.matchdict

@view_config(route_name='blog_post', renderer='templates/blog_base.jinja2', match_param='blog=anothervalue')
def blog_view_anothervalue(request):
    return request.matchdict

@view_config(route_name='blog_post', renderer='templates/blog_base.jinja2')
def blog_view_none(request):
    return request.matchdict


# Sample view config
# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(Entry).filter(Entry.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'journalapp'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initializedb" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
