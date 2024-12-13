import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
B="1.0"
gc.collect()
def do_connect():
 import network
 F=network.WLAN(network.AP_IF)
 F.active(False)
 Q=network.WLAN(network.STA_IF)
 Q.active(True)
 k=Q.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(k).decode())
 if not Q.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Q.connect(SSID,PASSWORD)
  X=0
  while not Q.isconnected():
   time.sleep(5)
   X+=5
   print("Waiting for connection... ",X,"seconds") 
   if X>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Q.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(k).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

