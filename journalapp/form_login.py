# coding=utf-8
from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.Length(min=4, max=50)])
