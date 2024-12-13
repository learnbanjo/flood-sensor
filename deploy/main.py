from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
I="1.0"
N=5
z="GenericSensor/SensorData"
v="OTA/OTARequest"
x="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 D=ADC(ANALOG_SENSOR_PIN)
else:
 D=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 g=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 g=""
M=mqtt_broker_address
Y=ubinascii.hexlify(DEVICE_NAME)
e=b'OTA/OTARequest'
B=b'GenericSensor/SensorData'
i=0
U=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  K="\"deviceType\":\""+DEVICE_TYPE+"\""
  o="\"deviceName\":\""+DEVICE_NAME+"\""
  j="\"deviceName\":\"*\"" 
  q=msg.decode()
  print('ESP received OTA message ',q)
  if K in q and(o in q or j in q):
   y=json.loads(q)
   from ota import OTAUpdater
   P="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   Q=y.get("otafiles")
   f=True
   q=DEVICE_NAME+" OTA: "+Q
   try:
    E=OTAUpdater(P,Q)
    if E.check_for_updates():
     if E.download_and_install_update():
      q+=" updated"
     else:
      q+=" update failed"
    else:
     q+=" up-to-date" 
     f=False
   except Exception as G:
    q+=" err:"+str(G)+" type:"+str(type(G))
   finally:
    print(q)
    F.publish(x,q)
    time.sleep(5)
    if f:
     machine.reset() 
def connect_and_subscribe():
 global Y,M,e
 F=MQTTClient(Y,M)
 F.set_callback(sub_cb)
 F.connect()
 F.subscribe(e)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(M,e))
 return F
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global D
 global g
 q="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(D!=""):
  q=q+",\"AnaR\":\""+str(D.read())+"\""
 if(g!=""):
  q=q+",\"DigR\":\""+str(g.value())+"\""
 if error!="":
  q=q+",\"err\":\""+error+"\""
 return q+"}"
try:
 F=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  F.check_msg()
  if(time.time()-i)>U:
   F.publish(B,create_sensor_message())
   i=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

