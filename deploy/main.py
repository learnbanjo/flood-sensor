from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
l="1.0"
P=5
N="GenericSensor/SensorData"
e="OTA/OTARequest"
M="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 F=ADC(ANALOG_SENSOR_PIN)
else:
 F=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 b=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 b=""
Y=mqtt_broker_address
T=ubinascii.hexlify(DEVICE_NAME)
X=b'OTA/OTARequest'
G=b'GenericSensor/SensorData'
a=0
f=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  q="\"deviceType\":\""+DEVICE_TYPE+"\""
  B="\"deviceName\":\""+DEVICE_NAME+"\""
  g="\"deviceName\":\"*\"" 
  K=msg.decode()
  print('ESP received OTA message ',K)
  if q in K and(B in K or g in K):
   V=json.loads(K)
   from ota import OTAUpdater
   y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   m=V.get("otafiles")
   z=True
   K=DEVICE_NAME+" OTA: "+m
   try:
    h=OTAUpdater(y,m)
    if h.check_for_updates():
     if h.download_and_install_update():
      K+=" updated"
     else:
      K+=" update failed"
    else:
     K+=" up-to-date" 
     z=False
   except Exception as L:
    K+=" err:"+str(L)+" type:"+str(type(L))
   finally:
    print(K)
    v.publish(M,K)
    time.sleep(5)
    if z:
     machine.reset() 
def connect_and_subscribe():
 global T,Y,X
 v=MQTTClient(T,Y)
 v.set_callback(sub_cb)
 v.connect()
 v.subscribe(X)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(Y,X))
 return v
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global F
 global b
 K="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(F!=""):
  K=K+",\"AnaR\":\""+str(F.read())+"\""
 if(b!=""):
  K=K+",\"DigR\":\""+str(b.value())+"\""
 if error!="":
  K=K+",\"err\":\""+error+"\""
 return K+"}"
try:
 v=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  v.check_msg()
  if(time.time()-a)>f:
   v.publish(G,create_sensor_message())
   a=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

