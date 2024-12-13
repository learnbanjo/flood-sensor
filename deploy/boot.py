import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
u="1.0"
gc.collect()
def do_connect():
 import network
 j=network.WLAN(network.AP_IF)
 j.active(False)
 B=network.WLAN(network.STA_IF)
 B.active(True)
 A=B.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(A).decode())
 if not B.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  B.connect(SSID,PASSWORD)
  T=0
  while not B.isconnected():
   time.sleep(5)
   T+=5
   print("Waiting for connection... ",T,"seconds") 
   if T>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",B.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(A).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

