from flask_wtf import FlaskForm, RecaptchaField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    recaptcha = RecaptchaField(validators=[DataRequired()])
