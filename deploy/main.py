from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
M="1.0"
D=5
G="GenericSensor/SensorData"
R="OTA/OTARequest"
I="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 U=ADC(ANALOG_SENSOR_PIN)
else:
 U=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 N=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 N=""
K=mqtt_broker_address
o=ubinascii.hexlify(DEVICE_NAME)
k=b'OTA/OTARequest'
P=b'GenericSensor/SensorData'
w=0
d=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  n="\"deviceType\":\""+DEVICE_TYPE+"\""
  p="\"deviceName\":\""+DEVICE_NAME+"\""
  x="\"deviceName\":\"*\"" 
  L=msg.decode()
  print('ESP received OTA message ',L)
  if n in L and(p in L or x in L):
   W=json.loads(L)
   from ota import OTAUpdater
   C="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   t=W.get("otafiles")
   V=True
   L=DEVICE_NAME+" OTA: "+t
   try:
    f=OTAUpdater(C,t)
    if f.check_for_updates():
     if f.download_and_install_update():
      L+=" updated"
     else:
      L+=" update failed"
    else:
     L+=" up-to-date" 
     V=False
   except Exception as J:
    L+=" err:"+str(J)+" type:"+str(type(J))
   finally:
    print(L)
    H.publish(I,L)
    time.sleep(5)
    if V:
     machine.reset() 
def connect_and_subscribe():
 global o,K,k
 H=MQTTClient(o,K)
 H.set_callback(sub_cb)
 H.connect()
 H.subscribe(k)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(K,k))
 return H
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global U
 global N
 L="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(U!=""):
  L=L+",\"AnaR\":\""+str(U.read())+"\""
 if(N!=""):
  L=L+",\"DigR\":\""+str(N.value())+"\""
 if error!="":
  L=L+",\"err\":\""+error+"\""
 return L+"}"
try:
 H=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  H.check_msg()
  if(time.time()-w)>d:
   H.publish(P,create_sensor_message())
   w=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

