from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('feedback', __name__)

@bp.route('/')
def index():
    return render_template('card/index.html')
#Lisitng the feedback function.

@bp.route('/listFeedback')
def listFeedback():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listFeedback"
    feedbacks = ""
    #g.user['id']
    #Make sure which user has done the feedback.

    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        feedbacks = response.json()

    return render_template('feedback/list.html', feedbacks=feedbacks)
#Same as the function above.

@bp.route('/listAllFeedback')
def listAllFeedback():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listAllFeedback"
    feedbacks = ""

    response = requests.post(api_endpoint)

    if response.status_code == 200:
        # Successful response

        feedbacks = response.json()

    return render_template('feedback/listAll.html', feedbacks=feedbacks)
#Create new feedback.

@bp.route('/createFeedback', methods=('GET', 'POST'))
@login_required
def createFeedback():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/createFeedback"
    if request.method == 'POST':
        #Getting the feedback from the form with 2 values.

        description = request.form['description']
        feedback = request.form['feedback']
        error = None
        #Passing the values as a payload to update the feedback table.

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

#Getting the feedback from the db
def get_feedback(id, check_author=True):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getFeedback"
    feedback = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        feedback = response.json()

    return feedback
#Updating the feedback with feedback_id as filtering.

@bp.route('/<int:id>/updateFeedback', methods=('GET', 'POST'))
@login_required
def updateFeedback(id):
    feedback = get_feedback(id)
#Making sure to update a certain feedback from the table.
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/updateFeedback"
    if request.method == 'POST':
        description = request.form['description']
        feedback_info = request.form['feedback']
        error = None
#Passing the values to api to update the feedback certain row in the db.

        payload = {
                "uid": g.user['id'],
                "description" : request.form['description'],
                "feedback_info" : request.form['feedback'],
        }

        response = requests.post(api_endpoint, json=payload)
#Checking the api response status.

        if response.status_code == 200:
            # Successful response
            feedbacks = response.json()

            return redirect(url_for('feedback.listFeedback'))

    return render_template('feedback/update.html', feedback=feedback[0])
#The same logic as code above but the sql command its not update but DELETE.

@bp.route('/<int:id>/deleteFeedback', methods=('POST',))
@login_required
def deleteFeedback(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/deleteFeedback"

    response = requests.post(api_endpoint)

    if response.status_code == 200:
        # Successful response
        feedbacks = response.json()
    return redirect(url_for('feedback.listFeedback'))