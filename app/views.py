from app import app, db
from flask import render_template, redirect, url_for, flash, session
from form import NameForm
from model import User, Post

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = NameForm()
    return render_template('index.html', form=form1)

@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    # username = None
    form = NameForm()

    if form.validate_on_submit():
        username = form.username.data

        # session['name'] = form.username.data
        #

        user = User.query.filter_by(username=username).first()
        if user is None:
            # # flash('the username has been existed')
            # return redirect(url_for('index'))
            username = User(username=form.username.data)
            db.session.add(username)
            db.session.commit()
            title = Post(title=form.title.data, content=form.content.data,
                         author_id=username.id)
            # content = Post(content=form.content.data)

            db.session.add(title)
            # db.session.add(content)
            db.session.commit()
            return redirect(url_for('strategy'))
        else:
            flash('the username has been existed')
            return redirect(url_for('index'))
    postl = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('strategy.html', form=form, username=form.username.data, postl=postl)

# @app.route('/')
# def gongl():
