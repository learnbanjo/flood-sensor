from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
W="1.0"
V=5
s="GenericSensor/SensorData"
N="OTA/OTARequest"
a="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 B=ADC(ANALOG_SENSOR_PIN)
else:
 B=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 x=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 x=""
C=mqtt_broker_address
b=ubinascii.hexlify(DEVICE_NAME)
L=b'OTA/OTARequest'
j=b'GenericSensor/SensorData'
T=0
H=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  l="\"deviceType\":\""+DEVICE_TYPE+"\""
  i="\"deviceName\":\""+DEVICE_NAME+"\""
  u="\"deviceName\":\"*\"" 
  E=msg.decode()
  print('ESP received OTA message ',E)
  if l in E and(i in E or u in E):
   p=json.loads(E)
   from ota import OTAUpdater
   Y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   J=p.get("otafiles")
   y=True
   E=DEVICE_NAME+" OTA: "+J
   try:
    A=OTAUpdater(Y,J)
    if A.check_for_updates():
     if A.download_and_install_update():
      E+=" updated"
     else:
      E+=" update failed"
    else:
     E+=" up-to-date" 
     y=False
   except Exception as R:
    E+=" err:"+str(R)+" type:"+str(type(R))
   finally:
    print(E)
    F.publish(a,E)
    time.sleep(5)
    if y:
     machine.reset() 
def connect_and_subscribe():
 global b,C,L
 F=MQTTClient(b,C)
 F.set_callback(sub_cb)
 F.connect()
 F.subscribe(L)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(C,L))
 return F
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global B
 global x
 E="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(B!=""):
  E=E+",\"AnaR\":\""+str(B.read())+"\""
 if(x!=""):
  E=E+",\"DigR\":\""+str(x.value())+"\""
 if error!="":
  E=E+",\"err\":\""+error+"\""
 return E+"}"
try:
 F=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  F.check_msg()
  if(time.time()-T)>H:
   F.publish(j,create_sensor_message())
   T=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

