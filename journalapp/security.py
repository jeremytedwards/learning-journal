# coding=utf-8
from passlib.context import CryptContext
from pyramid.security import ALL_PERMISSIONS, Allow, Everyone

import os

password_context = CryptContext(schemes=['pbkdf2_sha512'])


def is_valid_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'empty')
    print(hashed)
    return password_context.verify(pw, hashed)


def hash_of_pw(pw):
    return password_context.encrypt(pw)


class DefaultRootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'SecretUser', ALL_PERMISSIONS),
        ]

    def __init__(self, owner):
        self.owner = owner
