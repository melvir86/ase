from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('feedback', __name__)

@bp.route('/')
def index():
    return render_template('card/index.html')

@bp.route('/listFeedback')
def listFeedback():
    db = get_db()
    feedbacks = db.execute(
        'SELECT *'
        ' FROM feedback f JOIN user u ON f.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('feedback/list.html', feedbacks=feedbacks)

@bp.route('/createFeedback', methods=('GET', 'POST'))
@login_required
def createFeedback():
    if request.method == 'POST':
        description = request.form['description']
        feedback = request.form['feedback']
        error = None

        if not description:
            error = 'Description is required.'
        if not feedback:
            error = 'Feedback is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO feedback (user_id, description, feedback)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], description, feedback)
            )
            db.commit()
            return redirect(url_for('feedback.listFeedback'))

    return render_template('feedback/create.html')

def get_card(id, check_author=True):
    post = get_db().execute(
        'SELECT *'
        ' FROM card c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Card id {id} doesn't exist.")

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return post

def get_feedback(id, check_author=True):
    feedback = get_db().execute(
        'SELECT *'
        ' FROM feedback f JOIN user u ON f.user_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

    if feedback is None:
        abort(404, f"Feedback id {id} doesn't exist.")

    if check_author and feedback['user_id'] != g.user['id']:
        abort(403)

    return feedback

@bp.route('/<int:id>/updateFeedback', methods=('GET', 'POST'))
@login_required
def updateFeedback(id):
    feedback = get_feedback(id)

    if request.method == 'POST':
        description = request.form['description']
        feedback = request.form['feedback']
        error = None

        if not description:
            error = 'Description is required.'
        if not feedback:
            error = 'Feedback is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE feedback SET description = ?, feedback = ?'
                ' WHERE id = ?',
                (description, feedback, id)
            )
            db.commit()
            return redirect(url_for('feedback.listFeedback'))

    return render_template('feedback/update.html', feedback=feedback)

@bp.route('/<int:id>/deleteFeedback', methods=('POST',))
@login_required
def deleteFeedback(id):
    get_feedback(id)
    db = get_db()
    db.execute('DELETE FROM feedback WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('feedback.listFeedback'))