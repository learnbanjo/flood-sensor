from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
i="1.0"
y=5
P="GenericSensor/SensorData"
n="OTA/OTARequest"
J="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Y=ADC(ANALOG_SENSOR_PIN)
else:
 Y=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 a=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 a=""
N=mqtt_broker_address
B=ubinascii.hexlify(DEVICE_NAME)
q=b'OTA/OTARequest'
A=b'GenericSensor/SensorData'
d=0
V=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  o="\"deviceType\":\""+DEVICE_TYPE+"\""
  D="\"deviceName\":\""+DEVICE_NAME+"\""
  v="\"deviceName\":\"*\"" 
  M=msg.decode()
  print('ESP received OTA message ',M)
  if o in M and(D in M or v in M):
   c=json.loads(M)
   from ota import OTAUpdater
   X="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   t=c.get("otafiles")
   K=True
   M=DEVICE_NAME+" OTA: "+t
   try:
    Q=OTAUpdater(X,t)
    if Q.check_for_updates():
     if Q.download_and_install_update():
      M+=" updated"
     else:
      M+=" update failed"
    else:
     M+=" up-to-date" 
     K=False
   except Exception as T:
    M+=" err:"+str(T)+" type:"+str(type(T))
   finally:
    print(M)
    k.publish(J,M)
    time.sleep(5)
    if K:
     machine.reset() 
def connect_and_subscribe():
 global B,N,q
 k=MQTTClient(B,N)
 k.set_callback(sub_cb)
 k.connect()
 k.subscribe(q)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(N,q))
 return k
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Y
 global a
 M="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Y!=""):
  M=M+",\"AnaR\":\""+str(Y.read())+"\""
 if(a!=""):
  M=M+",\"DigR\":\""+str(a.value())+"\""
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
  if(time.time()-d)>V:
   k.publish(A,create_sensor_message())
   d=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

