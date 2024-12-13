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
 x=network.WLAN(network.AP_IF)
 x.active(False)
 U=network.WLAN(network.STA_IF)
 U.active(True)
 z=U.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 if not U.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  U.connect(SSID,PASSWORD)
  T=0
  while not U.isconnected():
   time.sleep(5)
   T+=5
   print("Waiting for connection... ",T,"seconds") 
   if T>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",U.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

