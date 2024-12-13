from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
g="1.0"
J=5
d="GenericSensor/SensorData"
n="OTA/OTARequest"
l="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 a=ADC(ANALOG_SENSOR_PIN)
else:
 a=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 k=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 k=""
X=mqtt_broker_address
T=ubinascii.hexlify(DEVICE_NAME)
y=b'OTA/OTARequest'
P=b'GenericSensor/SensorData'
m=0
i=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  r="\"deviceType\":\""+DEVICE_TYPE+"\""
  q="\"deviceName\":\""+DEVICE_NAME+"\""
  R="\"deviceName\":\"*\"" 
  S=msg.decode()
  print('ESP received OTA message ',S)
  if r in S and(q in S or R in S):
   E=json.loads(S)
   from ota import OTAUpdater
   s="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   M=E.get("otafiles")
   N=True
   S=DEVICE_NAME+" OTA: "+M
   try:
    Y=OTAUpdater(s,M)
    if Y.check_for_updates():
     if Y.download_and_install_update():
      S+=" updated"
     else:
      S+=" update failed"
    else:
     S+=" up-to-date" 
     N=False
   except Exception as G:
    S+=" err:"+str(G)+" type:"+str(type(G))
   finally:
    print(S)
    x.publish(l,S)
    time.sleep(5)
    if N:
     machine.reset() 
def connect_and_subscribe():
 global T,X,y
 x=MQTTClient(T,X)
 x.set_callback(sub_cb)
 x.connect()
 x.subscribe(y)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(X,y))
 return x
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global a
 global k
 S="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(a!=""):
  S=S+",\"AnaR\":\""+str(a.read())+"\""
 if(k!=""):
  S=S+",\"DigR\":\""+str(k.value())+"\""
 if error!="":
  S=S+",\"err\":\""+error+"\""
 return S+"}"
try:
 x=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  x.check_msg()
  if(time.time()-m)>i:
   x.publish(P,create_sensor_message())
   m=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

