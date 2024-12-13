from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
h="1.0"
Y=5
k="GenericSensor/SensorData"
v="OTA/OTARequest"
Q="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 x=ADC(ANALOG_SENSOR_PIN)
else:
 x=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 A=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 A=""
d=mqtt_broker_address
t=ubinascii.hexlify(DEVICE_NAME)
M=b'OTA/OTARequest'
U=b'GenericSensor/SensorData'
j=0
P=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  X="\"deviceType\":\""+DEVICE_TYPE+"\""
  n="\"deviceName\":\""+DEVICE_NAME+"\""
  R="\"deviceName\":\"*\"" 
  p=msg.decode()
  print('ESP received OTA message ',p)
  if X in p and(n in p or R in p):
   V=json.loads(p)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   s=V.get("otafiles")
   o=True
   p=DEVICE_NAME+" OTA: "+s
   try:
    O=OTAUpdater(e,s)
    if O.check_for_updates():
     if O.download_and_install_update():
      p+=" updated"
     else:
      p+=" update failed"
    else:
     p+=" up-to-date" 
     o=False
   except Exception as T:
    p+=" err:"+str(T)+" type:"+str(type(T))
   finally:
    print(p)
    i.publish(Q,p)
    time.sleep(5)
    if o:
     machine.reset() 
def connect_and_subscribe():
 global t,d,M
 i=MQTTClient(t,d)
 i.set_callback(sub_cb)
 i.connect()
 i.subscribe(M)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(d,M))
 return i
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global x
 global A
 p="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(x!=""):
  p=p+",\"AnaR\":\""+str(x.read())+"\""
 if(A!=""):
  p=p+",\"DigR\":\""+str(A.value())+"\""
 if error!="":
  p=p+",\"err\":\""+error+"\""
 return p+"}"
try:
 i=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  i.check_msg()
  if(time.time()-j)>P:
   i.publish(U,create_sensor_message())
   j=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

