#!/usr/bin/env python3
"""
HiveMQ Configuration for Electricity Monitor - Apartment 105
This script demonstrates how to send data to HiveMQ for apartment 105
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import sys
from datetime import datetime

# HiveMQ Configuration
HIVEMQ_BROKER = "broker.hivemq.com"  # Public HiveMQ broker
HIVEMQ_PORT = 1883
APARTMENT_NUMBER = "105"
FLOOR = "1"  # Adjust as needed
TOPIC_PREFIX = "electricity/building"

# For HiveMQ Cloud with authentication (uncomment if you have credentials)
# HIVEMQ_BROKER = "your-cluster.hivemq.cloud"
# HIVEMQ_PORT = 8883
# HIVEMQ_USERNAME = "your-username"
# HIVEMQ_PASSWORD = "your-password"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Broker!")
        print(f"📡 Broker: {HIVEMQ_BROKER}:{HIVEMQ_PORT}")
        print(f"🏠 Apartment: {APARTMENT_NUMBER} (Floor {FLOOR})")
    else:
        print(f"❌ Failed to connect to HiveMQ, return code {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    print(f"📤 Message {mid} published to HiveMQ")

def on_disconnect(client, userdata, rc):
    print("🔌 Disconnected from HiveMQ Broker")

def send_apartment_105_data(client, voltage, current, additional_data=None):
    """Send electricity data for apartment 105 to HiveMQ"""
    topic = f"{TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}"
    
    data = {
        "voltage": voltage,
        "current": current,
        "apartment": APARTMENT_NUMBER,
        "floor": FLOOR,
        "timestamp": datetime.now().isoformat(),
        "power": voltage * current,
        "broker": "HiveMQ"
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
        print(f"❌ Failed to publish to HiveMQ: {result.rc}")
        return False

def simulate_apartment_105_data(duration=60, interval=3):
    """Simulate continuous electricity data for apartment 105"""
    print(f"🏠 HiveMQ Electricity Monitor - Apartment {APARTMENT_NUMBER}")
    print("=" * 60)
    print(f"Broker: {HIVEMQ_BROKER}:{HIVEMQ_PORT}")
    print(f"Topic: {TOPIC_PREFIX}/floor/{APARTMENT_NUMBER}")
    print(f"Duration: {duration}s, Interval: {interval}s")
    print("=" * 60)
    
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        # Connect to HiveMQ
        print("🔄 Connecting to HiveMQ...")
        client.connect(HIVEMQ_BROKER, HIVEMQ_PORT, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        print(f"🔄 Starting simulation for apartment {APARTMENT_NUMBER}...")
        print("Press Ctrl+C to stop")
        
        start_time = time.time()
        reading_count = 0
        
        while time.time() - start_time < duration:
            # Simulate realistic electricity values for apartment 105
            voltage = round(random.uniform(220.0, 240.0), 2)
            current = round(random.uniform(0.5, 12.0), 2)  # Moderate consumption
            
            # Add some apartment-specific data
            additional_data = {
                "room_temperature": round(random.uniform(20.0, 25.0), 1),
                "humidity": round(random.uniform(40.0, 60.0), 1),
                "device_id": f"sensor_105_{reading_count % 3 + 1}"
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
        print(f"📊 Simulation complete: {reading_count} readings sent to HiveMQ")

def send_single_reading(voltage, current):
    """Send a single reading for apartment 105"""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        client.connect(HIVEMQ_BROKER, HIVEMQ_PORT, 60)
        client.loop_start()
        time.sleep(2)
        
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
    
    parser = argparse.ArgumentParser(description=f'HiveMQ Publisher for Apartment {APARTMENT_NUMBER}')
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
