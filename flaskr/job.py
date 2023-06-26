from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('job', __name__)

@bp.route('/listJob')
def listJob():
    db = get_db()
    jobs = db.execute(
        'SELECT *'
        ' FROM booking b JOIN car c ON b.car_id = c.id'
        ' WHERE c.user_id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('job/list.html', jobs=jobs)