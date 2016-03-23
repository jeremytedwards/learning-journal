# coding=utf-8
from passlib.hash import sha512_crypt

import os


def is_admin_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'empty')
    return sha512_crypt.verify(pw, hashed)


def hash_of_pw(pw):
    return sha512_crypt.encrypt(pw)

