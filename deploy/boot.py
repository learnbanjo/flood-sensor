import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
y="1.0"
gc.collect()
def do_connect():
 import network
 B=network.WLAN(network.AP_IF)
 B.active(False)
 b=network.WLAN(network.STA_IF)
 b.active(True)
 s=b.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not b.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  b.connect(SSID,PASSWORD)
  C=0
  while not b.isconnected():
   time.sleep(5)
   C+=5
   print("Waiting for connection... ",C,"seconds") 
   if C>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",b.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

