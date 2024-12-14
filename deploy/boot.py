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
 A=network.WLAN(network.AP_IF)
 A.active(False)
 a=network.WLAN(network.STA_IF)
 a.active(True)
 z=a.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 if not a.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  a.connect(SSID,PASSWORD)
  I=0
  while not a.isconnected():
   time.sleep(5)
   I+=5
   print("Waiting for connection... ",I,"seconds") 
   if I>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",a.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(z).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

