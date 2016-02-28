from app import app
from flask import render_template
from form import NameForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = NameForm()
    return render_template('index.html', form=form1)

@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    content = None
    form = NameForm()
    if form.validate_on_submit():
        content = form.content.data
        form.content.data = ''
    return render_template('strategy.html', form=form, content=content)