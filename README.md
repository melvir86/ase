# ase
This is a shared code repository for Group 3's Applied Software Engineering (ASE) project

[For instructors & testers - how to run our program]

# For Phase-Three of project
# Setting up dependencies for Codio
1. pip3.11 install flask
2. pip3.11 install pipenv
3. pip3.11 install --upgrade urllib3
4. pip3.11 install --upgrade urllib3 chardet
5. pip3.11 install requests==2.26.0
6. pip3.11 install geopy
7. pip3.11 install folium
8. pip3.11 install numpy --upgrade



# Avoiding possible conflicts
9. Delete existing database.db file on application/flaskr folder if it already exists prior to moving on

# Starting our application
10. Go to root folder directory --> cd ase
11. flask --app flaskr run --debug --host=0.0.0.0
12. Access it from your browser at https://[codio-domainname1]-[codio-domainname2]-5000.codio-box.uk/

# Logic for Booking car
Basic changes required from Phase 2 to Phase 3
1. Update Car table to contain current lat & long
2. Create new Booking table that will contain all booking requests (id, user_id, car_id, source, destination, status, created_date)
3. Change book button function to insert into Booking table
4. 'View Booking Requests' page for drivers to Accept or Ignore requests (only show those +- 5 lat/long from their current location)
5. Accepted requests get added into the Booking table
6. Create more sample data for users and cars

Booked Status -> Booked (no driver yet), Booking Accepted (accepted by driver), Started, Completed

When driver gets to customer
1. Update booking status to Started

'Simulate button'
1. Update booking status to Completed
2. Update car table for the driver's car lat and long to be destination's lat and long
3. Trigger refresh the page

To pull ase-backend
'git clone https://github.com/melvir86/ase-backend.git'
