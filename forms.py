from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask1.models import User

#we will create registation form first
class RegistrationForm(FlaskForm):
	name=StringField('Name', validators=[DataRequired(), Length(min=1, max=30)])
	email=StringField('Email', validators=[DataRequired(),Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Sign up')

	#custom validation
	def validate_username(self, name):
		user=User.query.filter_by(name=name.data).first()
		if user:
			raise ValidationError('The username you mentioned is already taken. Take a unique username')

	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('The email you mentioned is already taken. Take a valid email')
			

class LoginForm(FlaskForm):
	#we will use email id and password for login and not username
	#name=StringField('Name', validators=[DataRequired(), Length(min=1, max=30)])
	email=StringField('Email', validators=[DataRequired(),Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	#confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	remember=BooleanField('Remember Me')
	submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	name=StringField('Name', validators=[DataRequired(), Length(min=1, max=30)])
	email=StringField('Email', validators=[DataRequired(),Email()])
	profile_pic=FileField('Update your Profile Picture.', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	submit=SubmitField('Done with changes, Update! ')

	#custom validation
	def validate_username(self, name):
		if name.data!=current_user.name:
			user=User.query.filter_by(name=name.data).first()
			if user:
				raise ValidationError('The username you mentioned is already taken. Take a unique username')

	def validate_email(self, email):
		if email.data!=current_user.email:
			user=User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('The email you mentioned is already taken. Take a valid email')

class PostForm(FlaskForm):
	title=StringField('Title', validators=[DataRequired()])
	content=TextAreaField('Content', validators=[DataRequired()])
	submit=SubmitField('Post')
