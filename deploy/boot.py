import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
g="1.0"
gc.collect()
def do_connect():
 import network
 R=network.WLAN(network.AP_IF)
 R.active(False)
 h=network.WLAN(network.STA_IF)
 h.active(True)
 s=h.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not h.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  h.connect(SSID,PASSWORD)
  J=0
  while not h.isconnected():
   time.sleep(5)
   J+=5
   print("Waiting for connection... ",J,"seconds") 
   if J>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",h.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

