from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('car', __name__)
#function of listing the car details.
@bp.route('/listCarDetails')
def listCarDetails():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/listCarDetails"
    cars = ""
    #g.user['id'] making sure which driver has which car.
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # Successful response
        cars = response.json()

    return render_template('car/list.html', cars=cars)
#creating the new cars on a from.
@bp.route('/createCar', methods=('GET', 'POST'))
@login_required
def createCar():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/createCar"
    #getting the car details from the form.
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        colour = request.form['colour']
        next_service = request.form['next_service']
        status = request.form['status']
        error = None
#passing the values with payload from front end to the api to update the car table.
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
#Getting the car data .
def get_car(id, check_author=True):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/getCar"
    car = ""

    response = requests.post(api_endpoint)
    if response.status_code == 200:
        # Successful response
        car = response.json()

    return car
#updating the car data from the db and passing the id parameter as a query string to be sure we are updating. the car details we need.
@bp.route('/<int:id>/updateCar', methods=('GET', 'POST'))
@login_required
def updateCar(id):
    car = get_car(id)
    #Taking all the parameters from the form.
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/updateCar"
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        colour = request.form['colour']
        next_service = request.form['next_service']
        status = request.form['status']
        error = None
    #Passing all the parameters as payload.
        payload = {
                "uid": g.user['id'],
                "brand": brand,
                "model": model,
                "colour": colour,
                "next_service": next_service,
                "status": status,
        }

        response = requests.post(api_endpoint, json=payload)
#Check the response.
        if response.status_code == 200:
            # Successful response
            car = response.json()

            return redirect(url_for('car.listCarDetails'))

    return render_template('car/update.html', car=car[0])
#Deleting a car from the db.Again with query stringing id of the car to not delete a non desirable car.
@bp.route('/<int:id>/deleteCar', methods=('POST',))
@login_required
def deleteCar(id):
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(id) + "/deleteCar"

    response = requests.post(api_endpoint)
#Check check and check.
    if response.status_code == 200:
        # Successful response
        car = response.json()
    return redirect(url_for('car.listCarDetails'))