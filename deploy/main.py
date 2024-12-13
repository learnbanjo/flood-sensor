from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
m="1.0"
W=5
C="GenericSensor/SensorData"
p="OTA/OTARequest"
E="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 T=ADC(ANALOG_SENSOR_PIN)
else:
 T=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 t=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 t=""
s=mqtt_broker_address
u=ubinascii.hexlify(DEVICE_NAME)
z=b'OTA/OTARequest'
b=b'GenericSensor/SensorData'
f=0
q=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  k="\"deviceType\":\""+DEVICE_TYPE+"\""
  Y="\"deviceName\":\""+DEVICE_NAME+"\""
  o="\"deviceName\":\"*\"" 
  g=msg.decode()
  print('ESP received OTA message ',g)
  if k in g and(Y in g or o in g):
   R=json.loads(g)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   J=R.get("otafiles")
   B=True
   g=DEVICE_NAME+" OTA: "+J
   try:
    I=OTAUpdater(e,J)
    if I.check_for_updates():
     if I.download_and_install_update():
      g+=" updated"
     else:
      g+=" update failed"
    else:
     g+=" up-to-date" 
     B=False
   except Exception as a:
    g+=" err:"+str(a)+" type:"+str(type(a))
   finally:
    print(g)
    F.publish(E,g)
    time.sleep(5)
    if B:
     machine.reset() 
def connect_and_subscribe():
 global u,s,z
 F=MQTTClient(u,s)
 F.set_callback(sub_cb)
 F.connect()
 F.subscribe(z)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(s,z))
 return F
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global T
 global t
 g="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(T!=""):
  g=g+",\"AnaR\":\""+str(T.read())+"\""
 if(t!=""):
  g=g+",\"DigR\":\""+str(t.value())+"\""
 if error!="":
  g=g+",\"err\":\""+error+"\""
 return g+"}"
try:
 F=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  F.check_msg()
  if(time.time()-f)>q:
   F.publish(b,create_sensor_message())
   f=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

