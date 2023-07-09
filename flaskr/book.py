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

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('book', __name__)
#it takes the api endpoint of cars table from the back end and creates a folium map with the given coords.
@bp.route('/show_map')
def show_map():
    # Create a map object
    #map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    map = folium.Map(location=[0, 0], zoom_start=2)

    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/showCars"
    #session['booking_success'] = 'False' 
    response = requests.get(api_endpoint)
    #if the api call its sucessful it loops over the cars response from the db.
    if response.status_code == 200:
      cars = response.json()
      for car in cars:
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
#pop up windows for each and  every car using folium methods.
          folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            icon=icon
            ).add_to(map)
    booking_success = request.args.get('booking_success', 'False')
    #it saves the map in html format and passes it into the given dir html.     
    return render_template('book/map.html', map=map._repr_html_(), booking_success=booking_success)

#this is phase 2 booking car from your given endpoint.
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
#book car post function calling bookcar api provided on the back-end.
@bp.route('/bookcar', methods=('GET', 'POST'))
@login_required
def bookcar():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/bookcar"
    if request.method == 'POST':
        source = request.form.get('current_location')
        destination = request.form.get('destination')

        geolocator = Nominatim(user_agent="MyApp")
        #Passing as a payload the user id ,source and destination from the html form as their  values.
        payload = {
                "uid": g.user['id'],
                "source": source,
                "destination": destination,
        }

        response = requests.post(api_endpoint, json=payload)
        #waiting for a status 200 from json req,which means that the req is succesful.
        if response.status_code == 200:
            # Successful response
            booking = response.json()
            print("Booking json ", booking[0]["status"])
            #on the booking table if the status is booked it means that the user has Booked and is waiting for the driver response.
            if booking[0]["status"] == "Booked":
                flash("Booked successfully. Waiting for driver to accept...")
                session['source'] = source
                session['destination'] = destination
                session['booking_success'] = 'True'

            return redirect(url_for('book.show_map'))

    return render_template('book/map.html')
#phase 2 track car function.
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
#Checking the booking row from the db if its status has been changed by the driver.
@bp.route('/check_booking', methods=['POST'])
def check_booking():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/checkBooking"
    bookings = ""
    #making sure we check the user booking,not another wrongly user.
    params = {'uid': g.user['id']}

    response = requests.post(api_endpoint, params=params)

    if response.status_code == 200:
        # booking response
        bookings = response.json()
        #check if the api call returns us a status of accepted by the driver.
        if bookings[0]["status"] == "Accepted by Driver":
            flash("Your booking has been accepted by a Driver.")
            session['booking_success'] = 'True'
            session['booking_id'] = bookings[0]["id"]
            session['car_id'] = bookings[0]["car_id"]
            #Getting the details of the Booked Car
            api_endpoint2 = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(bookings[0]["car_id"]) + "/getCarDetails"
            response2 = requests.post(api_endpoint2)
            car = response2.json()
            print("car", car)
            #Flashing the car details only we have a succesful booking.
            message = "The Car details are as follows : " + car[0]["colour"] + " " + car[0]["brand"] + " " + car[0]["model"] + ". The Driver's id (username is masked) is : " + str(car[0]["user_id"]) + "."
            flash(message)

            return redirect(url_for('book.show_map'))
        #if the booking car is still booked,it means that the driver still has not accepted your booking.
        elif bookings[0]["status"] == "Booked":
            flash("Still waiting for a Driver...")
            session['booking_success'] = 'True'

            return redirect(url_for('book.show_map'))

    return render_template('book/map.html')
#when a succesful booking has been done you have to wait for the car to come at your destination.
@bp.route('/start_booking', methods=['POST'])
def start_booking():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/startBooking"
    # Get current location string from the form
    #current_location = request.form.get('current_location')
    current_location = session['source']
    geolocator = Nominatim(user_agent="MyApp")
    #making sure to convert your current location as pos_x and pos_y on the map,with this geolocator library.
    location = geolocator.geocode(current_location)
    print("Current location is ", location.latitude, location.longitude)
    
    payload = {'source_x': int(location.latitude), 'source_y': int(location.longitude), 'car_id': session['car_id'], 'booking_id': session['booking_id']}
    response = requests.post(api_endpoint, json=payload)

    if response.status_code == 200:
        message = "Driver has arrived at your location which is " + current_location + ". Ride has started."
        flash(message)
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
    #Passing as endpoint the location of user,car_id and booking_id.
    payload = {'destination_x': int(location.latitude), 'destination_y': int(location.longitude), 'car_id': session['car_id'], 'booking_id': session['booking_id']}
    response = requests.post(api_endpoint, json=payload)
#CHECK IF THE JSON response is succesful or not an flash the messages.We aim to change the car booked from its own poistion to the user position.
    if response.status_code == 200:
        message = "Your ride has completed successfuly at your destination which is " + destination + ". Pls rate your driver to end the flow!"
        flash(message)
        return redirect(url_for('book.show_map'))
    else:
        flash("Failed to update car's position")
        return redirect(url_for('book.show_map'))
#rate the driver function 
@bp.route('/rate_driver', methods=['POST'])
def rate_driver():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/rateDriver"
    # Get current location string from the form
    rating = request.form.get('rating')
    #send it as a payload to update the table.
    payload = {'rating': rating, 'car_id': session['car_id']}
    response = requests.post(api_endpoint, json=payload)
#check the status what to print on the user side.
    if response.status_code == 200:
        message = "You have rated your Driver successfully with rating of " + rating + ". Thank you for riding with us!"
        flash(message)
        return redirect(url_for('book.show_map'))
    else:
        flash("Failed to update car's position")
        return redirect(url_for('book.show_map'))

if __name__ == '__main__':
    app.run(debug=True)