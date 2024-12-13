from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
y="1.0"
D=5
b="GenericSensor/SensorData"
k="OTA/OTARequest"
L="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Q=ADC(ANALOG_SENSOR_PIN)
else:
 Q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 G=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 G=""
o=mqtt_broker_address
B=ubinascii.hexlify(DEVICE_NAME)
j=b'OTA/OTARequest'
H=b'GenericSensor/SensorData'
f=0
V=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  r="\"deviceType\":\""+DEVICE_TYPE+"\""
  q="\"deviceName\":\""+DEVICE_NAME+"\""
  w="\"deviceName\":\"*\"" 
  p=msg.decode()
  print('ESP received OTA message ',p)
  if r in p and(q in p or w in p):
   a=json.loads(p)
   from ota import OTAUpdater
   u="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   U=a.get("otafiles")
   Y=True
   p=DEVICE_NAME+" OTA: "+U
   try:
    F=OTAUpdater(u,U)
    if F.check_for_updates():
     if F.download_and_install_update():
      p+=" updated"
     else:
      p+=" update failed"
    else:
     p+=" up-to-date" 
     Y=False
   except Exception as C:
    p+=" err:"+str(C)+" type:"+str(type(C))
   finally:
    print(p)
    l.publish(L,p)
    time.sleep(5)
    if Y:
     machine.reset() 
def connect_and_subscribe():
 global B,o,j
 l=MQTTClient(B,o)
 l.set_callback(sub_cb)
 l.connect()
 l.subscribe(j)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(o,j))
 return l
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Q
 global G
 p="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Q!=""):
  p=p+",\"AnaR\":\""+str(Q.read())+"\""
 if(G!=""):
  p=p+",\"DigR\":\""+str(G.value())+"\""
 if error!="":
  p=p+",\"err\":\""+error+"\""
 return p+"}"
try:
 l=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  l.check_msg()
  if(time.time()-f)>V:
   l.publish(H,create_sensor_message())
   f=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

