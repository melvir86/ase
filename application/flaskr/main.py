from flask import Flask, render_template
from sqlmodel import Session, select, create_engine
from collections.abc import Mapping
import sqlmodel
import folium
from cars import Car

app = Flask(__name__)

@app.route('/')
def fetch_map():
    # Create a map object using Folium
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)  # London coordinates

    # Create the engine
    engine = create_engine("sqlite:///database.db")

    # Fetch car data from the SQLite database
    with Session(engine) as sess:
        statement = select(Car)
        results = sess.exec(statement).all()

    # Png path of the car provided on moodle    

    iconpath = 'https://apollo-media.codio.co.uk/media%2F1%2F9a9ed3e3e1ee96baf9da3e47d4570c5c-0e41f5b92e883928.webp'

    # Add markers for every car on the map 
    for car in results:
        folium.Marker(
            location=[car.latitude, car.longitude],
            icon=folium.CustomIcon(iconpath, icon_size=(50, 30)),
            popup=f"Vehicle ID: {car.vehicleId}<br>Place: {car.place}"
        ).add_to(map)

    # Save the map to an HTML file
    map.save('templates/map.html')

    # Render the template that displays the map
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
