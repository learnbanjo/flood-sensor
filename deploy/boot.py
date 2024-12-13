import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
G="1.0"
gc.collect()
def do_connect():
 import network
 c=network.WLAN(network.AP_IF)
 c.active(False)
 g=network.WLAN(network.STA_IF)
 g.active(True)
 k=g.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(k).decode())
 if not g.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  g.connect(SSID,PASSWORD)
  h=0
  while not g.isconnected():
   time.sleep(5)
   h+=5
   print("Waiting for connection... ",h,"seconds") 
   if h>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",g.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(k).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

