# This is a mock module for the network module in the ESP8266 micropython library

class WLAN:
    STA_IF = 0
    AP_IF = 1
    def __init__(self, mode):
        self.mode = mode
        print(f"WLAN({mode})")
    def active(self, active):
        self.active = active
        print(f"WLAN.active({active})")
    def connect(self, ssid, password):
        self.ssid = ssid
        self.password = password
        print(f"WLAN.connect({ssid}, {password})")
    def isconnected(self):
        return True
    def config(self, param):
        return "mac"