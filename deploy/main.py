from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
h="1.0"
m=5
l="GenericSensor/SensorData"
v="OTA/OTARequest"
y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 f=ADC(ANALOG_SENSOR_PIN)
else:
 f=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 K=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 K=""
x=mqtt_broker_address
R=ubinascii.hexlify(DEVICE_NAME)
s=b'OTA/OTARequest'
H=b'GenericSensor/SensorData'
N=0
i=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  r="\"deviceType\":\""+DEVICE_TYPE+"\""
  A="\"deviceName\":\""+DEVICE_NAME+"\""
  Y="\"deviceName\":\"*\"" 
  n=msg.decode()
  print('ESP received OTA message ',n)
  if r in n and(A in n or Y in n):
   Q=json.loads(n)
   from ota import OTAUpdater
   P="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   t=Q.get("otafiles")
   U=True
   n=DEVICE_NAME+" OTA: "+t
   try:
    O=OTAUpdater(P,t)
    if O.check_for_updates():
     if O.download_and_install_update():
      n+=" updated"
     else:
      n+=" update failed"
    else:
     n+=" up-to-date" 
     U=False
   except Exception as o:
    n+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(n)
    k.publish(y,n)
    time.sleep(5)
    if U:
     machine.reset() 
def connect_and_subscribe():
 global R,x,s
 k=MQTTClient(R,x)
 k.set_callback(sub_cb)
 k.connect()
 k.subscribe(s)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(x,s))
 return k
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global f
 global K
 n="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(f!=""):
  n=n+",\"AnaR\":\""+str(f.read())+"\""
 if(K!=""):
  n=n+",\"DigR\":\""+str(K.value())+"\""
 if error!="":
  n=n+",\"err\":\""+error+"\""
 return n+"}"
try:
 k=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  k.check_msg()
  if(time.time()-N)>i:
   k.publish(H,create_sensor_message())
   N=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

