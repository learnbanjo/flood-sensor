from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
a="1.0"
r=5
o="GenericSensor/SensorData"
B="OTA/OTARequest"
M="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 V=ADC(ANALOG_SENSOR_PIN)
else:
 V=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 j=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 j=""
S=mqtt_broker_address
L=ubinascii.hexlify(DEVICE_NAME)
G=b'OTA/OTARequest'
l=b'GenericSensor/SensorData'
E=0
g=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  J="\"deviceType\":\""+DEVICE_TYPE+"\""
  P="\"deviceName\":\""+DEVICE_NAME+"\""
  f="\"deviceName\":\"*\"" 
  W=msg.decode()
  print('ESP received OTA message ',W)
  if J in W and(P in W or f in W):
   I=json.loads(W)
   from ota import OTAUpdater
   F="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   k=I.get("otafiles")
   R=True
   W=DEVICE_NAME+" OTA: "+k
   try:
    A=OTAUpdater(F,k)
    if A.check_for_updates():
     if A.download_and_install_update():
      W+=" updated"
     else:
      W+=" update failed"
    else:
     W+=" up-to-date" 
     R=False
   except Exception as O:
    W+=" err:"+str(O)+" type:"+str(type(O))
   finally:
    print(W)
    b.publish(M,W)
    time.sleep(5)
    if R:
     machine.reset() 
def connect_and_subscribe():
 global L,S,G
 b=MQTTClient(L,S)
 b.set_callback(sub_cb)
 b.connect()
 b.subscribe(G)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(S,G))
 return b
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global V
 global j
 W="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(V!=""):
  W=W+",\"AnaR\":\""+str(V.read())+"\""
 if(j!=""):
  W=W+",\"DigR\":\""+str(j.value())+"\""
 if error!="":
  W=W+",\"err\":\""+error+"\""
 return W+"}"
try:
 b=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  b.check_msg()
  if(time.time()-E)>g:
   b.publish(l,create_sensor_message())
   E=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

