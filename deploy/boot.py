import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
i="1.0"
gc.collect()
def do_connect():
 import network
 c=network.WLAN(network.AP_IF)
 c.active(False)
 A=network.WLAN(network.STA_IF)
 A.active(True)
 T=A.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(T).decode())
 if not A.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  A.connect(SSID,PASSWORD)
  r=0
  while not A.isconnected():
   time.sleep(5)
   r+=5
   print("Waiting for connection... ",r,"seconds") 
   if r>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",A.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(T).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

