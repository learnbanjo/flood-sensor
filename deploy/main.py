from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
a="1.0"
T=5
S="GenericSensor/SensorData"
e="OTA/OTARequest"
r="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 W=ADC(ANALOG_SENSOR_PIN)
else:
 W=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 G=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 G=""
d=mqtt_broker_address
H=ubinascii.hexlify(DEVICE_NAME)
B=b'OTA/OTARequest'
c=b'GenericSensor/SensorData'
h=0
g=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  L="\"deviceType\":\""+DEVICE_TYPE+"\""
  v="\"deviceName\":\""+DEVICE_NAME+"\""
  j="\"deviceName\":\"*\"" 
  O=msg.decode()
  print('ESP received OTA message ',O)
  if L in O and(v in O or j in O):
   k=json.loads(O)
   from ota import OTAUpdater
   D="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   i=k.get("otafiles")
   F=True
   O=DEVICE_NAME+" OTA: "+i
   try:
    M=OTAUpdater(D,i)
    if M.check_for_updates():
     if M.download_and_install_update():
      O+=" updated"
     else:
      O+=" update failed"
    else:
     O+=" up-to-date" 
     F=False
   except Exception as U:
    O+=" err:"+str(U)+" type:"+str(type(U))
   finally:
    print(O)
    V.publish(r,O)
    time.sleep(5)
    if F:
     machine.reset() 
def connect_and_subscribe():
 global H,d,B
 V=MQTTClient(H,d)
 V.set_callback(sub_cb)
 V.connect()
 V.subscribe(B)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(d,B))
 return V
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global W
 global G
 O="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(W!=""):
  O=O+",\"AnaR\":\""+str(W.read())+"\""
 if(G!=""):
  O=O+",\"DigR\":\""+str(G.value())+"\""
 if error!="":
  O=O+",\"err\":\""+error+"\""
 return O+"}"
try:
 V=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  V.check_msg()
  if(time.time()-h)>g:
   V.publish(c,create_sensor_message())
   h=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

