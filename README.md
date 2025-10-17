# Multi-Apartment Electricity Monitoring Application

A web-based application for monitoring electricity consumption in multi-apartment buildings. Each apartment (user) has their own MQTT connection and dashboard, allowing individual monitoring of electricity consumption per apartment/floor. The app receives voltage and current data via MQTT in JSON format, calculates power consumption, and provides user authentication with apartment-specific data isolation.

## Features

- **Multi-Apartment Support**: Each user represents an apartment/floor with isolated data
- **Real-time Monitoring**: Receives voltage and current data via MQTT per apartment
- **Power Calculation**: Automatically calculates power (P = V × I) in Watts
- **User Authentication**: Secure login with email, password, and apartment number
- **Data Storage**: Stores power consumption history per apartment in SQLite database
- **Web Interface**: Modern, responsive dashboard for apartment-specific monitoring
- **History Tracking**: View past power consumption readings per apartment
- **MQTT Topic Isolation**: Each apartment has its own MQTT topic for data isolation

## Requirements

- Python 3.7+
- MQTT Broker (e.g., Mosquitto)
- Web browser

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   MQTT_BROKER=localhost
   MQTT_PORT=1883
   MQTT_TOPIC=electricity/data
   ```

4. **Set up MQTT Broker** (if not already running):
   - Install Mosquitto: https://mosquitto.org/download/
   - Start the broker: `mosquitto -v`

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   - Open your browser and go to `http://localhost:5000`
   - Register a new account or login with existing credentials

3. **Send MQTT data**:
   The application expects JSON messages on apartment-specific MQTT topics with the following format:
   
   **Topic Pattern**: `electricity/building/floor/{apartment_number}`
   
   **Message Format**:
   ```json
   {
     "voltage": 220.5,
     "current": 2.3,
     "apartment": "101",
     "floor": "1"
   }
   ```

   **Example MQTT publish commands**:
   ```bash
   # For apartment 101
   mosquitto_pub -h localhost -t "electricity/building/floor/101" -m '{"voltage": 220.5, "current": 2.3, "apartment": "101", "floor": "1"}'
   
   # For apartment 201
   mosquitto_pub -h localhost -t "electricity/building/floor/201" -m '{"voltage": 230.1, "current": 1.8, "apartment": "201", "floor": "2"}'
   ```

## MQTT Data Format

The application expects JSON messages with the following structure:

**Topic**: `electricity/building/floor/{apartment_number}`

**Message**:
```json
{
  "voltage": 220.5,    // Voltage in Volts (float)
  "current": 2.3,      // Current in Amperes (float)
  "apartment": "101",  // Apartment number (string)
  "floor": "1"         // Floor number (string)
}
```

The application will automatically calculate power using the formula: **Power = Voltage × Current**

### MQTT Topic Structure

- **Base Topic**: `electricity/building`
- **Apartment Topics**: `electricity/building/floor/{apartment_number}`
- **Examples**:
  - Apartment 101: `electricity/building/floor/101`
  - Apartment 201: `electricity/building/floor/201`
  - Apartment 302: `electricity/building/floor/302`

## Web Interface

### Dashboard
- Real-time display of voltage, current, and calculated power
- Auto-refreshing data every 2 seconds
- Save current readings to history
- Connection status indicators

### History
- View past power consumption readings
- Statistics: average power, maximum power, total readings
- Sortable table with timestamps

### Authentication
- User registration with email and password
- Secure login system
- Session management

## Database Schema

### Users Table
- `id`: Primary key
- `email`: User email (unique)
- `password_hash`: Hashed password
- `created_at`: Registration timestamp

### Power Readings Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `voltage`: Voltage reading in Volts
- `current`: Current reading in Amperes
- `power`: Calculated power in Watts
- `timestamp`: Reading timestamp

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `MQTT_BROKER`: MQTT broker hostname/IP
- `MQTT_PORT`: MQTT broker port (default: 1883)
- `MQTT_TOPIC`: MQTT topic for electricity data

### MQTT Topics
- **electricity/data**: Topic for receiving voltage and current data

## Security Notes

⚠️ **Important**: This is a development version. For production use:

1. Change the `SECRET_KEY` to a secure random string
2. Implement proper password hashing (bcrypt)
3. Use HTTPS for web interface
4. Secure MQTT broker with authentication
5. Use a production database (PostgreSQL, MySQL)
6. Implement proper error handling and logging

## Troubleshooting

### MQTT Connection Issues
- Ensure MQTT broker is running
- Check broker hostname and port in `.env` file
- Verify network connectivity to MQTT broker

### Database Issues
- The SQLite database is created automatically on first run
- Check file permissions in the application directory

### Web Interface Issues
- Ensure port 5000 is not in use by another application
- Check firewall settings if accessing remotely

## API Endpoints

- `GET /`: Dashboard (requires authentication)
- `GET /login`: Login page
- `POST /login`: Process login
- `GET /register`: Registration page
- `POST /register`: Process registration
- `GET /logout`: Logout user
- `GET /history`: View consumption history
- `GET /api/power-data`: Get current power data (JSON)
- `POST /api/save-reading`: Save current reading to history

## License

This project is open source and available under the MIT License.
