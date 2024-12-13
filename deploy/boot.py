import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
K="1.0"
gc.collect()
def do_connect():
 import network
 y=network.WLAN(network.AP_IF)
 y.active(False)
 i=network.WLAN(network.STA_IF)
 i.active(True)
 c=i.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(c).decode())
 if not i.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  i.connect(SSID,PASSWORD)
  e=0
  while not i.isconnected():
   time.sleep(5)
   e+=5
   print("Waiting for connection... ",e,"seconds") 
   if e>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",i.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(c).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

