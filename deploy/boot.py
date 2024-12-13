import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
S="1.0"
gc.collect()
def do_connect():
 import network
 l=network.WLAN(network.AP_IF)
 l.active(False)
 H=network.WLAN(network.STA_IF)
 H.active(True)
 L=H.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(L).decode())
 if not H.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  H.connect(SSID,PASSWORD)
  I=0
  while not H.isconnected():
   time.sleep(5)
   I+=5
   print("Waiting for connection... ",I,"seconds") 
   if I>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",H.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(L).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

