# MQTT Data Sending Guide

This guide explains how to send electricity data via MQTT in your Electricity Monitor project.

## 🚀 Quick Start

### 1. Start MQTT Broker
Make sure you have an MQTT broker running. You can use:
- **Mosquitto** (recommended): `mosquitto -v`
- **Eclipse Mosquitto**: Download from https://mosquitto.org/
- **Online broker**: Use a cloud MQTT service

### 2. Send Data Using Existing Scripts

#### Option A: Use Test Scripts
```bash
# Single apartment simulation
python test_mqtt.py

# Multiple apartments simulation
python test_multi_apartment.py
```

#### Option B: Use Custom Publisher
```bash
# Send single reading
python mqtt_publisher.py --apartment 101 --voltage 230.5 --current 5.2

# Continuous simulation
python mqtt_publisher.py --apartment 101 --continuous --interval 3

# Help
python mqtt_publisher.py --help
```

#### Option C: Use Examples
```bash
# Run interactive examples
python examples/send_mqtt_data.py

# Or use the batch file (Windows)
run_mqtt_examples.bat
```

## 📡 MQTT Configuration

### Topic Structure
- **Format**: `electricity/building/floor/{apartment_number}`
- **Examples**:
  - `electricity/building/floor/101` (Apartment 101)
  - `electricity/building/floor/202` (Apartment 202)

### Data Format
```json
{
    "voltage": 230.5,
    "current": 5.2,
    "apartment": "101",
    "floor": "1",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "power": 1198.6
}
```

### Configuration Variables
Set these in your `.env` file or environment:
```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC_PREFIX=electricity/building
```

## 🛠️ Programming Examples

### Python - Basic Usage
```python
from mqtt_utils import send_electricity_data, send_sensor_data

# Send single reading
send_electricity_data("101", 230.5, 5.2, "1")

# Send sensor data with additional info
sensor_data = {
    "voltage": 231.2,
    "current": 6.8,
    "floor": "1",
    "device_id": "sensor_001",
    "temperature": 25.3
}
send_sensor_data("101", sensor_data)
```

### Python - Advanced Usage
```python
from mqtt_utils import MQTTPublisher

# Create publisher instance
publisher = MQTTPublisher()
publisher.connect()

# Send multiple readings
readings = [
    {"apartment_number": "101", "voltage": 230.5, "current": 5.2, "floor": "1"},
    {"apartment_number": "102", "voltage": 235.1, "current": 3.8, "floor": "1"},
]
publisher.publish_batch_readings(readings)

publisher.disconnect()
```

### Arduino/ESP32 Example
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* mqtt_server = "your-broker-ip";
const int mqtt_port = 1883;
const char* topic = "electricity/building/floor/101";

void sendElectricityData(float voltage, float current) {
  DynamicJsonDocument doc(1024);
  doc["voltage"] = voltage;
  doc["current"] = current;
  doc["apartment"] = "101";
  doc["floor"] = "1";
  doc["timestamp"] = millis();
  doc["power"] = voltage * current;
  
  char buffer[1024];
  serializeJson(doc, buffer);
  
  client.publish(topic, buffer);
}
```

## 🔧 Integration with Your Flask App

Your Flask app already receives MQTT data. To also send data, you can:

1. **Add a route to send data**:
```python
@app.route('/api/send-reading', methods=['POST'])
@login_required
def send_reading():
    data = request.get_json()
    success = send_electricity_data(
        current_user.apartment_number,
        data['voltage'],
        data['current'],
        current_user.floor
    )
    return jsonify({'success': success})
```

2. **Use the MQTT utilities**:
```python
from mqtt_utils import send_electricity_data

# In your Flask routes
send_electricity_data("101", 230.5, 5.2, "1")
```

## 📊 Monitoring and Debugging

### View MQTT Messages
```bash
# Subscribe to all electricity topics
mosquitto_sub -h localhost -t "electricity/building/+/+"

# Subscribe to specific apartment
mosquitto_sub -h localhost -t "electricity/building/floor/101"
```

### Test MQTT Connection
```python
from mqtt_utils import MQTTPublisher

publisher = MQTTPublisher()
if publisher.connect():
    print("✅ Connected to MQTT broker")
    publisher.disconnect()
else:
    print("❌ Failed to connect to MQTT broker")
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if MQTT broker is running
   - Verify broker address and port
   - Check firewall settings

2. **Messages Not Received**
   - Verify topic names match exactly
   - Check JSON format is valid
   - Ensure broker is accessible

3. **Permission Denied**
   - Check MQTT broker authentication
   - Verify topic permissions

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Additional Resources

- [MQTT Protocol Specification](https://mqtt.org/mqtt-specification/)
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/)
- [Mosquitto MQTT Broker](https://mosquitto.org/)
- [MQTT Topics Best Practices](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)

## 🎯 Next Steps

1. Set up your MQTT broker
2. Run the test scripts to verify connectivity
3. Integrate MQTT publishing into your sensors/devices
4. Monitor data flow using MQTT tools
5. Set up data persistence and alerting

Happy MQTT publishing! 🚀
