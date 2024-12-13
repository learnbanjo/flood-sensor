from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
o="1.0"
C=5
q="GenericSensor/SensorData"
J="OTA/OTARequest"
f="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 A=ADC(ANALOG_SENSOR_PIN)
else:
 A=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 r=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 r=""
D=mqtt_broker_address
O=ubinascii.hexlify(DEVICE_NAME)
m=b'OTA/OTARequest'
z=b'GenericSensor/SensorData'
v=0
N=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  W="\"deviceType\":\""+DEVICE_TYPE+"\""
  u="\"deviceName\":\""+DEVICE_NAME+"\""
  t="\"deviceName\":\"*\"" 
  h=msg.decode()
  print('ESP received OTA message ',h)
  if W in h and(u in h or t in h):
   G=json.loads(h)
   from ota import OTAUpdater
   T="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   E=G.get("otafiles")
   n=True
   h=DEVICE_NAME+" OTA: "+E
   try:
    Y=OTAUpdater(T,E)
    if Y.check_for_updates():
     if Y.download_and_install_update():
      h+=" updated"
     else:
      h+=" update failed"
    else:
     h+=" up-to-date" 
     n=False
   except Exception as j:
    h+=" err:"+str(j)+" type:"+str(type(j))
   finally:
    print(h)
    x.publish(f,h)
    time.sleep(5)
    if n:
     machine.reset() 
def connect_and_subscribe():
 global O,D,m
 x=MQTTClient(O,D)
 x.set_callback(sub_cb)
 x.connect()
 x.subscribe(m)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(D,m))
 return x
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global A
 global r
 h="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(A!=""):
  h=h+",\"AnaR\":\""+str(A.read())+"\""
 if(r!=""):
  h=h+",\"DigR\":\""+str(r.value())+"\""
 if error!="":
  h=h+",\"err\":\""+error+"\""
 return h+"}"
try:
 x=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  x.check_msg()
  if(time.time()-v)>N:
   x.publish(z,create_sensor_message())
   v=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

