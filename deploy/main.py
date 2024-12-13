from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
p="1.0"
e=5
W="GenericSensor/SensorData"
C="OTA/OTARequest"
J="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 s=ADC(ANALOG_SENSOR_PIN)
else:
 s=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 y=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 y=""
V=mqtt_broker_address
R=ubinascii.hexlify(DEVICE_NAME)
H=b'OTA/OTARequest'
F=b'GenericSensor/SensorData'
m=0
Y=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  A="\"deviceType\":\""+DEVICE_TYPE+"\""
  k="\"deviceName\":\""+DEVICE_NAME+"\""
  r="\"deviceName\":\"*\"" 
  j=msg.decode()
  print('ESP received OTA message ',j)
  if A in j and(k in j or r in j):
   G=json.loads(j)
   from ota import OTAUpdater
   E="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   L=G.get("otafiles")
   T=True
   j=DEVICE_NAME+" OTA: "+L
   try:
    N=OTAUpdater(E,L)
    if N.check_for_updates():
     if N.download_and_install_update():
      j+=" updated"
     else:
      j+=" update failed"
    else:
     j+=" up-to-date" 
     T=False
   except Exception as o:
    j+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(j)
    f.publish(J,j)
    time.sleep(5)
    if T:
     machine.reset() 
def connect_and_subscribe():
 global R,V,H
 f=MQTTClient(R,V)
 f.set_callback(sub_cb)
 f.connect()
 f.subscribe(H)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(V,H))
 return f
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global s
 global y
 j="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(s!=""):
  j=j+",\"AnaR\":\""+str(s.read())+"\""
 if(y!=""):
  j=j+",\"DigR\":\""+str(y.value())+"\""
 if error!="":
  j=j+",\"err\":\""+error+"\""
 return j+"}"
try:
 f=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  f.check_msg()
  if(time.time()-m)>Y:
   f.publish(F,create_sensor_message())
   m=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

