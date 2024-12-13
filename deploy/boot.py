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
 t=network.WLAN(network.AP_IF)
 t.active(False)
 q=network.WLAN(network.STA_IF)
 q.active(True)
 X=q.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(X).decode())
 if not q.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  q.connect(SSID,PASSWORD)
  a=0
  while not q.isconnected():
   time.sleep(5)
   a+=5
   print("Waiting for connection... ",a,"seconds") 
   if a>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",q.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(X).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

