from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import paho.mqtt.client as mqtt
import json
import threading
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///electricity_monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', '99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud')
MQTT_PORT = int(os.getenv('MQTT_PORT', 8883))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'UNIVESP')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'Univesp2025')
MQTT_TOPIC_PREFIX = os.getenv('MQTT_TOPIC_PREFIX', 'electricity/building')

# Global variables for MQTT data - now user-specific
user_power_data = {}  # Dictionary to store data for each user

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    apartment_number = db.Column(db.String(10), unique=True, nullable=False)  # Floor/Apartment number
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PowerReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    voltage = db.Column(db.Float, nullable=False)
    current = db.Column(db.Float, nullable=False)
    power = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    apartment_number = StringField('Apartment/Floor Number', validators=[DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Register')

# MQTT Manager for Multiple Users
class MQTTManager:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.connected = False
        
        # Enable SSL/TLS for HiveMQ Cloud
        import ssl
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.client.tls_set_context(context)
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.connected = True
            # Subscribe to all apartment topics
            self.subscribe_to_all_apartments()
        else:
            print(f"Failed to connect, return code {rc}")
            self.connected = False
    
    def on_message(self, client, userdata, msg):
        try:
            # Extract apartment number from topic
            topic_parts = msg.topic.split('/')
            if len(topic_parts) >= 3:
                apartment_number = topic_parts[-1]  # Last part is apartment number
                
                data = json.loads(msg.payload.decode())
                voltage = float(data.get('voltage', 0))
                current = float(data.get('current', 0))
                power = voltage * current  # P = V × I
                
                global user_power_data
                user_power_data[apartment_number] = {
                    'voltage': voltage,
                    'current': current,
                    'power': power,
                    'timestamp': datetime.now()
                }
                
                print(f"Apartment {apartment_number}: V={voltage}V, I={current}A, P={power}W")
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error processing MQTT message: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT Broker")
        self.connected = False
    
    def subscribe_to_all_apartments(self):
        """Subscribe to all apartment topics"""
        # Subscribe to pattern: electricity/building/floor/apartment
        topic_pattern = f"{MQTT_TOPIC_PREFIX}/+/+"
        self.client.subscribe(topic_pattern)
        print(f"Subscribed to topic pattern: {topic_pattern}")
    
    def subscribe_to_apartment(self, apartment_number):
        """Subscribe to specific apartment topic"""
        topic = f"{MQTT_TOPIC_PREFIX}/floor/{apartment_number}"
        self.client.subscribe(topic)
        print(f"Subscribed to apartment {apartment_number}: {topic}")
    
    def start(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
    
    def get_apartment_topic(self, apartment_number):
        """Get the MQTT topic for a specific apartment"""
        return f"{MQTT_TOPIC_PREFIX}/floor/{apartment_number}"

# Initialize MQTT manager
mqtt_manager = MQTTManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        # Get data for current user's apartment
        apartment_data = user_power_data.get(current_user.apartment_number, {
            'voltage': 0,
            'current': 0,
            'power': 0,
            'timestamp': None
        })
        return render_template('dashboard.html', data=apartment_data, apartment_number=current_user.apartment_number)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash == form.password.data:  # In production, use proper password hashing
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered')
            return render_template('register.html', form=form)
        
        existing_apartment = User.query.filter_by(apartment_number=form.apartment_number.data).first()
        if existing_apartment:
            flash('Apartment number already registered')
            return render_template('register.html', form=form)
        
        user = User(
            email=form.email.data, 
            password_hash=form.password.data,  # In production, hash the password
            apartment_number=form.apartment_number.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Subscribe to this apartment's MQTT topic
        mqtt_manager.subscribe_to_apartment(form.apartment_number.data)
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/power-data')
@login_required
def get_power_data():
    apartment_data = user_power_data.get(current_user.apartment_number, {
        'voltage': 0,
        'current': 0,
        'power': 0,
        'timestamp': None
    })
    return jsonify(apartment_data)

@app.route('/api/save-reading', methods=['POST'])
@login_required
def save_reading():
    try:
        apartment_data = user_power_data.get(current_user.apartment_number, {
            'voltage': 0,
            'current': 0,
            'power': 0
        })
        
        reading = PowerReading(
            user_id=current_user.id,
            voltage=apartment_data['voltage'],
            current=apartment_data['current'],
            power=apartment_data['power']
        )
        db.session.add(reading)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/history')
@login_required
def history():
    readings = PowerReading.query.filter_by(user_id=current_user.id).order_by(PowerReading.timestamp.desc()).limit(100).all()
    return render_template('history.html', readings=readings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Start MQTT manager in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_manager.start)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)