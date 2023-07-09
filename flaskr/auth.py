import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

import hashlib

import requests

from flaskr.properties import codio_subdomain_endpoint as CODIO_SUBDOMAIN_ENDPOINT

bp = Blueprint('auth', __name__, url_prefix='/auth')
#Function that takes the from input as payloads to pass it to the user table.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/register"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        error = None

        payload = {
                "username": username,
                "password": password,
                "role": role,
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 201:
            # Successful response
            users = response.json()
            return redirect(url_for("auth.login"))
        else:
            flash(f"User {username} is already registered.")
            return redirect(url_for("auth.register"))

    return render_template('auth/register.html')
#function that checks the validity of the login credentials.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/login"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        error = None

        payload = {
                "username": username,
                "password": password,
                "role": role,
        }

        response = requests.post(api_endpoint, json=payload)

        if response.status_code == 200:
            # Successful response
            user = response.json()
            if user:
                session.clear()
                session['user_id'] = user[0]['id']
                session['role'] = user[0]['role']
                return redirect(url_for('index'))
            else:
                flash(f"No match of user with selected role. Please try again.")
        else:
            flash(f"No match of user with selected role. Please try again.")

    return render_template('auth/login.html')
#Logs the user out .
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
# It adds a layer of authentication by checking if a user is logged in before allowing access to the view. If the user is not logged in (g.user is None), the function redirects the user to the login page. If the user is logged in, the original view function is executed.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
#this function ,If the request is successful (status code 200), the user's data is stored in the global g object as g.user. If the user is not logged in (user_id is None), g.user is set to None.


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        api_endpoint = CODIO_SUBDOMAIN_ENDPOINT + "/" + str(user_id) + "/loadUser"

        response = requests.post(api_endpoint)
        if response.status_code == 200:
            # Successful response
            g.user = response.json()[0]