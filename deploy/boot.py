import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
p="1.0"
gc.collect()
def do_connect():
 import network
 y=network.WLAN(network.AP_IF)
 y.active(False)
 T=network.WLAN(network.STA_IF)
 T.active(True)
 v=T.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(v).decode())
 if not T.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  T.connect(SSID,PASSWORD)
  d=0
  while not T.isconnected():
   time.sleep(5)
   d+=5
   print("Waiting for connection... ",d,"seconds") 
   if d>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",T.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(v).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

