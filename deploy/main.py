from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
e="1.0"
m=5
z="GenericSensor/SensorData"
S="OTA/OTARequest"
x="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 v=ADC(ANALOG_SENSOR_PIN)
else:
 v=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 y=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 y=""
H=mqtt_broker_address
F=ubinascii.hexlify(DEVICE_NAME)
V=b'OTA/OTARequest'
L=b'GenericSensor/SensorData'
T=0
W=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  O="\"deviceType\":\""+DEVICE_TYPE+"\""
  i="\"deviceName\":\""+DEVICE_NAME+"\""
  E="\"deviceName\":\"*\"" 
  s=msg.decode()
  print('ESP received OTA message ',s)
  if O in s and(i in s or E in s):
   d=json.loads(s)
   from ota import OTAUpdater
   R="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   t=d.get("otafiles")
   N=True
   s=DEVICE_NAME+" OTA: "+t
   try:
    A=OTAUpdater(R,t)
    if A.check_for_updates():
     if A.download_and_install_update():
      s+=" updated"
     else:
      s+=" update failed"
    else:
     s+=" up-to-date" 
     N=False
   except Exception as h:
    s+=" err:"+str(h)+" type:"+str(type(h))
   finally:
    print(s)
    D.publish(x,s)
    time.sleep(5)
    if N:
     machine.reset() 
def connect_and_subscribe():
 global F,H,V
 D=MQTTClient(F,H)
 D.set_callback(sub_cb)
 D.connect()
 D.subscribe(V)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,V))
 return D
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global v
 global y
 s="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(v!=""):
  s=s+",\"AnaR\":\""+str(v.read())+"\""
 if(y!=""):
  s=s+",\"DigR\":\""+str(y.value())+"\""
 if error!="":
  s=s+",\"err\":\""+error+"\""
 return s+"}"
try:
 D=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  D.check_msg()
  if(time.time()-T)>W:
   D.publish(L,create_sensor_message())
   T=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

