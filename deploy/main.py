from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
u="1.0"
W=5
g="GenericSensor/SensorData"
R="OTA/OTARequest"
H="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Q=ADC(ANALOG_SENSOR_PIN)
else:
 Q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 I=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 I=""
J=mqtt_broker_address
s=ubinascii.hexlify(DEVICE_NAME)
E=b'OTA/OTARequest'
v=b'GenericSensor/SensorData'
O=0
V=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  G="\"deviceType\":\""+DEVICE_TYPE+"\""
  C="\"deviceName\":\""+DEVICE_NAME+"\""
  M="\"deviceName\":\"*\"" 
  X=msg.decode()
  print('ESP received OTA message ',X)
  if G in X and(C in X or M in X):
   n=json.loads(X)
   from ota import OTAUpdater
   i="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   t=n.get("otafiles")
   z=True
   X=DEVICE_NAME+" OTA: "+t
   try:
    o=OTAUpdater(i,t)
    if o.check_for_updates():
     if o.download_and_install_update():
      X+=" updated"
     else:
      X+=" update failed"
    else:
     X+=" up-to-date" 
     z=False
   except Exception as D:
    X+=" err:"+str(D)+" type:"+str(type(D))
   finally:
    print(X)
    F.publish(H,X)
    time.sleep(5)
    if z:
     machine.reset() 
def connect_and_subscribe():
 global s,J,E
 F=MQTTClient(s,J)
 F.set_callback(sub_cb)
 F.connect()
 F.subscribe(E)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(J,E))
 return F
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Q
 global I
 X="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Q!=""):
  X=X+",\"AnaR\":\""+str(Q.read())+"\""
 if(I!=""):
  X=X+",\"DigR\":\""+str(I.value())+"\""
 if error!="":
  X=X+",\"err\":\""+error+"\""
 return X+"}"
try:
 F=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  F.check_msg()
  if(time.time()-O)>V:
   F.publish(v,create_sensor_message())
   O=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

