from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
u="1.0"
I=5
i="GenericSensor/SensorData"
U="OTA/OTARequest"
e="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 o=ADC(ANALOG_SENSOR_PIN)
else:
 o=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 c=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 c=""
v=mqtt_broker_address
g=ubinascii.hexlify(DEVICE_NAME)
A=b'OTA/OTARequest'
R=b'GenericSensor/SensorData'
l=0
d=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  H="\"deviceType\":\""+DEVICE_TYPE+"\""
  j="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  z=msg.decode()
  print('ESP received OTA message ',z)
  if H in z and(j in z or Q in z):
   G=json.loads(z)
   from ota import OTAUpdater
   k="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   V=G.get("otafiles")
   O=True
   z=DEVICE_NAME+" OTA: "+V
   try:
    C=OTAUpdater(k,V)
    if C.check_for_updates():
     if C.download_and_install_update():
      z+=" updated"
     else:
      z+=" update failed"
    else:
     z+=" up-to-date" 
     O=False
   except Exception as t:
    z+=" err:"+str(t)+" type:"+str(type(t))
   finally:
    print(z)
    M.publish(e,z)
    time.sleep(5)
    if O:
     machine.reset() 
def connect_and_subscribe():
 global g,v,A
 M=MQTTClient(g,v)
 M.set_callback(sub_cb)
 M.connect()
 M.subscribe(A)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(v,A))
 return M
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global o
 global c
 z="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(o!=""):
  z=z+",\"AnaR\":\""+str(o.read())+"\""
 if(c!=""):
  z=z+",\"DigR\":\""+str(c.value())+"\""
 if error!="":
  z=z+",\"err\":\""+error+"\""
 return z+"}"
try:
 M=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  M.check_msg()
  if(time.time()-l)>d:
   M.publish(R,create_sensor_message())
   l=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

