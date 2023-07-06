from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('rating', __name__)

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

    #random data for demonstration
    num_ratings = 8
    average_rating = 5.9
    excellent_count = 0
    good_count = 4
    fair_count = 1
    poor_count = 2
    very_poor_count = 1

    return render_template('rating/driver_rating.html', num_ratings=num_ratings, average_rating=average_rating,
                           excellent_count=excellent_count, good_count=good_count, fair_count=fair_count,
                           poor_count=poor_count, very_poor_count=very_poor_count, rating = rating[0]["rating"])

