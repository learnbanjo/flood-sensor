from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
V="1.0"
J=5
R="GenericSensor/SensorData"
u="OTA/OTARequest"
L="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 d=ADC(ANALOG_SENSOR_PIN)
else:
 d=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 A=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 A=""
G=mqtt_broker_address
m=ubinascii.hexlify(DEVICE_NAME)
b=b'OTA/OTARequest'
v=b'GenericSensor/SensorData'
Y=0
B=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  T="\"deviceType\":\""+DEVICE_TYPE+"\""
  O="\"deviceName\":\""+DEVICE_NAME+"\""
  h="\"deviceName\":\"*\"" 
  z=msg.decode()
  print('ESP received OTA message ',z)
  if T in z and(O in z or h in z):
   j=json.loads(z)
   from ota import OTAUpdater
   H="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   P=j.get("otafiles")
   N=True
   z=DEVICE_NAME+" OTA: "+P
   try:
    e=OTAUpdater(H,P)
    if e.check_for_updates():
     if e.download_and_install_update():
      z+=" updated"
     else:
      z+=" update failed"
    else:
     z+=" up-to-date" 
     N=False
   except Exception as x:
    z+=" err:"+str(x)+" type:"+str(type(x))
   finally:
    print(z)
    D.publish(L,z)
    time.sleep(5)
    if N:
     machine.reset() 
def connect_and_subscribe():
 global m,G,b
 D=MQTTClient(m,G)
 D.set_callback(sub_cb)
 D.connect()
 D.subscribe(b)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(G,b))
 return D
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global d
 global A
 z="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(d!=""):
  z=z+",\"AnaR\":\""+str(d.read())+"\""
 if(A!=""):
  z=z+",\"DigR\":\""+str(A.value())+"\""
 if error!="":
  z=z+",\"err\":\""+error+"\""
 return z+"}"
try:
 D=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  D.check_msg()
  if(time.time()-Y)>B:
   D.publish(v,create_sensor_message())
   Y=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

