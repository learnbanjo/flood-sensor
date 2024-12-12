from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
W="1.0"
R=5
K="GenericSensor/SensorData"
a="OTA/OTARequest"
X="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 j=ADC(ANALOG_SENSOR_PIN)
else:
 j=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 g=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 g=""
U=mqtt_broker_address
t=ubinascii.hexlify(DEVICE_NAME)
l=b'OTA/OTARequest'
u=b'GenericSensor/SensorData'
q=0
F=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  A="\"deviceType\":\""+DEVICE_TYPE+"\""
  I="\"deviceName\":\""+DEVICE_NAME+"\""
  o="\"deviceName\":\"*\"" 
  S=msg.decode()
  print('ESP received OTA message ',S)
  if A in S and(I in S or o in S):
   D=json.loads(S)
   from ota import OTAUpdater
   b="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/src/deploy/"
   Y=D.get("otafiles")
   G=True
   S=DEVICE_NAME+" OTA: "+Y
   try:
    T=OTAUpdater(b,Y)
    if T.check_for_updates():
     if T.download_and_install_update():
      S+=" updated"
     else:
      S+=" update failed"
    else:
     S+=" up-to-date" 
     G=False
   except Exception as V:
    S+=" err:"+str(V)+" type:"+str(type(V))
   finally:
    print(S)
    P.publish(X,S)
    time.sleep(5)
    if G:
     machine.reset() 
def connect_and_subscribe():
 global t,U,l
 P=MQTTClient(t,U)
 P.set_callback(sub_cb)
 P.connect()
 P.subscribe(l)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(U,l))
 return P
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global j
 global g
 S="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(j!=""):
  S=S+",\"AnaR\":\""+str(j.read())+"\""
 if(g!=""):
  S=S+",\"DigR\":\""+str(g.value())+"\""
 if error!="":
  S=S+",\"err\":\""+error+"\""
 return S+"}"
try:
 P=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  P.check_msg()
  if(time.time()-q)>F:
   P.publish(u,create_sensor_message())
   q=time.time()
 except OSError as e:
  restart_and_reconnect()

