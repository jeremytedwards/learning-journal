# coding=utf-8
import os


def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'empty')
    return pwd_context.verify(pw, hashed)

