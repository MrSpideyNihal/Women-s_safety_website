from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])

class EmergencyForm(FlaskForm):
    lat = FloatField('Latitude', validators=[DataRequired()])
    lng = FloatField('Longitude', validators=[DataRequired()])
    description = TextAreaField('Description')
