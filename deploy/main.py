from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
T="1.0"
h=5
X="GenericSensor/SensorData"
q="OTA/OTARequest"
I="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 j=ADC(ANALOG_SENSOR_PIN)
else:
 j=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 m=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 m=""
x=mqtt_broker_address
V=ubinascii.hexlify(DEVICE_NAME)
v=b'OTA/OTARequest'
z=b'GenericSensor/SensorData'
i=0
Y=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  d="\"deviceType\":\""+DEVICE_TYPE+"\""
  e="\"deviceName\":\""+DEVICE_NAME+"\""
  c="\"deviceName\":\"*\"" 
  y=msg.decode()
  print('ESP received OTA message ',y)
  if d in y and(e in y or c in y):
   E=json.loads(y)
   from ota import OTAUpdater
   U="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   s=E.get("otafiles")
   p=True
   y=DEVICE_NAME+" OTA: "+s
   try:
    K=OTAUpdater(U,s)
    if K.check_for_updates():
     if K.download_and_install_update():
      y+=" updated"
     else:
      y+=" update failed"
    else:
     y+=" up-to-date" 
     p=False
   except Exception as f:
    y+=" err:"+str(f)+" type:"+str(type(f))
   finally:
    print(y)
    g.publish(I,y)
    time.sleep(5)
    if p:
     machine.reset() 
def connect_and_subscribe():
 global V,x,v
 g=MQTTClient(V,x)
 g.set_callback(sub_cb)
 g.connect()
 g.subscribe(v)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(x,v))
 return g
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global j
 global m
 y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(j!=""):
  y=y+",\"AnaR\":\""+str(j.read())+"\""
 if(m!=""):
  y=y+",\"DigR\":\""+str(m.value())+"\""
 if error!="":
  y=y+",\"err\":\""+error+"\""
 return y+"}"
try:
 g=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  g.check_msg()
  if(time.time()-i)>Y:
   g.publish(z,create_sensor_message())
   i=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

