import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
T="1.0"
gc.collect()
def do_connect():
 import network
 c=network.WLAN(network.AP_IF)
 c.active(False)
 Y=network.WLAN(network.STA_IF)
 Y.active(True)
 r=Y.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(r).decode())
 if not Y.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Y.connect(SSID,PASSWORD)
  m=0
  while not Y.isconnected():
   time.sleep(5)
   m+=5
   print("Waiting for connection... ",m,"seconds") 
   if m>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Y.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(r).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

