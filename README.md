# Flood Sensor

This MicroPython code is writting for ESP3266 connecting to a flood sensor
It has a simple HTTP server responds to request with web/dry state
It will automatically updates code when a new version becomes available

---

Requirement:
Device: MicroPython for ESP8266  version='v1.24.0 on 2024-10-25' or newer
MicroPython Ampy https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy
Serial Terminal such as CoolTerm https://freeware.the-meiers.org/

To use this code:

1. Create a file named `DEVICE_CONFIG.py` on your MicroPython device, which contains variables as follow:

    ```python
    DEVICE_NAME = "device host name" # Descriptive name for the device
    DEVICE_TYPE = "Flood Sensor" # Sensor Type. "Flood Sensor", "Pressure Sensor"
    DEVICE_KEY = "" #device private key for future use cases
    SSID = "my wifi hotspot name"
    PASSWORD = "wifi password". #Use "" for no password
    ANALOG_SENSOR_PIN = 0 # ESP8266 ADC pin is 0. Set to "" to disable
    DIGITAL_SENSOR_PIN = 14 # ESP8266 GPIO pin is 14. Set to "" to disable
    ```


2. connect device to the computer. If the device use PIN 15, make sure it's
in the low state. For flood sensor, that means to put the sensor in the wet 
state (in the water)

3. make sure terminal is not connected to the device. run installation script
    python3 install.sh

4. provision a WAP, such as Aerhive, with the ssid and password matching those
in the DEVICE_CONFIG.py

5. Reboot device (press RST button), connect computer terminal ( such as 
CoolTerm). you should see the terminal log showing "connected to " WAP name.

6. Access the device using browser. Open the device IP in the URL
