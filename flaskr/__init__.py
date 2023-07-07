import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app

    from . import auth
    app.register_blueprint(auth.bp)

    from . import card
    app.register_blueprint(card.bp)

    from . import feedback
    app.register_blueprint(feedback.bp)

    from . import booking
    app.register_blueprint(booking.bp)

    from . import job
    app.register_blueprint(job.bp)

    from . import book
    app.register_blueprint(book.bp)

    from . import provider
    app.register_blueprint(provider.bp)
    

    from . import car
    app.register_blueprint(car.bp)

    from . import rating
    app.register_blueprint(rating.bp)

    app.add_url_rule("/", endpoint="index")

    return app