# coding=utf-8
from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    un = StringField('un', [validators.Length(min=4, max=50)])
    pw = PasswordField('pw', [validators.Length(min=4, max=50)])
