import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
p="1.0"
gc.collect()
def do_connect():
 import network
 t=network.WLAN(network.AP_IF)
 t.active(False)
 j=network.WLAN(network.STA_IF)
 j.active(True)
 O=j.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 if not j.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  j.connect(SSID,PASSWORD)
  U=0
  while not j.isconnected():
   time.sleep(5)
   U+=5
   print("Waiting for connection... ",U,"seconds") 
   if U>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",j.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(O).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

