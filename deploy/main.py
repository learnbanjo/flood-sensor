from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
V="1.0"
z=5
D="GenericSensor/SensorData"
a="OTA/OTARequest"
r="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 k=ADC(ANALOG_SENSOR_PIN)
else:
 k=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 v=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 v=""
I=mqtt_broker_address
h=ubinascii.hexlify(DEVICE_NAME)
R=b'OTA/OTARequest'
l=b'GenericSensor/SensorData'
s=0
L=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  x="\"deviceType\":\""+DEVICE_TYPE+"\""
  m="\"deviceName\":\""+DEVICE_NAME+"\""
  d="\"deviceName\":\"*\"" 
  w=msg.decode()
  print('ESP received OTA message ',w)
  if x in w and(m in w or d in w):
   Y=json.loads(w)
   from ota import OTAUpdater
   F="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   e=Y.get("otafiles")
   T=True
   w=DEVICE_NAME+" OTA: "+e
   try:
    K=OTAUpdater(F,e)
    if K.check_for_updates():
     if K.download_and_install_update():
      w+=" updated"
     else:
      w+=" update failed"
    else:
     w+=" up-to-date" 
     T=False
   except Exception as o:
    w+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(w)
    N.publish(r,w)
    time.sleep(5)
    if T:
     machine.reset() 
def connect_and_subscribe():
 global h,I,R
 N=MQTTClient(h,I)
 N.set_callback(sub_cb)
 N.connect()
 N.subscribe(R)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,R))
 return N
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global k
 global v
 w="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(k!=""):
  w=w+",\"AnaR\":\""+str(k.read())+"\""
 if(v!=""):
  w=w+",\"DigR\":\""+str(v.value())+"\""
 if error!="":
  w=w+",\"err\":\""+error+"\""
 return w+"}"
try:
 N=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  N.check_msg()
  if(time.time()-s)>L:
   N.publish(l,create_sensor_message())
   s=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

