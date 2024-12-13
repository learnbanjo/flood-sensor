from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
t="1.0"
e=5
d="GenericSensor/SensorData"
f="OTA/OTARequest"
B="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 v=ADC(ANALOG_SENSOR_PIN)
else:
 v=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 Y=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 Y=""
U=mqtt_broker_address
c=ubinascii.hexlify(DEVICE_NAME)
x=b'OTA/OTARequest'
b=b'GenericSensor/SensorData'
X=0
C=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  M="\"deviceType\":\""+DEVICE_TYPE+"\""
  I="\"deviceName\":\""+DEVICE_NAME+"\""
  G="\"deviceName\":\"*\"" 
  q=msg.decode()
  print('ESP received OTA message ',q)
  if M in q and(I in q or G in q):
   O=json.loads(q)
   from ota import OTAUpdater
   K="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   D=O.get("otafiles")
   S=True
   q=DEVICE_NAME+" OTA: "+D
   try:
    k=OTAUpdater(K,D)
    if k.check_for_updates():
     if k.download_and_install_update():
      q+=" updated"
     else:
      q+=" update failed"
    else:
     q+=" up-to-date" 
     S=False
   except Exception as N:
    q+=" err:"+str(N)+" type:"+str(type(N))
   finally:
    print(q)
    h.publish(B,q)
    time.sleep(5)
    if S:
     machine.reset() 
def connect_and_subscribe():
 global c,U,x
 h=MQTTClient(c,U)
 h.set_callback(sub_cb)
 h.connect()
 h.subscribe(x)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(U,x))
 return h
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global v
 global Y
 q="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(v!=""):
  q=q+",\"AnaR\":\""+str(v.read())+"\""
 if(Y!=""):
  q=q+",\"DigR\":\""+str(Y.value())+"\""
 if error!="":
  q=q+",\"err\":\""+error+"\""
 return q+"}"
try:
 h=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  h.check_msg()
  if(time.time()-X)>C:
   h.publish(b,create_sensor_message())
   X=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

