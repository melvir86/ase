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
CAR_POSITION= 'http://aliaspelican-chiefprogram-8090.codio-box.uk/api/status'

bp = Blueprint('book', __name__)

@bp.route('/show_map')
def show_map():
    # Create a map object
    #map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    map = folium.Map(location=[0, 0], zoom_start=2)

    session['booking_success'] = 'False' 
    response = requests.get(CAR_POSITION)
    if response.status_code == 200:
      car_pos = response.json().get('status', [])
      for car in car_pos:
          currentPosition = car.get('currentPosition', {})
          latitude = currentPosition.get('x')
          longitude = currentPosition.get('y')
          car_id = car.get('id')
          print (latitude)
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

@bp.route('/track_car', methods=['POST'])
def track_car():
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=0)
    session['booking_success'] = 'True' 
    print(session['booking_success'])

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
                    print(latitude)
                    longitude = currentPosition.get('y')

          return redirect(url_for('book.show_map', booking_success='False'))

    return "Invalid request method"

if __name__ == '__main__':
    app.run(debug=True)


