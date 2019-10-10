from flask import Flask
from flask import Flask, render_template, redirect, url_for,g,session,request,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user,  logout_user, current_user#login_required,
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from pie.config import Config
pie = Flask(__name__)
pie.config.from_object(Config)
basedir = os.path.abspath(os.path.dirname(__file__))
pie.config['TESTING'] = False
db = SQLAlchemy(pie)
bootstrap = Bootstrap(pie)

login_manager = LoginManager(pie)
login_manager.init_app(pie)
login_manager.login_view = 'api.login'


ALLOWED_EXTENSIONS = {'xlsx'}


from pie.api.routes import mod

pie.register_blueprint(api.routes.mod)
