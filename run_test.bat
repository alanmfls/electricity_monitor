@echo off
echo Starting Multi-Apartment Electricity Monitor Test Environment
echo =============================================================

echo.
echo 1. Starting MQTT multi-apartment data simulator...
start "MQTT Multi-Apartment Simulator" python test_multi_apartment.py

echo.
echo 2. Waiting 3 seconds for MQTT simulator to start...
timeout /t 3 /nobreak > nul

echo.
echo 3. Starting Electricity Monitor Application...
echo    Web interface: http://localhost:5000
echo    Simulating apartments: 101, 102, 201, 202, 301, 302
echo    Press Ctrl+C to stop both applications
echo.

python app.py

echo.
echo Stopping applications...
taskkill /f /im python.exe > nul 2>&1
echo Done!
pause