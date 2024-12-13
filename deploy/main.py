from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
S="1.0"
h=5
C="GenericSensor/SensorData"
e="OTA/OTARequest"
D="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 T=ADC(ANALOG_SENSOR_PIN)
else:
 T=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 r=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 r=""
O=mqtt_broker_address
W=ubinascii.hexlify(DEVICE_NAME)
w=b'OTA/OTARequest'
k=b'GenericSensor/SensorData'
b=0
f=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  s="\"deviceType\":\""+DEVICE_TYPE+"\""
  H="\"deviceName\":\""+DEVICE_NAME+"\""
  B="\"deviceName\":\"*\"" 
  K=msg.decode()
  print('ESP received OTA message ',K)
  if s in K and(H in K or B in K):
   J=json.loads(K)
   from ota import OTAUpdater
   q="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   R=J.get("otafiles")
   y=True
   K=DEVICE_NAME+" OTA: "+R
   try:
    n=OTAUpdater(q,R)
    if n.check_for_updates():
     if n.download_and_install_update():
      K+=" updated"
     else:
      K+=" update failed"
    else:
     K+=" up-to-date" 
     y=False
   except Exception as L:
    K+=" err:"+str(L)+" type:"+str(type(L))
   finally:
    print(K)
    m.publish(D,K)
    time.sleep(5)
    if y:
     machine.reset() 
def connect_and_subscribe():
 global W,O,w
 m=MQTTClient(W,O)
 m.set_callback(sub_cb)
 m.connect()
 m.subscribe(w)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(O,w))
 return m
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global T
 global r
 K="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(T!=""):
  K=K+",\"AnaR\":\""+str(T.read())+"\""
 if(r!=""):
  K=K+",\"DigR\":\""+str(r.value())+"\""
 if error!="":
  K=K+",\"err\":\""+error+"\""
 return K+"}"
try:
 m=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  m.check_msg()
  if(time.time()-b)>f:
   m.publish(k,create_sensor_message())
   b=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

