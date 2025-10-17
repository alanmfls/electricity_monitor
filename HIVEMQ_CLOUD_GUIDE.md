# HiveMQ Cloud Setup for Apartment 105

This guide shows you how to send electricity data to your HiveMQ Cloud cluster for apartment 105.

## 🚀 Quick Start

### 1. Send Data to HiveMQ Cloud

#### Option A: Use the Ready-Made Script
```bash
# Continuous simulation (recommended)
python test_hivemq_cloud_105.py

# Single reading
python test_hivemq_cloud_105.py 230.5 5.2
```

#### Option B: Use the Batch File (Windows)
```bash
run_hivemq_cloud_105.bat
```

#### Option C: Use the Advanced Script
```bash
# Continuous simulation with custom duration
python hivemq_cloud_config.py --continuous --duration 120 --interval 5

# Single reading
python hivemq_cloud_config.py --voltage 230.5 --current 5.2
```

### 2. Monitor the Data

In a separate terminal, run the monitor:
```bash
python monitor_hivemq_cloud_105.py
```

## 📡 MQTT Configuration

### HiveMQ Cloud Settings
- **Cluster**: `99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud`
- **Port**: `8883` (SSL/TLS)
- **Username**: `UNIVESP`
- **Password**: `Univesp2025`
- **Topic**: `electricity/building/floor/105`
- **Apartment**: `105`
- **Floor**: `1`

### Data Format
```json
{
    "voltage": 230.5,
    "current": 5.2,
    "power": 1198.6,
    "apartment": "105",
    "floor": "1",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "broker": "HiveMQ Cloud",
    "cluster": "99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud",
    "device_id": "sensor_105_1",
    "room_temperature": 23.5,
    "humidity": 45.2,
    "battery_level": 85.0
}
```

## 🛠️ Integration with Your Flask App

Your Flask app is already configured to work with your HiveMQ Cloud cluster! Here's how to use it:

### 1. Environment Variables
Your Flask app will use these defaults:
```python
MQTT_BROKER = '99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
MQTT_USERNAME = 'UNIVESP'
MQTT_PASSWORD = 'Univesp2025'
```

### 2. Register Apartment 105
1. Start your Flask app: `python app.py`
2. Go to `http://localhost:5000/register`
3. Register with apartment number `105`
4. Login and view the dashboard

### 3. Send Data from Your App
```python
from mqtt_utils import send_electricity_data

# Send data for apartment 105
send_electricity_data("105", 230.5, 5.2, "1")
```

## 🔧 Programming Examples

### Python - Send Single Reading
```python
import paho.mqtt.client as mqtt
import json
import ssl
from datetime import datetime

# HiveMQ Cloud configuration
cluster = "99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud"
port = 8883
username = "UNIVESP"
password = "Univesp2025"
topic = "electricity/building/floor/105"

def send_reading(voltage, current):
    client = mqtt.Client()
    client.username_pw_set(username, password)
    
    # Enable SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    client.tls_set_context(context)
    
    client.connect(cluster, port, 60)
    
    data = {
        "voltage": voltage,
        "current": current,
        "power": voltage * current,
        "apartment": "105",
        "floor": "1",
        "timestamp": datetime.now().isoformat(),
        "broker": "HiveMQ Cloud"
    }
    
    message = json.dumps(data)
    client.publish(topic, message)
    client.disconnect()

# Send a reading
send_reading(230.5, 5.2)
```

### Python - Continuous Monitoring
```python
import paho.mqtt.client as mqtt
import json
import ssl
import time

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if data.get('apartment') == '105':
        print(f"Apartment 105: {data['voltage']}V, {data['current']}A, {data['power']}W")

client = mqtt.Client()
client.username_pw_set("UNIVESP", "Univesp2025")
client.on_message = on_message

# Enable SSL/TLS
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
client.tls_set_context(context)

client.connect("99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud", 8883, 60)
client.subscribe("electricity/building/floor/105")
client.loop_forever()
```

### Arduino/ESP32 Example
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <WiFiClientSecure.h>

const char* ssid = "your-wifi";
const char* password = "your-password";
const char* mqtt_server = "99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_username = "UNIVESP";
const char* mqtt_password = "Univesp2025";
const char* topic = "electricity/building/floor/105";

WiFiClientSecure espClient;
PubSubClient client(espClient);

