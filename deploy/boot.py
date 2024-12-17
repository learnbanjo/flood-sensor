import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
q="1.0"
gc.collect()
def do_connect():
 import network
 b=network.WLAN(network.AP_IF)
 b.active(False)
 c=network.WLAN(network.STA_IF)
 c.active(True)
 R=c.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(R).decode())
 if not c.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  c.connect(SSID,PASSWORD)
  X=0
  while not c.isconnected():
   time.sleep(5)
   X+=5
   print("Waiting for connection... ",X,"seconds") 
   if X>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",c.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(R).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

