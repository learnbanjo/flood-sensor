import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
d="1.0"
gc.collect()
def do_connect():
 import network
 s=network.WLAN(network.AP_IF)
 s.active(False)
 E=network.WLAN(network.STA_IF)
 E.active(True)
 a=E.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(a).decode())
 if not E.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  E.connect(SSID,PASSWORD)
  o=0
  while not E.isconnected():
   time.sleep(5)
   o+=5
   print("Waiting for connection... ",o,"seconds") 
   if o>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",E.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(a).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

