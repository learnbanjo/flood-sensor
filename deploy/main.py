from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
c="1.0"
D=5
F="GenericSensor/SensorData"
p="OTA/OTARequest"
w="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 E=ADC(ANALOG_SENSOR_PIN)
else:
 E=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 X=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 X=""
k=mqtt_broker_address
Y=ubinascii.hexlify(DEVICE_NAME)
r=b'OTA/OTARequest'
I=b'GenericSensor/SensorData'
b=0
a=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  L="\"deviceType\":\""+DEVICE_TYPE+"\""
  g="\"deviceName\":\""+DEVICE_NAME+"\""
  u="\"deviceName\":\"*\"" 
  W=msg.decode()
  print('ESP received OTA message ',W)
  if L in W and(g in W or u in W):
   Q=json.loads(W)
   from ota import OTAUpdater
   f="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   R=Q.get("otafiles")
   m=True
   W=DEVICE_NAME+" OTA: "+R
   try:
    V=OTAUpdater(f,R)
    if V.check_for_updates():
     if V.download_and_install_update():
      W+=" updated"
     else:
      W+=" update failed"
    else:
     W+=" up-to-date" 
     m=False
   except Exception as o:
    W+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(W)
    v.publish(w,W)
    time.sleep(5)
    if m:
     machine.reset() 
def connect_and_subscribe():
 global Y,k,r
 v=MQTTClient(Y,k)
 v.set_callback(sub_cb)
 v.connect()
 v.subscribe(r)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(k,r))
 return v
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global E
 global X
 W="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(E!=""):
  W=W+",\"AnaR\":\""+str(E.read())+"\""
 if(X!=""):
  W=W+",\"DigR\":\""+str(X.value())+"\""
 if error!="":
  W=W+",\"err\":\""+error+"\""
 return W+"}"
try:
 v=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  v.check_msg()
  if(time.time()-b)>a:
   v.publish(I,create_sensor_message())
   b=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

