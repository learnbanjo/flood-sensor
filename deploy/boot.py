import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
W="1.0"
gc.collect()
def do_connect():
 import network
 u=network.WLAN(network.AP_IF)
 u.active(False)
 S=network.WLAN(network.STA_IF)
 S.active(True)
 G=S.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(G).decode())
 if not S.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  S.connect(SSID,PASSWORD)
  R=0
  while not S.isconnected():
   time.sleep(5)
   R+=5
   print("Waiting for connection... ",R,"seconds") 
   if R>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",S.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(G).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

