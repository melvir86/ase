from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('job', __name__)
#Listing the job of the exact driver with passing its own login id.

@bp.route('/listJob')
def listJob():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listJob"
    jobs = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        jobs = response.json()

    return render_template('job/list.html', jobs=jobs)