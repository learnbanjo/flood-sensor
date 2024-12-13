import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
c="1.0"
gc.collect()
def do_connect():
 import network
 u=network.WLAN(network.AP_IF)
 u.active(False)
 L=network.WLAN(network.STA_IF)
 L.active(True)
 F=L.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(F).decode())
 if not L.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  L.connect(SSID,PASSWORD)
  D=0
  while not L.isconnected():
   time.sleep(5)
   D+=5
   print("Waiting for connection... ",D,"seconds") 
   if D>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",L.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(F).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()

