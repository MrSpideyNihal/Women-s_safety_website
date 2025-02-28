import os
import logging
import pywhatkit as kit
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Emergency, Alert
from forms import LoginForm, RegisterForm, EmergencyForm
from utils import get_nearby_alerts

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Ensure SQLAlchemy Database URI is set
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///default.db")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Updated for SQLAlchemy 2.0


# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    form = EmergencyForm()
    alerts = []
    
    if current_user.is_authenticated:
        alerts = get_nearby_alerts(current_user.lat, current_user.lng)
    
    return render_template('home.html', alerts=alerts, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)

        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            phone=form.phone.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/emergency', methods=['POST'])
@login_required
def emergency():
    form = EmergencyForm()
    if form.validate_on_submit():
        # Update the current user's location with the reported coordinates
        current_user.lat = form.lat.data
        current_user.lng = form.lng.data
        db.session.commit()

        # Create the emergency record
        emergency = Emergency(
            user_id=current_user.id,
            lat=form.lat.data,
            lng=form.lng.data,
            description=form.description.data
        )
        db.session.add(emergency)
        db.session.commit()

        # Create an alert based on the emergency
        alert = Alert(
            emergency_id=emergency.id,
            lat=emergency.lat,
            lng=emergency.lng
        )
        db.session.add(alert)
        db.session.commit()

        # Construct emergency message
        emergency_message = f"\U0001F6A8 Emergency Alert! \U0001F6A8\n" \
                            f"Location: https://www.google.com/maps?q={form.lat.data},{form.lng.data}\n" \
                            f"Description: {form.description.data if form.description.data else 'No details provided.'}"
        
        # Send WhatsApp message
        try:
            phone_number = current_user.phone  # Ensure this is in the format +91XXXXXXXXXX
            kit.sendwhatmsg_instantly(phone_number, emergency_message, wait_time=15)
            flash('Emergency reported! Message sent on WhatsApp.', 'success')
        except Exception as e:
            flash(f'Failed to send WhatsApp message: {str(e)}', 'error')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
