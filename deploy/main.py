from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
y="1.0"
M=5
W="GenericSensor/SensorData"
j="OTA/OTARequest"
U="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 k=ADC(ANALOG_SENSOR_PIN)
else:
 k=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 r=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 r=""
u=mqtt_broker_address
R=ubinascii.hexlify(DEVICE_NAME)
T=b'OTA/OTARequest'
p=b'GenericSensor/SensorData'
t=0
l=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  O="\"deviceType\":\""+DEVICE_TYPE+"\""
  c="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  z=msg.decode()
  print('ESP received OTA message ',z)
  if O in z and(c in z or Q in z):
   I=json.loads(z)
   from ota import OTAUpdater
   g="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   m=I.get("otafiles")
   s=True
   z=DEVICE_NAME+" OTA: "+m
   try:
    K=OTAUpdater(g,m)
    if K.check_for_updates():
     if K.download_and_install_update():
      z+=" updated"
     else:
      z+=" update failed"
    else:
     z+=" up-to-date" 
     s=False
   except Exception as q:
    z+=" err:"+str(q)+" type:"+str(type(q))
   finally:
    print(z)
    B.publish(U,z)
    time.sleep(5)
    if s:
     machine.reset() 
def connect_and_subscribe():
 global R,u,T
 B=MQTTClient(R,u)
 B.set_callback(sub_cb)
 B.connect()
 B.subscribe(T)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(u,T))
 return B
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global k
 global r
 z="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(k!=""):
  z=z+",\"AnaR\":\""+str(k.read())+"\""
 if(r!=""):
  z=z+",\"DigR\":\""+str(r.value())+"\""
 if error!="":
  z=z+",\"err\":\""+error+"\""
 return z+"}"
try:
 B=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  B.check_msg()
  if(time.time()-t)>l:
   B.publish(p,create_sensor_message())
   t=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

