from flask import Flask, render_template, request, jsonify,session
import folium
import requests
from geopy.geocoders import Nominatim

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from time import sleep

app = Flask(__name__)


CAR_API_ENDPOINT = 'https://localhost-8090.codio-box.uk/api/book'
#CAR_POSITION= 'http://biscuitinfo-controlgate-8090.codio-box.uk/api/status'

CAR_API_TRACK= 'http://aliaspelican-chiefprogram-8090.codio-box.uk/api/tick'
CAR_POSITION= 'https://natashaepisode-airlinelogic-8080.codio-box.uk/api/showCars'

bp = Blueprint('book', __name__)

# CHANGE THE BELOW BASED ON YOUR OWN CODIO SUBDOMAIN FOR APPLICATION TO WORK CORRECTLY
CODIO_SUBDOMAIN_ENDPOINT = 'https://platemessage-jargoncannon-8080.codio-box.uk/api'

@bp.route('/show_map')
def show_map():
    # Create a map object
    #map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    map = folium.Map(location=[0, 0], zoom_start=2)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/showCars"
    #session['booking_success'] = 'False' 
    response = requests.get(api_endpoint)
    if response.status_code == 200:
      cars = response.json()
      for car in cars:
          latitude = car.get('pos_x')
          longitude = car.get('pos_y')
          car_id = car.get('id')
          icon_path = 'https://www.clipartmax.com/png/middle/196-1961098_car-navigation-maps-for-lovers-of-long-distance-road-google-map-car.png'  
          icon = folium.CustomIcon(icon_image=icon_path, icon_size=(25, 25)) 
          folium.Marker(
              location=[latitude, longitude],
              popup=f"Car ID is : {car_id}",
              icon=icon
          ).add_to(map)
    booking_success = request.args.get('booking_success', 'False')     
    return render_template('book/map.html', map=map._repr_html_(), booking_success=booking_success)


@bp.route('/book_car', methods=['POST'])
def book_car():
    if request.method == 'POST':
        current_location = request.form.get('current_location')
        destination = request.form.get('destination')

        geolocator = Nominatim(user_agent="MyApp")

        location = geolocator.geocode(current_location)
        final_destination = geolocator.geocode(destination)

        api_endpoint = "http://localhost:8090/api/book"
        payload = {
            "source": {
                "x": location.latitude,
                "y": location.longitude
            },
            "destination": {
                "x": final_destination.latitude,
                "y": final_destination.longitude
            }
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 200:
            # Successful response
            data = response.json()
            car_id = data.get("car_id")
            total_time = data.get("total_time")
            session['booking_success'] = True
            session['car_id'] = car_id
            session['location.latitude'] = round(location.latitude)
            session['location.longitude'] = round(location.longitude)
            flash(f"Car booked ! :) Car ID: {car_id}, Total Time: {total_time}")
            
            return redirect(url_for('book.show_map', booking_success='True'))


        else:
            # Error response
            flash("Failed to book a car.")
            session['booking_success'] = 'False'
            return redirect(url_for('book.show_map', booking_success='False'))


    return "Invalid request method"

@bp.route('/bookcar', methods=('GET', 'POST'))
@login_required
def bookcar():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/bookcar"
    if request.method == 'POST':
        source = request.form.get('current_location')
        destination = request.form.get('destination')

        geolocator = Nominatim(user_agent="MyApp")
        
        payload = {
                "uid": g.user['id'],
                "source": source,
                "destination": destination,
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 200:
            # Successful response
            booking = response.json()
            print("Booking json ", booking[0]["status"])

            if booking[0]["status"] == "Booked":
                flash("Booked successfully. Waiting for driver to accept bro...")
                session['source'] = source
                session['destination'] = destination
                session['booking_success'] = 'True'

            return redirect(url_for('book.show_map'))

    return render_template('book/map.html')

@bp.route('/track_car', methods=['POST'])
def track_car():
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=0)
    session['booking_success'] = 'True' 
    

  #while loop calling the tick api
  #we keep checking if car ID position (lat, long) == current_location x and y
  #refresh the page to keep showing the car movement towards customer
    if request.method == 'POST':

        api_endpoint = "http://localhost:8090/api/tick"

        response = requests.post(CAR_API_TRACK)
        print("Showing the response format: ")
        data = response.json()
        status = data.get("status")
        print(status)
        customer_latitude = session['location.latitude']
        customer_longitude = session['location.latitude']

        if response.status_code == 200:
          car_pos = response.json().get('status', [])

          for car in car_pos:
            if (car.get('id') == session['car_id']):
              currentPosition = car.get('currentPosition', {})
              latitude = currentPosition.get('x')
              longitude = currentPosition.get('y')
              while latitude != customer_latitude:
                sleep(1)
                response2 = requests.post(CAR_API_TRACK)
                car_pos2 = response2.json().get('status', [])
                for car2 in car_pos2:
                  if (car2.get('id') == session['car_id']):
                    currentPosition2 = car2.get('currentPosition', {})
                    latitude = currentPosition2.get('x')
                    longitude = currentPosition.get('y')

          return redirect(url_for('book.show_map', booking_success='False'))

    return "Invalid request method"

@bp.route('/check_booking', methods=['POST'])
def check_booking():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/checkBooking"
    bookings = ""
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # booking response
        bookings = response.json()

        if bookings[0]["status"] == "Accepted by Driver":
            flash("Your booking has been accepted by a Driver. The Car details are as follow: XXX")
            session['booking_success'] = 'True'
            session['booking_id'] = bookings[0]["id"]
            session['car_id'] = bookings[0]["car_id"]

            return redirect(url_for('book.show_map'))

        elif bookings[0]["status"] == "Booked":
            flash("Still waiting for a Driver bro...")
            session['booking_success'] = 'True'

            return redirect(url_for('book.show_map'))

    return render_template('book/map.html')

@bp.route('/start_booking', methods=['POST'])
def start_booking():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/startBooking"
    # Get current location string from the form
    #current_location = request.form.get('current_location')
    current_location = session['source']
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(current_location)
    print("Current location is ", location.latitude, location.longitude)
    
    payload = {'source_x': int(location.latitude), 'source_y': int(location.longitude), 'car_id': session['car_id'], 'booking_id': session['booking_id']}
    response = requests.post(api_endpoint, json=payload)

    if response.status_code == 200:
        flash("Driver has arrived at your location which is XXX. Ride has started!")
        return redirect(url_for('book.show_map'))
    else:
        flash("Failed to update car's position")
        return redirect(url_for('book.show_map'))
    
@bp.route('/complete_booking', methods=['POST'])
def complete_booking():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/completeBooking"
    # Get current location string from the form
    #destination = request.form.get('destination')
    destination = session['destination']
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(destination)
    print("Destination is ", location.latitude, location.longitude)
    
    payload = {'destination_x': int(location.latitude), 'destination_y': int(location.longitude), 'car_id': session['car_id'], 'booking_id': session['booking_id']}
    response = requests.post(api_endpoint, json=payload)

    if response.status_code == 200:
        flash("Your ride has completed successfuly at your location which is XXX. Pls rate your driver!")
        return redirect(url_for('book.show_map'))
    else:
        flash("Failed to update car's position")
        return redirect(url_for('book.show_map'))
if __name__ == '__main__':
    app.run(debug=True)


