from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
o="1.0"
u=5
d="GenericSensor/SensorData"
A="OTA/OTARequest"
h="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 r=ADC(ANALOG_SENSOR_PIN)
else:
 r=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 y=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 y=""
S=mqtt_broker_address
g=ubinascii.hexlify(DEVICE_NAME)
l=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
t=0
q=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  n="\"deviceType\":\""+DEVICE_TYPE+"\""
  J="\"deviceName\":\""+DEVICE_NAME+"\""
  L="\"deviceName\":\"*\"" 
  C=msg.decode()
  print('ESP received OTA message ',C)
  if n in C and(J in C or L in C):
   z=json.loads(C)
   from ota import OTAUpdater
   V="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   B=z.get("otafiles")
   F=True
   C=DEVICE_NAME+" OTA: "+B
   try:
    X=OTAUpdater(V,B)
    if X.check_for_updates():
     if X.download_and_install_update():
      C+=" updated"
     else:
      C+=" update failed"
    else:
     C+=" up-to-date" 
     F=False
   except Exception as I:
    C+=" err:"+str(I)+" type:"+str(type(I))
   finally:
    print(C)
    f.publish(h,C)
    time.sleep(5)
    if F:
     machine.reset() 
def connect_and_subscribe():
 global g,S,l
 f=MQTTClient(g,S)
 f.set_callback(sub_cb)
 f.connect()
 f.subscribe(l)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(S,l))
 return f
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global r
 global y
 C="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(r!=""):
  C=C+",\"AnaR\":\""+str(r.read())+"\""
 if(y!=""):
  C=C+",\"DigR\":\""+str(y.value())+"\""
 if error!="":
  C=C+",\"err\":\""+error+"\""
 return C+"}"
try:
 f=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  f.check_msg()
  if(time.time()-t)>q:
   f.publish(E,create_sensor_message())
   t=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

