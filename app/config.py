import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_op.sqlite')
SECRET_KEY = 'hard to guess'
DEBUG = True