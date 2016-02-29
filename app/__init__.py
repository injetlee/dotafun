from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import config



SECRET_KEY = 'hard to guess'


app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)



from views import *

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask
# app = Flask(__name__)
#
# from views import *
# if __name__ == '__main__':
# 	app.run(debug=True)


