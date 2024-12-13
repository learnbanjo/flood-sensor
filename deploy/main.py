from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
Y="1.0"
N=5
q="GenericSensor/SensorData"
v="OTA/OTARequest"
R="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 C=ADC(ANALOG_SENSOR_PIN)
else:
 C=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 c=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 c=""
I=mqtt_broker_address
W=ubinascii.hexlify(DEVICE_NAME)
g=b'OTA/OTARequest'
M=b'GenericSensor/SensorData'
l=0
E=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  z="\"deviceType\":\""+DEVICE_TYPE+"\""
  D="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  F=msg.decode()
  print('ESP received OTA message ',F)
  if z in F and(D in F or Q in F):
   h=json.loads(F)
   from ota import OTAUpdater
   x="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   i=h.get("otafiles")
   d=True
   F=DEVICE_NAME+" OTA: "+i
   try:
    B=OTAUpdater(x,i)
    if B.check_for_updates():
     if B.download_and_install_update():
      F+=" updated"
     else:
      F+=" update failed"
    else:
     F+=" up-to-date" 
     d=False
   except Exception as L:
    F+=" err:"+str(L)+" type:"+str(type(L))
   finally:
    print(F)
    A.publish(R,F)
    time.sleep(5)
    if d:
     machine.reset() 
def connect_and_subscribe():
 global W,I,g
 A=MQTTClient(W,I)
 A.set_callback(sub_cb)
 A.connect()
 A.subscribe(g)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,g))
 return A
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global C
 global c
 F="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(C!=""):
  F=F+",\"AnaR\":\""+str(C.read())+"\""
 if(c!=""):
  F=F+",\"DigR\":\""+str(c.value())+"\""
 if error!="":
  F=F+",\"err\":\""+error+"\""
 return F+"}"
try:
 A=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  A.check_msg()
  if(time.time()-l)>E:
   A.publish(M,create_sensor_message())
   l=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

