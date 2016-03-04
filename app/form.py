# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import  SubmitField, TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email
class NameForm(Form):
    title = StringField(u'标题', validators=[DataRequired()])
    content = TextAreaField(u'内容', validators=[DataRequired()])
    submit = SubmitField(u'提交')

class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])

    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'保持登录状态')
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z0-9_.]*$', 0, u'用户名由字母数字或下划线组成'
    )])

    password1 = PasswordField(u'密码', validators=[DataRequired(), EqualTo('password', message=u'两次密码必须一致')] )
    password = PasswordField(u'再次输入密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

class ChangePwd(Form):
    oldpwd = StringField(u'旧密码', validators=[DataRequired()])
    newpwd1 = StringField(u'新密码', validators=[DataRequired(), EqualTo('newpwd2', message=u'两次密码必须一致')])
    newpwd2 = StringField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'更改')

class ForgetPwd(Form):
    email = StringField(u'请输入邮箱地址', validators=[DataRequired(), Email(), Length(1,64)])
    submit = SubmitField(u'提交')

class ResetPwd(Form):
    email = StringField(u'请输入邮箱地址', validators=[DataRequired(), Email(), Length(1,64)])
    newpwd1 = StringField(u'新密码', validators=[DataRequired(), EqualTo('newpwd2', message=u'两次密码必须一致')])
    newpwd2 = StringField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'提交')

class Profile(Form):
    name = StringField(u'你的名字', validators=[DataRequired(), Length(1,32)])
    location = StringField(u'你的地址', validators=[DataRequired()])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'提交')