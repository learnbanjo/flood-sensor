import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
l="1.0"
gc.collect()
def do_connect():
 import network
 V=network.WLAN(network.AP_IF)
 V.active(False)
 N=network.WLAN(network.STA_IF)
 N.active(True)
 v=N.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(v).decode())
 if not N.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  N.connect(SSID,PASSWORD)
  S=0
  while not N.isconnected():
   time.sleep(5)
   S+=5
   print("Waiting for connection... ",S,"seconds") 
   if S>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",N.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(v).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

