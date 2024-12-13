import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
c="1.0"
gc.collect()
def do_connect():
 import network
 w=network.WLAN(network.AP_IF)
 w.active(False)
 P=network.WLAN(network.STA_IF)
 P.active(True)
 y=P.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(y).decode())
 if not P.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  P.connect(SSID,PASSWORD)
  s=0
  while not P.isconnected():
   time.sleep(5)
   s+=5
   print("Waiting for connection... ",s,"seconds") 
   if s>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",P.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(y).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

