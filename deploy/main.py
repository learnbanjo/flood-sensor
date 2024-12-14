from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
p="1.0"
E=5
y="GenericSensor/SensorData"
T="OTA/OTARequest"
N="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 G=ADC(ANALOG_SENSOR_PIN)
else:
 G=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 g=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 g=""
c=mqtt_broker_address
R=ubinascii.hexlify(DEVICE_NAME)
v=b'OTA/OTARequest'
K=b'GenericSensor/SensorData'
C=0
m=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  s="\"deviceType\":\""+DEVICE_TYPE+"\""
  i="\"deviceName\":\""+DEVICE_NAME+"\""
  w="\"deviceName\":\"*\"" 
  F=msg.decode()
  print('ESP received OTA message ',F)
  if s in F and(i in F or w in F):
   k=json.loads(F)
   from ota import OTAUpdater
   f="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   u=k.get("otafiles")
   A=True
   F=DEVICE_NAME+" OTA: "+u
   try:
    M=OTAUpdater(f,u)
    if M.check_for_updates():
     if M.download_and_install_update():
      F+=" updated"
     else:
      F+=" update failed"
    else:
     F+=" up-to-date" 
     A=False
   except Exception as j:
    F+=" err:"+str(j)+" type:"+str(type(j))
   finally:
    print(F)
    r.publish(N,F)
    time.sleep(5)
    if A:
     machine.reset() 
def connect_and_subscribe():
 global R,c,v
 r=MQTTClient(R,c)
 r.set_callback(sub_cb)
 r.connect()
 r.subscribe(v)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(c,v))
 return r
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global G
 global g
 F="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(G!=""):
  F=F+",\"AnaR\":\""+str(G.read())+"\""
 if(g!=""):
  F=F+",\"DigR\":\""+str(g.value())+"\""
 if error!="":
  F=F+",\"err\":\""+error+"\""
 return F+"}"
try:
 r=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  r.check_msg()
  if(time.time()-C)>m:
   r.publish(K,create_sensor_message())
   C=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

