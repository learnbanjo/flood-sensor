import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
o="1.0"
gc.collect()
def do_connect():
 import network
 s=network.WLAN(network.AP_IF)
 s.active(False)
 u=network.WLAN(network.STA_IF)
 u.active(True)
 g=u.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(g).decode())
 if not u.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  u.connect(SSID,PASSWORD)
  v=0
  while not u.isconnected():
   time.sleep(5)
   v+=5
   print("Waiting for connection... ",v,"seconds") 
   if v>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",u.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(g).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()

