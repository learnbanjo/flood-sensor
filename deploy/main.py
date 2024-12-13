from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
V="1.0"
D=5
C="GenericSensor/SensorData"
a="OTA/OTARequest"
W="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 A=ADC(ANALOG_SENSOR_PIN)
else:
 A=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 X=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 X=""
M=mqtt_broker_address
J=ubinascii.hexlify(DEVICE_NAME)
U=b'OTA/OTARequest'
S=b'GenericSensor/SensorData'
O=0
i=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  Y="\"deviceType\":\""+DEVICE_TYPE+"\""
  k="\"deviceName\":\""+DEVICE_NAME+"\""
  h="\"deviceName\":\"*\"" 
  G=msg.decode()
  print('ESP received OTA message ',G)
  if Y in G and(k in G or h in G):
   b=json.loads(G)
   from ota import OTAUpdater
   z="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   l=b.get("otafiles")
   v=True
   G=DEVICE_NAME+" OTA: "+l
   try:
    d=OTAUpdater(z,l)
    if d.check_for_updates():
     if d.download_and_install_update():
      G+=" updated"
     else:
      G+=" update failed"
    else:
     G+=" up-to-date" 
     v=False
   except Exception as E:
    G+=" err:"+str(E)+" type:"+str(type(E))
   finally:
    print(G)
    j.publish(W,G)
    time.sleep(5)
    if v:
     machine.reset() 
def connect_and_subscribe():
 global J,M,U
 j=MQTTClient(J,M)
 j.set_callback(sub_cb)
 j.connect()
 j.subscribe(U)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(M,U))
 return j
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global A
 global X
 G="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(A!=""):
  G=G+",\"AnaR\":\""+str(A.read())+"\""
 if(X!=""):
  G=G+",\"DigR\":\""+str(X.value())+"\""
 if error!="":
  G=G+",\"err\":\""+error+"\""
 return G+"}"
try:
 j=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  j.check_msg()
  if(time.time()-O)>i:
   j.publish(S,create_sensor_message())
   O=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

