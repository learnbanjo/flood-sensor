# Flood Sensor

This MicroPython code is writting for ESP3266 connecting to a flood sensor
It has a simple HTTP server responds to request with web/dry state
It will automatically updates code when a new version becomes available

---

To use this code:

1. Create a file named `DEVICE_CONFIG.py` on your MicroPython device, which contains three variables: `SSID`, `PASSWORD`, `DEVICE_NAME`:

    ```python
    SSID = "my wifi hotspot name"
    PASSWORD = "wifi password"
    DEVICE_NAME = "device host name"
    ```