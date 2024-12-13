import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
Q="1.0"
gc.collect()
def do_connect():
 import network
 V=network.WLAN(network.AP_IF)
 V.active(False)
 m=network.WLAN(network.STA_IF)
 m.active(True)
 s=m.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 if not m.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  m.connect(SSID,PASSWORD)
  J=0
  while not m.isconnected():
   time.sleep(5)
   J+=5
   print("Waiting for connection... ",J,"seconds") 
   if J>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",m.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(s).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()

