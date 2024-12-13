from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
A="1.0"
v=5
l="GenericSensor/SensorData"
L="OTA/OTARequest"
S="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 h=ADC(ANALOG_SENSOR_PIN)
else:
 h=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 R=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 R=""
z=mqtt_broker_address
r=ubinascii.hexlify(DEVICE_NAME)
e=b'OTA/OTARequest'
K=b'GenericSensor/SensorData'
N=0
E=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  b="\"deviceType\":\""+DEVICE_TYPE+"\""
  m="\"deviceName\":\""+DEVICE_NAME+"\""
  c="\"deviceName\":\"*\"" 
  Y=msg.decode()
  print('ESP received OTA message ',Y)
  if b in Y and(m in Y or c in Y):
   u=json.loads(Y)
   from ota import OTAUpdater
   X="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   q=u.get("otafiles")
   I=True
   Y=DEVICE_NAME+" OTA: "+q
   try:
    T=OTAUpdater(X,q)
    if T.check_for_updates():
     if T.download_and_install_update():
      Y+=" updated"
     else:
      Y+=" update failed"
    else:
     Y+=" up-to-date" 
     I=False
   except Exception as M:
    Y+=" err:"+str(M)+" type:"+str(type(M))
   finally:
    print(Y)
    d.publish(S,Y)
    time.sleep(5)
    if I:
     machine.reset() 
def connect_and_subscribe():
 global r,z,e
 d=MQTTClient(r,z)
 d.set_callback(sub_cb)
 d.connect()
 d.subscribe(e)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(z,e))
 return d
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global h
 global R
 Y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(h!=""):
  Y=Y+",\"AnaR\":\""+str(h.read())+"\""
 if(R!=""):
  Y=Y+",\"DigR\":\""+str(R.value())+"\""
 if error!="":
  Y=Y+",\"err\":\""+error+"\""
 return Y+"}"
try:
 d=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  d.check_msg()
  if(time.time()-N)>E:
   d.publish(K,create_sensor_message())
   N=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

