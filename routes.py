from PIL import Image
from flask import render_template,url_for, flash, redirect, request, abort
from flask1 import app, db
from flask1.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask1.models import User, Post
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
#current user will help the logged in user to surf through site and not go to login and register page again and again
"""
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
        'image_file':'default.jpg'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
        'image_file':'default.jpg'
    }
]
"""
#db=SQLAlchemy(app)#SQLAlchemy instance
bcrypt=Bcrypt(app)


@app.route("/")
@app.route("/home")
def home():
	posts=Post.query.order_by(Post.dateof_post.desc()).all()
	return render_template('home.html', posts=posts)
#now for our home page we'll set title to default and change it for about

@app.route("/about")
def about():
   # return render_template('about.html')
   return render_template('about.html',title='About')

 #now route for registration and login form
@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(name=form.name.data, email=form.email.data, password=hashed_password)
		#temp_session=db.session.merge()
		db.session.add(user)
		try:
			db.session.commit()
		except:
			db.session.rollback()
		finally:
			db.session.close()
		flash(f'Your Account creation is successful, Congratulations!!{form.name.data}! You are now a member', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page=request.args.get('next')
			#args is dictionary, get method returns none if next parameter exists else return the page
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Oops! Incorrect Credentials! Try Again to Login', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

#saving the updated profile picture
def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	#os returns filename and extension
	_, f_ext=os.path.splitext(form_picture.filename)
	#we only will use extension variable and not the name so we just put underscore
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(app.root_path, 'static/profile_pictures', picture_fn)
	output_size=(120,120)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

#account to create, edit profile and posts
@app.route("/account", methods=['GET', 'POST'])
@login_required#decorator
def account():
	form=UpdateAccountForm()
	if form.validate_on_submit():
		if form.profile_pic.data:
			picture_file=save_picture(form.profile_pic.data)
			current_user.image_file=picture_file
		current_user.name=form.name.data
		current_user.email=form.email.data
		try:
			db.session.commit()
		except:
			db.session.rollback()
		finally:
			db.session.close()
		flash('Yayay!! Account updated successfully.','success')
		return redirect(url_for('account'))
	elif request.method=='GET':
		form.name.data=current_user.name
		form.email.data=current_user.email
	image_file=url_for('static', filename='profile_pictures/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)

#creating new posts
@app.route("/post/new", methods=['GET', 'POST'] )
@login_required
def new_post():
	form=PostForm()
	if form.validate_on_submit():
		#add database
		#session.clear()
		post=Post(title=form.title.data, content=form.content.data, author=current_user)
		db.create_all()
		db.session.add(post)
		try:
			db.session.commit()
		except:
			db.session.rollback()
		finally:
			db.session.close()
		#console.log(post)
		flash('Congratulations on finally creating a post!', 'success')
		return redirect(url_for('home'))
	#db.session.rollback()
	return render_template('post_create.html', title='Create New Post', form=form, legend='You made it till here!!Hurray, Create new posts:)')

#creating post
@app.route("/post/<int:post_id>")
def post(post_id):
	post=Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

#updating a post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		abort(403)#http command for forbidden actions, gives error message
	form=PostForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		db.session.commit()
		flash('Changes have been made, Post Updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method=='GET':
		form.title.data=post.title
		form.content.data=post.content
	return render_template('post_create.html', title='Update Post', form=form, legend='Want to make changes? Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ahh! Post deleted.', 'success')
    return redirect(url_for('home'))
