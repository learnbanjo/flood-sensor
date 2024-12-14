import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
Q="1.0"
gc.collect()
def do_connect():
 import network
 O=network.WLAN(network.AP_IF)
 O.active(False)
 C=network.WLAN(network.STA_IF)
 C.active(True)
 d=C.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(d).decode())
 if not C.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  C.connect(SSID,PASSWORD)
  E=0
  while not C.isconnected():
   time.sleep(5)
   E+=5
   print("Waiting for connection... ",E,"seconds") 
   if E>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",C.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(d).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

