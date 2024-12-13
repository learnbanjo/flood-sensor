from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
d="1.0"
V=5
R="GenericSensor/SensorData"
B="OTA/OTARequest"
p="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 x=ADC(ANALOG_SENSOR_PIN)
else:
 x=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 m=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 m=""
b=mqtt_broker_address
c=ubinascii.hexlify(DEVICE_NAME)
S=b'OTA/OTARequest'
r=b'GenericSensor/SensorData'
s=0
g=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  j="\"deviceType\":\""+DEVICE_TYPE+"\""
  U="\"deviceName\":\""+DEVICE_NAME+"\""
  k="\"deviceName\":\"*\"" 
  q=msg.decode()
  print('ESP received OTA message ',q)
  if j in q and(U in q or k in q):
   y=json.loads(q)
   from ota import OTAUpdater
   i="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   X=y.get("otafiles")
   Q=True
   q=DEVICE_NAME+" OTA: "+X
   try:
    J=OTAUpdater(i,X)
    if J.check_for_updates():
     if J.download_and_install_update():
      q+=" updated"
     else:
      q+=" update failed"
    else:
     q+=" up-to-date" 
     Q=False
   except Exception as T:
    q+=" err:"+str(T)+" type:"+str(type(T))
   finally:
    print(q)
    M.publish(p,q)
    time.sleep(5)
    if Q:
     machine.reset() 
def connect_and_subscribe():
 global c,b,S
 M=MQTTClient(c,b)
 M.set_callback(sub_cb)
 M.connect()
 M.subscribe(S)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(b,S))
 return M
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global x
 global m
 q="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(x!=""):
  q=q+",\"AnaR\":\""+str(x.read())+"\""
 if(m!=""):
  q=q+",\"DigR\":\""+str(m.value())+"\""
 if error!="":
  q=q+",\"err\":\""+error+"\""
 return q+"}"
try:
 M=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  M.check_msg()
  if(time.time()-s)>g:
   M.publish(r,create_sensor_message())
   s=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

