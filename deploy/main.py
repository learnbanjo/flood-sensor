from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
w="1.0"
x=5
A="GenericSensor/SensorData"
T="OTA/OTARequest"
f="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 j=ADC(ANALOG_SENSOR_PIN)
else:
 j=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 z=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 z=""
y=mqtt_broker_address
n=ubinascii.hexlify(DEVICE_NAME)
l=b'OTA/OTARequest'
M=b'GenericSensor/SensorData'
W=0
F=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  t="\"deviceType\":\""+DEVICE_TYPE+"\""
  a="\"deviceName\":\""+DEVICE_NAME+"\""
  V="\"deviceName\":\"*\"" 
  s=msg.decode()
  print('ESP received OTA message ',s)
  if t in s and(a in s or V in s):
   G=json.loads(s)
   from ota import OTAUpdater
   I="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   J=G.get("otafiles")
   h=True
   s=DEVICE_NAME+" OTA: "+J
   try:
    Y=OTAUpdater(I,J)
    if Y.check_for_updates():
     if Y.download_and_install_update():
      s+=" updated"
     else:
      s+=" update failed"
    else:
     s+=" up-to-date" 
     h=False
   except Exception as c:
    s+=" err:"+str(c)+" type:"+str(type(c))
   finally:
    print(s)
    b.publish(f,s)
    time.sleep(5)
    if h:
     machine.reset() 
def connect_and_subscribe():
 global n,y,l
 b=MQTTClient(n,y)
 b.set_callback(sub_cb)
 b.connect()
 b.subscribe(l)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(y,l))
 return b
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global j
 global z
 s="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(j!=""):
  s=s+",\"AnaR\":\""+str(j.read())+"\""
 if(z!=""):
  s=s+",\"DigR\":\""+str(z.value())+"\""
 if error!="":
  s=s+",\"err\":\""+error+"\""
 return s+"}"
try:
 b=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  b.check_msg()
  if(time.time()-W)>F:
   b.publish(M,create_sensor_message())
   W=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

