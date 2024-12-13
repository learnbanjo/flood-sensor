from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
Q="1.0"
I=5
c="GenericSensor/SensorData"
s="OTA/OTARequest"
Y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 y=ADC(ANALOG_SENSOR_PIN)
else:
 y=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 D=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 D=""
p=mqtt_broker_address
B=ubinascii.hexlify(DEVICE_NAME)
J=b'OTA/OTARequest'
k=b'GenericSensor/SensorData'
w=0
o=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  n="\"deviceType\":\""+DEVICE_TYPE+"\""
  i="\"deviceName\":\""+DEVICE_NAME+"\""
  v="\"deviceName\":\"*\"" 
  e=msg.decode()
  print('ESP received OTA message ',e)
  if n in e and(i in e or v in e):
   z=json.loads(e)
   from ota import OTAUpdater
   U="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   d=z.get("otafiles")
   g=True
   e=DEVICE_NAME+" OTA: "+d
   try:
    A=OTAUpdater(U,d)
    if A.check_for_updates():
     if A.download_and_install_update():
      e+=" updated"
     else:
      e+=" update failed"
    else:
     e+=" up-to-date" 
     g=False
   except Exception as O:
    e+=" err:"+str(O)+" type:"+str(type(O))
   finally:
    print(e)
    T.publish(Y,e)
    time.sleep(5)
    if g:
     machine.reset() 
def connect_and_subscribe():
 global B,p,J
 T=MQTTClient(B,p)
 T.set_callback(sub_cb)
 T.connect()
 T.subscribe(J)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(p,J))
 return T
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global y
 global D
 e="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(y!=""):
  e=e+",\"AnaR\":\""+str(y.read())+"\""
 if(D!=""):
  e=e+",\"DigR\":\""+str(D.value())+"\""
 if error!="":
  e=e+",\"err\":\""+error+"\""
 return e+"}"
try:
 T=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  T.check_msg()
  if(time.time()-w)>o:
   T.publish(k,create_sensor_message())
   w=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

