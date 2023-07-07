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

@bp.route('/createCar', methods=('GET', 'POST'))
@login_required
def createCar():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/createCar"
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        colour = request.form['colour']
        next_service = request.form['next_service']
        status = request.form['status']
        error = None

        payload = {
                "uid": g.user['id'],
                "brand": brand,
                "model": model,
                "colour": colour,
                "next_service": next_service,
                "status": status,
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 201:
            # Successful response
            cars = response.json()

            return redirect(url_for('car.listCarDetails'))

    return render_template('car/create.html')

def get_car(id, check_author=True):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getCar"
    car = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        car = response.json()

    return car

@bp.route('/<int:id>/updateCar', methods=('GET', 'POST'))
@login_required
def updateCar(id):
    car = get_car(id)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/updateCar"
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        colour = request.form['colour']
        next_service = request.form['next_service']
        status = request.form['status']
        error = None

        payload = {
                "uid": g.user['id'],
                "brand": brand,
                "model": model,
                "colour": colour,
                "next_service": next_service,
                "status": status,
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 200:
            # Successful response
            car = response.json()

            return redirect(url_for('car.listCarDetails'))

    return render_template('car/update.html', car=car[0])

@bp.route('/<int:id>/deleteCar', methods=('POST',))
@login_required
def deleteCar(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/deleteCar"

    response = requests.post(api_endpoint)

    if response.status_code == 200:
        # Successful response
        car = response.json()
    return redirect(url_for('car.listCarDetails'))