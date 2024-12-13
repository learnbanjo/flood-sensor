import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
G="1.0"
gc.collect()
def do_connect():
 import network
 c=network.WLAN(network.AP_IF)
 c.active(False)
 l=network.WLAN(network.STA_IF)
 l.active(True)
 w=l.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(w).decode())
 if not l.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  l.connect(SSID,PASSWORD)
  T=0
  while not l.isconnected():
   time.sleep(5)
   T+=5
   print("Waiting for connection... ",T,"seconds") 
   if T>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",l.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(w).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

