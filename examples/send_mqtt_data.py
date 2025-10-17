#!/usr/bin/env python3
"""
Examples of how to send MQTT data for the Electricity Monitor
This file demonstrates various ways to publish electricity data via MQTT
"""

import sys
import os
import time
import random

# Add parent directory to path to import mqtt_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqtt_utils import send_electricity_data, send_sensor_data, simulate_apartment_data

def example_1_single_reading():
    """Example 1: Send a single electricity reading"""
    print("📊 Example 1: Single Reading")
    print("-" * 30)
    
    # Send a single reading for apartment 101
    success = send_electricity_data(
        apartment_number="101",
        voltage=230.5,
        current=5.2,
        floor="1"
    )
    
    if success:
        print("✅ Single reading sent successfully!")
    else:
        print("❌ Failed to send reading")

def example_2_multiple_readings():
    """Example 2: Send multiple readings for different apartments"""
    print("\n📊 Example 2: Multiple Readings")
    print("-" * 30)
    
    apartments = [
        {"apartment": "101", "voltage": 230.5, "current": 5.2, "floor": "1"},
        {"apartment": "102", "voltage": 235.1, "current": 3.8, "floor": "1"},
        {"apartment": "201", "voltage": 228.9, "current": 7.1, "floor": "2"},
        {"apartment": "202", "voltage": 232.3, "current": 4.5, "floor": "2"},
    ]
    
    for apt in apartments:
        success = send_electricity_data(**apt)
        if success:
            print(f"✅ Sent data for apartment {apt['apartment']}")
        else:
            print(f"❌ Failed to send data for apartment {apt['apartment']}")
        time.sleep(1)  # Small delay between readings

def example_3_sensor_data():
    """Example 3: Send data from a sensor device with additional information"""
    print("\n📊 Example 3: Sensor Data with Additional Info")
    print("-" * 30)
    
    # Simulate sensor data with additional information
    sensor_data = {
        "voltage": 231.2,
        "current": 6.8,
        "floor": "3",
        "device_id": "sensor_001",
        "temperature": 25.3,
        "humidity": 45.2,
        "battery_level": 85,
        "signal_strength": -45
    }
    
    success = send_sensor_data("301", sensor_data)
    if success:
        print("✅ Sensor data sent successfully!")
    else:
        print("❌ Failed to send sensor data")

def example_4_continuous_simulation():
    """Example 4: Run continuous simulation for an apartment"""
    print("\n📊 Example 4: Continuous Simulation")
    print("-" * 30)
    print("This will run for 30 seconds with 2-second intervals")
    print("Press Ctrl+C to stop early")
    
    try:
        simulate_apartment_data(
            apartment_number="101",
            floor="1",
            duration=30,  # 30 seconds
            interval=2    # 2 seconds between readings
        )
    except KeyboardInterrupt:
        print("\n⏹️ Simulation stopped by user")

def example_5_real_world_scenario():
    """Example 5: Simulate a real-world scenario with multiple apartments"""
    print("\n📊 Example 5: Real-World Multi-Apartment Scenario")
    print("-" * 30)
    
    # Simulate different apartments with different consumption patterns
    apartments = [
        {"number": "101", "floor": "1", "base_current": 2.0, "variation": 1.5},
        {"number": "102", "floor": "1", "base_current": 3.5, "variation": 2.0},
        {"number": "201", "floor": "2", "base_current": 1.8, "variation": 1.2},
        {"number": "202", "floor": "2", "base_current": 4.2, "variation": 2.5},
    ]
    
    print("Simulating 20 readings for each apartment...")
    
    for reading in range(20):
        print(f"\n--- Reading {reading + 1}/20 ---")
        
        for apt in apartments:
            # Simulate realistic voltage (220-240V)
            voltage = round(random.uniform(220.0, 240.0), 2)
            
            # Simulate current with base + variation
            current = round(
                apt["base_current"] + random.uniform(-apt["variation"], apt["variation"]), 
                2
            )
            
            # Ensure current is positive
            current = max(0.1, current)
            
            success = send_electricity_data(
                apartment_number=apt["number"],
                voltage=voltage,
                current=current,
                floor=apt["floor"]
            )
            
            if success:
                power = voltage * current
                print(f"  Apartment {apt['number']}: {voltage}V, {current}A, {power:.1f}W")
        
        time.sleep(1)  # 1 second between rounds

def main():
    """Run all examples"""
    print("🏠 Electricity Monitor - MQTT Data Sending Examples")
    print("=" * 60)
    print("Make sure your MQTT broker is running on localhost:1883")
    print("=" * 60)
    
    try:
        # Run examples
        example_1_single_reading()
        time.sleep(2)
        
        example_2_multiple_readings()
        time.sleep(2)
        
        example_3_sensor_data()
        time.sleep(2)
        
        # Ask user if they want to run continuous simulation
        response = input("\n🤔 Run continuous simulation? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            example_4_continuous_simulation()
        
        # Ask user if they want to run real-world scenario
        response = input("\n🤔 Run real-world multi-apartment scenario? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            example_5_real_world_scenario()
        
        print("\n✅ All examples completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Examples stopped by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
