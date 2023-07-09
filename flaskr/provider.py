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


from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('provider', __name__)

@bp.route('/show_car')
def show_car():
    # Create a map object
    #map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    map = folium.Map(location=[0, 0], zoom_start=2)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/showCars"
    #session['booking_success'] = 'False'
    #Print all the car db positions. 
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
    flash("Cars are displayed on their position : ")    
    return render_template('car/map.html',map=map._repr_html_())
