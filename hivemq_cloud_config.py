#!/usr/bin/env python3
"""
HiveMQ Cloud Configuration for Electricity Monitor - Apartment 105
This script is configured to connect to your HiveMQ Cloud cluster
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import sys
import ssl
from datetime import datetime

# HiveMQ Cloud Configuration
HIVEMQ_CLUSTER = "99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud"
HIVEMQ_PORT = 8883
HIVEMQ_USERNAME = "UNIVESP"
HIVEMQ_PASSWORD = "Univesp2025"
APARTMENT_NUMBER = "105"
FLOOR = "1"
TOPIC_PREFIX = "electricity/building"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud!")
        print(f"📡 Cluster: {HIVEMQ_CLUSTER}")
        print(f"👤 Username: {HIVEMQ_USERNAME}")
        print(f"🏠 Apartment: {APARTMENT_NUMBER} (Floor {FLOOR})")
    else:
        print(f"❌ Failed to connect to HiveMQ Cloud, return code {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    print(f"📤 Message {mid} published to HiveMQ Cloud")

def on_disconnect(client, userdata, rc):
    print("🔌 Disconnected from HiveMQ Cloud")

def send_apartment_105_data(client, voltage, current, additional_data=None):
    """Send electricity data for apartment 105 to HiveMQ Cloud"""
    topic = f"{TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}"
    
    data = {
        "voltage": voltage,
        "current": current,
        "apartment": APARTMENT_NUMBER,
        "floor": FLOOR,
        "timestamp": datetime.now().isoformat(),
        "power": voltage * current,
        "broker": "HiveMQ Cloud",
        "cluster": HIVEMQ_CLUSTER
    }
    
    # Add any additional data
    if additional_data:
        data.update(additional_data)
    
    message = json.dumps(data, indent=2)
    result = client.publish(topic, message)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        power = voltage * current
        print(f"📊 Apartment {APARTMENT_NUMBER}: V={voltage}V, I={current}A, P={power:.2f}W")
        print(f"📡 Topic: {topic}")
        return True
    else:
        print(f"❌ Failed to publish to HiveMQ Cloud: {result.rc}")
        return False

def simulate_apartment_105_data(duration=60, interval=3):
    """Simulate continuous electricity data for apartment 105"""
    print(f"🏠 HiveMQ Cloud Electricity Monitor - Apartment {APARTMENT_NUMBER}")
    print("=" * 70)
    print(f"Cluster: {HIVEMQ_CLUSTER}")
    print(f"Username: {HIVEMQ_USERNAME}")
    print(f"Topic: {TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}")
    print(f"Duration: {duration}s, Interval: {interval}s")
    print("=" * 70)
    
    # Create MQTT client
    client = mqtt.Client()
    client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    # Enable SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    client.tls_set_context(context)
    
    try:
        # Connect to HiveMQ Cloud
        print("🔄 Connecting to HiveMQ Cloud...")
        client.connect(HIVEMQ_CLUSTER, HIVEMQ_PORT, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(3)
        
        print(f"🔄 Starting simulation for apartment {APARTMENT_NUMBER}...")
        print("Press Ctrl+C to stop")
        
        start_time = time.time()
        reading_count = 0
        
        while time.time() - start_time < duration:
            # Simulate realistic electricity values for apartment 105
            voltage = round(random.uniform(220.0, 240.0), 2)
            current = round(random.uniform(0.5, 12.0), 2)  # Moderate consumption for apartment 105
            
            # Add some apartment-specific data
            additional_data = {
                "room_temperature": round(random.uniform(20.0, 25.0), 1),
                "humidity": round(random.uniform(40.0, 60.0), 1),
                "device_id": f"sensor_105_{reading_count % 3 + 1}",
                "battery_level": round(random.uniform(80.0, 100.0), 1)
            }
            
            if send_apartment_105_data(client, voltage, current, additional_data):
                reading_count += 1
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print(f"\n⏹️ Simulation stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print(f"📊 Simulation complete: {reading_count} readings sent to HiveMQ Cloud")

def send_single_reading(voltage, current):
    """Send a single reading for apartment 105"""
    client = mqtt.Client()
    client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    # Enable SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    client.tls_set_context(context)
    
    try:
        client.connect(HIVEMQ_CLUSTER, HIVEMQ_PORT, 60)
        client.loop_start()
        time.sleep(3)
        
        success = send_apartment_105_data(client, voltage, current)
        return success
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        client.loop_stop()
        client.disconnect()

def main():
    """Main function with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description=f'HiveMQ Cloud Publisher for Apartment {APARTMENT_NUMBER}')
    parser.add_argument('--voltage', '-v', type=float, help='Voltage value')
    parser.add_argument('--current', '-c', type=float, help='Current value')
    parser.add_argument('--continuous', action='store_true', help='Run continuous simulation')
    parser.add_argument('--duration', '-d', type=int, default=60, help='Duration in seconds for continuous mode')
    parser.add_argument('--interval', '-i', type=int, default=3, help='Interval in seconds for continuous mode')
    
    args = parser.parse_args()
    
    if args.continuous:
        simulate_apartment_105_data(args.duration, args.interval)
    elif args.voltage is not None and args.current is not None:
        send_single_reading(args.voltage, args.current)
    else:
        # Default: run simulation for 30 seconds
        simulate_apartment_105_data(30, 3)

if __name__ == "__main__":
    main()
