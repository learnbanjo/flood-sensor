import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
F="1.0"
gc.collect()
def do_connect():
 import network
 Y=network.WLAN(network.AP_IF)
 Y.active(False)
 v=network.WLAN(network.STA_IF)
 v.active(True)
 U=v.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(U).decode())
 if not v.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  v.connect(SSID,PASSWORD)
  k=0
  while not v.isconnected():
   time.sleep(5)
   k+=5
   print("Waiting for connection... ",k,"seconds") 
   if k>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",v.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(U).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

