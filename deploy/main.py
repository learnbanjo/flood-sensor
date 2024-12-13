from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
x="1.0"
q=5
u="GenericSensor/SensorData"
m="OTA/OTARequest"
k="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 n=ADC(ANALOG_SENSOR_PIN)
else:
 n=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 G=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 G=""
v=mqtt_broker_address
d=ubinascii.hexlify(DEVICE_NAME)
K=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
X=0
r=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  y="\"deviceType\":\""+DEVICE_TYPE+"\""
  V="\"deviceName\":\""+DEVICE_NAME+"\""
  O="\"deviceName\":\"*\"" 
  i=msg.decode()
  print('ESP received OTA message ',i)
  if y in i and(V in i or O in i):
   C=json.loads(i)
   from ota import OTAUpdater
   J="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   N=C.get("otafiles")
   M=True
   i=DEVICE_NAME+" OTA: "+N
   try:
    A=OTAUpdater(J,N)
    if A.check_for_updates():
     if A.download_and_install_update():
      i+=" updated"
     else:
      i+=" update failed"
    else:
     i+=" up-to-date" 
     M=False
   except Exception as W:
    i+=" err:"+str(W)+" type:"+str(type(W))
   finally:
    print(i)
    P.publish(k,i)
    time.sleep(5)
    if M:
     machine.reset() 
def connect_and_subscribe():
 global d,v,K
 P=MQTTClient(d,v)
 P.set_callback(sub_cb)
 P.connect()
 P.subscribe(K)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(v,K))
 return P
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global n
 global G
 i="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(n!=""):
  i=i+",\"AnaR\":\""+str(n.read())+"\""
 if(G!=""):
  i=i+",\"DigR\":\""+str(G.value())+"\""
 if error!="":
  i=i+",\"err\":\""+error+"\""
 return i+"}"
try:
 P=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  P.check_msg()
  if(time.time()-X)>r:
   P.publish(E,create_sensor_message())
   X=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

