import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'SECRETKEY'
    SQLALCHEMY_DATABASE_URI =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	
	
