from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
P="1.0"
z=5
V="GenericSensor/SensorData"
N="OTA/OTARequest"
a="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 c=ADC(ANALOG_SENSOR_PIN)
else:
 c=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 A=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 A=""
H=mqtt_broker_address
X=ubinascii.hexlify(DEVICE_NAME)
B=b'OTA/OTARequest'
e=b'GenericSensor/SensorData'
E=0
l=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  j="\"deviceType\":\""+DEVICE_TYPE+"\""
  R="\"deviceName\":\""+DEVICE_NAME+"\""
  p="\"deviceName\":\"*\"" 
  D=msg.decode()
  print('ESP received OTA message ',D)
  if j in D and(R in D or p in D):
   m=json.loads(D)
   from ota import OTAUpdater
   J="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   v=m.get("otafiles")
   K=True
   D=DEVICE_NAME+" OTA: "+v
   try:
    k=OTAUpdater(J,v)
    if k.check_for_updates():
     if k.download_and_install_update():
      D+=" updated"
     else:
      D+=" update failed"
    else:
     D+=" up-to-date" 
     K=False
   except Exception as x:
    D+=" err:"+str(x)+" type:"+str(type(x))
   finally:
    print(D)
    g.publish(a,D)
    time.sleep(5)
    if K:
     machine.reset() 
def connect_and_subscribe():
 global X,H,B
 g=MQTTClient(X,H)
 g.set_callback(sub_cb)
 g.connect()
 g.subscribe(B)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,B))
 return g
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global c
 global A
 D="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(c!=""):
  D=D+",\"AnaR\":\""+str(c.read())+"\""
 if(A!=""):
  D=D+",\"DigR\":\""+str(A.value())+"\""
 if error!="":
  D=D+",\"err\":\""+error+"\""
 return D+"}"
try:
 g=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  g.check_msg()
  if(time.time()-E)>l:
   g.publish(e,create_sensor_message())
   E=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

