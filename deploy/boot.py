import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
m="1.0"
gc.collect()
def do_connect():
 import network
 D=network.WLAN(network.AP_IF)
 D.active(False)
 L=network.WLAN(network.STA_IF)
 L.active(True)
 s=L.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not L.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  L.connect(SSID,PASSWORD)
  q=0
  while not L.isconnected():
   time.sleep(5)
   q+=5
   print("Waiting for connection... ",q,"seconds") 
   if q>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",L.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

