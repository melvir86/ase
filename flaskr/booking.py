from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

bp = Blueprint('booking', __name__)

# CHANGE THE BELOW BASED ON YOUR OWN CODIO SUBDOMAIN FOR APPLICATION TO WORK CORRECTLY
CODIO_SUBDOMAIN_ENDPOINT = 'https://natashaepisode-airlinelogic-8080.codio-box.uk/api'

@bp.route('/listBookings')
def listBookings():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listBookings"
    booking_history = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        booking_history = response.json()

    return render_template('booking/listhistory.html', booking_history=booking_history)
  
@bp.route('/listRequests')
def listRequests():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listRequests"
    customer_requests = ""
    #g.user['id']
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        customer_requests = response.json()

    return render_template('booking/listrequests.html', customer_requests=customer_requests)

@bp.route('/<int:id>/acceptJob', methods=('POST',))
@login_required
def acceptJob(id):

    #Get driver's car id first
    car_id = get_car_id(g.user['id'])

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/acceptJob"

    params = {'carid': car_id}

    response = requests.post(api_endpoint, params=params)
    
    if response.status_code == 200:
        # Successful response
        cards = response.json()
    return redirect(url_for('booking.listRequests'))

def get_car_id(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getCarId"
    car_id = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        car_id = response.json()

    return car_id