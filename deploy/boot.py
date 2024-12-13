import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
y="1.0"
gc.collect()
def do_connect():
 import network
 Y=network.WLAN(network.AP_IF)
 Y.active(False)
 K=network.WLAN(network.STA_IF)
 K.active(True)
 u=K.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(u).decode())
 if not K.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  K.connect(SSID,PASSWORD)
  b=0
  while not K.isconnected():
   time.sleep(5)
   b+=5
   print("Waiting for connection... ",b,"seconds") 
   if b>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",K.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(u).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

