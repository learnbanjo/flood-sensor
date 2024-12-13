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
 b=network.WLAN(network.AP_IF)
 b.active(False)
 Q=network.WLAN(network.STA_IF)
 Q.active(True)
 c=Q.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(c).decode())
 if not Q.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Q.connect(SSID,PASSWORD)
  v=0
  while not Q.isconnected():
   time.sleep(5)
   v+=5
   print("Waiting for connection... ",v,"seconds") 
   if v>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Q.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(c).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

