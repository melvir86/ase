from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

bp = Blueprint('card', __name__)

# CHANGE THE BELOW BASED ON YOUR OWN CODIO SUBDOMAIN FOR APPLICATION TO WORK CORRECTLY
CODIO_SUBDOMAIN_ENDPOINT = 'https://natashaepisode-airlinelogic-8080.codio-box.uk/api'

@bp.route('/')
def index():
    return render_template('card/index.html')

@bp.route('/listCard')
def listCard():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listCard"
    cards = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        cards = response.json()

    return render_template('card/list.html', cards=cards)

@bp.route('/createCard', methods=('GET', 'POST'))
@login_required
def createCard():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/createCard"
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        cve = request.form['cve']
        description = request.form['description']
        status = request.form['status']
        error = None

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

        if response.status_code == 201:
            # Successful response
            cards = response.json()

            return redirect(url_for('card.listCard'))

    return render_template('card/create.html')

def get_card(id, check_author=True):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getCard"
    card = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        card = response.json()

    return card

@bp.route('/<int:id>/updateCard', methods=('GET', 'POST'))
@login_required
def updateCard(id):
    card = get_card(id)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/updateCard"
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        expiry_month = request.form['expiry_month']
        expiry_year = request.form['expiry_year']
        cve = request.form['cve']
        description = request.form['description']
        status = request.form['status']
        error = None

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

        if response.status_code == 200:
            # Successful response
            cards = response.json()

            return redirect(url_for('card.listCard'))

    return render_template('card/update.html', card=card[0])

@bp.route('/<int:id>/deleteCard', methods=('POST',))
@login_required
def deleteCard(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/deleteCard"

    response = requests.post(api_endpoint)

    if response.status_code == 200:
        # Successful response
        cards = response.json()
    return redirect(url_for('card.listCard'))