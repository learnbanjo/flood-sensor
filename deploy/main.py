from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
x="1.0"
R=5
b="GenericSensor/SensorData"
P="OTA/OTARequest"
g="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 S=ADC(ANALOG_SENSOR_PIN)
else:
 S=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 A=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 A=""
G=mqtt_broker_address
p=ubinascii.hexlify(DEVICE_NAME)
W=b'OTA/OTARequest'
d=b'GenericSensor/SensorData'
J=0
D=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  e="\"deviceType\":\""+DEVICE_TYPE+"\""
  F="\"deviceName\":\""+DEVICE_NAME+"\""
  Y="\"deviceName\":\"*\"" 
  N=msg.decode()
  print('ESP received OTA message ',N)
  if e in N and(F in N or Y in N):
   E=json.loads(N)
   from ota import OTAUpdater
   c="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   o=E.get("otafiles")
   O=True
   N=DEVICE_NAME+" OTA: "+o
   try:
    B=OTAUpdater(c,o)
    if B.check_for_updates():
     if B.download_and_install_update():
      N+=" updated"
     else:
      N+=" update failed"
    else:
     N+=" up-to-date" 
     O=False
   except Exception as z:
    N+=" err:"+str(z)+" type:"+str(type(z))
   finally:
    print(N)
    I.publish(g,N)
    time.sleep(5)
    if O:
     machine.reset() 
def connect_and_subscribe():
 global p,G,W
 I=MQTTClient(p,G)
 I.set_callback(sub_cb)
 I.connect()
 I.subscribe(W)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(G,W))
 return I
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global S
 global A
 N="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(S!=""):
  N=N+",\"AnaR\":\""+str(S.read())+"\""
 if(A!=""):
  N=N+",\"DigR\":\""+str(A.value())+"\""
 if error!="":
  N=N+",\"err\":\""+error+"\""
 return N+"}"
try:
 I=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  I.check_msg()
  if(time.time()-J)>D:
   I.publish(d,create_sensor_message())
   J=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

