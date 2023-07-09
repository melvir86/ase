from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('rating', __name__)
#List all the cards.
@bp.route('/listCard')
def listCard():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listCard"
    cards = ""
    #g.user['id'] making sure listing the cards of the user.
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        cards = response.json()

    return render_template('card/list.html', cards=cards)
#Driver rating function
@bp.route('/driver_rating')
def driver_rating():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/driverRating"
    rating = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        rating = response.json()
        print("Rating is ", rating[0]["rating"])


    return render_template('rating/driver_rating.html', rating = rating[0]["rating"])

