import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
l="1.0"
gc.collect()
def do_connect():
 import network
 G=network.WLAN(network.AP_IF)
 G.active(False)
 w=network.WLAN(network.STA_IF)
 w.active(True)
 s=w.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not w.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  w.connect(SSID,PASSWORD)
  e=0
  while not w.isconnected():
   time.sleep(5)
   e+=5
   print("Waiting for connection... ",e,"seconds") 
   if e>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",w.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

