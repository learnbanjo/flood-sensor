from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
r="1.0"
P=5
W="GenericSensor/SensorData"
Y="OTA/OTARequest"
u="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 x=ADC(ANALOG_SENSOR_PIN)
else:
 x=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 K=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 K=""
Q=mqtt_broker_address
k=ubinascii.hexlify(DEVICE_NAME)
v=b'OTA/OTARequest'
C=b'GenericSensor/SensorData'
l=0
L=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  H="\"deviceType\":\""+DEVICE_TYPE+"\""
  U="\"deviceName\":\""+DEVICE_NAME+"\""
  w="\"deviceName\":\"*\"" 
  o=msg.decode()
  print('ESP received OTA message ',o)
  if H in o and(U in o or w in o):
   S=json.loads(o)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   G=S.get("otafiles")
   b=True
   o=DEVICE_NAME+" OTA: "+G
   try:
    n=OTAUpdater(e,G)
    if n.check_for_updates():
     if n.download_and_install_update():
      o+=" updated"
     else:
      o+=" update failed"
    else:
     o+=" up-to-date" 
     b=False
   except Exception as N:
    o+=" err:"+str(N)+" type:"+str(type(N))
   finally:
    print(o)
    t.publish(u,o)
    time.sleep(5)
    if b:
     machine.reset() 
def connect_and_subscribe():
 global k,Q,v
 t=MQTTClient(k,Q)
 t.set_callback(sub_cb)
 t.connect()
 t.subscribe(v)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(Q,v))
 return t
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global x
 global K
 o="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(x!=""):
  o=o+",\"AnaR\":\""+str(x.read())+"\""
 if(K!=""):
  o=o+",\"DigR\":\""+str(K.value())+"\""
 if error!="":
  o=o+",\"err\":\""+error+"\""
 return o+"}"
try:
 t=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  t.check_msg()
  if(time.time()-l)>L:
   t.publish(C,create_sensor_message())
   l=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

