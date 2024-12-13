from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
j="1.0"
N=5
A="GenericSensor/SensorData"
O="OTA/OTARequest"
f="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 m=ADC(ANALOG_SENSOR_PIN)
else:
 m=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 T=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 T=""
z=mqtt_broker_address
q=ubinascii.hexlify(DEVICE_NAME)
a=b'OTA/OTARequest'
d=b'GenericSensor/SensorData'
U=0
B=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  Q="\"deviceType\":\""+DEVICE_TYPE+"\""
  R="\"deviceName\":\""+DEVICE_NAME+"\""
  s="\"deviceName\":\"*\"" 
  Y=msg.decode()
  print('ESP received OTA message ',Y)
  if Q in Y and(R in Y or s in Y):
   L=json.loads(Y)
   from ota import OTAUpdater
   t="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   P=L.get("otafiles")
   l=True
   Y=DEVICE_NAME+" OTA: "+P
   try:
    J=OTAUpdater(t,P)
    if J.check_for_updates():
     if J.download_and_install_update():
      Y+=" updated"
     else:
      Y+=" update failed"
    else:
     Y+=" up-to-date" 
     l=False
   except Exception as o:
    Y+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(Y)
    H.publish(f,Y)
    time.sleep(5)
    if l:
     machine.reset() 
def connect_and_subscribe():
 global q,z,a
 H=MQTTClient(q,z)
 H.set_callback(sub_cb)
 H.connect()
 H.subscribe(a)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(z,a))
 return H
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global m
 global T
 Y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(m!=""):
  Y=Y+",\"AnaR\":\""+str(m.read())+"\""
 if(T!=""):
  Y=Y+",\"DigR\":\""+str(T.value())+"\""
 if error!="":
  Y=Y+",\"err\":\""+error+"\""
 return Y+"}"
try:
 H=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  H.check_msg()
  if(time.time()-U)>B:
   H.publish(d,create_sensor_message())
   U=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

