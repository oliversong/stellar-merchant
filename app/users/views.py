from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm
from app.users.models import User
from tornado import web, ioloop

mod = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@mod.route('/login', methods=('GET', 'POST'))
def login_view():
  form = LoginForm(request.form)
  if form.validate_on_submit():
    flash("Logged in successfully.")
    login_user(form.user)
    return redirect('/home')
  return render_template('users/login.html', form=form)

@mod.route('/home')
@login_required
def home():
  user = db.session.query(User).filter_by(id=session['user_id']).first()
  return render_template('users/home.html', user=user)

@mod.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index'))
