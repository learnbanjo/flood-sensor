from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
e="1.0"
o=5
D="GenericSensor/SensorData"
h="OTA/OTARequest"
H="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 g=ADC(ANALOG_SENSOR_PIN)
else:
 g=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 f=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 f=""
F=mqtt_broker_address
S=ubinascii.hexlify(DEVICE_NAME)
M=b'OTA/OTARequest'
a=b'GenericSensor/SensorData'
m=0
d=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  P="\"deviceType\":\""+DEVICE_TYPE+"\""
  A="\"deviceName\":\""+DEVICE_NAME+"\""
  T="\"deviceName\":\"*\"" 
  k=msg.decode()
  print('ESP received OTA message ',k)
  if P in k and(A in k or T in k):
   q=json.loads(k)
   from ota import OTAUpdater
   G="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   O=q.get("otafiles")
   w=True
   k=DEVICE_NAME+" OTA: "+O
   try:
    p=OTAUpdater(G,O)
    if p.check_for_updates():
     if p.download_and_install_update():
      k+=" updated"
     else:
      k+=" update failed"
    else:
     k+=" up-to-date" 
     w=False
   except Exception as v:
    k+=" err:"+str(v)+" type:"+str(type(v))
   finally:
    print(k)
    L.publish(H,k)
    time.sleep(5)
    if w:
     machine.reset() 
def connect_and_subscribe():
 global S,F,M
 L=MQTTClient(S,F)
 L.set_callback(sub_cb)
 L.connect()
 L.subscribe(M)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(F,M))
 return L
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global g
 global f
 k="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(g!=""):
  k=k+",\"AnaR\":\""+str(g.read())+"\""
 if(f!=""):
  k=k+",\"DigR\":\""+str(f.value())+"\""
 if error!="":
  k=k+",\"err\":\""+error+"\""
 return k+"}"
try:
 L=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  L.check_msg()
  if(time.time()-m)>d:
   L.publish(a,create_sensor_message())
   m=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

