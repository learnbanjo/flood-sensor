from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
x="1.0"
p=5
A="GenericSensor/SensorData"
M="OTA/OTARequest"
u="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 E=ADC(ANALOG_SENSOR_PIN)
else:
 E=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 W=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 W=""
n=mqtt_broker_address
P=ubinascii.hexlify(DEVICE_NAME)
v=b'OTA/OTARequest'
a=b'GenericSensor/SensorData'
J=0
o=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  L="\"deviceType\":\""+DEVICE_TYPE+"\""
  k="\"deviceName\":\""+DEVICE_NAME+"\""
  V="\"deviceName\":\"*\"" 
  r=msg.decode()
  print('ESP received OTA message ',r)
  if L in r and(k in r or V in r):
   l=json.loads(r)
   from ota import OTAUpdater
   b="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   c=l.get("otafiles")
   Y=True
   r=DEVICE_NAME+" OTA: "+c
   try:
    q=OTAUpdater(b,c)
    if q.check_for_updates():
     if q.download_and_install_update():
      r+=" updated"
     else:
      r+=" update failed"
    else:
     r+=" up-to-date" 
     Y=False
   except Exception as S:
    r+=" err:"+str(S)+" type:"+str(type(S))
   finally:
    print(r)
    d.publish(u,r)
    time.sleep(5)
    if Y:
     machine.reset() 
def connect_and_subscribe():
 global P,n,v
 d=MQTTClient(P,n)
 d.set_callback(sub_cb)
 d.connect()
 d.subscribe(v)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(n,v))
 return d
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global E
 global W
 r="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(E!=""):
  r=r+",\"AnaR\":\""+str(E.read())+"\""
 if(W!=""):
  r=r+",\"DigR\":\""+str(W.value())+"\""
 if error!="":
  r=r+",\"err\":\""+error+"\""
 return r+"}"
try:
 d=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  d.check_msg()
  if(time.time()-J)>o:
   d.publish(a,create_sensor_message())
   J=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

