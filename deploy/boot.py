import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
t="1.0"
gc.collect()
def do_connect():
 import network
 g=network.WLAN(network.AP_IF)
 g.active(False)
 o=network.WLAN(network.STA_IF)
 o.active(True)
 l=o.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(l).decode())
 if not o.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  o.connect(SSID,PASSWORD)
  D=0
  while not o.isconnected():
   time.sleep(5)
   D+=5
   print("Waiting for connection... ",D,"seconds") 
   if D>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",o.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(l).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

