from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
v="1.0"
D=5
w="GenericSensor/SensorData"
B="OTA/OTARequest"
F="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 U=ADC(ANALOG_SENSOR_PIN)
else:
 U=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 N=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 N=""
k=mqtt_broker_address
m=ubinascii.hexlify(DEVICE_NAME)
e=b'OTA/OTARequest'
L=b'GenericSensor/SensorData'
M=0
i=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  I="\"deviceType\":\""+DEVICE_TYPE+"\""
  p="\"deviceName\":\""+DEVICE_NAME+"\""
  n="\"deviceName\":\"*\"" 
  H=msg.decode()
  print('ESP received OTA message ',H)
  if I in H and(p in H or n in H):
   P=json.loads(H)
   from ota import OTAUpdater
   u="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   d=P.get("otafiles")
   t=True
   H=DEVICE_NAME+" OTA: "+d
   try:
    V=OTAUpdater(u,d)
    if V.check_for_updates():
     if V.download_and_install_update():
      H+=" updated"
     else:
      H+=" update failed"
    else:
     H+=" up-to-date" 
     t=False
   except Exception as C:
    H+=" err:"+str(C)+" type:"+str(type(C))
   finally:
    print(H)
    j.publish(F,H)
    time.sleep(5)
    if t:
     machine.reset() 
def connect_and_subscribe():
 global m,k,e
 j=MQTTClient(m,k)
 j.set_callback(sub_cb)
 j.connect()
 j.subscribe(e)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(k,e))
 return j
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global U
 global N
 H="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(U!=""):
  H=H+",\"AnaR\":\""+str(U.read())+"\""
 if(N!=""):
  H=H+",\"DigR\":\""+str(N.value())+"\""
 if error!="":
  H=H+",\"err\":\""+error+"\""
 return H+"}"
try:
 j=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  j.check_msg()
  if(time.time()-M)>i:
   j.publish(L,create_sensor_message())
   M=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

