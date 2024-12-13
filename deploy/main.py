from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
F="1.0"
j=5
b="GenericSensor/SensorData"
G="OTA/OTARequest"
S="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 y=ADC(ANALOG_SENSOR_PIN)
else:
 y=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 a=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 a=""
z=mqtt_broker_address
w=ubinascii.hexlify(DEVICE_NAME)
P=b'OTA/OTARequest'
d=b'GenericSensor/SensorData'
n=0
Q=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  U="\"deviceType\":\""+DEVICE_TYPE+"\""
  v="\"deviceName\":\""+DEVICE_NAME+"\""
  t="\"deviceName\":\"*\"" 
  M=msg.decode()
  print('ESP received OTA message ',M)
  if U in M and(v in M or t in M):
   q=json.loads(M)
   from ota import OTAUpdater
   O="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   R=q.get("otafiles")
   D=True
   M=DEVICE_NAME+" OTA: "+R
   try:
    J=OTAUpdater(O,R)
    if J.check_for_updates():
     if J.download_and_install_update():
      M+=" updated"
     else:
      M+=" update failed"
    else:
     M+=" up-to-date" 
     D=False
   except Exception as K:
    M+=" err:"+str(K)+" type:"+str(type(K))
   finally:
    print(M)
    s.publish(S,M)
    time.sleep(5)
    if D:
     machine.reset() 
def connect_and_subscribe():
 global w,z,P
 s=MQTTClient(w,z)
 s.set_callback(sub_cb)
 s.connect()
 s.subscribe(P)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(z,P))
 return s
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global y
 global a
 M="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(y!=""):
  M=M+",\"AnaR\":\""+str(y.read())+"\""
 if(a!=""):
  M=M+",\"DigR\":\""+str(a.value())+"\""
 if error!="":
  M=M+",\"err\":\""+error+"\""
 return M+"}"
try:
 s=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  s.check_msg()
  if(time.time()-n)>Q:
   s.publish(d,create_sensor_message())
   n=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

