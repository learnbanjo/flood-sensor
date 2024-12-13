import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
U="1.0"
gc.collect()
def do_connect():
 import network
 G=network.WLAN(network.AP_IF)
 G.active(False)
 R=network.WLAN(network.STA_IF)
 R.active(True)
 i=R.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(i).decode())
 if not R.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  R.connect(SSID,PASSWORD)
  j=0
  while not R.isconnected():
   time.sleep(5)
   j+=5
   print("Waiting for connection... ",j,"seconds") 
   if j>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",R.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(i).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

