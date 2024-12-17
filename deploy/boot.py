import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
b="1.0"
gc.collect()
def do_connect():
 import network
 C=network.WLAN(network.AP_IF)
 C.active(False)
 K=network.WLAN(network.STA_IF)
 K.active(True)
 z=K.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 if not K.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  K.connect(SSID,PASSWORD)
  e=0
  while not K.isconnected():
   time.sleep(5)
   e+=5
   print("Waiting for connection... ",e,"seconds") 
   if e>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",K.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

