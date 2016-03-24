from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config


import os

from .models import DBSession, Base


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
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'SecretUser')
    settings['auth.password'] = os.environ.get('AUTH_PASSWORD', hash)

    ## Config settings
    config = Configurator(settings=settings)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/entry/{pkey:\d+}')
    config.add_route('new', '/new/')
    config.add_route('edit', '/edit/{pkey:\d+}')
    config.add_route('login', '/login/')
    # config.add_route('logout', '/logout/')
    config.scan()
    return config.make_wsgi_app()
