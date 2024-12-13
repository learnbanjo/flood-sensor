from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
U="1.0"
T=5
S="GenericSensor/SensorData"
a="OTA/OTARequest"
E="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 P=ADC(ANALOG_SENSOR_PIN)
else:
 P=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 u=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 u=""
o=mqtt_broker_address
s=ubinascii.hexlify(DEVICE_NAME)
c=b'OTA/OTARequest'
q=b'GenericSensor/SensorData'
C=0
f=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  V="\"deviceType\":\""+DEVICE_TYPE+"\""
  L="\"deviceName\":\""+DEVICE_NAME+"\""
  G="\"deviceName\":\"*\"" 
  M=msg.decode()
  print('ESP received OTA message ',M)
  if V in M and(L in M or G in M):
   X=json.loads(M)
   from ota import OTAUpdater
   I="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   p=X.get("otafiles")
   i=True
   M=DEVICE_NAME+" OTA: "+p
   try:
    x=OTAUpdater(I,p)
    if x.check_for_updates():
     if x.download_and_install_update():
      M+=" updated"
     else:
      M+=" update failed"
    else:
     M+=" up-to-date" 
     i=False
   except Exception as d:
    M+=" err:"+str(d)+" type:"+str(type(d))
   finally:
    print(M)
    z.publish(E,M)
    time.sleep(5)
    if i:
     machine.reset() 
def connect_and_subscribe():
 global s,o,c
 z=MQTTClient(s,o)
 z.set_callback(sub_cb)
 z.connect()
 z.subscribe(c)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(o,c))
 return z
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global P
 global u
 M="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(P!=""):
  M=M+",\"AnaR\":\""+str(P.read())+"\""
 if(u!=""):
  M=M+",\"DigR\":\""+str(u.value())+"\""
 if error!="":
  M=M+",\"err\":\""+error+"\""
 return M+"}"
try:
 z=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  z.check_msg()
  if(time.time()-C)>f:
   z.publish(q,create_sensor_message())
   C=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

