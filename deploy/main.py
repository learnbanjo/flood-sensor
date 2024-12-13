from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
Y="1.0"
P=5
C="GenericSensor/SensorData"
l="OTA/OTARequest"
g="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 H=ADC(ANALOG_SENSOR_PIN)
else:
 H=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 T=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 T=""
I=mqtt_broker_address
p=ubinascii.hexlify(DEVICE_NAME)
J=b'OTA/OTARequest'
K=b'GenericSensor/SensorData'
u=0
W=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  X="\"deviceType\":\""+DEVICE_TYPE+"\""
  a="\"deviceName\":\""+DEVICE_NAME+"\""
  x="\"deviceName\":\"*\"" 
  F=msg.decode()
  print('ESP received OTA message ',F)
  if X in F and(a in F or x in F):
   j=json.loads(F)
   from ota import OTAUpdater
   n="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   R=j.get("otafiles")
   A=True
   F=DEVICE_NAME+" OTA: "+R
   try:
    r=OTAUpdater(n,R)
    if r.check_for_updates():
     if r.download_and_install_update():
      F+=" updated"
     else:
      F+=" update failed"
    else:
     F+=" up-to-date" 
     A=False
   except Exception as Q:
    F+=" err:"+str(Q)+" type:"+str(type(Q))
   finally:
    print(F)
    f.publish(g,F)
    time.sleep(5)
    if A:
     machine.reset() 
def connect_and_subscribe():
 global p,I,J
 f=MQTTClient(p,I)
 f.set_callback(sub_cb)
 f.connect()
 f.subscribe(J)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,J))
 return f
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global H
 global T
 F="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(H!=""):
  F=F+",\"AnaR\":\""+str(H.read())+"\""
 if(T!=""):
  F=F+",\"DigR\":\""+str(T.value())+"\""
 if error!="":
  F=F+",\"err\":\""+error+"\""
 return F+"}"
try:
 f=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  f.check_msg()
  if(time.time()-u)>W:
   f.publish(K,create_sensor_message())
   u=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

