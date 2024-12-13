import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
e="1.0"
gc.collect()
def do_connect():
 import network
 Y=network.WLAN(network.AP_IF)
 Y.active(False)
 t=network.WLAN(network.STA_IF)
 t.active(True)
 i=t.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(i).decode())
 if not t.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  t.connect(SSID,PASSWORD)
  b=0
  while not t.isconnected():
   time.sleep(5)
   b+=5
   print("Waiting for connection... ",b,"seconds") 
   if b>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",t.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(i).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

