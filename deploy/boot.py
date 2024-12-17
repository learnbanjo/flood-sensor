import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
G="1.0"
gc.collect()
def do_connect():
 import network
 P=network.WLAN(network.AP_IF)
 P.active(False)
 M=network.WLAN(network.STA_IF)
 M.active(True)
 F=M.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(F).decode())
 if not M.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  M.connect(SSID,PASSWORD)
  y=0
  while not M.isconnected():
   time.sleep(5)
   y+=5
   print("Waiting for connection... ",y,"seconds") 
   if y>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",M.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(F).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

