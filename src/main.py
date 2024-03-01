from machine import Pin
from ota import OTAUpdater
from DEVICE_CONFIG import SENSOR_PIN, SSID, PASSWORD

dry = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)

import socket

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
firmware_url = "https://raw.githubusercontent.com/learnbanjo/flood-sensor/main"

s = socket.socket()
s.bind(addr)
s.listen(1)

while True:
    cl, addr = s.accept()
    print("client connected from", addr)
    cl_file = cl.makefile("rwb", 0)
    while True:
        line = cl_file.readline()
        if not line or line == b"\r\n":
            break
    if dry.value() == 1:
        wd = "dry"
    else:
        wd = "wet"
    cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
    cl.send(wd)
    cl.close()

    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "ota.py")
    ota_updater.download_and_install_update_if_available()
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
    ota_updater.download_and_install_update_if_available()
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "boot.py")
    ota_updater.download_and_install_update_if_available()

