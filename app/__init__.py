# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import config
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.mail import Mail



SECRET_KEY = 'hard to guess'


app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = u'请先登录'
db = SQLAlchemy(app)
from model import Permission

@app.context_processor
def inject_permissions():
    return dict(Permission=Permission)



from views import *

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask
# app = Flask(__name__)
#
# from views import *
# if __name__ == '__main__':
# 	app.run(debug=True)


