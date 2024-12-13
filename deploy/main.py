from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
y="1.0"
z=5
P="GenericSensor/SensorData"
X="OTA/OTARequest"
D="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 l=ADC(ANALOG_SENSOR_PIN)
else:
 l=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 e=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 e=""
i=mqtt_broker_address
m=ubinascii.hexlify(DEVICE_NAME)
C=b'OTA/OTARequest'
S=b'GenericSensor/SensorData'
p=0
q=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  I="\"deviceType\":\""+DEVICE_TYPE+"\""
  L="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  F=msg.decode()
  print('ESP received OTA message ',F)
  if I in F and(L in F or Q in F):
   s=json.loads(F)
   from ota import OTAUpdater
   w="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   v=s.get("otafiles")
   c=True
   F=DEVICE_NAME+" OTA: "+v
   try:
    J=OTAUpdater(w,v)
    if J.check_for_updates():
     if J.download_and_install_update():
      F+=" updated"
     else:
      F+=" update failed"
    else:
     F+=" up-to-date" 
     c=False
   except Exception as N:
    F+=" err:"+str(N)+" type:"+str(type(N))
   finally:
    print(F)
    h.publish(D,F)
    time.sleep(5)
    if c:
     machine.reset() 
def connect_and_subscribe():
 global m,i,C
 h=MQTTClient(m,i)
 h.set_callback(sub_cb)
 h.connect()
 h.subscribe(C)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(i,C))
 return h
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global l
 global e
 F="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(l!=""):
  F=F+",\"AnaR\":\""+str(l.read())+"\""
 if(e!=""):
  F=F+",\"DigR\":\""+str(e.value())+"\""
 if error!="":
  F=F+",\"err\":\""+error+"\""
 return F+"}"
try:
 h=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  h.check_msg()
  if(time.time()-p)>q:
   h.publish(S,create_sensor_message())
   p=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

