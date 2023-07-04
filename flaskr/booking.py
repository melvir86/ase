from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

bp = Blueprint('booking', __name__)

# CHANGE THE BELOW BASED ON YOUR OWN CODIO SUBDOMAIN FOR APPLICATION TO WORK CORRECTLY
CODIO_SUBDOMAIN_ENDPOINT = 'https://platemessage-jargoncannon-8080.codio-box.uk/api'

@bp.route('/listBooking')
def listBooking():
    db = get_db()
    bookings = db.execute(
        'SELECT *'
        ' FROM booking b '
        ' JOIN user u ON b.user_id = u.id'
        ' JOIN car c ON b.car_id = c.id'
        ' WHERE b.user_id = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('booking/list.html', bookings=bookings)
  
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