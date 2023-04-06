from datetime import datetime
import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, json
from flask.cli import load_dotenv
from flask_mail import Mail, Message
from config import Config

pages = Blueprint("pages", __name__, template_folder="templates", static_folder="static")

current_year = datetime.now().year

load_dotenv()
mail = Mail()


@pages.context_processor
def inject_current_year():
    return {"year": current_year, "date_of_birth": 1987, "recaptcha_site_key": Config.RECAPTCHA_PUBLIC_KEY,
            "recaptcha_secret_key": Config.RECAPTCHA_PRIVATE_KEY}


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/portfolio")
def portfolio_details():
    return render_template("portfolio-details.html")


@pages.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Sending mail notification
        msg = Message(subject, recipients=[Config.MAIL_USERNAME])
        msg.body = f"Subject:New Message!\n\nName: {name}\nEmail: {email}\nMessage: {message}"

        try:
            mail.send(msg)
            return jsonify({"success": True}), 200
        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "errors": ["An error occurred while sending the message. Please try "
                                                         "again later."]}), 404

### I can use Flask and flash messages in Html to make recaptcha with python using google recaptcha api for python
# recaptcha_response = request.form.get("g-recaptcha-response")
#
# # Verify reCAPTCHA response
# data = {
#     "secret": Config.RECAPTCHA_PRIVATE_KEY,
#     "response": recaptcha_response
# }
#
# response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
# result = json.loads(response.text)
#
# if not result["success"]:
#     # Log invalid attempts
#     status = "Sorry ! Please Check Im not a robot."
#     flash(status)
#     return jsonify({"success": False, "errors": ["Invalid reCAPTCHA response"]})
