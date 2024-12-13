from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
G="1.0"
k=5
n="GenericSensor/SensorData"
A="OTA/OTARequest"
X="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 F=ADC(ANALOG_SENSOR_PIN)
else:
 F=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 T=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 T=""
E=mqtt_broker_address
P=ubinascii.hexlify(DEVICE_NAME)
R=b'OTA/OTARequest'
g=b'GenericSensor/SensorData'
m=0
c=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  h="\"deviceType\":\""+DEVICE_TYPE+"\""
  C="\"deviceName\":\""+DEVICE_NAME+"\""
  f="\"deviceName\":\"*\"" 
  K=msg.decode()
  print('ESP received OTA message ',K)
  if h in K and(C in K or f in K):
   N=json.loads(K)
   from ota import OTAUpdater
   a="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   j=N.get("otafiles")
   s=True
   K=DEVICE_NAME+" OTA: "+j
   try:
    y=OTAUpdater(a,j)
    if y.check_for_updates():
     if y.download_and_install_update():
      K+=" updated"
     else:
      K+=" update failed"
    else:
     K+=" up-to-date" 
     s=False
   except Exception as B:
    K+=" err:"+str(B)+" type:"+str(type(B))
   finally:
    print(K)
    W.publish(X,K)
    time.sleep(5)
    if s:
     machine.reset() 
def connect_and_subscribe():
 global P,E,R
 W=MQTTClient(P,E)
 W.set_callback(sub_cb)
 W.connect()
 W.subscribe(R)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(E,R))
 return W
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global F
 global T
 K="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(F!=""):
  K=K+",\"AnaR\":\""+str(F.read())+"\""
 if(T!=""):
  K=K+",\"DigR\":\""+str(T.value())+"\""
 if error!="":
  K=K+",\"err\":\""+error+"\""
 return K+"}"
try:
 W=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  W.check_msg()
  if(time.time()-m)>c:
   W.publish(g,create_sensor_message())
   m=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

