from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
y="1.0"
u=5
F="GenericSensor/SensorData"
N="OTA/OTARequest"
X="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 J=ADC(ANALOG_SENSOR_PIN)
else:
 J=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 j=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 j=""
E=mqtt_broker_address
M=ubinascii.hexlify(DEVICE_NAME)
x=b'OTA/OTARequest'
t=b'GenericSensor/SensorData'
D=0
I=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  s="\"deviceType\":\""+DEVICE_TYPE+"\""
  b="\"deviceName\":\""+DEVICE_NAME+"\""
  A="\"deviceName\":\"*\"" 
  O=msg.decode()
  print('ESP received OTA message ',O)
  if s in O and(b in O or A in O):
   L=json.loads(O)
   from ota import OTAUpdater
   d="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   q=L.get("otafiles")
   U=True
   O=DEVICE_NAME+" OTA: "+q
   try:
    B=OTAUpdater(d,q)
    if B.check_for_updates():
     if B.download_and_install_update():
      O+=" updated"
     else:
      O+=" update failed"
    else:
     O+=" up-to-date" 
     U=False
   except Exception as h:
    O+=" err:"+str(h)+" type:"+str(type(h))
   finally:
    print(O)
    C.publish(X,O)
    time.sleep(5)
    if U:
     machine.reset() 
def connect_and_subscribe():
 global M,E,x
 C=MQTTClient(M,E)
 C.set_callback(sub_cb)
 C.connect()
 C.subscribe(x)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(E,x))
 return C
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global J
 global j
 O="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(J!=""):
  O=O+",\"AnaR\":\""+str(J.read())+"\""
 if(j!=""):
  O=O+",\"DigR\":\""+str(j.value())+"\""
 if error!="":
  O=O+",\"err\":\""+error+"\""
 return O+"}"
try:
 C=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  C.check_msg()
  if(time.time()-D)>I:
   C.publish(t,create_sensor_message())
   D=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

