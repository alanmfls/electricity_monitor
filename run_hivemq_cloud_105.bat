@echo off
echo HiveMQ Cloud Test for Apartment 105
echo ===================================
echo.
echo Cluster: 99c268dc5c2849e4a28a6723863ddb8d.s1.eu.hivemq.cloud
echo Username: UNIVESP
echo Apartment: 105
echo.
echo Options:
echo 1. Continuous simulation (default)
echo 2. Single reading
echo 3. Monitor incoming data
echo.
set /p choice="Choose option (1, 2, or 3): "

if "%choice%"=="2" (
    set /p voltage="Enter voltage (e.g., 230.5): "
    set /p current="Enter current (e.g., 5.2): "
    echo.
    echo Sending single reading to HiveMQ Cloud...
    python test_hivemq_cloud_105.py %voltage% %current%
) else if "%choice%"=="3" (
    echo.
    echo Starting monitor for apartment 105...
    echo Press Ctrl+C to stop
    echo.
    python monitor_hivemq_cloud_105.py
) else (
    echo.
    echo Starting continuous simulation...
    echo Press Ctrl+C to stop
    echo.
    python test_hivemq_cloud_105.py
)

pause
