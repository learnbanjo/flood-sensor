from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
b="1.0"
L=5
j="GenericSensor/SensorData"
A="OTA/OTARequest"
J="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 V=ADC(ANALOG_SENSOR_PIN)
else:
 V=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 F=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 F=""
T=mqtt_broker_address
a=ubinascii.hexlify(DEVICE_NAME)
s=b'OTA/OTARequest'
u=b'GenericSensor/SensorData'
t=0
f=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  N="\"deviceType\":\""+DEVICE_TYPE+"\""
  D="\"deviceName\":\""+DEVICE_NAME+"\""
  p="\"deviceName\":\"*\"" 
  I=msg.decode()
  print('ESP received OTA message ',I)
  if N in I and(D in I or p in I):
   h=json.loads(I)
   from ota import OTAUpdater
   Y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   d=h.get("otafiles")
   S=True
   I=DEVICE_NAME+" OTA: "+d
   try:
    B=OTAUpdater(Y,d)
    if B.check_for_updates():
     if B.download_and_install_update():
      I+=" updated"
     else:
      I+=" update failed"
    else:
     I+=" up-to-date" 
     S=False
   except Exception as C:
    I+=" err:"+str(C)+" type:"+str(type(C))
   finally:
    print(I)
    n.publish(J,I)
    time.sleep(5)
    if S:
     machine.reset() 
def connect_and_subscribe():
 global a,T,s
 n=MQTTClient(a,T)
 n.set_callback(sub_cb)
 n.connect()
 n.subscribe(s)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(T,s))
 return n
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global V
 global F
 I="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(V!=""):
  I=I+",\"AnaR\":\""+str(V.read())+"\""
 if(F!=""):
  I=I+",\"DigR\":\""+str(F.value())+"\""
 if error!="":
  I=I+",\"err\":\""+error+"\""
 return I+"}"
try:
 n=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  n.check_msg()
  if(time.time()-t)>f:
   n.publish(u,create_sensor_message())
   t=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

