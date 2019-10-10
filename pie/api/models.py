from flask_sqlalchemy  import SQLAlchemy
from ..import db
from flask_login import UserMixin



class UserLogin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(22), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    permission = db.Column(db.String(20))

    def __repr__(self):
        return "<UserLogin(username='%s',email='%s',permission='%s')>"%(self.username,self.email,self.permission)

class Data(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True)
    attributes = db.Column(db.Text())
    owner = db.Column(db.String(22))
    
    def __init__(self,name,attributes,owner):
        self.name = name
        self.attributes = attributes
        self.owner = owner

   
        
    def __repr__(self):
        return "<Data(name='%s')>"%(self.name)
