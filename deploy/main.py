from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
F="1.0"
G=5
Q="GenericSensor/SensorData"
m="OTA/OTARequest"
q="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 V=ADC(ANALOG_SENSOR_PIN)
else:
 V=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 i=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 i=""
K=mqtt_broker_address
R=ubinascii.hexlify(DEVICE_NAME)
p=b'OTA/OTARequest'
B=b'GenericSensor/SensorData'
E=0
j=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  a="\"deviceType\":\""+DEVICE_TYPE+"\""
  N="\"deviceName\":\""+DEVICE_NAME+"\""
  o="\"deviceName\":\"*\"" 
  W=msg.decode()
  print('ESP received OTA message ',W)
  if a in W and(N in W or o in W):
   X=json.loads(W)
   from ota import OTAUpdater
   f="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   h=X.get("otafiles")
   l=True
   W=DEVICE_NAME+" OTA: "+h
   try:
    b=OTAUpdater(f,h)
    if b.check_for_updates():
     if b.download_and_install_update():
      W+=" updated"
     else:
      W+=" update failed"
    else:
     W+=" up-to-date" 
     l=False
   except Exception as k:
    W+=" err:"+str(k)+" type:"+str(type(k))
   finally:
    print(W)
    D.publish(q,W)
    time.sleep(5)
    if l:
     machine.reset() 
def connect_and_subscribe():
 global R,K,p
 D=MQTTClient(R,K)
 D.set_callback(sub_cb)
 D.connect()
 D.subscribe(p)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(K,p))
 return D
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global V
 global i
 W="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(V!=""):
  W=W+",\"AnaR\":\""+str(V.read())+"\""
 if(i!=""):
  W=W+",\"DigR\":\""+str(i.value())+"\""
 if error!="":
  W=W+",\"err\":\""+error+"\""
 return W+"}"
try:
 D=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  D.check_msg()
  if(time.time()-E)>j:
   D.publish(B,create_sensor_message())
   E=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

