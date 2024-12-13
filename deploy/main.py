from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
w="1.0"
M=5
f="GenericSensor/SensorData"
s="OTA/OTARequest"
g="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 o=ADC(ANALOG_SENSOR_PIN)
else:
 o=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 W=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 W=""
I=mqtt_broker_address
H=ubinascii.hexlify(DEVICE_NAME)
q=b'OTA/OTARequest'
O=b'GenericSensor/SensorData'
Y=0
X=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  p="\"deviceType\":\""+DEVICE_TYPE+"\""
  d="\"deviceName\":\""+DEVICE_NAME+"\""
  m="\"deviceName\":\"*\"" 
  C=msg.decode()
  print('ESP received OTA message ',C)
  if p in C and(d in C or m in C):
   S=json.loads(C)
   from ota import OTAUpdater
   R="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   u=S.get("otafiles")
   G=True
   C=DEVICE_NAME+" OTA: "+u
   try:
    j=OTAUpdater(R,u)
    if j.check_for_updates():
     if j.download_and_install_update():
      C+=" updated"
     else:
      C+=" update failed"
    else:
     C+=" up-to-date" 
     G=False
   except Exception as L:
    C+=" err:"+str(L)+" type:"+str(type(L))
   finally:
    print(C)
    Q.publish(g,C)
    time.sleep(5)
    if G:
     machine.reset() 
def connect_and_subscribe():
 global H,I,q
 Q=MQTTClient(H,I)
 Q.set_callback(sub_cb)
 Q.connect()
 Q.subscribe(q)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(I,q))
 return Q
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global o
 global W
 C="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(o!=""):
  C=C+",\"AnaR\":\""+str(o.read())+"\""
 if(W!=""):
  C=C+",\"DigR\":\""+str(W.value())+"\""
 if error!="":
  C=C+",\"err\":\""+error+"\""
 return C+"}"
try:
 Q=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  Q.check_msg()
  if(time.time()-Y)>X:
   Q.publish(O,create_sensor_message())
   Y=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

