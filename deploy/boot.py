import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
Y="1.0"
gc.collect()
def do_connect():
 import network
 A=network.WLAN(network.AP_IF)
 A.active(False)
 y=network.WLAN(network.STA_IF)
 y.active(True)
 V=y.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(V).decode())
 if not y.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  y.connect(SSID,PASSWORD)
  a=0
  while not y.isconnected():
   time.sleep(5)
   a+=5
   print("Waiting for connection... ",a,"seconds") 
   if a>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",y.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(V).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

