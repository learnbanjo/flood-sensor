import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
b="1.0"
gc.collect()
def do_connect():
 import network
 H=network.WLAN(network.AP_IF)
 H.active(False)
 k=network.WLAN(network.STA_IF)
 k.active(True)
 O=k.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 if not k.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  k.connect(SSID,PASSWORD)
  e=0
  while not k.isconnected():
   time.sleep(5)
   e+=5
   print("Waiting for connection... ",e,"seconds") 
   if e>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",k.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

