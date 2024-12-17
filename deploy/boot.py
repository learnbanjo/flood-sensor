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
 E=network.WLAN(network.AP_IF)
 E.active(False)
 Q=network.WLAN(network.STA_IF)
 Q.active(True)
 s=Q.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not Q.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Q.connect(SSID,PASSWORD)
  c=0
  while not Q.isconnected():
   time.sleep(5)
   c+=5
   print("Waiting for connection... ",c,"seconds") 
   if c>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Q.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

