from datetime import datetime
import requests
from flask import Blueprint, render_template, request, jsonify, abort, send_from_directory, current_app
from flask.cli import load_dotenv
from flask_mail import Mail, Message
from werkzeug.middleware.proxy_fix import ProxyFix
from my_portfolio import mongo
from my_portfolio.config import Config
from my_portfolio.projects.projects import projects
from my_portfolio.models import Visitor

pages = Blueprint("pages", __name__, template_folder="templates", static_folder="static")

current_year = datetime.now().year

load_dotenv()
mail = Mail()

current_app.wsgi_app = ProxyFix(current_app.wsgi_app, x_for=1, x_proto=1, x_host=1)


@pages.context_processor
def inject_current_year():
    """use global constants in jinja (don't need to inject each one for every template)"""
    return {"year": current_year, "date_of_birth": 1987, "recaptcha_site_key": Config.RECAPTCHA_PUBLIC_KEY,
            "recaptcha_secret_key": Config.RECAPTCHA_PRIVATE_KEY}


@pages.route("/")
def index():

    # ip_address = "41.227.76.44"
    try:
        ip_address = request.remote_addr
        response = requests.get(f'http://api.ipstack.com/{ip_address}?access_key={Config.ACCESS_KEY}')
        data = response.json()
        country = data['country_name']
        city = data['city']
        message = f"A person with {ip_address} from {city}-{country} has visited your website."
    except Exception as e:
        print(f"Error tracking IP address: {str(e)}")
        country = "Unknown"
        city = "Unknown"
        message = f"A person with IP address {ip_address} has visited your website, but their location could not be " \
                  f"determined."

    # Create a new Visitor object and insert it into the database
    visitor = Visitor(ip_address=ip_address, city=city, country=country, message=message)
    # Sending mail notification
    subject = "Someone has consulted your home website"
    msg = Message(subject, recipients=[Config.MAIL_USERNAME])
    msg.body = f"Subject: New Message: {message}!"
    try:
        mail.send(msg)
        mongo.db.visitors.insert_one(visitor.to_dict())
    except Exception as e:
        print(str(e))

    return render_template("index.html")


@pages.route("/portfolio/<int:i>")
def portfolio_details(i):
    """returns each HTML page according to the desired project number i"""
    if i - 1 not in range(len(projects)):
        abort(404)
    return render_template("portfolio-details.html", project=projects[i - 1])


@pages.route('/resume')
def resume():
    return render_template("resume.html")


@pages.route('/resume/Heni Bouafia-fr')
def download():
    """ download the resume from the directory"""
    try:
        ip_address = request.remote_addr

        # ip_address = "41.227.76.44"
        response = requests.get(f'http://api.ipstack.com/{ip_address}?access_key={Config.ACCESS_KEY}')
        data = response.json()
        country = data['country_name']
        city = data['city']
        message = f"A person with {ip_address} from {city}-{country} has Downloaded french resume"

        # Create a new Visitor object and insert it into the database
        visitor = Visitor(ip_address=ip_address, city=city, country=country, message=message)
        # Sending mail notification
        subject = "Someone has Consulted your French resume"
        msg = Message(subject, recipients=[Config.MAIL_USERNAME])
        msg.body = f"Subject: New Message: {message}!"
        mail.send(msg)
        mongo.db.visitors.insert_one(visitor.to_dict())
    except Exception as e:
        print(str(e))

    return send_from_directory(directory="static", path="files/Resume-Heni Bouafia-fr.pdf", as_attachment=False)


@pages.route('/resume/download-en')
def download_en_resume():
    """ download the resume from the directory"""
    try:
        ip_address = request.remote_addr

        # ip_address = "41.227.76.44"
        response = requests.get(f'http://api.ipstack.com/{ip_address}?access_key={Config.ACCESS_KEY}')
        data = response.json()
        country = data['country_name']
        city = data['city']
        message = f"A person with {ip_address} from {city}-{country} has Downloaded french resume"

        # Create a new Visitor object and insert it into the database
        visitor = Visitor(ip_address=ip_address, city=city, country=country, message=message)
        # Sending mail notification
        subject = "Someone has Consulted your English resume"
        msg = Message(subject, recipients=[Config.MAIL_USERNAME])
        msg.body = f"Subject: New Message: {message}!"
        mail.send(msg)
        mongo.db.visitors.insert_one(visitor.to_dict())
    except Exception as e:
        print(str(e))

    return send_from_directory(directory="static", path="files/Resume-Heni Bouafia-en.pdf", as_attachment=False)


@pages.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message_body = request.form.get("message")

        try:
            ip_address = request.remote_addr
            response = requests.get(f'http://api.ipstack.com/{ip_address}?access_key={Config.ACCESS_KEY}')
            data = response.json()
            country = data['country_name']
            city = data['city']
            message = f"A person with {ip_address} from {city}-{country} has sent you a message!"
        except Exception as e:
            print(str(e))
            country = None
            city = None
            message = f"A person with {ip_address} has sent you a message, but their location could not be determined."

        # Create a new Visitor object and insert it into the database
        visitor = Visitor(ip_address=ip_address, city=city, country=country, message=message)

        # Sending mail notification
        msg = Message(subject, recipients=[Config.MAIL_USERNAME])
        msg.body = f"Subject: New Message: {message}!\n\nName: {name}\nEmail: {email}\nMessage: {message_body}"

        try:
            mail.send(msg)
            mongo.db.visitors.insert_one(visitor.to_dict())
            return jsonify({"success": True}), 200
        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "errors": ["An error occurred while sending the message. Please try "
                                                         "again later."]}), 404
