from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
i="1.0"
M=5
Q="GenericSensor/SensorData"
S="OTA/OTARequest"
Y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 V=ADC(ANALOG_SENSOR_PIN)
else:
 V=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 D=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 D=""
I=mqtt_broker_address
L=ubinascii.hexlify(DEVICE_NAME)
c=b'OTA/OTARequest'
N=b'GenericSensor/SensorData'
E=0
a=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  e="\"deviceType\":\""+DEVICE_TYPE+"\""
  m="\"deviceName\":\""+DEVICE_NAME+"\""
  R="\"deviceName\":\"*\"" 
  w=msg.decode()
  print('ESP received OTA message ',w)
  if e in w and(m in w or R in w):
   T=json.loads(w)
   from ota import OTAUpdater
   l="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   v=T.get("otafiles")
   p=True
   w=DEVICE_NAME+" OTA: "+v
   try:
    u=OTAUpdater(l,v)
    if u.check_for_updates():
     if u.download_and_install_update():
      w+=" updated"
     else:
      w+=" update failed"
    else:
     w+=" up-to-date" 
     p=False
   except Exception as K:
    w+=" err:"+str(K)+" type:"+str(type(K))
   finally:
    print(w)
    h.publish(Y,w)
    time.sleep(5)
    if p:
     machine.reset() 
def connect_and_subscribe():
 global L,I,c
 h=MQTTClient(L,I)
 h.set_callback(sub_cb)
 h.connect()
 h.subscribe(c)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,c))
 return h
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global V
 global D
 w="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(V!=""):
  w=w+",\"AnaR\":\""+str(V.read())+"\""
 if(D!=""):
  w=w+",\"DigR\":\""+str(D.value())+"\""
 if error!="":
  w=w+",\"err\":\""+error+"\""
 return w+"}"
try:
 h=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  h.check_msg()
  if(time.time()-E)>a:
   h.publish(N,create_sensor_message())
   E=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

