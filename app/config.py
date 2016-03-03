import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_op.sqlite')
SECRET_KEY = 'hard to guess'
DEBUG = True
MAIL_SERVER = 'smtp.126.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'liyingjie26@126.com'
MAIL_PASSWORD = 'ipnumkmbpiyteftt'
FLASK_ADMIN = '838500806@qq.com'
FLASKY_MAIL_SUBJECT_PREFIX = '[DotaFun]'
FLASKY_MAIL_SENDER = 'liyingjie26@126.com'