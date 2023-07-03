from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import folium
import requests

bp = Blueprint('feedback', __name__)

# CHANGE THE BELOW BASED ON YOUR OWN CODIO SUBDOMAIN FOR APPLICATION TO WORK CORRECTLY
CODIO_SUBDOMAIN_ENDPOINT = 'https://platemessage-jargoncannon-8080.codio-box.uk/api'

@bp.route('/')
def index():
    return render_template('card/index.html')

@bp.route('/listFeedback')
def listFeedback():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listFeedback"
    feedbacks = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        feedbacks = response.json()

    return render_template('feedback/list.html', feedbacks=feedbacks)

@bp.route('/createFeedback', methods=('GET', 'POST'))
@login_required
def createFeedback():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/createFeedback"
    if request.method == 'POST':
        description = request.form['description']
        feedback = request.form['feedback']
        error = None

        payload = {
                "uid": g.user['id'],
                "description" : request.form['description'],
                "feedback" : request.form['feedback'],
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 201:
            # Successful response
            feedbacks = response.json()

            return redirect(url_for('feedback.listFeedback'))

    return render_template('feedback/create.html')

def get_feedback(id, check_author=True):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getFeedback"
    feedback = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        feedback = response.json()

    return feedback

@bp.route('/<int:id>/updateFeedback', methods=('GET', 'POST'))
@login_required
def updateFeedback(id):
    feedback = get_feedback(id)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/updateFeedback"
    if request.method == 'POST':
        description = request.form['description']
        feedback_info = request.form['feedback']
        error = None

        payload = {
                "uid": g.user['id'],
                "description" : request.form['description'],
                "feedback_info" : request.form['feedback'],
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 200:
            # Successful response
            feedbacks = response.json()

            return redirect(url_for('feedback.listFeedback'))

    return render_template('feedback/update.html', feedback=feedback[0])

@bp.route('/<int:id>/deleteFeedback', methods=('POST',))
@login_required
def deleteFeedback(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/deleteFeedback"

    response = requests.post(api_endpoint)

    if response.status_code == 200:
        # Successful response
        feedbacks = response.json()
    return redirect(url_for('feedback.listFeedback'))