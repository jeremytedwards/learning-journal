# coding=utf-8
from wtforms import Form, StringField, TextAreaField, validators


class NewBlogEntryForm(Form):
    title = StringField('title', [validators.Length(min=4, max=25)])
    text = TextAreaField('text', [validators.Length(min=4, max=250)])
