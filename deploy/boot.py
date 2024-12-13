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
 e=network.WLAN(network.AP_IF)
 e.active(False)
 X=network.WLAN(network.STA_IF)
 X.active(True)
 n=X.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(n).decode())
 if not X.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  X.connect(SSID,PASSWORD)
  w=0
  while not X.isconnected():
   time.sleep(5)
   w+=5
   print("Waiting for connection... ",w,"seconds") 
   if w>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",X.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(n).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

