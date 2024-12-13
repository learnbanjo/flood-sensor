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
 b=network.WLAN(network.AP_IF)
 b.active(False)
 X=network.WLAN(network.STA_IF)
 X.active(True)
 d=X.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(d).decode())
 if not X.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  X.connect(SSID,PASSWORD)
  H=0
  while not X.isconnected():
   time.sleep(5)
   H+=5
   print("Waiting for connection... ",H,"seconds") 
   if H>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",X.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(d).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

