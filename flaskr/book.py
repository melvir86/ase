from flask import Flask, render_template, request, jsonify
import folium
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

CAR_API_ENDPOINT = 'https://locatecrystal-anitacave-8090.codio-box.uk/api/book'

@app.route('/')
def show_map():
    # Create a map object
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

    # Render the template that displays the map
    return render_template('map.html', map=map._repr_html_())

@app.route('/book_car', methods=['POST'])
def book_car():
    if request.method == 'POST':
        current_location = request.form.get('current_location')
        destination = request.form.get('destination')

       
        geolocator = Nominatim(user_agent="MyApp")

       

        location = geolocator.geocode(current_location)
        final_destination=geolocator.geocode(destination)

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
            return f"Car booked successfully! Car ID: {car_id}, Total Time: {total_time}"
        else:
            # Error response
            return "Failed to book a car."

   


    return "Invalid request method"

if __name__ == '__main__':
    app.run(debug=True)


