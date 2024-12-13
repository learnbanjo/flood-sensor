import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
s="1.0"
gc.collect()
def do_connect():
 import network
 i=network.WLAN(network.AP_IF)
 i.active(False)
 B=network.WLAN(network.STA_IF)
 B.active(True)
 e=B.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(e).decode())
 if not B.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  B.connect(SSID,PASSWORD)
  u=0
  while not B.isconnected():
   time.sleep(5)
   u+=5
   print("Waiting for connection... ",u,"seconds") 
   if u>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",B.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(e).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

