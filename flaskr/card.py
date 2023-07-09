from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('card', __name__)

@bp.route('/')
def index():
    return render_template('card/index.html')
#Lisitng the card details but making sure passing the user id to be ceratin we are getting the user card.
@bp.route('/listCard')
def listCard():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listCard"
    cards = ""
    #g.user['id'] user id .
    params = {'uid': g.user['id']}
#Payloading the user id.
    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        cards = response.json()

    return render_template('card/list.html', cards=cards)
#Creating a new card for the user.
@bp.route('/createCard', methods=('GET', 'POST'))
@login_required
def createCard():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/createCard"
    #Taking all the values from the html form of creating a card.
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        cve = request.form['cve']
        description = request.form['description']
        status = request.form['status']
        error = None
#Passing the html values as a payload to the api to update the cards table.
        payload = {
                "uid": g.user['id'],
                "name": request.form['name'],
                "number": request.form['number'],
                "expiry_month": request.form['expiry_month'],
                "expiry_year": request.form['expiry_year'],
                "cve": request.form['cve'],
                "description": request.form['description'],
                "status": request.form['status'],
        }

        response = requests.post(api_endpoint, json=payload)
#Check the status of api response.
        if response.status_code == 201:
            # Successful response
            cards = response.json()

            return redirect(url_for('card.listCard'))

    return render_template('card/create.html')
#Getting the card  info.
def get_card(id, check_author=True):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getCard"
    card = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        card = response.json()

    return card
#Update the cards.We take card_id as filtering to make sure which card are we updating.
@bp.route('/<int:id>/updateCard', methods=('GET', 'POST'))
@login_required
def updateCard(id):
    card = get_card(id)
#query string
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/updateCard"
    #Getting the data from the html form.
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        cve = request.form['cve']
        description = request.form['description']
        status = request.form['status']
        error = None
#Payloading the data.
        payload = {
                "uid": g.user['id'],
                "name": request.form['name'],
                "number": request.form['number'],
                "expiry_month": request.form['expiry_month'],
                "expiry_year": request.form['expiry_year'],
                "cve": request.form['cve'],
                "description": request.form['description'],
                "status": request.form['status'],
        }
#Checking the response.
        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 200:
            # Successful response
            cards = response.json()

            return redirect(url_for('card.listCard'))

    return render_template('card/update.html', card=card[0])
#Delete of the card.Again referencing the ID.
@bp.route('/<int:id>/deleteCard', methods=('POST',))
@login_required
def deleteCard(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/deleteCard"

    response = requests.post(api_endpoint)

    if response.status_code == 200:
        # Successful response
        cards = response.json()
    return redirect(url_for('card.listCard'))