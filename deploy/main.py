from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
q="1.0"
y=5
w="GenericSensor/SensorData"
E="OTA/OTARequest"
Y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 s=ADC(ANALOG_SENSOR_PIN)
else:
 s=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 h=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 h=""
K=mqtt_broker_address
p=ubinascii.hexlify(DEVICE_NAME)
b=b'OTA/OTARequest'
f=b'GenericSensor/SensorData'
r=0
B=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  I="\"deviceType\":\""+DEVICE_TYPE+"\""
  x="\"deviceName\":\""+DEVICE_NAME+"\""
  i="\"deviceName\":\"*\"" 
  t=msg.decode()
  print('ESP received OTA message ',t)
  if I in t and(x in t or i in t):
   D=json.loads(t)
   from ota import OTAUpdater
   M="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   n=D.get("otafiles")
   X=True
   t=DEVICE_NAME+" OTA: "+n
   try:
    Q=OTAUpdater(M,n)
    if Q.check_for_updates():
     if Q.download_and_install_update():
      t+=" updated"
     else:
      t+=" update failed"
    else:
     t+=" up-to-date" 
     X=False
   except Exception as u:
    t+=" err:"+str(u)+" type:"+str(type(u))
   finally:
    print(t)
    O.publish(Y,t)
    time.sleep(5)
    if X:
     machine.reset() 
def connect_and_subscribe():
 global p,K,b
 O=MQTTClient(p,K)
 O.set_callback(sub_cb)
 O.connect()
 O.subscribe(b)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(K,b))
 return O
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global s
 global h
 t="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(s!=""):
  t=t+",\"AnaR\":\""+str(s.read())+"\""
 if(h!=""):
  t=t+",\"DigR\":\""+str(h.value())+"\""
 if error!="":
  t=t+",\"err\":\""+error+"\""
 return t+"}"
try:
 O=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  O.check_msg()
  if(time.time()-r)>B:
   O.publish(f,create_sensor_message())
   r=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

