import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
L="1.0"
gc.collect()
def do_connect():
 import network
 h=network.WLAN(network.AP_IF)
 h.active(False)
 Y=network.WLAN(network.STA_IF)
 Y.active(True)
 z=Y.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 if not Y.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Y.connect(SSID,PASSWORD)
  A=0
  while not Y.isconnected():
   time.sleep(5)
   A+=5
   print("Waiting for connection... ",A,"seconds") 
   if A>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Y.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

