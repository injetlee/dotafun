# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, redirect, url_for, flash, session, request
from functools import wraps
from form import NameForm, LoginForm, RegisterForm
from model import User, Post
from flask.ext.login import login_required, login_user, logout_user, current_user, current_app

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
        if User.query.filter_by(email=form.email.data).first():
            flash(u'邮箱已经注册，请登录')
            return redirect(url_for('.login'))
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'你已经注册成功了，请登录')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
