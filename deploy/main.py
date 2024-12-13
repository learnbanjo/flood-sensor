from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
m="1.0"
e=5
j="GenericSensor/SensorData"
G="OTA/OTARequest"
H="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 I=ADC(ANALOG_SENSOR_PIN)
else:
 I=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 u=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 u=""
T=mqtt_broker_address
d=ubinascii.hexlify(DEVICE_NAME)
X=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
a=0
Q=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  t="\"deviceType\":\""+DEVICE_TYPE+"\""
  r="\"deviceName\":\""+DEVICE_NAME+"\""
  L="\"deviceName\":\"*\"" 
  y=msg.decode()
  print('ESP received OTA message ',y)
  if t in y and(r in y or L in y):
   o=json.loads(y)
   from ota import OTAUpdater
   q="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   O=o.get("otafiles")
   p=True
   y=DEVICE_NAME+" OTA: "+O
   try:
    U=OTAUpdater(q,O)
    if U.check_for_updates():
     if U.download_and_install_update():
      y+=" updated"
     else:
      y+=" update failed"
    else:
     y+=" up-to-date" 
     p=False
   except Exception as x:
    y+=" err:"+str(x)+" type:"+str(type(x))
   finally:
    print(y)
    J.publish(H,y)
    time.sleep(5)
    if p:
     machine.reset() 
def connect_and_subscribe():
 global d,T,X
 J=MQTTClient(d,T)
 J.set_callback(sub_cb)
 J.connect()
 J.subscribe(X)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(T,X))
 return J
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global I
 global u
 y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(I!=""):
  y=y+",\"AnaR\":\""+str(I.read())+"\""
 if(u!=""):
  y=y+",\"DigR\":\""+str(u.value())+"\""
 if error!="":
  y=y+",\"err\":\""+error+"\""
 return y+"}"
try:
 J=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  J.check_msg()
  if(time.time()-a)>Q:
   J.publish(E,create_sensor_message())
   a=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

