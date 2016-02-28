from flask import Flask


app = Flask(__name__)
from views import *
app.config['SECRET_KEY'] = 'hard to guess'
if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask
# app = Flask(__name__)
#
# from views import *
# if __name__ == '__main__':
# 	app.run(debug=True)


