from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm
from app.users.models import User
from tornado import web, ioloop
from werkzeug.datastructures import ImmutableMultiDict
import requests
import json

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
    if '?' in request.args.get('next'):
      what = request.args.get('next')
      split = what.split('?')
      request.args = {
              "next": split[0]
              }
      for x in split[1].split('&'):
        y = x.split('=')
        request.args[y[0]]=y[1]
      session['wtf'] = request.args
    return redirect(request.args["next"] or "/home")
  return render_template('users/login.html', form=form)

@mod.route('/home', methods=('GET', 'POST'))
@login_required
def home():
  if request.method == 'POST':
    g.user.redirect_target = request.form['redirect_target']
    g.user.redirect_endpoint = request.form['redirect_endpoint']
    g.user.failure_target = request.form['failure_target']
    db.session.commit()
  user = db.session.query(User).filter_by(id=session['user_id']).first()
  return render_template('users/home.html', user=user)

@mod.route('/pay')
@login_required
def pay():
  username = request.args['username']
  auth_token = request.args['auth_token']
  user = db.session.query(User).filter_by(id=session['user_id']).first()
  other = db.session.query(User).filter_by(username=username, authToken=auth_token).first()
  price = request.args['price']
  return render_template('/users/pay.html', user=user, merchant=other, price=price)

@mod.route('/gift', methods=('GET', 'POST'))
@login_required
def gift():
  username = session['wtf']['username']
  auth_token = session['wtf']['auth_token']
  user = db.session.query(User).filter_by(id=session['user_id']).first()
  other = db.session.query(User).filter_by(username=username).first()
  price = session['wtf']['price']
  if request.method == 'POST':
    # user extend trust
    url = 'https://live.stellar.org:9002'
    headers = {'content-type': 'application/json'}
    payload = {
        "method": "submit",
        "params": [
            {
                "secret": user.secret,
                "tx_json": {
                    "Account": user.address,
                    "LimitAmount": {
                        "currency": "AST",
                        "issuer": other.address,
                        "value": price
                        },
                    "TransactionType": "TrustSet"
                    }
                }
            ]
        }
    r1 = requests.post(url, data=json.dumps(payload), headers=headers)
    print r1.content
    if json.loads(r1.content)["result"]["status"] == "error":
      return redirect(other.failure_target, code=302)
    # merchant issue credit
    url = 'https://live.stellar.org:9002'
    headers = {'content-type': 'application/json'}
    payload = {
        "method": "submit",
        "params": [
            {
                "secret": other.secret,
                "tx_json": {
                    "Account": other.address,
                    "Amount": {
                        "currency": "AST",
                        "issuer": other.address,
                        "value": price
                        },
                    "Destination": user.address,
                    "TransactionType": "Payment"
                    }
                }
            ]
        }
    r2 = requests.post(url, data=json.dumps(payload), headers=headers)
    if json.loads(r2.content)["result"]["status"] == "error":
      return redirect(other.failure_target, code=302)
    print r1.content
    return redirect(other.redirect_target, code=302)

  return render_template('/users/gift.html', user=user, merchant=other, price=price)

@mod.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index'))
