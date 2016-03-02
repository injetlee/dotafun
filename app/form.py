# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import  SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired
class NameForm(Form):
    username = StringField('email address', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('what is your oponion', validators=[DataRequired()])
    submit = SubmitField('Submit')
