from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
h="1.0"
g=5
C="GenericSensor/SensorData"
B="OTA/OTARequest"
P="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 r=ADC(ANALOG_SENSOR_PIN)
else:
 r=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 S=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 S=""
m=mqtt_broker_address
V=ubinascii.hexlify(DEVICE_NAME)
q=b'OTA/OTARequest'
u=b'GenericSensor/SensorData'
Y=0
R=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  T="\"deviceType\":\""+DEVICE_TYPE+"\""
  J="\"deviceName\":\""+DEVICE_NAME+"\""
  f="\"deviceName\":\"*\"" 
  M=msg.decode()
  print('ESP received OTA message ',M)
  if T in M and(J in M or f in M):
   E=json.loads(M)
   from ota import OTAUpdater
   l="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   a=E.get("otafiles")
   v=True
   M=DEVICE_NAME+" OTA: "+a
   try:
    i=OTAUpdater(l,a)
    if i.check_for_updates():
     if i.download_and_install_update():
      M+=" updated"
     else:
      M+=" update failed"
    else:
     M+=" up-to-date" 
     v=False
   except Exception as z:
    M+=" err:"+str(z)+" type:"+str(type(z))
   finally:
    print(M)
    k.publish(P,M)
    time.sleep(5)
    if v:
     machine.reset() 
def connect_and_subscribe():
 global V,m,q
 k=MQTTClient(V,m)
 k.set_callback(sub_cb)
 k.connect()
 k.subscribe(q)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(m,q))
 return k
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global r
 global S
 M="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(r!=""):
  M=M+",\"AnaR\":\""+str(r.read())+"\""
 if(S!=""):
  M=M+",\"DigR\":\""+str(S.value())+"\""
 if error!="":
  M=M+",\"err\":\""+error+"\""
 return M+"}"
try:
 k=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  k.check_msg()
  if(time.time()-Y)>R:
   k.publish(u,create_sensor_message())
   Y=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

