#!/usr/bin/env python3
"""
HiveMQ Cloud Test Script for Apartment 105
This script sends electricity data to your HiveMQ Cloud cluster for apartment 105
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

def simulate_apartment_105_data():
    """Simulate electricity data for apartment 105"""
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
        print("🔄 Connecting to HiveMQ Cloud...")
        client.connect(HIVEMQ_CLUSTER, HIVEMQ_PORT, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(3)
        
        print(f"🔄 Starting electricity data simulation for apartment {APARTMENT_NUMBER}...")
        print("Press Ctrl+C to stop")
        
        reading_count = 0
        
        while True:
            # Simulate realistic electricity values for apartment 105
            voltage = round(random.uniform(220.0, 240.0), 2)
            current = round(random.uniform(0.5, 12.0), 2)  # Moderate consumption for apartment 105
            power = voltage * current
            
            # Create JSON payload with apartment 105 specific data
            data = {
                "voltage": voltage,
                "current": current,
                "power": power,
                "apartment": APARTMENT_NUMBER,
                "floor": FLOOR,
                "timestamp": datetime.now().isoformat(),
                "broker": "HiveMQ Cloud",
                "cluster": HIVEMQ_CLUSTER,
                "device_id": f"sensor_105_{reading_count % 3 + 1}",
                "room_temperature": round(random.uniform(20.0, 25.0), 1),
                "humidity": round(random.uniform(40.0, 60.0), 1),
                "battery_level": round(random.uniform(80.0, 100.0), 1)
            }
            
            # Publish to HiveMQ Cloud
            topic = f"{TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}"
            message = json.dumps(data, indent=2)
            result = client.publish(topic, message)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                reading_count += 1
                print(f"📊 Reading #{reading_count}: V={voltage}V, I={current}A, P={power:.2f}W")
                print(f"📡 Topic: {topic}")
                print(f"🌡️  Temperature: {data['room_temperature']}°C, Humidity: {data['humidity']}%")
                print(f"🔋 Battery: {data['battery_level']}%")
                print("-" * 60)
            else:
                print(f"❌ Failed to publish message: {result.rc}")
            
            # Wait 3 seconds before next reading
            time.sleep(3)
    
    except KeyboardInterrupt:
        print(f"\n⏹️ Simulation stopped by user")
        print(f"📊 Total readings sent: {reading_count}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("🔌 Disconnected from HiveMQ Cloud")

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
        
        power = voltage * current
        data = {
            "voltage": voltage,
            "current": current,
            "power": power,
            "apartment": APARTMENT_NUMBER,
            "floor": FLOOR,
            "timestamp": datetime.now().isoformat(),
            "broker": "HiveMQ Cloud",
            "cluster": HIVEMQ_CLUSTER
        }
        
        topic = f"{TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}"
        message = json.dumps(data, indent=2)
        result = client.publish(topic, message)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✅ Single reading sent successfully!")
            print(f"📊 Apartment {APARTMENT_NUMBER}: V={voltage}V, I={current}A, P={power:.2f}W")
            print(f"📡 Topic: {topic}")
            return True
        else:
            print(f"❌ Failed to publish message: {result.rc}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        client.loop_stop()
        client.disconnect()

def main():
    """Main function"""
    print("🏠 HiveMQ Cloud Electricity Monitor - Apartment 105")
    print("=" * 70)
    print(f"Cluster: {HIVEMQ_CLUSTER}")
    print(f"Username: {HIVEMQ_USERNAME}")
    print(f"Topic: {TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}")
    print("=" * 70)
    
    if len(sys.argv) == 3:
        try:
            voltage = float(sys.argv[1])
            current = float(sys.argv[2])
            print(f"📊 Sending single reading: {voltage}V, {current}A")
            send_single_reading(voltage, current)
        except ValueError:
            print("❌ Invalid voltage or current values. Use: python test_hivemq_cloud_105.py <voltage> <current>")
    else:
        print("🔄 Starting continuous simulation...")
        print("Usage: python test_hivemq_cloud_105.py [voltage] [current]")
        print("Example: python test_hivemq_cloud_105.py 230.5 5.2")
        print("Press Ctrl+C to stop continuous simulation")
        print()
        simulate_apartment_105_data()

if __name__ == "__main__":
    main()
