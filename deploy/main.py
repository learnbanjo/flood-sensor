from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
K="1.0"
h=5
T="GenericSensor/SensorData"
Y="OTA/OTARequest"
i="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 J=ADC(ANALOG_SENSOR_PIN)
else:
 J=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 Q=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 Q=""
f=mqtt_broker_address
l=ubinascii.hexlify(DEVICE_NAME)
H=b'OTA/OTARequest'
e=b'GenericSensor/SensorData'
a=0
m=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  o="\"deviceType\":\""+DEVICE_TYPE+"\""
  S="\"deviceName\":\""+DEVICE_NAME+"\""
  x="\"deviceName\":\"*\"" 
  O=msg.decode()
  print('ESP received OTA message ',O)
  if o in O and(S in O or x in O):
   A=json.loads(O)
   from ota import OTAUpdater
   I="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   E=A.get("otafiles")
   U=True
   O=DEVICE_NAME+" OTA: "+E
   try:
    p=OTAUpdater(I,E)
    if p.check_for_updates():
     if p.download_and_install_update():
      O+=" updated"
     else:
      O+=" update failed"
    else:
     O+=" up-to-date" 
     U=False
   except Exception as d:
    O+=" err:"+str(d)+" type:"+str(type(d))
   finally:
    print(O)
    M.publish(i,O)
    time.sleep(5)
    if U:
     machine.reset() 
def connect_and_subscribe():
 global l,f,H
 M=MQTTClient(l,f)
 M.set_callback(sub_cb)
 M.connect()
 M.subscribe(H)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(f,H))
 return M
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global J
 global Q
 O="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(J!=""):
  O=O+",\"AnaR\":\""+str(J.read())+"\""
 if(Q!=""):
  O=O+",\"DigR\":\""+str(Q.value())+"\""
 if error!="":
  O=O+",\"err\":\""+error+"\""
 return O+"}"
try:
 M=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  M.check_msg()
  if(time.time()-a)>m:
   M.publish(e,create_sensor_message())
   a=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

