from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
O="1.0"
o=5
s="GenericSensor/SensorData"
Y="OTA/OTARequest"
D="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 c=ADC(ANALOG_SENSOR_PIN)
else:
 c=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 M=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 M=""
g=mqtt_broker_address
V=ubinascii.hexlify(DEVICE_NAME)
C=b'OTA/OTARequest'
z=b'GenericSensor/SensorData'
l=0
y=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  f="\"deviceType\":\""+DEVICE_TYPE+"\""
  d="\"deviceName\":\""+DEVICE_NAME+"\""
  j="\"deviceName\":\"*\"" 
  h=msg.decode()
  print('ESP received OTA message ',h)
  if f in h and(d in h or j in h):
   i=json.loads(h)
   from ota import OTAUpdater
   S="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   I=i.get("otafiles")
   W=True
   h=DEVICE_NAME+" OTA: "+I
   try:
    E=OTAUpdater(S,I)
    if E.check_for_updates():
     if E.download_and_install_update():
      h+=" updated"
     else:
      h+=" update failed"
    else:
     h+=" up-to-date" 
     W=False
   except Exception as U:
    h+=" err:"+str(U)+" type:"+str(type(U))
   finally:
    print(h)
    N.publish(D,h)
    time.sleep(5)
    if W:
     machine.reset() 
def connect_and_subscribe():
 global V,g,C
 N=MQTTClient(V,g)
 N.set_callback(sub_cb)
 N.connect()
 N.subscribe(C)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(g,C))
 return N
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global c
 global M
 h="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(c!=""):
  h=h+",\"AnaR\":\""+str(c.read())+"\""
 if(M!=""):
  h=h+",\"DigR\":\""+str(M.value())+"\""
 if error!="":
  h=h+",\"err\":\""+error+"\""
 return h+"}"
try:
 N=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  N.check_msg()
  if(time.time()-l)>y:
   N.publish(z,create_sensor_message())
   l=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

