# ase
This is a shared code repository for Group 3's Applied Software Engineering (ASE) project

[For instructors & testers - how to run our program]

# For Phase-Three of project
# Setting up dependencies for Codio (if you're testing on any of own existing Codio environments that are already set up and working, you can skip this step and move to Starting our application step)
1. pip3.11 install flask
2. pip3.11 install pipenv
3. pip3.11 install --upgrade urllib3
4. pip3.11 install --upgrade urllib3 chardet
5. pip3.11 install requests==2.26.0
6. pip3.11 install geopy
7. pip3.11 install folium
8. pip3.11 install numpy --upgrade

# Starting our application
10. Go to root folder directory --> cd ase
11. Edit flaskr/properties.py to update with the latest codio-subdomain so that it will connect to the backend services correctly <br>
(chgange the value of variable codio_subdomain_endpoint = 'https://codio-domainname1-codio-domainname2-8080.codio-box.uk/api')
12. flask --app flaskr run --debug --host=0.0.0.0
13. Make sure ase-backend is also running (follow steps at https://github.com/melvir86/ase-backend/tree/phase-three)
14. Access ase (frontend) from your browser at https://[codio-domainname1]-[codio-domainname2]-5000.codio-box.uk/
15. You can use the below sample users to try out the flow (you also have the option of registering your own users to try the flow out)
Customer - Mary / Password123 / Customer <br>
Driver - DriverRobert / Password123 / Driver <br>
Provider - Alan / Password123 / Provider
