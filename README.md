# ase
This is a shared code repository for Group 3's Applied Software Engineering (ASE) project

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
=======
# Steps to run our code
1. pip3.11 install module-name flask [If you are using Codio]
2. pip3.11 install pipenv [If you are using Codio]
3. flask --app flaskr run --debug --host=0.0.0.0
4. Access it from your browser at https://[codio-domainname1]-[codio-domainname2]-5000.codio-box.uk/
