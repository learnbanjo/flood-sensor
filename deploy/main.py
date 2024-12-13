from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
C="1.0"
I=5
Y="GenericSensor/SensorData"
Q="OTA/OTARequest"
A="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 m=ADC(ANALOG_SENSOR_PIN)
else:
 m=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 w=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 w=""
H=mqtt_broker_address
E=ubinascii.hexlify(DEVICE_NAME)
k=b'OTA/OTARequest'
b=b'GenericSensor/SensorData'
K=0
J=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  o="\"deviceType\":\""+DEVICE_TYPE+"\""
  p="\"deviceName\":\""+DEVICE_NAME+"\""
  n="\"deviceName\":\"*\"" 
  T=msg.decode()
  print('ESP received OTA message ',T)
  if o in T and(p in T or n in T):
   l=json.loads(T)
   from ota import OTAUpdater
   L="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   h=l.get("otafiles")
   y=True
   T=DEVICE_NAME+" OTA: "+h
   try:
    v=OTAUpdater(L,h)
    if v.check_for_updates():
     if v.download_and_install_update():
      T+=" updated"
     else:
      T+=" update failed"
    else:
     T+=" up-to-date" 
     y=False
   except Exception as q:
    T+=" err:"+str(q)+" type:"+str(type(q))
   finally:
    print(T)
    B.publish(A,T)
    time.sleep(5)
    if y:
     machine.reset() 
def connect_and_subscribe():
 global E,H,k
 B=MQTTClient(E,H)
 B.set_callback(sub_cb)
 B.connect()
 B.subscribe(k)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,k))
 return B
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global m
 global w
 T="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(m!=""):
  T=T+",\"AnaR\":\""+str(m.read())+"\""
 if(w!=""):
  T=T+",\"DigR\":\""+str(w.value())+"\""
 if error!="":
  T=T+",\"err\":\""+error+"\""
 return T+"}"
try:
 B=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  B.check_msg()
  if(time.time()-K)>J:
   B.publish(b,create_sensor_message())
   K=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

