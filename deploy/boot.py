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
 A=network.WLAN(network.AP_IF)
 A.active(False)
 f=network.WLAN(network.STA_IF)
 f.active(True)
 s=f.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not f.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  f.connect(SSID,PASSWORD)
  t=0
  while not f.isconnected():
   time.sleep(5)
   t+=5
   print("Waiting for connection... ",t,"seconds") 
   if t>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",f.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

