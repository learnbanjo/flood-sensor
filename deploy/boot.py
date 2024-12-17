import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
d="1.0"
gc.collect()
def do_connect():
 import network
 x=network.WLAN(network.AP_IF)
 x.active(False)
 e=network.WLAN(network.STA_IF)
 e.active(True)
 M=e.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(M).decode())
 if not e.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  e.connect(SSID,PASSWORD)
  O=0
  while not e.isconnected():
   time.sleep(5)
   O+=5
   print("Waiting for connection... ",O,"seconds") 
   if O>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",e.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(M).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

