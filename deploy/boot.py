import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
w="1.0"
gc.collect()
def do_connect():
 import network
 k=network.WLAN(network.AP_IF)
 k.active(False)
 N=network.WLAN(network.STA_IF)
 N.active(True)
 g=N.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(g).decode())
 if not N.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  N.connect(SSID,PASSWORD)
  I=0
  while not N.isconnected():
   time.sleep(5)
   I+=5
   print("Waiting for connection... ",I,"seconds") 
   if I>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",N.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(g).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

