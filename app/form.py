# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import  SubmitField, TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email
class NameForm(Form):
    # username = StringField('email address', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('what is your oponion', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])

    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField(u'保持登录状态')
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z0-9_.]*$', 0, u'用户名由字母数字或下划线组成'
    )])

    password1 = PasswordField('password1', validators=[DataRequired(), EqualTo('password', message=u'两次密码必须一致')] )
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField(u'注册')