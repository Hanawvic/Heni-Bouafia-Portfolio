from flask import Flask
from flask_bootstrap import Bootstrap5
from flask.cli import load_dotenv
from my_portfolio.config import Config
from my_portfolio.errors.handlers import errors
from my_portfolio.routes.routes import pages, mail

bootstrap = Bootstrap5()

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)

    # initialize the app with the extension mail
    mail.init_app(app)

    app.register_blueprint(pages)
    app.register_blueprint(errors)

    return app
