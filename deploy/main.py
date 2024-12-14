from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
Q="1.0"
D=5
Y="GenericSensor/SensorData"
R="OTA/OTARequest"
J="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 l=ADC(ANALOG_SENSOR_PIN)
else:
 l=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 T=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 T=""
V=mqtt_broker_address
W=ubinascii.hexlify(DEVICE_NAME)
c=b'OTA/OTARequest'
P=b'GenericSensor/SensorData'
j=0
H=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  d="\"deviceType\":\""+DEVICE_TYPE+"\""
  w="\"deviceName\":\""+DEVICE_NAME+"\""
  A="\"deviceName\":\"*\"" 
  i=msg.decode()
  print('ESP received OTA message ',i)
  if d in i and(w in i or A in i):
   z=json.loads(i)
   from ota import OTAUpdater
   t="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   I=z.get("otafiles")
   h=True
   i=DEVICE_NAME+" OTA: "+I
   try:
    o=OTAUpdater(t,I)
    if o.check_for_updates():
     if o.download_and_install_update():
      i+=" updated"
     else:
      i+=" update failed"
    else:
     i+=" up-to-date" 
     h=False
   except Exception as N:
    i+=" err:"+str(N)+" type:"+str(type(N))
   finally:
    print(i)
    p.publish(J,i)
    time.sleep(5)
    if h:
     machine.reset() 
def connect_and_subscribe():
 global W,V,c
 p=MQTTClient(W,V)
 p.set_callback(sub_cb)
 p.connect()
 p.subscribe(c)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(V,c))
 return p
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global l
 global T
 i="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(l!=""):
  i=i+",\"AnaR\":\""+str(l.read())+"\""
 if(T!=""):
  i=i+",\"DigR\":\""+str(T.value())+"\""
 if error!="":
  i=i+",\"err\":\""+error+"\""
 return i+"}"
try:
 p=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  p.check_msg()
  if(time.time()-j)>H:
   p.publish(P,create_sensor_message())
   j=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

