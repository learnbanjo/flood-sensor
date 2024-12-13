from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
E="1.0"
M=5
g="GenericSensor/SensorData"
C="OTA/OTARequest"
b="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 f=ADC(ANALOG_SENSOR_PIN)
else:
 f=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 n=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 n=""
i=mqtt_broker_address
t=ubinascii.hexlify(DEVICE_NAME)
S=b'OTA/OTARequest'
B=b'GenericSensor/SensorData'
c=0
X=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  F="\"deviceType\":\""+DEVICE_TYPE+"\""
  l="\"deviceName\":\""+DEVICE_NAME+"\""
  R="\"deviceName\":\"*\"" 
  Q=msg.decode()
  print('ESP received OTA message ',Q)
  if F in Q and(l in Q or R in Q):
   U=json.loads(Q)
   from ota import OTAUpdater
   j="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   o=U.get("otafiles")
   W=True
   Q=DEVICE_NAME+" OTA: "+o
   try:
    P=OTAUpdater(j,o)
    if P.check_for_updates():
     if P.download_and_install_update():
      Q+=" updated"
     else:
      Q+=" update failed"
    else:
     Q+=" up-to-date" 
     W=False
   except Exception as r:
    Q+=" err:"+str(r)+" type:"+str(type(r))
   finally:
    print(Q)
    v.publish(b,Q)
    time.sleep(5)
    if W:
     machine.reset() 
def connect_and_subscribe():
 global t,i,S
 v=MQTTClient(t,i)
 v.set_callback(sub_cb)
 v.connect()
 v.subscribe(S)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(i,S))
 return v
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global f
 global n
 Q="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(f!=""):
  Q=Q+",\"AnaR\":\""+str(f.read())+"\""
 if(n!=""):
  Q=Q+",\"DigR\":\""+str(n.value())+"\""
 if error!="":
  Q=Q+",\"err\":\""+error+"\""
 return Q+"}"
try:
 v=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  v.check_msg()
  if(time.time()-c)>X:
   v.publish(B,create_sensor_message())
   c=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

