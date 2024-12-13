from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
A="1.0"
B=5
G="GenericSensor/SensorData"
h="OTA/OTARequest"
w="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 s=ADC(ANALOG_SENSOR_PIN)
else:
 s=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 H=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 H=""
X=mqtt_broker_address
x=ubinascii.hexlify(DEVICE_NAME)
N=b'OTA/OTARequest'
b=b'GenericSensor/SensorData'
R=0
W=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  L="\"deviceType\":\""+DEVICE_TYPE+"\""
  O="\"deviceName\":\""+DEVICE_NAME+"\""
  k="\"deviceName\":\"*\"" 
  M=msg.decode()
  print('ESP received OTA message ',M)
  if L in M and(O in M or k in M):
   y=json.loads(M)
   from ota import OTAUpdater
   z="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   a=y.get("otafiles")
   v=True
   M=DEVICE_NAME+" OTA: "+a
   try:
    U=OTAUpdater(z,a)
    if U.check_for_updates():
     if U.download_and_install_update():
      M+=" updated"
     else:
      M+=" update failed"
    else:
     M+=" up-to-date" 
     v=False
   except Exception as F:
    M+=" err:"+str(F)+" type:"+str(type(F))
   finally:
    print(M)
    T.publish(w,M)
    time.sleep(5)
    if v:
     machine.reset() 
def connect_and_subscribe():
 global x,X,N
 T=MQTTClient(x,X)
 T.set_callback(sub_cb)
 T.connect()
 T.subscribe(N)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(X,N))
 return T
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global s
 global H
 M="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(s!=""):
  M=M+",\"AnaR\":\""+str(s.read())+"\""
 if(H!=""):
  M=M+",\"DigR\":\""+str(H.value())+"\""
 if error!="":
  M=M+",\"err\":\""+error+"\""
 return M+"}"
try:
 T=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  T.check_msg()
  if(time.time()-R)>W:
   T.publish(b,create_sensor_message())
   R=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

