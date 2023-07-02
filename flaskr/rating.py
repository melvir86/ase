from flask import Blueprint, render_template
from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('rating', __name__)

@bp.route('/driver_rating')
@login_required
def driver_rating():
    #random data for demonstration
    num_ratings = 8
    average_rating = 5.9
    excellent_count = 0
    good_count = 4
    fair_count = 1
    poor_count = 2
    very_poor_count = 1

    return render_template('rating/driver_rating.html', num_ratings=num_ratings, average_rating=average_rating,
                           excellent_count=excellent_count, good_count=good_count, fair_count=fair_count,
                           poor_count=poor_count, very_poor_count=very_poor_count)

