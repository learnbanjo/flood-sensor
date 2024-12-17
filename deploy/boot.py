import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
Y="1.0"
gc.collect()
def do_connect():
 import network
 U=network.WLAN(network.AP_IF)
 U.active(False)
 q=network.WLAN(network.STA_IF)
 q.active(True)
 u=q.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(u).decode())
 if not q.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  q.connect(SSID,PASSWORD)
  R=0
  while not q.isconnected():
   time.sleep(5)
   R+=5
   print("Waiting for connection... ",R,"seconds") 
   if R>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",q.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(u).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

