from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
J="1.0"
P=5
f="GenericSensor/SensorData"
s="OTA/OTARequest"
r="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 o=ADC(ANALOG_SENSOR_PIN)
else:
 o=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 X=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 X=""
q=mqtt_broker_address
F=ubinascii.hexlify(DEVICE_NAME)
t=b'OTA/OTARequest'
B=b'GenericSensor/SensorData'
S=0
v=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  L="\"deviceType\":\""+DEVICE_TYPE+"\""
  u="\"deviceName\":\""+DEVICE_NAME+"\""
  I="\"deviceName\":\"*\"" 
  e=msg.decode()
  print('ESP received OTA message ',e)
  if L in e and(u in e or I in e):
   V=json.loads(e)
   from ota import OTAUpdater
   y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   l=V.get("otafiles")
   D=True
   e=DEVICE_NAME+" OTA: "+l
   try:
    m=OTAUpdater(y,l)
    if m.check_for_updates():
     if m.download_and_install_update():
      e+=" updated"
     else:
      e+=" update failed"
    else:
     e+=" up-to-date" 
     D=False
   except Exception as E:
    e+=" err:"+str(E)+" type:"+str(type(E))
   finally:
    print(e)
    U.publish(r,e)
    time.sleep(5)
    if D:
     machine.reset() 
def connect_and_subscribe():
 global F,q,t
 U=MQTTClient(F,q)
 U.set_callback(sub_cb)
 U.connect()
 U.subscribe(t)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(q,t))
 return U
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global o
 global X
 e="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(o!=""):
  e=e+",\"AnaR\":\""+str(o.read())+"\""
 if(X!=""):
  e=e+",\"DigR\":\""+str(X.value())+"\""
 if error!="":
  e=e+",\"err\":\""+error+"\""
 return e+"}"
try:
 U=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  U.check_msg()
  if(time.time()-S)>v:
   U.publish(B,create_sensor_message())
   S=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

