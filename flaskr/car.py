from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('car', __name__)

@bp.route('/listCarDetails')
def listCarDetails():
    db = get_db()
    cars = db.execute(
        'SELECT * FROM car WHERE user_id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('car/list.html', cars=cars)