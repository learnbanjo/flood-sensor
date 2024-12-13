from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
L="1.0"
d=5
a="GenericSensor/SensorData"
Y="OTA/OTARequest"
A="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 N=ADC(ANALOG_SENSOR_PIN)
else:
 N=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 F=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 F=""
W=mqtt_broker_address
g=ubinascii.hexlify(DEVICE_NAME)
r=b'OTA/OTARequest'
w=b'GenericSensor/SensorData'
D=0
I=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  E="\"deviceType\":\""+DEVICE_TYPE+"\""
  j="\"deviceName\":\""+DEVICE_NAME+"\""
  k="\"deviceName\":\"*\"" 
  H=msg.decode()
  print('ESP received OTA message ',H)
  if E in H and(j in H or k in H):
   p=json.loads(H)
   from ota import OTAUpdater
   l="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   h=p.get("otafiles")
   R=True
   H=DEVICE_NAME+" OTA: "+h
   try:
    O=OTAUpdater(l,h)
    if O.check_for_updates():
     if O.download_and_install_update():
      H+=" updated"
     else:
      H+=" update failed"
    else:
     H+=" up-to-date" 
     R=False
   except Exception as K:
    H+=" err:"+str(K)+" type:"+str(type(K))
   finally:
    print(H)
    v.publish(A,H)
    time.sleep(5)
    if R:
     machine.reset() 
def connect_and_subscribe():
 global g,W,r
 v=MQTTClient(g,W)
 v.set_callback(sub_cb)
 v.connect()
 v.subscribe(r)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(W,r))
 return v
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global N
 global F
 H="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(N!=""):
  H=H+",\"AnaR\":\""+str(N.read())+"\""
 if(F!=""):
  H=H+",\"DigR\":\""+str(F.value())+"\""
 if error!="":
  H=H+",\"err\":\""+error+"\""
 return H+"}"
try:
 v=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  v.check_msg()
  if(time.time()-D)>I:
   v.publish(w,create_sensor_message())
   D=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

