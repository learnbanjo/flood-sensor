import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
a="1.0"
gc.collect()
def do_connect():
 import network
 b=network.WLAN(network.AP_IF)
 b.active(False)
 z=network.WLAN(network.STA_IF)
 z.active(True)
 k=z.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(k).decode())
 if not z.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  z.connect(SSID,PASSWORD)
  o=0
  while not z.isconnected():
   time.sleep(5)
   o+=5
   print("Waiting for connection... ",o,"seconds") 
   if o>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",z.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(k).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

