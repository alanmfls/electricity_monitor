#!/usr/bin/env python3
"""
Custom MQTT Publisher for Electricity Monitor
Send real or simulated electricity data via MQTT
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import sys
import argparse
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "electricity/building"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
    else:
        print(f"❌ Failed to connect, return code {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    print(f"📤 Message {mid} published successfully")

def on_disconnect(client, userdata, rc):
    print("🔌 Disconnected from MQTT Broker")

def send_single_reading(client, apartment_number, voltage, current, floor="1"):
    """Send a single electricity reading"""
    topic = f"{MQTT_TOPIC_PREFIX}/floor/{apartment_number}"
    
    data = {
        "voltage": voltage,
        "current": current,
        "apartment": apartment_number,
        "floor": floor,
        "timestamp": datetime.now().isoformat()
    }
    
    message = json.dumps(data)
    result = client.publish(topic, message)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        power = voltage * current
        print(f"📊 Apartment {apartment_number}: V={voltage}V, I={current}A, P={power:.2f}W")
        return True
    else:
        print(f"❌ Failed to publish for apartment {apartment_number}: {result.rc}")
        return False

def simulate_continuous_data(client, apartment_number, floor="1", interval=3):
    """Simulate continuous electricity data"""
    print(f"🔄 Starting continuous simulation for apartment {apartment_number}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Simulate realistic values
            voltage = round(random.uniform(220.0, 240.0), 2)
            current = round(random.uniform(0.5, 15.0), 2)
            
            send_single_reading(client, apartment_number, voltage, current, floor)
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Stopped simulation for apartment {apartment_number}")

def send_real_data(client, apartment_number, voltage, current, floor="1"):
    """Send real electricity data (from sensors)"""
    print(f"📡 Sending real data for apartment {apartment_number}")
    return send_single_reading(client, apartment_number, voltage, current, floor)

def main():
    parser = argparse.ArgumentParser(description='MQTT Publisher for Electricity Monitor')
    parser.add_argument('--apartment', '-a', required=True, help='Apartment number (e.g., 101)')
    parser.add_argument('--floor', '-f', default='1', help='Floor number (default: 1)')
    parser.add_argument('--voltage', '-v', type=float, help='Voltage value (if not provided, will simulate)')
    parser.add_argument('--current', '-c', type=float, help='Current value (if not provided, will simulate)')
    parser.add_argument('--continuous', action='store_true', help='Run continuous simulation')
    parser.add_argument('--interval', '-i', type=int, default=3, help='Interval in seconds for continuous mode')
    parser.add_argument('--broker', '-b', default=MQTT_BROKER, help='MQTT broker address')
    parser.add_argument('--port', '-p', type=int, default=MQTT_PORT, help='MQTT broker port')
    
    args = parser.parse_args()
    
    print("🏠 Electricity Monitor - MQTT Publisher")
    print("=" * 50)
    print(f"MQTT Broker: {args.broker}:{args.port}")
    print(f"Apartment: {args.apartment} (Floor {args.floor})")
    print("=" * 50)
    
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        client.connect(args.broker, args.port, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        if args.continuous:
            # Continuous simulation mode
            simulate_continuous_data(client, args.apartment, args.floor, args.interval)
        else:
            # Single reading mode
            if args.voltage is not None and args.current is not None:
                # Send real data
                send_real_data(client, args.apartment, args.voltage, args.current, args.floor)
            else:
                # Send simulated data
                voltage = round(random.uniform(220.0, 240.0), 2)
                current = round(random.uniform(0.5, 15.0), 2)
                send_single_reading(client, args.apartment, voltage, current, args.floor)
    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
