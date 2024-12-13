import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
P="1.0"
gc.collect()
def do_connect():
 import network
 d=network.WLAN(network.AP_IF)
 d.active(False)
 M=network.WLAN(network.STA_IF)
 M.active(True)
 a=M.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(a).decode())
 if not M.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  M.connect(SSID,PASSWORD)
  r=0
  while not M.isconnected():
   time.sleep(5)
   r+=5
   print("Waiting for connection... ",r,"seconds") 
   if r>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",M.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(a).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

