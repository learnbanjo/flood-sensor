from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
X="1.0"
A=5
K="GenericSensor/SensorData"
m="OTA/OTARequest"
M="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 B=ADC(ANALOG_SENSOR_PIN)
else:
 B=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 o=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 o=""
I=mqtt_broker_address
h=ubinascii.hexlify(DEVICE_NAME)
l=b'OTA/OTARequest'
D=b'GenericSensor/SensorData'
a=0
C=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  p="\"deviceType\":\""+DEVICE_TYPE+"\""
  F="\"deviceName\":\""+DEVICE_NAME+"\""
  N="\"deviceName\":\"*\"" 
  P=msg.decode()
  print('ESP received OTA message ',P)
  if p in P and(F in P or N in P):
   H=json.loads(P)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   c=H.get("otafiles")
   S=True
   P=DEVICE_NAME+" OTA: "+c
   try:
    q=OTAUpdater(e,c)
    if q.check_for_updates():
     if q.download_and_install_update():
      P+=" updated"
     else:
      P+=" update failed"
    else:
     P+=" up-to-date" 
     S=False
   except Exception as L:
    P+=" err:"+str(L)+" type:"+str(type(L))
   finally:
    print(P)
    r.publish(M,P)
    time.sleep(5)
    if S:
     machine.reset() 
def connect_and_subscribe():
 global h,I,l
 r=MQTTClient(h,I)
 r.set_callback(sub_cb)
 r.connect()
 r.subscribe(l)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,l))
 return r
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global B
 global o
 P="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(B!=""):
  P=P+",\"AnaR\":\""+str(B.read())+"\""
 if(o!=""):
  P=P+",\"DigR\":\""+str(o.value())+"\""
 if error!="":
  P=P+",\"err\":\""+error+"\""
 return P+"}"
try:
 r=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  r.check_msg()
  if(time.time()-a)>C:
   r.publish(D,create_sensor_message())
   a=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

