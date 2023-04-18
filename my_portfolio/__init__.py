from flask import Flask
from flask.cli import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_pymongo import PyMongo
from my_portfolio.config import Config

# from flask_pymongo import PyMongo

bootstrap = Bootstrap5()

load_dotenv()

mongo = PyMongo()


# client = MongoClient(Config.MONGO_URI)
# db = client.portfolio_visitors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)

    #  wrap the code that is causing the error in a with app.app_context():
    # LOAD the default db from the URI
    # with app.app_context():
        # app.db = db

    from my_portfolio.errors.handlers import errors
    from my_portfolio.routes.routes import pages, mail
    mongo.init_app(app)
    # initialize the app with the extension mail
    mail.init_app(app)
    app.register_blueprint(pages)
    app.register_blueprint(errors)

    return app
