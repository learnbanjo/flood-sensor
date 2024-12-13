from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
m="1.0"
A=5
u="GenericSensor/SensorData"
N="OTA/OTARequest"
B="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 t=ADC(ANALOG_SENSOR_PIN)
else:
 t=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 W=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 W=""
G=mqtt_broker_address
r=ubinascii.hexlify(DEVICE_NAME)
g=b'OTA/OTARequest'
O=b'GenericSensor/SensorData'
P=0
d=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  H="\"deviceType\":\""+DEVICE_TYPE+"\""
  S="\"deviceName\":\""+DEVICE_NAME+"\""
  R="\"deviceName\":\"*\"" 
  F=msg.decode()
  print('ESP received OTA message ',F)
  if H in F and(S in F or R in F):
   w=json.loads(F)
   from ota import OTAUpdater
   c="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   U=w.get("otafiles")
   X=True
   F=DEVICE_NAME+" OTA: "+U
   try:
    M=OTAUpdater(c,U)
    if M.check_for_updates():
     if M.download_and_install_update():
      F+=" updated"
     else:
      F+=" update failed"
    else:
     F+=" up-to-date" 
     X=False
   except Exception as x:
    F+=" err:"+str(x)+" type:"+str(type(x))
   finally:
    print(F)
    i.publish(B,F)
    time.sleep(5)
    if X:
     machine.reset() 
def connect_and_subscribe():
 global r,G,g
 i=MQTTClient(r,G)
 i.set_callback(sub_cb)
 i.connect()
 i.subscribe(g)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(G,g))
 return i
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global t
 global W
 F="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(t!=""):
  F=F+",\"AnaR\":\""+str(t.read())+"\""
 if(W!=""):
  F=F+",\"DigR\":\""+str(W.value())+"\""
 if error!="":
  F=F+",\"err\":\""+error+"\""
 return F+"}"
try:
 i=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  i.check_msg()
  if(time.time()-P)>d:
   i.publish(O,create_sensor_message())
   P=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

