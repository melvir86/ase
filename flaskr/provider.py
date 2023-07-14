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
    #Map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    
    map = folium.Map(location=[0, 0], zoom_start=2)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/showCars"
    #Session['booking_success'] = 'False'
    #Print all the car db positions. 

    response = requests.get(api_endpoint)
    if response.status_code == 200:
        #Getting all the json response from the cars Db.

          latitude = car.get('pos_x')
          longitude = car.get('pos_y')
          car_id = car.get('id')
          car_model=car.get('model')
          car_brand=car.get('brand')
          car_color=car.get('colour')
          icon_path = 'https://w7.pngwing.com/pngs/733/606/png-transparent-scuderia-ferrari-laferrari-car-formula-1-ferrari-logo-signage-ferrari-thumbnail.png'  
          icon = folium.CustomIcon(icon_image=icon_path, icon_size=(25, 25)) 
          popup_content = f"<div style='font-size: 16px;'><b>{car_color} {car_brand} {car_model}</b></div>" \
               f"<div style='font-size: 14px;'>Car ID: {car_id}</div>"
          #Pop up windows for each and  every car using folium methods.

          folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            icon=icon
            ).add_to(map)
    flash("Cars are displayed on their position : ")    
    return render_template('car/map.html',map=map._repr_html_())
