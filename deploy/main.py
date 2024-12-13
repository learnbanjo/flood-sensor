from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
j="1.0"
L=5
r="GenericSensor/SensorData"
X="OTA/OTARequest"
A="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 h=ADC(ANALOG_SENSOR_PIN)
else:
 h=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 u=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 u=""
f=mqtt_broker_address
w=ubinascii.hexlify(DEVICE_NAME)
Y=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
g=0
W=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  C="\"deviceType\":\""+DEVICE_TYPE+"\""
  V="\"deviceName\":\""+DEVICE_NAME+"\""
  R="\"deviceName\":\"*\"" 
  d=msg.decode()
  print('ESP received OTA message ',d)
  if C in d and(V in d or R in d):
   l=json.loads(d)
   from ota import OTAUpdater
   G="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   I=l.get("otafiles")
   z=True
   d=DEVICE_NAME+" OTA: "+I
   try:
    c=OTAUpdater(G,I)
    if c.check_for_updates():
     if c.download_and_install_update():
      d+=" updated"
     else:
      d+=" update failed"
    else:
     d+=" up-to-date" 
     z=False
   except Exception as U:
    d+=" err:"+str(U)+" type:"+str(type(U))
   finally:
    print(d)
    n.publish(A,d)
    time.sleep(5)
    if z:
     machine.reset() 
def connect_and_subscribe():
 global w,f,Y
 n=MQTTClient(w,f)
 n.set_callback(sub_cb)
 n.connect()
 n.subscribe(Y)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(f,Y))
 return n
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global h
 global u
 d="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(h!=""):
  d=d+",\"AnaR\":\""+str(h.read())+"\""
 if(u!=""):
  d=d+",\"DigR\":\""+str(u.value())+"\""
 if error!="":
  d=d+",\"err\":\""+error+"\""
 return d+"}"
try:
 n=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  n.check_msg()
  if(time.time()-g)>W:
   n.publish(E,create_sensor_message())
   g=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

