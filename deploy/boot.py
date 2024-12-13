import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
O="1.0"
gc.collect()
def do_connect():
 import network
 s=network.WLAN(network.AP_IF)
 s.active(False)
 R=network.WLAN(network.STA_IF)
 R.active(True)
 E=R.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(E).decode())
 if not R.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  R.connect(SSID,PASSWORD)
  H=0
  while not R.isconnected():
   time.sleep(5)
   H+=5
   print("Waiting for connection... ",H,"seconds") 
   if H>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",R.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(E).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

