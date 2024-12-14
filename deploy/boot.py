import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
q="1.0"
gc.collect()
def do_connect():
 import network
 f=network.WLAN(network.AP_IF)
 f.active(False)
 e=network.WLAN(network.STA_IF)
 e.active(True)
 W=e.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(W).decode())
 if not e.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  e.connect(SSID,PASSWORD)
  i=0
  while not e.isconnected():
   time.sleep(5)
   i+=5
   print("Waiting for connection... ",i,"seconds") 
   if i>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",e.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(W).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

