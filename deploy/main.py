from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
z="1.0"
K=5
R="GenericSensor/SensorData"
F="OTA/OTARequest"
y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 d=ADC(ANALOG_SENSOR_PIN)
else:
 d=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 i=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 i=""
H=mqtt_broker_address
G=ubinascii.hexlify(DEVICE_NAME)
J=b'OTA/OTARequest'
j=b'GenericSensor/SensorData'
D=0
g=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  f="\"deviceType\":\""+DEVICE_TYPE+"\""
  W="\"deviceName\":\""+DEVICE_NAME+"\""
  h="\"deviceName\":\"*\"" 
  X=msg.decode()
  print('ESP received OTA message ',X)
  if f in X and(W in X or h in X):
   L=json.loads(X)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   C=L.get("otafiles")
   T=True
   X=DEVICE_NAME+" OTA: "+C
   try:
    p=OTAUpdater(e,C)
    if p.check_for_updates():
     if p.download_and_install_update():
      X+=" updated"
     else:
      X+=" update failed"
    else:
     X+=" up-to-date" 
     T=False
   except Exception as P:
    X+=" err:"+str(P)+" type:"+str(type(P))
   finally:
    print(X)
    I.publish(y,X)
    time.sleep(5)
    if T:
     machine.reset() 
def connect_and_subscribe():
 global G,H,J
 I=MQTTClient(G,H)
 I.set_callback(sub_cb)
 I.connect()
 I.subscribe(J)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,J))
 return I
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global d
 global i
 X="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(d!=""):
  X=X+",\"AnaR\":\""+str(d.read())+"\""
 if(i!=""):
  X=X+",\"DigR\":\""+str(i.value())+"\""
 if error!="":
  X=X+",\"err\":\""+error+"\""
 return X+"}"
try:
 I=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  I.check_msg()
  if(time.time()-D)>g:
   I.publish(j,create_sensor_message())
   D=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

