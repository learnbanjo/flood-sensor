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
 D=network.WLAN(network.AP_IF)
 D.active(False)
 k=network.WLAN(network.STA_IF)
 k.active(True)
 o=k.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(o).decode())
 if not k.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  k.connect(SSID,PASSWORD)
  y=0
  while not k.isconnected():
   time.sleep(5)
   y+=5
   print("Waiting for connection... ",y,"seconds") 
   if y>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",k.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(o).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

