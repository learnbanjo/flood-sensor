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
 n=network.WLAN(network.AP_IF)
 n.active(False)
 a=network.WLAN(network.STA_IF)
 a.active(True)
 K=a.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(K).decode())
 if not a.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  a.connect(SSID,PASSWORD)
  G=0
  while not a.isconnected():
   time.sleep(5)
   G+=5
   print("Waiting for connection... ",G,"seconds") 
   if G>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",a.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(K).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

