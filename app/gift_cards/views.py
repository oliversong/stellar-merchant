from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.users.models import User
from app.gift_cards.models import GiftCard
import requests
import json

mod = Blueprint('gift_cards', __name__)

@mod.route('/card/', methods=['POST', 'DELETE', 'PUT'])
@login_required
def newCard():
    if request.method == 'POST':
        new_card_name = request.form['cardName']
        new_card_cost = request.form['cardCost']
        new_card_credit = request.form['cardCredit']
        gc = GiftCard(new_card_name, new_card_cost, new_card_credit)
        g.user.gift_cards.append(gc)
        db.session.commit()
        return redirect(url_for('users.home'))
    elif request.method == 'DELETE':
        gc = db.session.query(GiftCard).filter(GiftCard.id == request.form['id']).first()
        db.session.delete(gc)
        db.session.commit()
        return 'OK'
    else: #PUT
        gc = db.session.query(GiftCard).filter(GiftCard.id == request.form['id']).first()
        gc.name = request.form['cardName']
        gc.cost = request.form['cardCost']
        gc.credit = request.form['cardCredit']
        db.session.commit()
        return 'OK'
