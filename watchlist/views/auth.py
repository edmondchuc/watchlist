from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from passlib.context import CryptContext

from watchlist.models import User
from watchlist.extensions import db


routes = Blueprint('auth', __name__)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def user_exists(username: str):
    user = User.query.filter_by(username=username).first()
    if user:
        return True
    return False


@routes.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        valid_input = True

        if not username:
            flash('Username is required.', 'alert-danger')
            valid_input = False
        if not password:
            flash('Password is required.', 'alert-danger')
            valid_input = False

        if len(username) > 30:
            flash('Username cannot be more than 30 characters long.', 'alert-danger')
            valid_input = False
        if len(password) > 100:
            flash('Password cannot be more than 100 characters long.', 'alert-danger')
            valid_input = False

        if valid_input:
            password_hash = get_password_hash(password)
            if not user_exists(username):
                user = User(username=username, password_hash=password_hash)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash(f'Successfully created account. Welcome {username} 😊', 'alert-success')
                return redirect(url_for('main.home'))
            else:
                flash(f'Username {username} is already taken.', 'alert-danger')

    return render_template('auth/registration.html')


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Username is required.', 'alert-danger')
        if not password:
            flash('Password is required.', 'alert-danger')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                valid_password = verify_password(password, user.password_hash)

                if valid_password:
                    login_user(user)
                    flash('Logged in successfully.', 'alert-success')
                    return redirect(url_for('main.home'))

            flash('Incorrect username or password.', 'alert-danger')
            return redirect(request.referrer)

    return render_template('auth/login.html')


@routes.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))
