# ase
This is a shared code repository for Group 3's Applied Software Engineering (ASE) project

[For instructors & testers - how to run our program]

# For Phase-Three of project
# Setting up dependencies for Codio (if you're not testing on any of own existing Codio environments and setting up a new one. if not, you can skip this step)
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
11. flask --app flaskr init-db
12. flask --app flaskr run --debug --host=0.0.0.0
13. Access it from your browser at https://[codio-domainname1]-[codio-domainname2]-5000.codio-box.uk/
