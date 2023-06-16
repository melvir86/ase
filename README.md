# ase
This is a shared code repository for Group 3's Applied Software Engineering (ASE) project

[For instructors & testers - how to run our program]

# For Phase-One of project
# Setting up dependencies for Codio
1. pip3.11 install flask
2. pip3.11 install pipenv
3. pip install --upgrade urllib3
4. pip install --upgrade urllib3 chardet
5. pip install requests==2.26.0

# Avoiding possible conflicts
6. Delete existing database.db file on application/flaskr folder if it already exists prior to moving on

# Starting our application
7. Go to folder directory --> cd application/flaskr/
8. flask --app main run --host=0.0.0.0
5. Access it from your browser at https://[codio-domainname1]-[codio-domainname2]-5000.codio-box.uk/

[For our own knowledge - how to run common sqlite & flask commands]
How to run car python file to create database
1. python3.11 car.py

How to access database and tables through sqlite
1. Installing sqlite
   sudo apt-get install sqlite3
   
2. Accessing sqlite
   sqlite3
    
3. Show list of databases
    .databases
    
4. Show list of tables
    .tables
    
5. Show schema of table
    .schema car
    
6. Show data from car table
    select * from car;
