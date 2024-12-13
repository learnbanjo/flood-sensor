from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
b="1.0"
C=5
y="GenericSensor/SensorData"
Q="OTA/OTARequest"
a="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 r=ADC(ANALOG_SENSOR_PIN)
else:
 r=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 E=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 E=""
G=mqtt_broker_address
T=ubinascii.hexlify(DEVICE_NAME)
i=b'OTA/OTARequest'
p=b'GenericSensor/SensorData'
N=0
u=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  t="\"deviceType\":\""+DEVICE_TYPE+"\""
  R="\"deviceName\":\""+DEVICE_NAME+"\""
  j="\"deviceName\":\"*\"" 
  d=msg.decode()
  print('ESP received OTA message ',d)
  if t in d and(R in d or j in d):
   h=json.loads(d)
   from ota import OTAUpdater
   m="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   v=h.get("otafiles")
   g=True
   d=DEVICE_NAME+" OTA: "+v
   try:
    x=OTAUpdater(m,v)
    if x.check_for_updates():
     if x.download_and_install_update():
      d+=" updated"
     else:
      d+=" update failed"
    else:
     d+=" up-to-date" 
     g=False
   except Exception as e:
    d+=" err:"+str(e)+" type:"+str(type(e))
   finally:
    print(d)
    B.publish(a,d)
    time.sleep(5)
    if g:
     machine.reset() 
def connect_and_subscribe():
 global T,G,i
 B=MQTTClient(T,G)
 B.set_callback(sub_cb)
 B.connect()
 B.subscribe(i)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(G,i))
 return B
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global r
 global E
 d="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(r!=""):
  d=d+",\"AnaR\":\""+str(r.read())+"\""
 if(E!=""):
  d=d+",\"DigR\":\""+str(E.value())+"\""
 if error!="":
  d=d+",\"err\":\""+error+"\""
 return d+"}"
try:
 B=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  B.check_msg()
  if(time.time()-N)>u:
   B.publish(p,create_sensor_message())
   N=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

