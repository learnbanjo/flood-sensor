from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
x="1.0"
f=5
p="GenericSensor/SensorData"
l="OTA/OTARequest"
w="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 O=ADC(ANALOG_SENSOR_PIN)
else:
 O=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 z=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 z=""
n=mqtt_broker_address
m=ubinascii.hexlify(DEVICE_NAME)
D=b'OTA/OTARequest'
I=b'GenericSensor/SensorData'
S=0
F=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  A="\"deviceType\":\""+DEVICE_TYPE+"\""
  g="\"deviceName\":\""+DEVICE_NAME+"\""
  q="\"deviceName\":\"*\"" 
  L=msg.decode()
  print('ESP received OTA message ',L)
  if A in L and(g in L or q in L):
   j=json.loads(L)
   from ota import OTAUpdater
   N="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   T=j.get("otafiles")
   Q=True
   L=DEVICE_NAME+" OTA: "+T
   try:
    W=OTAUpdater(N,T)
    if W.check_for_updates():
     if W.download_and_install_update():
      L+=" updated"
     else:
      L+=" update failed"
    else:
     L+=" up-to-date" 
     Q=False
   except Exception as X:
    L+=" err:"+str(X)+" type:"+str(type(X))
   finally:
    print(L)
    E.publish(w,L)
    time.sleep(5)
    if Q:
     machine.reset() 
def connect_and_subscribe():
 global m,n,D
 E=MQTTClient(m,n)
 E.set_callback(sub_cb)
 E.connect()
 E.subscribe(D)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(n,D))
 return E
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global O
 global z
 L="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(O!=""):
  L=L+",\"AnaR\":\""+str(O.read())+"\""
 if(z!=""):
  L=L+",\"DigR\":\""+str(z.value())+"\""
 if error!="":
  L=L+",\"err\":\""+error+"\""
 return L+"}"
try:
 E=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  E.check_msg()
  if(time.time()-S)>F:
   E.publish(I,create_sensor_message())
   S=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

