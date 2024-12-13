import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
s="1.0"
gc.collect()
def do_connect():
 import network
 h=network.WLAN(network.AP_IF)
 h.active(False)
 b=network.WLAN(network.STA_IF)
 b.active(True)
 r=b.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(r).decode())
 if not b.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  b.connect(SSID,PASSWORD)
  T=0
  while not b.isconnected():
   time.sleep(5)
   T+=5
   print("Waiting for connection... ",T,"seconds") 
   if T>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",b.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(r).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

