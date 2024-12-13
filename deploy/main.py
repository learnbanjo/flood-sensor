from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
E="1.0"
C=5
K="GenericSensor/SensorData"
F="OTA/OTARequest"
u="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 O=ADC(ANALOG_SENSOR_PIN)
else:
 O=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 R=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 R=""
b=mqtt_broker_address
B=ubinascii.hexlify(DEVICE_NAME)
s=b'OTA/OTARequest'
c=b'GenericSensor/SensorData'
i=0
U=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  L="\"deviceType\":\""+DEVICE_TYPE+"\""
  f="\"deviceName\":\""+DEVICE_NAME+"\""
  N="\"deviceName\":\"*\"" 
  o=msg.decode()
  print('ESP received OTA message ',o)
  if L in o and(f in o or N in o):
   G=json.loads(o)
   from ota import OTAUpdater
   A="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   d=G.get("otafiles")
   e=True
   o=DEVICE_NAME+" OTA: "+d
   try:
    v=OTAUpdater(A,d)
    if v.check_for_updates():
     if v.download_and_install_update():
      o+=" updated"
     else:
      o+=" update failed"
    else:
     o+=" up-to-date" 
     e=False
   except Exception as Y:
    o+=" err:"+str(Y)+" type:"+str(type(Y))
   finally:
    print(o)
    Q.publish(u,o)
    time.sleep(5)
    if e:
     machine.reset() 
def connect_and_subscribe():
 global B,b,s
 Q=MQTTClient(B,b)
 Q.set_callback(sub_cb)
 Q.connect()
 Q.subscribe(s)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(b,s))
 return Q
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global O
 global R
 o="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(O!=""):
  o=o+",\"AnaR\":\""+str(O.read())+"\""
 if(R!=""):
  o=o+",\"DigR\":\""+str(R.value())+"\""
 if error!="":
  o=o+",\"err\":\""+error+"\""
 return o+"}"
try:
 Q=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  Q.check_msg()
  if(time.time()-i)>U:
   Q.publish(c,create_sensor_message())
   i=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

