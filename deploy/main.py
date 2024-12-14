from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
s="1.0"
X=5
r="GenericSensor/SensorData"
K="OTA/OTARequest"
l="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 H=ADC(ANALOG_SENSOR_PIN)
else:
 H=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 g=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 g=""
q=mqtt_broker_address
f=ubinascii.hexlify(DEVICE_NAME)
D=b'OTA/OTARequest'
G=b'GenericSensor/SensorData'
I=0
P=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  h="\"deviceType\":\""+DEVICE_TYPE+"\""
  v="\"deviceName\":\""+DEVICE_NAME+"\""
  e="\"deviceName\":\"*\"" 
  Q=msg.decode()
  print('ESP received OTA message ',Q)
  if h in Q and(v in Q or e in Q):
   o=json.loads(Q)
   from ota import OTAUpdater
   V="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   w=o.get("otafiles")
   M=True
   Q=DEVICE_NAME+" OTA: "+w
   try:
    y=OTAUpdater(V,w)
    if y.check_for_updates():
     if y.download_and_install_update():
      Q+=" updated"
     else:
      Q+=" update failed"
    else:
     Q+=" up-to-date" 
     M=False
   except Exception as T:
    Q+=" err:"+str(T)+" type:"+str(type(T))
   finally:
    print(Q)
    U.publish(l,Q)
    time.sleep(5)
    if M:
     machine.reset() 
def connect_and_subscribe():
 global f,q,D
 U=MQTTClient(f,q)
 U.set_callback(sub_cb)
 U.connect()
 U.subscribe(D)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(q,D))
 return U
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global H
 global g
 Q="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(H!=""):
  Q=Q+",\"AnaR\":\""+str(H.read())+"\""
 if(g!=""):
  Q=Q+",\"DigR\":\""+str(g.value())+"\""
 if error!="":
  Q=Q+",\"err\":\""+error+"\""
 return Q+"}"
try:
 U=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  U.check_msg()
  if(time.time()-I)>P:
   U.publish(G,create_sensor_message())
   I=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

