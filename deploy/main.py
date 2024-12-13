from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
D="1.0"
t=5
k="GenericSensor/SensorData"
b="OTA/OTARequest"
h="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 i=ADC(ANALOG_SENSOR_PIN)
else:
 i=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 a=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 a=""
M=mqtt_broker_address
j=ubinascii.hexlify(DEVICE_NAME)
R=b'OTA/OTARequest'
S=b'GenericSensor/SensorData'
O=0
g=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  z="\"deviceType\":\""+DEVICE_TYPE+"\""
  G="\"deviceName\":\""+DEVICE_NAME+"\""
  F="\"deviceName\":\"*\"" 
  Y=msg.decode()
  print('ESP received OTA message ',Y)
  if z in Y and(G in Y or F in Y):
   w=json.loads(Y)
   from ota import OTAUpdater
   T="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   U=w.get("otafiles")
   J=True
   Y=DEVICE_NAME+" OTA: "+U
   try:
    B=OTAUpdater(T,U)
    if B.check_for_updates():
     if B.download_and_install_update():
      Y+=" updated"
     else:
      Y+=" update failed"
    else:
     Y+=" up-to-date" 
     J=False
   except Exception as l:
    Y+=" err:"+str(l)+" type:"+str(type(l))
   finally:
    print(Y)
    f.publish(h,Y)
    time.sleep(5)
    if J:
     machine.reset() 
def connect_and_subscribe():
 global j,M,R
 f=MQTTClient(j,M)
 f.set_callback(sub_cb)
 f.connect()
 f.subscribe(R)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(M,R))
 return f
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global i
 global a
 Y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(i!=""):
  Y=Y+",\"AnaR\":\""+str(i.read())+"\""
 if(a!=""):
  Y=Y+",\"DigR\":\""+str(a.value())+"\""
 if error!="":
  Y=Y+",\"err\":\""+error+"\""
 return Y+"}"
try:
 f=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  f.check_msg()
  if(time.time()-O)>g:
   f.publish(S,create_sensor_message())
   O=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

