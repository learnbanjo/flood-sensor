from DEVICE_CONFIG import DEVICE_NAME, SSID, PASSWORD, OTA_ENABLED
# DEVICE_NAME default depends on the device
# SSID default depends on the device
# PASSWORD default is none ""
# OTA_ENABLED default is "false"

SENSOR_PIN = 15

from machine import Pin
dry = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)

import socket

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

while True:
    cl, addr = s.accept()
    print("client connected from", addr)
    print(free(full=True))

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
    message = "{"
    message = message + "\"deviceName\":\"" + DEVICE_NAME + "\""
    message = message + ",\"AP\":\"" + SSID + "\""    
    message = message + ",\"state\":\"" + wd + "\""    
    message = message + "}"
    cl.send(message)

    if (OTA_ENABLED == "true"):
        from ota import OTAUpdater
        firmware_url = "https://raw.githubusercontent.com/learnbanjo/flood-sensor/main/src/"
        try:
            ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "ota.py")
            ota_updater.download_and_install_update_if_available()
            ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
            ota_updater.download_and_install_update_if_available()
            ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "boot.py")
            ota_updater.download_and_install_update_if_available()
        except Exception as err:
            print("OTA failed.")
            print("Unexpected error:", err, " type:", type(err))
            cl.send('<p>OTA failed.')
            cl.send("Unexpected errorr=", err, " type=", type(err))
    cl.close()
