# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, redirect, url_for, flash, session, request
from functools import wraps
from form import NameForm, LoginForm, RegisterForm, ChangePwd, ForgetPwd, ResetPwd, Profile
from model import User, Post
from flask.ext.login import login_required, login_user, logout_user, current_user, current_app
from flask.ext.mail import Message
import config
from . import mail
def abc(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = NameForm()
    return render_template('index.html', form=form1)

@app.route('/strategy', methods=['GET', 'POST'])
# @login_required
def strategy():
    #
    # if current_user.is_authenticated and form.validate_on_submit():
    #     post = Post(title=form.title.data, content=form.content.data,
    #                  author=current_user._get_current_object())
    #
    #     db.session.add(post)
    #     # db.session.add(content)
    #     db.session.commit()
    #     return redirect(url_for('strategy'))
    postl = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('strategy.html', postl=postl)

@app.route('/writepost', methods=['GET', 'POST'])
@abc
def writepost():
    form = NameForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                     author=current_user._get_current_object())

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('strategy'))
    return render_template('writepost.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('.index'))
        flash(u'邮箱或密码错误')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(u'你已经登出')
    return redirect(url_for('.index'))

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user_name = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash(u'邮箱已经注册，请登录')
            return redirect(url_for('.login'))
        elif user_name:
            flash(u'用户名已经存在')
            return redirect(url_for('.register'))

        else:
            user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
            db.session.add(user)
            db.session.commit()
            send_email(config.FLASK_ADMIN, 'NEW USER', 'mail/new_user', user=user)
            token = user.generate_confirm_token()
            send_email(user.email, u'确认你的账户', 'mail/confirm', user=user, token=token)
        flash(u'一封确认邮件已经发送到你的邮箱')
        return redirect(url_for('.index'))
    return render_template('register.html', form=form)

@app.route('/update')
def updatepost():
    return render_template('updatepost.html')

def send_email(to, subject, template, **kwargs):
    msg = Message(config.FLASKY_MAIL_SUBJECT_PREFIX + subject,
                  sender=config.FLASKY_MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.route('/confirm/<token>')
@abc
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.index'))
    if current_user.confirm(token):
        flash(u'你已经确认了你的账户，可查看所有功能')
    else:
        flash(u'链接无效，或者过期')
    return redirect(url_for('.index'))

# @app.before_request
# def before_request():
#     if current_user.is_authenticated \
#         and not current_user.confirmed \
#         and request.endpoint == 'writepost':
#         flash(u'请确认你的邮件地址')
#         return redirect(url_for('.unconfirmed'))

@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('.index'))
    return render_template('unconfirmed.html')

@app.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.generate_confirm_token()
    send_email(current_user.email, u'确认你的账户', 'mail/confirm', user=current_user, token=token)
    flash(u'请登录邮箱确认')

    return redirect(url_for('.index'))

@app.route('/changepwd',methods=['GET', 'POST'])
@login_required
def changepwd():
    form = ChangePwd()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpwd.data):
            current_user.password = form.newpwd1.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'你的密码已经修改')
            return redirect(url_for('.index'))
        else:
            flash(u'无效的密码')
    return render_template('changepwd.html', form=form)

@app.route('/resetpwd', methods=['GET', 'POST'])
def resetpwd():
    form = ForgetPwd()
    if not current_user.is_anonymous:
        redirect(url_for('.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_resetpwd_token()
            send_email(user.email, u'确认你的账户', 'mail/resetpwd', user=user, token=token)
            flash(u'验证邮件已发到你的邮箱')
            return redirect(url_for('.index'))
        else:
            flash(u'邮箱不存在')
    return render_template('resetpwd.html', form=form)

@app.route('/resetpwd/<token>', methods=['GET', 'POST'])
def resetpwd_sub(token):
    if not current_user.is_anonymous:
        return redirect(url_for('.index'))
    form = ResetPwd()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('.index'))
        if user.confirm_resetpwd(token, form.newpwd1.data):
            flash(u'密码已经更改')
            return redirect(url_for('.login'))
        else:
            return redirect(url_for('.index'))
    return render_template('resetpwd.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = Profile()
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
    return render_template('profile.html', form=form)

@app.before_request
def berore_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint == 'writepost':
            flash(u'请确认你的邮箱地址')
            return redirect(url_for('.unconfirmed'))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html',  user=user)