import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
M="1.0"
gc.collect()
def do_connect():
 import network
 F=network.WLAN(network.AP_IF)
 F.active(False)
 d=network.WLAN(network.STA_IF)
 d.active(True)
 O=d.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 if not d.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  d.connect(SSID,PASSWORD)
  L=0
  while not d.isconnected():
   time.sleep(5)
   L+=5
   print("Waiting for connection... ",L,"seconds") 
   if L>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",d.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

