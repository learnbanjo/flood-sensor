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
 X=network.WLAN(network.AP_IF)
 X.active(False)
 x=network.WLAN(network.STA_IF)
 x.active(True)
 e=x.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(e).decode())
 if not x.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  x.connect(SSID,PASSWORD)
  G=0
  while not x.isconnected():
   time.sleep(5)
   G+=5
   print("Waiting for connection... ",G,"seconds") 
   if G>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",x.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(e).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

