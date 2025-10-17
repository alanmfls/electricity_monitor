#!/usr/bin/env python3
"""
MQTT Utilities for Electricity Monitor
Helper functions for publishing MQTT data
"""

import paho.mqtt.client as mqtt
import json
import threading
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', '99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud')
MQTT_PORT = int(os.getenv('MQTT_PORT', 8883))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'UNIVESP')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'Univesp2025')
MQTT_TOPIC_PREFIX = os.getenv('MQTT_TOPIC_PREFIX', 'electricity/building')

class MQTTPublisher:
    """MQTT Publisher for sending electricity data"""
    
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
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
            print("✅ MQTT Publisher connected!")
            self.connected = True
        else:
            print(f"❌ MQTT Publisher failed to connect: {rc}")
            self.connected = False
    
    def on_publish(self, client, userdata, mid):
        print(f"📤 Published message {mid}")
    
    def on_disconnect(self, client, userdata, rc):
        print("🔌 MQTT Publisher disconnected")
        self.connected = False
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            time.sleep(1)  # Wait for connection
            return self.connected
        except Exception as e:
            print(f"❌ Failed to connect to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish_reading(self, apartment_number, voltage, current, floor="1", additional_data=None):
        """Publish a single electricity reading"""
        if not self.connected:
            print("❌ Not connected to MQTT broker")
            return False
        
        topic = f"{MQTT_TOPIC_PREFIX}/floor/{apartment_number}"
        
        data = {
            "voltage": voltage,
            "current": current,
            "apartment": apartment_number,
            "floor": floor,
            "timestamp": datetime.now().isoformat(),
            "power": voltage * current
        }
        
        # Add any additional data
        if additional_data:
            data.update(additional_data)
        
        message = json.dumps(data)
        result = self.client.publish(topic, message)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            power = voltage * current
            print(f"📊 Published: Apartment {apartment_number} - V={voltage}V, I={current}A, P={power:.2f}W")
            return True
        else:
            print(f"❌ Failed to publish for apartment {apartment_number}: {result.rc}")
            return False
    
    def publish_batch_readings(self, readings):
        """Publish multiple readings at once"""
        if not self.connected:
            print("❌ Not connected to MQTT broker")
            return False
        
        success_count = 0
        for reading in readings:
            if self.publish_reading(**reading):
                success_count += 1
        
        print(f"📊 Published {success_count}/{len(readings)} readings successfully")
        return success_count == len(readings)

# Global publisher instance
mqtt_publisher = MQTTPublisher()

def send_electricity_data(apartment_number, voltage, current, floor="1", additional_data=None):
    """
    Convenience function to send electricity data via MQTT
    
    Args:
        apartment_number (str): Apartment number (e.g., "101")
        voltage (float): Voltage reading in volts
        current (float): Current reading in amperes
        floor (str): Floor number (default: "1")
        additional_data (dict): Any additional data to include
    
    Returns:
        bool: True if published successfully, False otherwise
    """
    if not mqtt_publisher.connected:
        if not mqtt_publisher.connect():
            return False
    
    return mqtt_publisher.publish_reading(apartment_number, voltage, current, floor, additional_data)

def send_sensor_data(apartment_number, sensor_data):
    """
    Send data from a sensor device
    
    Args:
        apartment_number (str): Apartment number
        sensor_data (dict): Dictionary containing sensor readings
            Expected keys: voltage, current, floor (optional)
    """
    voltage = sensor_data.get('voltage')
    current = sensor_data.get('current')
    floor = sensor_data.get('floor', '1')
    
    if voltage is None or current is None:
        print("❌ Missing voltage or current data")
        return False
    
    # Remove voltage, current, floor from additional_data
    additional_data = {k: v for k, v in sensor_data.items() 
                      if k not in ['voltage', 'current', 'floor']}
    
    return send_electricity_data(apartment_number, voltage, current, floor, additional_data)

# Example usage functions
def simulate_apartment_data(apartment_number, floor="1", duration=60, interval=3):
    """
    Simulate electricity data for an apartment
    
    Args:
        apartment_number (str): Apartment number
        floor (str): Floor number
        duration (int): Duration in seconds
        interval (int): Interval between readings in seconds
    """
    import random
    
    print(f"🔄 Starting simulation for apartment {apartment_number} (Floor {floor})")
    print(f"Duration: {duration}s, Interval: {interval}s")
    
    if not mqtt_publisher.connect():
        return
    
    start_time = time.time()
    reading_count = 0
    
    try:
        while time.time() - start_time < duration:
            voltage = round(random.uniform(220.0, 240.0), 2)
            current = round(random.uniform(0.5, 15.0), 2)
            
            if send_electricity_data(apartment_number, voltage, current, floor):
                reading_count += 1
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n⏹️ Simulation stopped by user")
    
    print(f"📊 Simulation complete: {reading_count} readings sent")
    mqtt_publisher.disconnect()

if __name__ == "__main__":
    # Example usage
    print("🏠 MQTT Utilities - Example Usage")
    print("=" * 40)
    
    # Connect to MQTT broker
    if mqtt_publisher.connect():
        # Send a single reading
        send_electricity_data("101", 230.5, 5.2, "1")
        
        # Send with additional data
        additional_data = {
            "device_id": "sensor_001",
            "temperature": 25.3,
            "humidity": 45.2
        }
        send_electricity_data("102", 235.1, 3.8, "1", additional_data)
        
        # Disconnect
        mqtt_publisher.disconnect()
    else:
        print("❌ Could not connect to MQTT broker")
