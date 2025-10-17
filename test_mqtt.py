#!/usr/bin/env python3
"""
Test script to simulate MQTT electricity data
This script publishes random voltage and current values to test the application
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import sys

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "electricity/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")

def simulate_electricity_data():
    """Simulate realistic electricity consumption data"""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        print("Starting electricity data simulation...")
        print("Press Ctrl+C to stop")
        
        while True:
            # Simulate realistic residential electricity values
            # Voltage: typically 220-240V in most countries
            voltage = round(random.uniform(220.0, 240.0), 2)
            
            # Current: varies based on appliances (0.5A to 15A for residential)
            current = round(random.uniform(0.5, 15.0), 2)
            
            # Create JSON payload
            data = {
                "voltage": voltage,
                "current": current
            }
            
            # Calculate power for display
            power = voltage * current
            
            # Publish to MQTT
            message = json.dumps(data)
            result = client.publish(MQTT_TOPIC, message)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published: V={voltage}V, I={current}A, P={power:.2f}W")
            else:
                print(f"Failed to publish message: {result.rc}")
            
            # Wait 3 seconds before next reading
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nStopping simulation...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT Broker")

if __name__ == "__main__":
    print("Electricity Monitor - MQTT Test Simulator")
    print("=" * 50)
    print(f"MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Topic: {MQTT_TOPIC}")
    print("=" * 50)
    
    simulate_electricity_data()