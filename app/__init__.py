"""Flask Hello World App"""

from flask import Flask

from app.home.views import home
from app.chart.views import chart


def create_app():
    """Creates the Flask app."""
    app = Flask(__name__)
    # setup with the configuration provided by the user / environment
    #app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object('app.config.Config')

    # setup all our dependencies
    #database.init_app(app)
    #commands.init_app(app)

    # register blueprint
    app.register_blueprint(home)
    app.register_blueprint(chart)

    return app


if __name__ == "__main__":
    create_app().run()
