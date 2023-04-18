from flask import Flask
from flask_bootstrap import Bootstrap5
from flask.cli import load_dotenv
from pymongo import MongoClient
from my_portfolio.config import Config
from my_portfolio.errors.handlers import errors
from my_portfolio.routes.routes import pages, mail

# from flask_pymongo import PyMongo

bootstrap = Bootstrap5()

load_dotenv()


# mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)

    #  wrap the code that is causing the error in a with app.app_context():
    # with app.app_context():
    client = MongoClient(Config.MONGO_URI)
    # LOAD the default db from the URI
    app.db = client.get_default_database()

    # initialize the app with the extension mail
    mail.init_app(app)
    app.register_blueprint(pages)
    app.register_blueprint(errors)

    return app
