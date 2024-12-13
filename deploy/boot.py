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
 I=network.WLAN(network.AP_IF)
 I.active(False)
 u=network.WLAN(network.STA_IF)
 u.active(True)
 B=u.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(B).decode())
 if not u.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  u.connect(SSID,PASSWORD)
  e=0
  while not u.isconnected():
   time.sleep(5)
   e+=5
   print("Waiting for connection... ",e,"seconds") 
   if e>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",u.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(B).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

