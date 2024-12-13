import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
R="1.0"
gc.collect()
def do_connect():
 import network
 B=network.WLAN(network.AP_IF)
 B.active(False)
 g=network.WLAN(network.STA_IF)
 g.active(True)
 p=g.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(p).decode())
 if not g.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  g.connect(SSID,PASSWORD)
  U=0
  while not g.isconnected():
   time.sleep(5)
   U+=5
   print("Waiting for connection... ",U,"seconds") 
   if U>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",g.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(p).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

