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
 m=network.WLAN(network.AP_IF)
 m.active(False)
 S=network.WLAN(network.STA_IF)
 S.active(True)
 E=S.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(E).decode())
 if not S.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  S.connect(SSID,PASSWORD)
  f=0
  while not S.isconnected():
   time.sleep(5)
   f+=5
   print("Waiting for connection... ",f,"seconds") 
   if f>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",S.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(E).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

