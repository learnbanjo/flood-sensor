import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
t="1.0"
gc.collect()
def do_connect():
 import network
 O=network.WLAN(network.AP_IF)
 O.active(False)
 f=network.WLAN(network.STA_IF)
 f.active(True)
 x=f.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 if not f.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  f.connect(SSID,PASSWORD)
  g=0
  while not f.isconnected():
   time.sleep(5)
   g+=5
   print("Waiting for connection... ",g,"seconds") 
   if g>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",f.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(x).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

