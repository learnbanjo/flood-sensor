import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
x="1.0"
gc.collect()
def do_connect():
 import network
 k=network.WLAN(network.AP_IF)
 k.active(False)
 L=network.WLAN(network.STA_IF)
 L.active(True)
 T=L.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(T).decode())
 if not L.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  L.connect(SSID,PASSWORD)
  S=0
  while not L.isconnected():
   time.sleep(5)
   S+=5
   print("Waiting for connection... ",S,"seconds") 
   if S>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",L.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(T).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

