# Flood Sensor

This MicroPython code is writting for ESP3266 connecting to a flood sensor
It has a simple HTTP server responds to request with web/dry state
It will automatically updates code when a new version becomes available

---

Device Requirement:
MicroPython for ESP8266  version='v1.24.0 on 2024-10-25' or newer

To use this code:

1. Create a file named `DEVICE_CONFIG.py` on your MicroPython device, which contains variables as follow:

    ```python
    SSID = "my wifi hotspot name"
    PASSWORD = "wifi password". #Use "" for no password
    DEVICE_NAME = "device host name" # Descriptive name for the device
    DEVICE_TYPE = "Flood Sensor" # Sensor Type. "Flood Sensor", "Pressure Sensor"
    ANALOG_SENSOR_PIN = 0 # ESP8266 ADC pin is 0. Set to "" to disable
    DIGITAL_SENSOR_PIN = 14 # ESP8266 GPIO pin is 14. Set to "" to disable
```
