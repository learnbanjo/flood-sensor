from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
Q="1.0"
d=5
s="GenericSensor/SensorData"
J="OTA/OTARequest"
S="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 T=ADC(ANALOG_SENSOR_PIN)
else:
 T=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 k=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 k=""
W=mqtt_broker_address
c=ubinascii.hexlify(DEVICE_NAME)
m=b'OTA/OTARequest'
r=b'GenericSensor/SensorData'
v=0
h=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  P="\"deviceType\":\""+DEVICE_TYPE+"\""
  H="\"deviceName\":\""+DEVICE_NAME+"\""
  M="\"deviceName\":\"*\"" 
  l=msg.decode()
  print('ESP received OTA message ',l)
  if P in l and(H in l or M in l):
   f=json.loads(l)
   from ota import OTAUpdater
   N="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   w=f.get("otafiles")
   O=True
   l=DEVICE_NAME+" OTA: "+w
   try:
    L=OTAUpdater(N,w)
    if L.check_for_updates():
     if L.download_and_install_update():
      l+=" updated"
     else:
      l+=" update failed"
    else:
     l+=" up-to-date" 
     O=False
   except Exception as X:
    l+=" err:"+str(X)+" type:"+str(type(X))
   finally:
    print(l)
    F.publish(S,l)
    time.sleep(5)
    if O:
     machine.reset() 
def connect_and_subscribe():
 global c,W,m
 F=MQTTClient(c,W)
 F.set_callback(sub_cb)
 F.connect()
 F.subscribe(m)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(W,m))
 return F
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global T
 global k
 l="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(T!=""):
  l=l+",\"AnaR\":\""+str(T.read())+"\""
 if(k!=""):
  l=l+",\"DigR\":\""+str(k.value())+"\""
 if error!="":
  l=l+",\"err\":\""+error+"\""
 return l+"}"
try:
 F=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  F.check_msg()
  if(time.time()-v)>h:
   F.publish(r,create_sensor_message())
   v=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

