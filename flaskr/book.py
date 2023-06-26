from flask import Flask, render_template, request, jsonify
import folium
import requests
from geopy.geocoders import Nominatim

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

app = Flask(__name__)

CAR_API_ENDPOINT = 'https://localhost-8090.codio-box.uk/api/book'
CAR_POSITION= 'http://biscuitinfo-controlgate-8090.codio-box.uk/api/status'

bp = Blueprint('book', __name__)

@bp.route('/show_map')
def show_map():
    # Create a map object
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
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
    return render_template('book/map.html', map=map._repr_html_())

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
            flash(f"Car booked ! :) Car ID: {car_id}, Total Time: {total_time}")
            return redirect(url_for('book.show_map'))
        else:
            # Error response
            flash("Failed to book a car.")
            return redirect(url_for('book.show_map'))

    return "Invalid request method"

if __name__ == '__main__':
    app.run(debug=True)


