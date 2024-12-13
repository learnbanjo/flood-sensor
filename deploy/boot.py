import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
p="1.0"
gc.collect()
def do_connect():
 import network
 S=network.WLAN(network.AP_IF)
 S.active(False)
 W=network.WLAN(network.STA_IF)
 W.active(True)
 l=W.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(l).decode())
 if not W.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  W.connect(SSID,PASSWORD)
  z=0
  while not W.isconnected():
   time.sleep(5)
   z+=5
   print("Waiting for connection... ",z,"seconds") 
   if z>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",W.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(l).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

