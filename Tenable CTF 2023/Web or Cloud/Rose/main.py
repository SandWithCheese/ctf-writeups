from flask import Blueprint, render_template, render_template_string, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if("name" in session.keys()):
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main.route('/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('main.index'))

    login_user(user, remember=remember)
    session["name"] = current_user.name
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    template = '''
{% extends "base.html" %} {% block content %}
<h1 class="title">
    Welcome, '''+ session["name"] +'''!
</h1>
<p> The dashboard feature is currently under construction! </p>
{% endblock %}
'''
    return render_template_string(template)

#@main.route('/signup')
#def signup():
#    return render_template('signup.html')

#@main.route('/signup', methods=['POST'])
#def signup_post():
#
#    email = request.form.get('email')
#    name = request.form.get('name')
#    password = request.form.get('password')
#
#    user = User.query.filter_by(email=email).first()
#
#    if user: 
#        flash('Email address already exists')
#        return redirect(url_for('main.signup'))
#
#    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
#
#    db.session.add(new_user)
#    db.session.commit()
#
#    return redirect(url_for('main.index'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.index'))