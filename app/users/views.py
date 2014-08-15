from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm
from app.users.models import User
from app.gift_cards.models import GiftCard
from werkzeug.datastructures import ImmutableMultiDict
import requests
import json
import urllib

mod = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@mod.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        if not form.user.is_new():
            flash("Logged in successfully.")
        if len(request.args.items())!=0:
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
            return redirect(request.args["next"] or url_for('users.home'))
        return redirect(url_for('users.home'))
    return render_template('users/login.html', form=form)

@mod.route('/endpoints/', methods=['POST'])
@login_required
def endpoints():
    if request.form['isWalkthrough'] == "true":
        if (not request.form['redirect_target']) or (not request.form['redirect_endpoint']) or (not request.form['failure_target']):
            return 'missing_fields', 406
        g.user.redirect_target = request.form['redirect_target']
        g.user.redirect_endpoint = request.form['redirect_endpoint']
        g.user.failure_target = request.form['failure_target']
        db.session.commit()
        return "OK", 200
    else:
        if (not request.form['redirect_target']) or (not request.form['redirect_endpoint']) or (not request.form['failure_target']):
            flash('Missing some endpoints!')
            return redirect(url_for('users.home'))
        g.user.redirect_target = request.form['redirect_target']
        g.user.redirect_endpoint = request.form['redirect_endpoint']
        g.user.failure_target = request.form['failure_target']
        db.session.commit()
        flash("Endpoints updated!")
        return redirect(url_for('users.home'))


@mod.route('/make_active/', methods=['POST'])
@login_required
def make_active():
    g.user.status = "ACTIVE"
    db.session.commit()
    return "OK"

@mod.route('/home/', methods=('GET', 'POST'))
@login_required
def home():
    user = db.session.query(User).filter_by(id=session['user_id']).first()
    if user.is_new():
        return render_template('users/walkthrough.html', user=user)
    else:
        return render_template('users/home.html', user=user)

@mod.route('/docs/', methods=['GET'])
def docs():
    return render_template('doc.html')

@mod.route('/pay/', methods=('GET',"POST"))
@login_required
def pay():
    try:
        auth_token = urllib.unquote(session['wtf']['auth_token']).decode('utf8')
        price = session['wtf']['price']
    except:
        auth_token = urllib.unquote(request.args.get('auth_token')).decode('utf8')
        price = request.args.get('price')
    user = db.session.query(User).filter_by(id=session['user_id']).first()
    other = db.session.query(User).filter_by(authToken=auth_token).first()
    if request.method == 'POST':
        # # gateway extend trust?
        # url = 'https://live.stellar.org:9002'
        # headers = {'content-type': 'application/json'}
        # payload = {
        #           "method": "submit",
        #           "params": [
        #                   {
        #                           "secret": other.secret,
        #                           "tx_json": {
        #                                   "Account": other.address,
        #                                   "LimitAmount": {
        #                                           "currency": "AST",
        #                                           "issuer": other.address,
        #                                           "value": price
        #                                           },
        #                                   "TransactionType": "TrustSet"
        #                                   }
        #                           }
        #                   ]
        #           }
        # r1 = requests.post(url, data=json.dumps(payload), headers=headers)
        # print r1.content
        # if json.loads(r1.content)["result"]["status"] == "error":
        #       return redirect(other.failure_target, code=302)
        # customer pay
        url = 'https://live.stellar.org:9002'
        headers = {'content-type': 'application/json'}
        payload = {
            "method": "submit",
            "params": [{
                "secret": user.secret,
                "tx_json": {
                    "Account": user.address,
                    "Amount": {
                        "currency": "AST",
                        "issuer": other.address,
                        "value": price
                        },
                    "Destination": other.address,
                    "TransactionType": "Payment"
                }
            }]
        }
        r2 = requests.post(url, data=json.dumps(payload), headers=headers)
        if json.loads(r2.content)["result"]["status"] == "error":
            return redirect(other.failure_target, code=302)
        print r2.content
        return redirect(other.redirect_endpoint, code=302)

    return render_template('/users/pay.html', user=user, merchant=other, price=price)

@mod.route('/gift/', methods=('GET', 'POST'))
@login_required
def gift():
    try:
        auth_token = urllib.unquote(session['wtf']['auth_token']).decode('utf8')
        gcid = session['wtf']['gcid']
    except:
        auth_token = urllib.unquote(request.args.get('auth_token')).decode('utf8')
        gcid = request.args.get('gcid')
    user = db.session.query(User).filter_by(id=session['user_id']).first()
    other = db.session.query(User).filter_by(authToken=auth_token).first()
    gc = db.session.query(GiftCard).filter_by(id=gcid).first()
    if request.method == 'POST':
        # user extend trust
        url = 'https://live.stellar.org:9002'
        headers = {'content-type': 'application/json'}
        payload = {
            "method": "submit",
            "params": [{
                "secret": user.secret,
                "tx_json": {
                    "Account": user.address,
                    "LimitAmount": {
                            "currency": "AST",
                            "issuer": other.address,
                            "value": 10000
                            },
                    "TransactionType": "TrustSet"
                }
            }]
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
            "params": [{
                "secret": other.secret,
                "tx_json": {
                    "Account": other.address,
                    "Amount": {
                        "currency": "AST",
                        "issuer": other.address,
                        "value": gc.credit
                    },
                    "Destination": user.address,
                    "TransactionType": "Payment"
                }
            }]
        }
        r2 = requests.post(url, data=json.dumps(payload), headers=headers)
        if json.loads(r2.content)["result"]["status"] == "error":
            return redirect(other.failure_target, code=302)
        print r2.content
        return redirect(other.redirect_target, code=302)

    return render_template('/users/gift.html', user=user, merchant=other, gc=gc)

@mod.route('/logout/')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index'))