void sendElectricityData(float voltage, float current) {
  DynamicJsonDocument doc(1024);
  doc["voltage"] = voltage;
  doc["current"] = current;
  doc["power"] = voltage * current;
  doc["apartment"] = "105";
  doc["floor"] = "1";
  doc["timestamp"] = millis();
  doc["broker"] = "HiveMQ Cloud";
  
  char buffer[1024];
  serializeJson(doc, buffer);
  
  client.publish(topic, buffer);
}

void setup() {
  // WiFi setup
  WiFi.begin(ssid, password);
  
  // SSL/TLS setup
  espClient.setInsecure();
  
  // MQTT setup
  client.setServer(mqtt_server, mqtt_port);
  
  // Connect to MQTT
  while (!client.connected()) {
    if (client.connect("ESP32_105", mqtt_username, mqtt_password)) {
      Serial.println("Connected to HiveMQ Cloud");
    }
  }
}

void loop() {
  // Read sensor data and send
  float voltage = readVoltage(); // Your voltage reading function
  float current = readCurrent(); // Your current reading function
  
  sendElectricityData(voltage, current);
  delay(3000); // Send every 3 seconds
}
```

## 📊 Monitoring and Testing

### 1. View MQTT Messages
```bash
# Using mosquitto client with SSL
mosquitto_sub -h 99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud -p 8883 -u UNIVESP -P Univesp2025 -t "electricity/building/floor/105" --cafile /path/to/ca.crt

# Using Python monitor
python monitor_hivemq_cloud_105.py
```

### 2. Test Connection
```python
import paho.mqtt.client as mqtt
import ssl

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud!")
    else:
        print(f"❌ Failed to connect: {rc}")

client = mqtt.Client()
client.username_pw_set("UNIVESP", "Univesp2025")

# Enable SSL/TLS
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
client.tls_set_context(context)

client.on_connect = on_connect
client.connect("99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud", 8883, 60)
client.loop_start()
```

### 3. Web-based MQTT Client
Visit: https://www.hivemq.com/demos/websocket-client/
- Host: `99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud`
- Port: `8884` (WebSocket SSL)
- Username: `UNIVESP`
- Password: `Univesp2025`
- Topic: `electricity/building/floor/105`

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check internet connection
   - Verify cluster address: `99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud`
   - Check port: `8883` (SSL/TLS)
   - Verify credentials: `UNIVESP` / `Univesp2025`

2. **SSL/TLS Errors**
   - Ensure SSL/TLS is enabled
   - Check certificate validation settings
   - Verify port 8883 is used (not 1883)

3. **Authentication Failed**
   - Double-check username: `UNIVESP`
   - Double-check password: `Univesp2025`
   - Ensure credentials are correct in HiveMQ Cloud console

4. **Messages Not Received**
   - Verify topic name: `electricity/building/floor/105`
   - Check JSON format is valid
   - Ensure apartment number is "105"

### Debug Commands
```bash
# Test MQTT connection
python -c "
import paho.mqtt.client as mqtt
import ssl
client = mqtt.Client()
client.username_pw_set('UNIVESP', 'Univesp2025')
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
client.tls_set_context(context)
client.connect('99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud', 8883, 60)
print('Connected!' if client.is_connected() else 'Failed')
"

# Send test message
python test_hivemq_cloud_105.py 230.0 5.0

# Monitor messages
python monitor_hivemq_cloud_105.py
```

## 🎯 Next Steps

1. **Start Sending Data**:
   ```bash
   python test_hivemq_cloud_105.py
   ```

2. **Monitor the Data**:
   ```bash
   python monitor_hivemq_cloud_105.py
   ```

3. **Integrate with Flask App**:
   - Register apartment 105
   - View real-time data on dashboard

4. **Connect Real Sensors**:
   - Use Arduino/ESP32 examples
   - Send actual sensor readings

5. **Set Up Alerts**:
   - Monitor power consumption
   - Set thresholds for alerts

## 📚 Additional Resources

- [HiveMQ Cloud Documentation](https://www.hivemq.com/cloud/)
- [MQTT WebSocket Client](https://www.hivemq.com/demos/websocket-client/)
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/)
- [Arduino MQTT Library](https://github.com/knolleary/pubsubclient)

Happy MQTT publishing with HiveMQ Cloud! 🚀
