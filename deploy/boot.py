import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
g="1.0"
gc.collect()
def do_connect():
 import network
 H=network.WLAN(network.AP_IF)
 H.active(False)
 m=network.WLAN(network.STA_IF)
 m.active(True)
 x=m.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 if not m.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  m.connect(SSID,PASSWORD)
  d=0
  while not m.isconnected():
   time.sleep(5)
   d+=5
   print("Waiting for connection... ",d,"seconds") 
   if d>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",m.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

