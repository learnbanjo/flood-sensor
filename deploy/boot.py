import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
y="1.0"
gc.collect()
def do_connect():
 import network
 A=network.WLAN(network.AP_IF)
 A.active(False)
 V=network.WLAN(network.STA_IF)
 V.active(True)
 v=V.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(v).decode())
 if not V.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  V.connect(SSID,PASSWORD)
  F=0
  while not V.isconnected():
   time.sleep(5)
   F+=5
   print("Waiting for connection... ",F,"seconds") 
   if F>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",V.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(v).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

