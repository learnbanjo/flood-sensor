import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
O="1.0"
gc.collect()
def do_connect():
 import network
 i=network.WLAN(network.AP_IF)
 i.active(False)
 b=network.WLAN(network.STA_IF)
 b.active(True)
 B=b.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(B).decode())
 if not b.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  b.connect(SSID,PASSWORD)
  j=0
  while not b.isconnected():
   time.sleep(5)
   j+=5
   print("Waiting for connection... ",j,"seconds") 
   if j>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",b.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(B).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

