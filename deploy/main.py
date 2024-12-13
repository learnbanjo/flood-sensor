from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
U="1.0"
E=5
D="GenericSensor/SensorData"
N="OTA/OTARequest"
u="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 b=ADC(ANALOG_SENSOR_PIN)
else:
 b=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 B=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 B=""
x=mqtt_broker_address
J=ubinascii.hexlify(DEVICE_NAME)
a=b'OTA/OTARequest'
V=b'GenericSensor/SensorData'
I=0
C=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  O="\"deviceType\":\""+DEVICE_TYPE+"\""
  w="\"deviceName\":\""+DEVICE_NAME+"\""
  y="\"deviceName\":\"*\"" 
  A=msg.decode()
  print('ESP received OTA message ',A)
  if O in A and(w in A or y in A):
   f=json.loads(A)
   from ota import OTAUpdater
   i="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   S=f.get("otafiles")
   h=True
   A=DEVICE_NAME+" OTA: "+S
   try:
    v=OTAUpdater(i,S)
    if v.check_for_updates():
     if v.download_and_install_update():
      A+=" updated"
     else:
      A+=" update failed"
    else:
     A+=" up-to-date" 
     h=False
   except Exception as p:
    A+=" err:"+str(p)+" type:"+str(type(p))
   finally:
    print(A)
    K.publish(u,A)
    time.sleep(5)
    if h:
     machine.reset() 
def connect_and_subscribe():
 global J,x,a
 K=MQTTClient(J,x)
 K.set_callback(sub_cb)
 K.connect()
 K.subscribe(a)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(x,a))
 return K
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global b
 global B
 A="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(b!=""):
  A=A+",\"AnaR\":\""+str(b.read())+"\""
 if(B!=""):
  A=A+",\"DigR\":\""+str(B.value())+"\""
 if error!="":
  A=A+",\"err\":\""+error+"\""
 return A+"}"
try:
 K=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  K.check_msg()
  if(time.time()-I)>C:
   K.publish(V,create_sensor_message())
   I=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

