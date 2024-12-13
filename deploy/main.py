from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
c="1.0"
P=5
N="GenericSensor/SensorData"
R="OTA/OTARequest"
b="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 p=ADC(ANALOG_SENSOR_PIN)
else:
 p=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 G=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 G=""
u=mqtt_broker_address
W=ubinascii.hexlify(DEVICE_NAME)
Y=b'OTA/OTARequest'
U=b'GenericSensor/SensorData'
H=0
B=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  k="\"deviceType\":\""+DEVICE_TYPE+"\""
  A="\"deviceName\":\""+DEVICE_NAME+"\""
  I="\"deviceName\":\"*\"" 
  i=msg.decode()
  print('ESP received OTA message ',i)
  if k in i and(A in i or I in i):
   S=json.loads(i)
   from ota import OTAUpdater
   o="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   m=S.get("otafiles")
   C=True
   i=DEVICE_NAME+" OTA: "+m
   try:
    V=OTAUpdater(o,m)
    if V.check_for_updates():
     if V.download_and_install_update():
      i+=" updated"
     else:
      i+=" update failed"
    else:
     i+=" up-to-date" 
     C=False
   except Exception as F:
    i+=" err:"+str(F)+" type:"+str(type(F))
   finally:
    print(i)
    a.publish(b,i)
    time.sleep(5)
    if C:
     machine.reset() 
def connect_and_subscribe():
 global W,u,Y
 a=MQTTClient(W,u)
 a.set_callback(sub_cb)
 a.connect()
 a.subscribe(Y)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(u,Y))
 return a
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global p
 global G
 i="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(p!=""):
  i=i+",\"AnaR\":\""+str(p.read())+"\""
 if(G!=""):
  i=i+",\"DigR\":\""+str(G.value())+"\""
 if error!="":
  i=i+",\"err\":\""+error+"\""
 return i+"}"
try:
 a=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  a.check_msg()
  if(time.time()-H)>B:
   a.publish(U,create_sensor_message())
   H=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

