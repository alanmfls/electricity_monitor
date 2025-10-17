#!/usr/bin/env python3
"""
Test script to simulate MQTT electricity data for multiple apartments
This script publishes random voltage and current values for different apartments
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import sys
import threading

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "electricity/building"

# Apartment configurations
APARTMENTS = [
    {"number": "101", "floor": "1", "voltage_range": (220, 240), "current_range": (0.5, 8.0)},
    {"number": "102", "floor": "1", "voltage_range": (220, 240), "current_range": (0.5, 12.0)},
    {"number": "201", "floor": "2", "voltage_range": (220, 240), "current_range": (0.5, 15.0)},
    {"number": "202", "floor": "2", "voltage_range": (220, 240), "current_range": (0.5, 10.0)},
    {"number": "301", "floor": "3", "voltage_range": (220, 240), "current_range": (0.5, 6.0)},
    {"number": "302", "floor": "3", "voltage_range": (220, 240), "current_range": (0.5, 9.0)},
]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    pass  # Silent publish

def simulate_apartment_data(apartment, client):
    """Simulate electricity data for a specific apartment"""
    apartment_number = apartment["number"]
    floor = apartment["floor"]
    voltage_range = apartment["voltage_range"]
    current_range = apartment["current_range"]
    
    topic = f"{MQTT_TOPIC_PREFIX}/floor/{apartment_number}"
    
    while True:
        try:
            # Simulate realistic electricity values for this apartment
            voltage = round(random.uniform(*voltage_range), 2)
            current = round(random.uniform(*current_range), 2)
            power = voltage * current
            
            # Create JSON payload
            data = {
                "voltage": voltage,
                "current": current,
                "apartment": apartment_number,
                "floor": floor
            }
            
            # Publish to MQTT
            message = json.dumps(data)
            result = client.publish(topic, message)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Apartment {apartment_number} (Floor {floor}): V={voltage}V, I={current}A, P={power:.2f}W")
            else:
                print(f"Failed to publish for apartment {apartment_number}: {result.rc}")
            
            # Wait 2-5 seconds before next reading (varies per apartment)
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Error in apartment {apartment_number}: {e}")
            time.sleep(5)

def main():
    """Main function to start simulation for all apartments"""
    print("Multi-Apartment Electricity Monitor - MQTT Test Simulator")
    print("=" * 60)
    print(f"MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Topic Prefix: {MQTT_TOPIC_PREFIX}")
    print(f"Simulating {len(APARTMENTS)} apartments")
    print("=" * 60)
    
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        # Start simulation threads for each apartment
        threads = []
        for apartment in APARTMENTS:
            thread = threading.Thread(
                target=simulate_apartment_data, 
                args=(apartment, client),
                daemon=True
            )
            thread.start()
            threads.append(thread)
            print(f"Started simulation for apartment {apartment['number']}")
        
        print("\nAll apartment simulations started!")
        print("Press Ctrl+C to stop all simulations")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping all simulations...")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT Broker")

if __name__ == "__main__":
    main()
