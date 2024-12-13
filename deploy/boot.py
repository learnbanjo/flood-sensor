import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
v="1.0"
gc.collect()
def do_connect():
 import network
 d=network.WLAN(network.AP_IF)
 d.active(False)
 r=network.WLAN(network.STA_IF)
 r.active(True)
 c=r.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(c).decode())
 if not r.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  r.connect(SSID,PASSWORD)
  K=0
  while not r.isconnected():
   time.sleep(5)
   K+=5
   print("Waiting for connection... ",K,"seconds") 
   if K>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",r.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(c).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

