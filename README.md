# Flood Sensor

This MicroPython code is written for ESP3266 connecting to a digital or analog sensor.
It has a simple HTTP server responding to requests with the state of the sensor.
It supports code when a new version becomes available.

---
# Deply the code
## Supported Device
ESP8266

## Prepare your computer:
**Serial Terminal:** Install a serial terminal tool such as CoolTerm https://freeware.the-meiers.org/ so you can see the ESP output

**Ampy:** Install Ampy so you can upload Python code: MicroPython Ampy https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy

**MicroPython firmware:** Download MicroPython code newer than 2024-10-25. For ESP8266, that would be version='v1.24.0 on 2024-10-25' (https://micropython.org/download/ESP8266_GENERIC/)

## Prepare device with the proper firmware:
Follow instruction at https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#deploying-the-firmware and install the firmware 

## Install/update code to the device:

1. Copy DEVICE_CONFIG_template.py to DEVICE_CONFIG.py if you don't have a DEVICE_CONFIG.py yet

2. Modify DEVICE_CONFIG.py according to the setting of the device.

3. Connect device to the computer. **Attention!** If the device use PIN 15, make sure it's in the low state otherwise the device will not boot up properly. For flood sensor, that means to put the sensor in the wet state (in the water) 

4. Make sure terminal is not connected to the device so the serial port is not occupied. Run installation script as follow:

```
python3 install.sh
```

## Provision a WAP, such as Aerhive

Provision WAP with the ssid and password matching those
in the DEVICE_CONFIG.py

## Verify the setup

1. Connect termial ( such as Cool Term). The baudrate is 115200
2. Reboot device (press RST button). you should see the terminal log showing "connected to " WAP name.
3. Access the device using browser. Open the device IP in the URL. You should see the device respond with data

