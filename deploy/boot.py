import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
D="1.0"
gc.collect()
def do_connect():
 import network
 N=network.WLAN(network.AP_IF)
 N.active(False)
 B=network.WLAN(network.STA_IF)
 B.active(True)
 C=B.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(C).decode())
 if not B.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  B.connect(SSID,PASSWORD)
  c=0
  while not B.isconnected():
   time.sleep(5)
   c+=5
   print("Waiting for connection... ",c,"seconds") 
   if c>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",B.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(C).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

