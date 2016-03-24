from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config


import os

from .models import DBSession, Base
from .security import DefaultRootFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    ## DBConnection
    database_url = os.environ.get('DATABASE_URL', None)
    if database_url is not None:
        settings['sqlalchemy.url'] = database_url
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    ## Security
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    default_permission = 'view'

    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'SecretUser')
    settings['auth.password'] = os.environ.get('AUTH_PASSWORD', hash)

    ## Config settings
    config = Configurator(settings=settings)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_session_factory(my_session_factory)
    config.set_default_permission(default_permission)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', factory=DefaultRootFactory)
    config.add_route('detail', '/entry/{pkey:\d+}', factory=DefaultRootFactory)
    config.add_route('new', '/new/', factory=DefaultRootFactory)
    config.add_route('edit', '/edit/{pkey:\d+}', factory=DefaultRootFactory)
    config.add_route('login', '/login/', factory=DefaultRootFactory)
    config.add_route('logout', '/logout/', factory=DefaultRootFactory)
    config.scan()
    return config.make_wsgi_app()
