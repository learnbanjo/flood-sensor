from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
E="1.0"
u=5
Q="GenericSensor/SensorData"
S="OTA/OTARequest"
B="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 g=ADC(ANALOG_SENSOR_PIN)
else:
 g=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 T=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 T=""
m=mqtt_broker_address
x=ubinascii.hexlify(DEVICE_NAME)
F=b'OTA/OTARequest'
R=b'GenericSensor/SensorData'
D=0
H=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  b="\"deviceType\":\""+DEVICE_TYPE+"\""
  h="\"deviceName\":\""+DEVICE_NAME+"\""
  j="\"deviceName\":\"*\"" 
  N=msg.decode()
  print('ESP received OTA message ',N)
  if b in N and(h in N or j in N):
   f=json.loads(N)
   from ota import OTAUpdater
   l="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   p=f.get("otafiles")
   X=True
   N=DEVICE_NAME+" OTA: "+p
   try:
    L=OTAUpdater(l,p)
    if L.check_for_updates():
     if L.download_and_install_update():
      N+=" updated"
     else:
      N+=" update failed"
    else:
     N+=" up-to-date" 
     X=False
   except Exception as O:
    N+=" err:"+str(O)+" type:"+str(type(O))
   finally:
    print(N)
    c.publish(B,N)
    time.sleep(5)
    if X:
     machine.reset() 
def connect_and_subscribe():
 global x,m,F
 c=MQTTClient(x,m)
 c.set_callback(sub_cb)
 c.connect()
 c.subscribe(F)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(m,F))
 return c
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global g
 global T
 N="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(g!=""):
  N=N+",\"AnaR\":\""+str(g.read())+"\""
 if(T!=""):
  N=N+",\"DigR\":\""+str(T.value())+"\""
 if error!="":
  N=N+",\"err\":\""+error+"\""
 return N+"}"
try:
 c=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  c.check_msg()
  if(time.time()-D)>H:
   c.publish(R,create_sensor_message())
   D=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

