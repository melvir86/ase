from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('car', __name__)

@bp.route('/listCarDetails')
def listCarDetails():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listCarDetails"
    cars = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        cars = response.json()

    return render_template('car/list.html', cars=cars)