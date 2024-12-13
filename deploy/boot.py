import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
c="1.0"
gc.collect()
def do_connect():
 import network
 y=network.WLAN(network.AP_IF)
 y.active(False)
 E=network.WLAN(network.STA_IF)
 E.active(True)
 b=E.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(b).decode())
 if not E.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  E.connect(SSID,PASSWORD)
  A=0
  while not E.isconnected():
   time.sleep(5)
   A+=5
   print("Waiting for connection... ",A,"seconds") 
   if A>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",E.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(b).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

