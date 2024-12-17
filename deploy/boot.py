import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
N="1.0"
gc.collect()
def do_connect():
 import network
 d=network.WLAN(network.AP_IF)
 d.active(False)
 o=network.WLAN(network.STA_IF)
 o.active(True)
 x=o.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 if not o.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  o.connect(SSID,PASSWORD)
  U=0
  while not o.isconnected():
   time.sleep(5)
   U+=5
   print("Waiting for connection... ",U,"seconds") 
   if U>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",o.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

