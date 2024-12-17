import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
I="1.0"
gc.collect()
def do_connect():
 import network
 D=network.WLAN(network.AP_IF)
 D.active(False)
 F=network.WLAN(network.STA_IF)
 F.active(True)
 N=F.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(N).decode())
 if not F.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  F.connect(SSID,PASSWORD)
  W=0
  while not F.isconnected():
   time.sleep(5)
   W+=5
   print("Waiting for connection... ",W,"seconds") 
   if W>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",F.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(N).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

