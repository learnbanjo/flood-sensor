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
 s=network.WLAN(network.AP_IF)
 s.active(False)
 D=network.WLAN(network.STA_IF)
 D.active(True)
 r=D.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(r).decode())
 if not D.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  D.connect(SSID,PASSWORD)
  W=0
  while not D.isconnected():
   time.sleep(5)
   W+=5
   print("Waiting for connection... ",W,"seconds") 
   if W>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",D.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(r).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

