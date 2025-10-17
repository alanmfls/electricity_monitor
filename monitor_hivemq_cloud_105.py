#!/usr/bin/env python3
"""
HiveMQ Cloud Monitor for Apartment 105
This script subscribes to your HiveMQ Cloud cluster and monitors electricity data for apartment 105
"""

import paho.mqtt.client as mqtt
import json
import time
import ssl
from datetime import datetime

# HiveMQ Cloud Configuration
HIVEMQ_CLUSTER = "99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud"
HIVEMQ_PORT = 8883
HIVEMQ_USERNAME = "UNIVESP"
HIVEMQ_PASSWORD = "Univesp2025"
APARTMENT_NUMBER = "105"
TOPIC_PREFIX = "electricity/building"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud!")
        print(f"📡 Cluster: {HIVEMQ_CLUSTER}")
        print(f"👤 Username: {HIVEMQ_USERNAME}")
        print(f"🏠 Monitoring Apartment: {APARTMENT_NUMBER}")
        print("=" * 70)
    else:
        print(f"❌ Failed to connect to HiveMQ Cloud, return code {rc}")

def on_message(client, userdata, msg):
    try:
        # Parse the JSON message
        data = json.loads(msg.payload.decode())
        
        # Check if this is for apartment 105
        if data.get('apartment') == APARTMENT_NUMBER:
            print(f"📊 Apartment {APARTMENT_NUMBER} Data Received:")
            print(f"   ⚡ Voltage: {data.get('voltage', 'N/A')}V")
            print(f"   🔌 Current: {data.get('current', 'N/A')}A")
            print(f"   💡 Power: {data.get('power', 'N/A')}W")
            print(f"   🏠 Floor: {data.get('floor', 'N/A')}")
            print(f"   🕐 Timestamp: {data.get('timestamp', 'N/A')}")
            
            # Display additional data if available
            if 'room_temperature' in data:
                print(f"   🌡️  Temperature: {data['room_temperature']}°C")
            if 'humidity' in data:
                print(f"   💧 Humidity: {data['humidity']}%")
            if 'battery_level' in data:
                print(f"   🔋 Battery: {data['battery_level']}%")
            if 'device_id' in data:
                print(f"   📱 Device: {data['device_id']}")
            if 'cluster' in data:
                print(f"   ☁️  Cluster: {data['cluster']}")
            
            print(f"   📡 Topic: {msg.topic}")
            print("-" * 70)
        else:
            # Show other apartments briefly
            print(f"📊 Other apartment data: {data.get('apartment', 'Unknown')} - {data.get('power', 0):.1f}W")
    
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def on_disconnect(client, userdata, rc):
    print("🔌 Disconnected from HiveMQ Cloud")

def main():
    """Main function to start monitoring"""
    print("🏠 HiveMQ Cloud Monitor - Apartment 105")
    print("=" * 70)
    print(f"Cluster: {HIVEMQ_CLUSTER}")
    print(f"Username: {HIVEMQ_USERNAME}")
    print(f"Topic: {TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}")
    print("=" * 70)
    
    # Create MQTT client
    client = mqtt.Client()
    client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
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
        
        # Subscribe to apartment 105 topic
        topic = f"{TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}"
        client.subscribe(topic)
        print(f"📡 Subscribed to: {topic}")
        
        # Also subscribe to all electricity topics to see other apartments
        all_topics = f"{TOPIC_PREFIX}/+/+"
        client.subscribe(all_topics)
        print(f"📡 Also monitoring: {all_topics}")
        
        print("\n🔄 Monitoring started...")
        print("Press Ctrl+C to stop")
        print("=" * 70)
        
        # Start the loop
        client.loop_forever()
    
    except KeyboardInterrupt:
        print(f"\n⏹️ Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.disconnect()
        print("🔌 Disconnected from HiveMQ Cloud")

if __name__ == "__main__":
    main()
