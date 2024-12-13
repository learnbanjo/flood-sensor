from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
s="1.0"
l=5
Y="GenericSensor/SensorData"
g="OTA/OTARequest"
C="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 B=ADC(ANALOG_SENSOR_PIN)
else:
 B=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 F=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 F=""
p=mqtt_broker_address
v=ubinascii.hexlify(DEVICE_NAME)
u=b'OTA/OTARequest'
K=b'GenericSensor/SensorData'
h=0
m=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  J="\"deviceType\":\""+DEVICE_TYPE+"\""
  O="\"deviceName\":\""+DEVICE_NAME+"\""
  L="\"deviceName\":\"*\"" 
  T=msg.decode()
  print('ESP received OTA message ',T)
  if J in T and(O in T or L in T):
   e=json.loads(T)
   from ota import OTAUpdater
   k="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   b=e.get("otafiles")
   S=True
   T=DEVICE_NAME+" OTA: "+b
   try:
    N=OTAUpdater(k,b)
    if N.check_for_updates():
     if N.download_and_install_update():
      T+=" updated"
     else:
      T+=" update failed"
    else:
     T+=" up-to-date" 
     S=False
   except Exception as z:
    T+=" err:"+str(z)+" type:"+str(type(z))
   finally:
    print(T)
    w.publish(C,T)
    time.sleep(5)
    if S:
     machine.reset() 
def connect_and_subscribe():
 global v,p,u
 w=MQTTClient(v,p)
 w.set_callback(sub_cb)
 w.connect()
 w.subscribe(u)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(p,u))
 return w
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global B
 global F
 T="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(B!=""):
  T=T+",\"AnaR\":\""+str(B.read())+"\""
 if(F!=""):
  T=T+",\"DigR\":\""+str(F.value())+"\""
 if error!="":
  T=T+",\"err\":\""+error+"\""
 return T+"}"
try:
 w=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  w.check_msg()
  if(time.time()-h)>m:
   w.publish(K,create_sensor_message())
   h=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

