import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
H="1.0"
gc.collect()
def do_connect():
 import network
 N=network.WLAN(network.AP_IF)
 N.active(False)
 V=network.WLAN(network.STA_IF)
 V.active(True)
 l=V.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(l).decode())
 if not V.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  V.connect(SSID,PASSWORD)
  a=0
  while not V.isconnected():
   time.sleep(5)
   a+=5
   print("Waiting for connection... ",a,"seconds") 
   if a>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",V.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(l).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

