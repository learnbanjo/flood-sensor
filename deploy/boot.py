import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
e="1.0"
gc.collect()
def do_connect():
 import network
 c=network.WLAN(network.AP_IF)
 c.active(False)
 U=network.WLAN(network.STA_IF)
 U.active(True)
 o=U.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(o).decode())
 if not U.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  U.connect(SSID,PASSWORD)
  D=0
  while not U.isconnected():
   time.sleep(5)
   D+=5
   print("Waiting for connection... ",D,"seconds") 
   if D>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",U.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(o).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

