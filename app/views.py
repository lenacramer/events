import secrets
import os
from PIL import Image
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, EventForm
from app.models import User, Post, Event
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
   events = Event.query.all()
   return render_template('index.html', events=events)

@app.route('/all-users')
def all_users():
      users = User.query.all()
      return render_template('all_users.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   form = RegistrationForm()
   if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username=form.username.data, email=form.email.data, password=hashed_password)
      db.session.add(user)
      db.session.commit()
      flash('Your account has been created!', 'success')
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
         login_user(user, remember=form.remember.data)
         return redirect(url_for('home'))
      else: 
         flash('Login unsuccessful', 'danger')
   return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('home'))

def save_profile_picture(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   picture_fn = random_hex + f_ext
   picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
   output_size = (150, 150)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(picture_path)
   prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
   if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
      os.remove(prev_picture)
   return picture_fn

def save_flier_picture(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   picture_fn = random_hex + f_ext
   picture_path = os.path.join(app.root_path, 'static/flier_pics', picture_fn)
   output_size = (300, 300)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(picture_path)
   return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
   form = UpdateAccountForm()
   if form.validate_on_submit():
      if form.picture.data:
         picture_file = save_profile_picture(form.picture.data)
         current_user.image_file = picture_file
      current_user.username = form.username.data
      current_user.email = form.email.data
      db.session.commit()
      flash('Account has been updated.', 'success')
      return redirect(url_for('account'))
   elif request.method == 'GET':
      form.username.data = current_user.username
      form.email.data = current_user.email
   image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
   return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
   form = EventForm()
   if form.validate_on_submit():
      if form.picture.data:
         picture_file = save_flier_picture(form.picture.data)
         flash(picture_file)
         event = Event(name=form.name.data, description=form.description.data, 
            picture=picture_file, date=form.date.data, description_long=form.description_long.data,
            category=form.category.data, tags=form.category.data, 
            author=current_user)
         db.session.add(event)
         db.session.commit()
         flash('Your event has been created!', 'success')
         return redirect(url_for('home'))
   return render_template('create_event.html', title='New Event', form=form, legend='New Event')

@app.route('/post/<int:post_id>')
def post(post_id):
      post = Post.query.get_or_404(post_id)
      return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
      post = Post.query.get_or_404(post_id)
      if post.author != current_user:
         abort(403)
      form = PostForm()
      
      if form.validate_on_submit():
         post.title = form.title.data
         post.content = form.content.data
         db.session.commit()
         flash('Your post has been updated!', 'success')
         return redirect(url_for('home'))
      elif request.method == 'GET':
         form.title.data = post.title
         form.content.data = post.content
      return render_template('create_post.html', title='Update Post', 
               form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
      post = Post.query.get_or_404(post_id)
      if post.author != current_user:
         abort(403)
      db.session.delete(post)
      db.session.commit()
      flash('Your post has been deleted!', 'success')
      return redirect(url_for('home'))

# @app.route('/post/new', methods=['GET', 'POST'])
# @login_required
# def new_post():
#    form = PostForm()
#    if form.validate_on_submit():
#       post = Post(title=form.title.data, content=form.content.data, author=current_user)
#       db.session.add(post)
#       db.session.commit()
#       flash('Your post has been created!', 'success')
#       return redirect(url_for('home'))
#    return render_template('create_post.html', title='New Post', form=form, legend='New Post')
