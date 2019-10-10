from flask import Blueprint
from flask import Flask, render_template, redirect, url_for,g,session,request,flash
from flask_bootstrap import Bootstrap
from .forms import LoginForm, RegisterForm, PieSelector, SpreadieForm

from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user #,login_required
import os
from werkzeug import secure_filename
from .dictionaryJSON3 import JSONify 
import json
from .. import db
from .. import login_manager
from .. import basedir
from .models import UserLogin, Data
from sqlalchemy.exc import IntegrityError

mod = Blueprint('api',__name__)



ALLOWED_EXTENSIONS = {'xlsx'}

from functools import wraps
from flask import g, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        	
        if not current_user.is_authenticated:
	    
            return redirect(url_for('api.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.permission == 'ADMIN':
            return redirect(url_for('api.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(int(user_id))



@mod.route('/')
def index():
    return render_template('index.html')

@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    cwd = os.getcwd()
    if form.validate_on_submit():
        user = UserLogin.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                if not os.path.isdir('userfiles'):
                    os.makedirs('userfiles')
                if os.path.exists(os.path.join('userfiles',current_user.username)):
                       print("Yes")
                else:
                    os.chdir(os.path.join(cwd,'userfiles'))
                    os.makedirs(current_user.username)
                    os.chdir(cwd)
                    
                return redirect(url_for('api.dashboard'))   
    
    return render_template('login.html', form=form)

@mod.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        
        new_user = UserLogin(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
		
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "<h1> That username or email is already in use. </h1>"

       
    
        

        return '<h1>New user has been created!</h1>'
        

    return render_template('signup.html', form=form)


@mod.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    a = None
    
    if os.getcwd() != basedir: 
        os.chdir(basedir)
    cwd = os.getcwd()
    
    pieform = PieSelector()
    if current_user:
        yourpies = [(data.name,data.name)for data in Data.query.filter_by(owner=current_user.username).all()]
        
        pieform.options.choices = yourpies

        if pieform.validate_on_submit():
            choice = pieform.options.data
            retrieved_data = Data.query.filter_by(name=choice).first()
            a = retrieved_data.attributes
            a = json.loads(a)
            session['a']=a
            ####
            ##return render_template("testscript-restart.html", a=a)
            return redirect(url_for("api.piechart",a=a))
        return render_template('dashboard.html', pieform=pieform,name=current_user.username)
    else:
        return "<h1> This sucks </h1>"
##
@mod.route('/list',methods=['GET','POST'])
@login_required
def list_files():
    from .deleter import delfunc
    pieform = PieSelector()
    if current_user:
        yourpies = [(data.name,data.name)for data in Data.query.filter_by(owner=current_user.username).all()]
        
        pieform.options.choices = yourpies

        if pieform.validate_on_submit():
            choice = pieform.options.data
            retrieved_data = Data.query.filter_by(name=choice).first()
            delfunc(retrieved_data.name)
            return "<h1> You chose {} </h1>".format(retrieved_data.name)
    return render_template('list.html',pieform=pieform,name=current_user.username) 

##
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@mod.route('/uploadform',methods=['GET','POST'])
@login_required
def uploadform():
        spreadform = SpreadieForm()
        os.chdir(basedir)
        cwd = os.getcwd()
        username=current_user.username
        
        
        if os.path.exists(os.path.join('userfiles',username)):
                os.chdir(os.path.join('userfiles',username))
                cwd = os.getcwd()
               
        else:
                print("You don't got no folder bruh")
                	
                
        if spreadform.validate_on_submit():
            f = spreadform.file.data
            
			
            if allowed_file(f.filename) == False:
                    return "<h1> This file extension is not permitted. </h1>"
            f.save(secure_filename(f.filename))
            data = JSONify(f.filename)
            
            d = json.dumps(data)
            try:
                new = Data(f.filename,d,current_user.username)
                db.session.add(new)
                db.session.commit()
            except:
                return "<h1> That file already exists</h1>"
            
                
            return '<h1> Success </h1>'  
        
        return render_template('uploadform.html',spreadform=spreadform)


@mod.route('/admin')
@login_required
@admin_required
def admin():
    return "<h1> If you are looking at this you must be the administrator </h1>"
    

@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('api.index'))

@mod.route('/testpage')
@login_required
def testpage():
	##print("logged in as "+current_user)
	return "<h1> this is the test page </h1>"

@mod.route('/piechart',methods=['GET','POST'])
@login_required
def piechart():
    a = session.get('a')
    return render_template('testscript-restart.html',a=a)