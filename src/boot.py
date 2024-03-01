# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import os
import ubinascii
from DEVICE_CONFIG import SSID, PASSWORD, DEVICE_NAME

gc.collect()


def do_connect():
    import network

    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    wlan_mac = sta_if.config("mac")
    print("\nMAC Address:", ubinascii.hexlify(wlan_mac).decode())
    if not sta_if.isconnected():
        print("\nConnecting to network...")
        print("Connecting to SSID:", SSID)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print("\nnetwork config:", sta_if.ifconfig())


print("\n\n\nFlood Sensor Booting Up...")
print("\nmircopython version:", os.uname())
print("\nDevice Name:", DEVICE_NAME)

do_connect()
