from datetime import datetime

from flask import render_template, flash, redirect
from flask import request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Agarwal Ji'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Rishabh', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = 'index'
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('login')
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect('index')
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect('user', username=username)
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect('user', username=username)


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect('index')
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect('user', username=username)
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect('user', username=username)


@app.route('/testing')
def test():
    movies = []
    return jsonify({'movies': movies})

@app.route('/send_image_url', methods=['POST'])
def recieve():
    movie_name = request.get_json()
    title = movie_name['title']
    writer = movie_name['writer']
    url = movie_name['url']
    import PIL
    # image loading libraries down
    from PIL import Image
    import requests
    from io import BytesIO
    import numpy as np
    response = requests.get(url)
    img=Image.open(BytesIO(response.content))
    img = np.array(img)
    image_shape = str(img.shape[0])+','+str(img.shape[1])
    # return render_template('movie.html', mtitle=title, mwriter=writer, murl=url)
    return jsonify({'result':image_shape})

# @app.route lines above the function are decorators
# A common pattern with decorators is to use them to register functions as callbacks for certain events
# This means that when a web browser requests either of these two URLs,
# Flask is going to invoke this function and pass the return value of it back to the browser as a response.
# The way Flask-Login protects a view function against anonymous users is with a decorator called @login_required