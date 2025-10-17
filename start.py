#!/usr/bin/env python3
"""
Startup script for the Electricity Monitoring Application
This script handles the initial setup and starts the application
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Set up environment file if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("Creating .env file from template...")
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            print("✓ .env file created")
            print("⚠️  Please edit .env file with your configuration before running the application")
        else:
            print("Warning: .env.example not found, creating basic .env file...")
            with open('.env', 'w') as f:
                f.write("SECRET_KEY=your-secret-key-here-change-this\n")
                f.write("MQTT_BROKER=localhost\n")
                f.write("MQTT_PORT=1883\n")
                f.write("MQTT_TOPIC=electricity/data\n")
            print("✓ Basic .env file created")
    else:
        print("✓ .env file already exists")

def check_mqtt_broker():
    """Check if MQTT broker is accessible"""
    try:
        import paho.mqtt.client as mqtt
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("✓ MQTT broker is accessible")
                client.disconnect()
            else:
                print(f"⚠️  MQTT broker connection failed (code: {rc})")
                print("   Make sure MQTT broker is running on localhost:1883")
        
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("localhost", 1883, 5)
        client.loop_start()
        time.sleep(2)
        client.loop_stop()
        
    except ImportError:
        print("⚠️  paho-mqtt not installed, cannot check MQTT broker")
    except Exception as e:
        print(f"⚠️  MQTT broker check failed: {e}")
        print("   Make sure MQTT broker (e.g., Mosquitto) is running")

def start_application():
    """Start the Flask application"""
    print("\n" + "="*50)
    print("Starting Electricity Monitoring Application")
    print("="*50)
    print("Web interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    print("="*50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("Electricity Monitoring Application - Startup")
    print("="*50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Check MQTT broker
    check_mqtt_broker()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()
