# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID, PASSWORD, DEVICE_NAME

VERSION = "1.0"


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
        waittime = 0
        while not sta_if.isconnected():
            time.sleep(5)
            waittime += 5
            print("Waiting for connection... ", waittime, "seconds")    
            if waittime > 30:
                print("Connection failed. Rebooting...")
                machine.reset()
            pass
    print("\nnetwork config:", sta_if.ifconfig())
    print("\nMAC Address:", ubinascii.hexlify(wlan_mac).decode())
    print("Connecting to SSID:", SSID)

print("\n\n\nSensor Booting Up...")
print("\nmircopython version:", os.uname())
print("\nDevice Name:", DEVICE_NAME)

do_connect()
