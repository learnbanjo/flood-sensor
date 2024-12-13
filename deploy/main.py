from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
q="1.0"
j=5
R="GenericSensor/SensorData"
D="OTA/OTARequest"
e="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 b=ADC(ANALOG_SENSOR_PIN)
else:
 b=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 M=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 M=""
H=mqtt_broker_address
G=ubinascii.hexlify(DEVICE_NAME)
n=b'OTA/OTARequest'
h=b'GenericSensor/SensorData'
J=0
l=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  Q="\"deviceType\":\""+DEVICE_TYPE+"\""
  y="\"deviceName\":\""+DEVICE_NAME+"\""
  F="\"deviceName\":\"*\"" 
  s=msg.decode()
  print('ESP received OTA message ',s)
  if Q in s and(y in s or F in s):
   t=json.loads(s)
   from ota import OTAUpdater
   K="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   O=t.get("otafiles")
   g=True
   s=DEVICE_NAME+" OTA: "+O
   try:
    I=OTAUpdater(K,O)
    if I.check_for_updates():
     if I.download_and_install_update():
      s+=" updated"
     else:
      s+=" update failed"
    else:
     s+=" up-to-date" 
     g=False
   except Exception as v:
    s+=" err:"+str(v)+" type:"+str(type(v))
   finally:
    print(s)
    C.publish(e,s)
    time.sleep(5)
    if g:
     machine.reset() 
def connect_and_subscribe():
 global G,H,n
 C=MQTTClient(G,H)
 C.set_callback(sub_cb)
 C.connect()
 C.subscribe(n)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,n))
 return C
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global b
 global M
 s="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(b!=""):
  s=s+",\"AnaR\":\""+str(b.read())+"\""
 if(M!=""):
  s=s+",\"DigR\":\""+str(M.value())+"\""
 if error!="":
  s=s+",\"err\":\""+error+"\""
 return s+"}"
try:
 C=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  C.check_msg()
  if(time.time()-J)>l:
   C.publish(h,create_sensor_message())
   J=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

