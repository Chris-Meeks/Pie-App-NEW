from flask_sqlalchemy  import SQLAlchemy
from ..import db
from . models import Data

def delfunc(filename):
    Data.query.filter_by(name=filename).delete()
    db.session.commit()
    return filename, " deleted"


##def delete_users_data(username):
##    files = [a.name for a in Data.query.filter_by(owner=username).all()
##    for file in files:
##             delfunc(file)
##    
##    return username, "data deleted"


    
