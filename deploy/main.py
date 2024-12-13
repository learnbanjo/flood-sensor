from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
v="1.0"
i=5
e="GenericSensor/SensorData"
D="OTA/OTARequest"
l="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 U=ADC(ANALOG_SENSOR_PIN)
else:
 U=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 r=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 r=""
z=mqtt_broker_address
R=ubinascii.hexlify(DEVICE_NAME)
g=b'OTA/OTARequest'
d=b'GenericSensor/SensorData'
k=0
K=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  O="\"deviceType\":\""+DEVICE_TYPE+"\""
  b="\"deviceName\":\""+DEVICE_NAME+"\""
  M="\"deviceName\":\"*\"" 
  q=msg.decode()
  print('ESP received OTA message ',q)
  if O in q and(b in q or M in q):
   Q=json.loads(q)
   from ota import OTAUpdater
   V="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   w=Q.get("otafiles")
   t=True
   q=DEVICE_NAME+" OTA: "+w
   try:
    C=OTAUpdater(V,w)
    if C.check_for_updates():
     if C.download_and_install_update():
      q+=" updated"
     else:
      q+=" update failed"
    else:
     q+=" up-to-date" 
     t=False
   except Exception as S:
    q+=" err:"+str(S)+" type:"+str(type(S))
   finally:
    print(q)
    I.publish(l,q)
    time.sleep(5)
    if t:
     machine.reset() 
def connect_and_subscribe():
 global R,z,g
 I=MQTTClient(R,z)
 I.set_callback(sub_cb)
 I.connect()
 I.subscribe(g)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(z,g))
 return I
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global U
 global r
 q="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(U!=""):
  q=q+",\"AnaR\":\""+str(U.read())+"\""
 if(r!=""):
  q=q+",\"DigR\":\""+str(r.value())+"\""
 if error!="":
  q=q+",\"err\":\""+error+"\""
 return q+"}"
try:
 I=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  I.check_msg()
  if(time.time()-k)>K:
   I.publish(d,create_sensor_message())
   k=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

