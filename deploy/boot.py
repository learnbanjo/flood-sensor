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
 T=network.WLAN(network.AP_IF)
 T.active(False)
 H=network.WLAN(network.STA_IF)
 H.active(True)
 e=H.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(e).decode())
 if not H.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  H.connect(SSID,PASSWORD)
  D=0
  while not H.isconnected():
   time.sleep(5)
   D+=5
   print("Waiting for connection... ",D,"seconds") 
   if D>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",H.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(e).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

