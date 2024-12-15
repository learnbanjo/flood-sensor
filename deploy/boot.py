import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
k="1.0"
gc.collect()
def do_connect():
 import network
 B=network.WLAN(network.AP_IF)
 B.active(False)
 p=network.WLAN(network.STA_IF)
 p.active(True)
 V=p.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(V).decode())
 if not p.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  p.connect(SSID,PASSWORD)
  u=0
  while not p.isconnected():
   time.sleep(5)
   u+=5
   print("Waiting for connection... ",u,"seconds") 
   if u>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",p.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(V).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

