import gc
import machine
import os
import time
import ubinascii
from DEVICE_CONFIG import SSID,PASSWORD,DEVICE_NAME
q="1.0"
gc.collect()
def do_connect():
 import network
 N=network.WLAN(network.AP_IF)
 N.active(False)
 P=network.WLAN(network.STA_IF)
 P.active(True)
 A=P.config("mac")
 print("\nMAC Address:",ubinascii.hexlify(A).decode())
 if not P.isconnected():
  print("\nConnecting to network...")
  print("Connecting to SSID:",SSID)
  P.connect(SSID,PASSWORD)
  F=0
  while not P.isconnected():
   time.sleep(5)
   F+=5
   print("Waiting for connection... ",F,"seconds") 
   if F>30:
    print("Connection failed. Rebooting...")
    machine.reset()
   pass
 print("\nnetwork config:",P.ifconfig())
 print("\nMAC Address:",ubinascii.hexlify(A).decode())
 print("Connecting to SSID:",SSID)
print("\n\n\nSensor Booting Up...")
print("\nmircopython version:",os.uname())
print("\nDevice Name:",DEVICE_NAME)
do_connect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

