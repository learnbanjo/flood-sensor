from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
R="1.0"
A=5
P="GenericSensor/SensorData"
B="OTA/OTARequest"
y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Q=ADC(ANALOG_SENSOR_PIN)
else:
 Q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 H=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 H=""
o=mqtt_broker_address
V=ubinascii.hexlify(DEVICE_NAME)
E=b'OTA/OTARequest'
K=b'GenericSensor/SensorData'
r=0
O=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  i="\"deviceType\":\""+DEVICE_TYPE+"\""
  n="\"deviceName\":\""+DEVICE_NAME+"\""
  J="\"deviceName\":\"*\"" 
  j=msg.decode()
  print('ESP received OTA message ',j)
  if i in j and(n in j or J in j):
   k=json.loads(j)
   from ota import OTAUpdater
   W="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   m=k.get("otafiles")
   I=True
   j=DEVICE_NAME+" OTA: "+m
   try:
    C=OTAUpdater(W,m)
    if C.check_for_updates():
     if C.download_and_install_update():
      j+=" updated"
     else:
      j+=" update failed"
    else:
     j+=" up-to-date" 
     I=False
   except Exception as X:
    j+=" err:"+str(X)+" type:"+str(type(X))
   finally:
    print(j)
    w.publish(y,j)
    time.sleep(5)
    if I:
     machine.reset() 
def connect_and_subscribe():
 global V,o,E
 w=MQTTClient(V,o)
 w.set_callback(sub_cb)
 w.connect()
 w.subscribe(E)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(o,E))
 return w
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Q
 global H
 j="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Q!=""):
  j=j+",\"AnaR\":\""+str(Q.read())+"\""
 if(H!=""):
  j=j+",\"DigR\":\""+str(H.value())+"\""
 if error!="":
  j=j+",\"err\":\""+error+"\""
 return j+"}"
try:
 w=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  w.check_msg()
  if(time.time()-r)>O:
   w.publish(K,create_sensor_message())
   r=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

