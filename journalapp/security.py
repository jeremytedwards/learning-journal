# coding=utf-8
from passlib.hash import sha512_crypt
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
# from pyramid.config.Configurator import SignedCookieSessionFactory
from pyramid.security import ALL_PERMISSIONS, Allow, Everyone
from pyramid.security import Authenticated
from wtforms.ext.csrf.form import SecureForm
from hashlib import md5


import os


authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
# my_session_factory = SignedCookieSessionFactory('itsaseekreet')

def is_admin_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'empty')
    return sha512_crypt.verify(pw, hashed)


def hash_of_pw(pw):
    return sha512_crypt.encrypt(pw)


USERS = {
    'editor': 'editor',
    }


GROUPS = {
    'editor': ['group:editors'],
    }


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'SecretUser', ALL_PERMISSIONS),
        (Allow, 'group:editors', ('add', 'edit')),
        ]

    def __init__(self, owner):
        self.owner = owner


# class GlobalAuthPolicy(AuthTktAuthenticationPolicy):
#     def authenticated_userid(self, request):
#         userid = self.unauthenticated_userid(request)
#         if userid:
#             if request.verify_userid_is_still_valid(userid):
#                 return userid
#
#     def effective_principals(self, request):
#         principals = [Everyone]
#         userid = self.authenticated_userid(request)
#         if userid:
#             principals += [Authenticated, str(userid)]
#         return principals


# # Authentication
# class IAuthenticationPolicy(object):
#     """ An object representing a Pyramid authentication policy. """
#
#     def authenticated_userid(self, request):
#         """ Return the authenticated :term:`userid` or ``None`` if
#         no authenticated userid can be found. This method of the
#         policy should ensure that a record exists in whatever
#         persistent store is used related to the user (the user
#         should not have been deleted); if a record associated with
#         the current id does not exist in a persistent store, it
#         should return ``None``.
#
#         """
#         pass
#
#     def unauthenticated_userid(self, request):
#         """ Return the *unauthenticated* userid.  This method
#         performs the same duty as ``authenticated_userid`` but is
#         permitted to return the userid based only on data present
#         in the request; it needn't (and shouldn't) check any
#         persistent store to ensure that the user record related to
#         the request userid exists.
#
#         This method is intended primarily a helper to assist the
#         ``authenticated_userid`` method in pulling credentials out
#         of the request data, abstracting away the specific headers,
#         query strings, etc that are used to authenticate the request.
#
#         """
#         pass
#
#     def effective_principals(self, request):
#         """ Return a sequence representing the effective principals
#         typically including the :term:`userid` and any groups belonged
#         to by the current user, always including 'system' groups such
#         as ``pyramid.security.Everyone`` and
#         ``pyramid.security.Authenticated``.
#
#         """
#
#     def remember(self, request, userid, **kw):
#         """ Return a set of headers suitable for 'remembering' the
#         :term:`userid` named ``userid`` when set in a response.  An
#         individual authentication policy and its consumers can
#         decide on the composition and meaning of **kw.
#
#         """
#         pass
#
#     def forget(self, request):
#         """ Return a set of headers suitable for 'forgetting' the
#         current user on subsequent requests.
#         """
#         pass
#
# # Authorization
# class IAuthorizationPolicy(object):
#     """ An object representing a Pyramid authorization policy. """
#     def permits(self, context, principals, permission):
#         """ Return ``True`` if any of the ``principals`` is allowed the
#         ``permission`` in the current ``context``, else return ``False``
#         """
#         pass
#
#     def principals_allowed_by_permission(self, context, permission):
#         """ Return a set of principal identifiers allowed by the
#         ``permission`` in ``context``.  This behavior is optional; if you
#         choose to not implement it you should define this method as
#         something which raises a ``NotImplementedError``.  This method
#         will only be called when the
#         ``pyramid.security.principals_allowed_by_permission`` API is
#         used."""
#         pass
