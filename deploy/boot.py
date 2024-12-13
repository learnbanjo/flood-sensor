import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
e="1.0"
gc.collect()
def do_connect():
 import network
 n=network.WLAN(network.AP_IF)
 n.active(False)
 U=network.WLAN(network.STA_IF)
 U.active(True)
 T=U.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(T).decode())
 if not U.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  U.connect(SSID,PASSWORD)
  w=0
  while not U.isconnected():
   time.sleep(5)
   w+=5
   print("Waiting for connection... ",w,"seconds") 
   if w>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",U.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(T).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

