import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
g="1.0"
gc.collect()
def do_connect():
 import network
 b=network.WLAN(network.AP_IF)
 b.active(False)
 N=network.WLAN(network.STA_IF)
 N.active(True)
 s=N.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not N.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  N.connect(SSID,PASSWORD)
  Q=0
  while not N.isconnected():
   time.sleep(5)
   Q+=5
   print("Waiting for connection... ",Q,"seconds") 
   if Q>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",N.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

