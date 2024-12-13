import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
g="1.0"
gc.collect()
def do_connect():
 import network
 W=network.WLAN(network.AP_IF)
 W.active(False)
 Y=network.WLAN(network.STA_IF)
 Y.active(True)
 h=Y.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(h).decode())
 if not Y.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Y.connect(SSID,PASSWORD)
  U=0
  while not Y.isconnected():
   time.sleep(5)
   U+=5
   print("Waiting for connection... ",U,"seconds") 
   if U>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Y.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(h).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

