from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
B="1.0"
E=5
d="GenericSensor/SensorData"
p="OTA/OTARequest"
K="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 R=ADC(ANALOG_SENSOR_PIN)
else:
 R=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 m=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 m=""
H=mqtt_broker_address
L=ubinascii.hexlify(DEVICE_NAME)
Q=b'OTA/OTARequest'
y=b'GenericSensor/SensorData'
t=0
C=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  T="\"deviceType\":\""+DEVICE_TYPE+"\""
  f="\"deviceName\":\""+DEVICE_NAME+"\""
  u="\"deviceName\":\"*\"" 
  g=msg.decode()
  print('ESP received OTA message ',g)
  if T in g and(f in g or u in g):
   n=json.loads(g)
   from ota import OTAUpdater
   b="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   U=n.get("otafiles")
   r=True
   g=DEVICE_NAME+" OTA: "+U
   try:
    c=OTAUpdater(b,U)
    if c.check_for_updates():
     if c.download_and_install_update():
      g+=" updated"
     else:
      g+=" update failed"
    else:
     g+=" up-to-date" 
     r=False
   except Exception as X:
    g+=" err:"+str(X)+" type:"+str(type(X))
   finally:
    print(g)
    j.publish(K,g)
    time.sleep(5)
    if r:
     machine.reset() 
def connect_and_subscribe():
 global L,H,Q
 j=MQTTClient(L,H)
 j.set_callback(sub_cb)
 j.connect()
 j.subscribe(Q)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,Q))
 return j
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global R
 global m
 g="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(R!=""):
  g=g+",\"AnaR\":\""+str(R.read())+"\""
 if(m!=""):
  g=g+",\"DigR\":\""+str(m.value())+"\""
 if error!="":
  g=g+",\"err\":\""+error+"\""
 return g+"}"
try:
 j=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  j.check_msg()
  if(time.time()-t)>C:
   j.publish(y,create_sensor_message())
   t=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

