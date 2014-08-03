from flask import Flask, render_template, request, redirect, url_for, abort, g, flash, escape, session, make_response
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime, tzinfo, timedelta
from flask.ext.sqlalchemy import SQLAlchemy
from flask.sessions import SessionInterface, SessionMixin
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('config') # pull in configs from config.py

db = SQLAlchemy(app) # init DB conn

# set up login manager
login_manager = LoginManager(app)
login_manager.login_view = "users.login_view"

# register users module
from app.users.views import mod as usersModule
app.register_blueprint(usersModule)

def initdb():
  db.drop_all()
  db.create_all()
  db.session.commit()

#-----------------------
# generic routes
#-----------------------

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.before_request
def before_request():
  if current_user.is_authenticated():
    g.user = current_user
  else:
    g.user = None
