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
 m=network.WLAN(network.AP_IF)
 m.active(False)
 I=network.WLAN(network.STA_IF)
 I.active(True)
 y=I.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(y).decode())
 if not I.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  I.connect(SSID,PASSWORD)
  z=0
  while not I.isconnected():
   time.sleep(5)
   z+=5
   print("Waiting for connection... ",z,"seconds") 
   if z>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",I.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(y).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

