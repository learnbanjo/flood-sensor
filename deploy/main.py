from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
W="1.0"
L=5
S="GenericSensor/SensorData"
l="OTA/OTARequest"
M="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 o=ADC(ANALOG_SENSOR_PIN)
else:
 o=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 i=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 i=""
P=mqtt_broker_address
s=ubinascii.hexlify(DEVICE_NAME)
F=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
N=0
H=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  b="\"deviceType\":\""+DEVICE_TYPE+"\""
  d="\"deviceName\":\""+DEVICE_NAME+"\""
  I="\"deviceName\":\"*\"" 
  x=msg.decode()
  print('ESP received OTA message ',x)
  if b in x and(d in x or I in x):
   R=json.loads(x)
   from ota import OTAUpdater
   u="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   h=R.get("otafiles")
   c=True
   x=DEVICE_NAME+" OTA: "+h
   try:
    O=OTAUpdater(u,h)
    if O.check_for_updates():
     if O.download_and_install_update():
      x+=" updated"
     else:
      x+=" update failed"
    else:
     x+=" up-to-date" 
     c=False
   except Exception as X:
    x+=" err:"+str(X)+" type:"+str(type(X))
   finally:
    print(x)
    U.publish(M,x)
    time.sleep(5)
    if c:
     machine.reset() 
def connect_and_subscribe():
 global s,P,F
 U=MQTTClient(s,P)
 U.set_callback(sub_cb)
 U.connect()
 U.subscribe(F)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(P,F))
 return U
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global o
 global i
 x="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(o!=""):
  x=x+",\"AnaR\":\""+str(o.read())+"\""
 if(i!=""):
  x=x+",\"DigR\":\""+str(i.value())+"\""
 if error!="":
  x=x+",\"err\":\""+error+"\""
 return x+"}"
try:
 U=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  U.check_msg()
  if(time.time()-N)>H:
   U.publish(E,create_sensor_message())
   N=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

