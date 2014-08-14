from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.users.models import User
from app.gift_cards.models import GiftCard
import requests
import json

mod = Blueprint('gift_cards', __name__)

@mod.route('/newCard/', methods=['POST'])
@login_required
def newCard():
    new_card_name = request.form['cardName']
    new_card_cost = request.form['cardCost']
    new_card_credit = request.form['cardCredit']
    if (not new_card_cost.isdigit()) or (not new_card_credit.isdigit()):
        flash('Cost or credit not a number!')
        return redirect(url_for('users.home'))
    if (not new_card_cost) or (not new_card_credit) or (not new_card_name):
        flash('Card missing fields!')
    gc = GiftCard(new_card_name, new_card_cost, new_card_credit)
    g.user.gift_cards.append(gc)
    db.session.commit()
    flash('Card created.')
    return redirect(url_for('users.home'))

@mod.route('/card/', methods=['POST', 'DELETE', 'PUT'])
@login_required
def card():
    if request.method == 'POST':
        new_card_name = request.form['cardName']
        new_card_cost = request.form['cardCost']
        new_card_credit = request.form['cardCredit']
        if (not new_card_cost.isdigit()) or (not new_card_credit.isdigit()):
            return 'not_number', 406
        if (not new_card_cost) or (not new_card_credit) or (not new_card_name):
            return 'missing_fields', 406
        gc = GiftCard(new_card_name, new_card_cost, new_card_credit)
        g.user.gift_cards.append(gc)
        db.session.commit()
        return str(gc.id), 200
    elif request.method == 'DELETE':
        gc = db.session.query(GiftCard).filter(GiftCard.id == request.form['id']).first()
        db.session.delete(gc)
        db.session.commit()
        return 'OK', 200
    else: #PUT
        new_card_name = request.form['cardName']
        new_card_cost = request.form['cardCost']
        new_card_credit = request.form['cardCredit']
        if (not new_card_cost.isdigit()) or (not new_card_credit.isdigit()):
            return 'not_number', 406
        if (not new_card_cost) or (not new_card_credit) or (not new_card_name):
            return 'missing_fields', 406
        gc = db.session.query(GiftCard).filter(GiftCard.id == request.form['id']).first()
        gc.name = request.form['cardName']
        gc.cost = request.form['cardCost']
        gc.credit = request.form['cardCredit']
        db.session.commit()
        return 'OK'
