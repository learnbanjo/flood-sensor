import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
p="1.0"
gc.collect()
def do_connect():
 import network
 A=network.WLAN(network.AP_IF)
 A.active(False)
 Y=network.WLAN(network.STA_IF)
 Y.active(True)
 P=Y.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(P).decode())
 if not Y.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  Y.connect(SSID,PASSWORD)
  N=0
  while not Y.isconnected():
   time.sleep(5)
   N+=5
   print("Waiting for connection... ",N,"seconds") 
   if N>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",Y.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(P).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

