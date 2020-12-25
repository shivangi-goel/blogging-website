from flask1 import db, login_manager
from datetime import datetime
from flask_login import UserMixin#default implementation of functions
#that flask_login is supposed to have

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(30), unique=True, nullable=False)
	email=db.Column(db.String(150), unique=True, nullable=False)
	image_file=db.Column(db.String(20), nullable=True, default='default.jpg')
	password=db.Column(db.String(60), nullable=False)
	posts=db.relationship('Post', backref='author', lazy=True)
	#get all of the posts created by a user.
	#we will hash the images and the size of hashed images will be 20 units
	#we will hash the password, length=60

	def __repr__(self):
		return f"User('{self.name}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(200), nullable=False)
	dateof_post=db.Column(db.DateTime, nullable=False, default=datetime.now)
	content=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.dateof_post}')"