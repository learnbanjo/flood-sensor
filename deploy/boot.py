import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
E="1.0"
gc.collect()
def do_connect():
 import network
 u=network.WLAN(network.AP_IF)
 u.active(False)
 N=network.WLAN(network.STA_IF)
 N.active(True)
 J=N.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(J).decode())
 if not N.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  N.connect(SSID,PASSWORD)
  A=0
  while not N.isconnected():
   time.sleep(5)
   A+=5
   print("Waiting for connection... ",A,"seconds") 
   if A>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",N.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(J).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

