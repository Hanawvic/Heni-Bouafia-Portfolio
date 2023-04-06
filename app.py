from flask import Flask
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from config import Config
from routes import pages, mail

bootstrap = Bootstrap5()

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)
    # INIT MONGODB
    # client = MongoClient(os.environ.get("MONGODB_URI"))
    # LOAD the default db from the URI
    # app.db = client.get_default_database()

    # initialize the app with the extension mail
    mail.init_app(app)

    app.register_blueprint(pages)
    return app


if __name__ == "__main__":
    create_app().run(host='localhost', port=5000, debug=True)




