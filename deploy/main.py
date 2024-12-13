from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
m="1.0"
s=5
G="GenericSensor/SensorData"
d="OTA/OTARequest"
K="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 v=ADC(ANALOG_SENSOR_PIN)
else:
 v=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 S=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 S=""
B=mqtt_broker_address
o=ubinascii.hexlify(DEVICE_NAME)
u=b'OTA/OTARequest'
M=b'GenericSensor/SensorData'
H=0
t=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  j="\"deviceType\":\""+DEVICE_TYPE+"\""
  Q="\"deviceName\":\""+DEVICE_NAME+"\""
  N="\"deviceName\":\"*\"" 
  e=msg.decode()
  print('ESP received OTA message ',e)
  if j in e and(Q in e or N in e):
   L=json.loads(e)
   from ota import OTAUpdater
   Y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   h=L.get("otafiles")
   b=True
   e=DEVICE_NAME+" OTA: "+h
   try:
    z=OTAUpdater(Y,h)
    if z.check_for_updates():
     if z.download_and_install_update():
      e+=" updated"
     else:
      e+=" update failed"
    else:
     e+=" up-to-date" 
     b=False
   except Exception as y:
    e+=" err:"+str(y)+" type:"+str(type(y))
   finally:
    print(e)
    x.publish(K,e)
    time.sleep(5)
    if b:
     machine.reset() 
def connect_and_subscribe():
 global o,B,u
 x=MQTTClient(o,B)
 x.set_callback(sub_cb)
 x.connect()
 x.subscribe(u)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(B,u))
 return x
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global v
 global S
 e="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(v!=""):
  e=e+",\"AnaR\":\""+str(v.read())+"\""
 if(S!=""):
  e=e+",\"DigR\":\""+str(S.value())+"\""
 if error!="":
  e=e+",\"err\":\""+error+"\""
 return e+"}"
try:
 x=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  x.check_msg()
  if(time.time()-H)>t:
   x.publish(M,create_sensor_message())
   H=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

