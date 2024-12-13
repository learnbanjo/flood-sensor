import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
I="1.0"
gc.collect()
def do_connect():
 import network
 o=network.WLAN(network.AP_IF)
 o.active(False)
 d=network.WLAN(network.STA_IF)
 d.active(True)
 x=d.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 if not d.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  d.connect(SSID,PASSWORD)
  P=0
  while not d.isconnected():
   time.sleep(5)
   P+=5
   print("Waiting for connection... ",P,"seconds") 
   if P>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",d.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

