from flask import Flask

#SQLAlchemy is a database creating tool in python where we can edit database without making changes in python code
#it is a kind of SQL.
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

app.config['SECRET_KEY']='343c4a8e72d61ad2a6a1ceddde934ea6'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)#SQLAlchemy instance
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from flask1 import routes