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
 r=network.WLAN(network.AP_IF)
 r.active(False)
 t=network.WLAN(network.STA_IF)
 t.active(True)
 E=t.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(E).decode())
 if not t.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  t.connect(SSID,PASSWORD)
  z=0
  while not t.isconnected():
   time.sleep(5)
   z+=5
   print("Waiting for connection... ",z,"seconds") 
   if z>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",t.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(E).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

