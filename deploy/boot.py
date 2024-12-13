import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
u="1.0"
gc.collect()
def do_connect():
 import network
 H=network.WLAN(network.AP_IF)
 H.active(False)
 d=network.WLAN(network.STA_IF)
 d.active(True)
 i=d.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(i).decode())
 if not d.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  d.connect(SSID,PASSWORD)
  h=0
  while not d.isconnected():
   time.sleep(5)
   h+=5
   print("Waiting for connection... ",h,"seconds") 
   if h>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",d.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(i).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

