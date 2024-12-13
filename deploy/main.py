from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
B="1.0"
U=5
F="GenericSensor/SensorData"
o="OTA/OTARequest"
D="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 c=ADC(ANALOG_SENSOR_PIN)
else:
 c=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 a=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 a=""
I=mqtt_broker_address
s=ubinascii.hexlify(DEVICE_NAME)
G=b'OTA/OTARequest'
C=b'GenericSensor/SensorData'
L=0
w=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  n="\"deviceType\":\""+DEVICE_TYPE+"\""
  Y="\"deviceName\":\""+DEVICE_NAME+"\""
  z="\"deviceName\":\"*\"" 
  T=msg.decode()
  print('ESP received OTA message ',T)
  if n in T and(Y in T or z in T):
   Q=json.loads(T)
   from ota import OTAUpdater
   J="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   v=Q.get("otafiles")
   e=True
   T=DEVICE_NAME+" OTA: "+v
   try:
    S=OTAUpdater(J,v)
    if S.check_for_updates():
     if S.download_and_install_update():
      T+=" updated"
     else:
      T+=" update failed"
    else:
     T+=" up-to-date" 
     e=False
   except Exception as H:
    T+=" err:"+str(H)+" type:"+str(type(H))
   finally:
    print(T)
    y.publish(D,T)
    time.sleep(5)
    if e:
     machine.reset() 
def connect_and_subscribe():
 global s,I,G
 y=MQTTClient(s,I)
 y.set_callback(sub_cb)
 y.connect()
 y.subscribe(G)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,G))
 return y
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global c
 global a
 T="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(c!=""):
  T=T+",\"AnaR\":\""+str(c.read())+"\""
 if(a!=""):
  T=T+",\"DigR\":\""+str(a.value())+"\""
 if error!="":
  T=T+",\"err\":\""+error+"\""
 return T+"}"
try:
 y=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  y.check_msg()
  if(time.time()-L)>w:
   y.publish(C,create_sensor_message())
   L=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

