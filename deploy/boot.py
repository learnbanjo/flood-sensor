import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
h="1.0"
gc.collect()
def do_connect():
 import network
 o=network.WLAN(network.AP_IF)
 o.active(False)
 J=network.WLAN(network.STA_IF)
 J.active(True)
 O=J.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 if not J.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  J.connect(SSID,PASSWORD)
  b=0
  while not J.isconnected():
   time.sleep(5)
   b+=5
   print("Waiting for connection... ",b,"seconds") 
   if b>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",J.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

