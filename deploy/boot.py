import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
H="1.0"
gc.collect()
def do_connect():
 import network
 J=network.WLAN(network.AP_IF)
 J.active(False)
 e=network.WLAN(network.STA_IF)
 e.active(True)
 A=e.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(A).decode())
 if not e.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  e.connect(SSID,PASSWORD)
  c=0
  while not e.isconnected():
   time.sleep(5)
   c+=5
   print("Waiting for connection... ",c,"seconds") 
   if c>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",e.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(A).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

