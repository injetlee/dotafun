# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import  SubmitField, TextAreaField
from wtforms.validators import DataRequired
class NameForm(Form):
    content = TextAreaField('what is your oponion', validators=[DataRequired()])
    submit = SubmitField('Submit')
