from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
m="1.0"
D=5
X="GenericSensor/SensorData"
g="OTA/OTARequest"
Q="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 y=ADC(ANALOG_SENSOR_PIN)
else:
 y=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 d=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 d=""
b=mqtt_broker_address
J=ubinascii.hexlify(DEVICE_NAME)
f=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
e=0
s=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  z="\"deviceType\":\""+DEVICE_TYPE+"\""
  O="\"deviceName\":\""+DEVICE_NAME+"\""
  p="\"deviceName\":\"*\"" 
  N=msg.decode()
  print('ESP received OTA message ',N)
  if z in N and(O in N or p in N):
   T=json.loads(N)
   from ota import OTAUpdater
   H="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   S=T.get("otafiles")
   u=True
   N=DEVICE_NAME+" OTA: "+S
   try:
    Y=OTAUpdater(H,S)
    if Y.check_for_updates():
     if Y.download_and_install_update():
      N+=" updated"
     else:
      N+=" update failed"
    else:
     N+=" up-to-date" 
     u=False
   except Exception as W:
    N+=" err:"+str(W)+" type:"+str(type(W))
   finally:
    print(N)
    P.publish(Q,N)
    time.sleep(5)
    if u:
     machine.reset() 
def connect_and_subscribe():
 global J,b,f
 P=MQTTClient(J,b)
 P.set_callback(sub_cb)
 P.connect()
 P.subscribe(f)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(b,f))
 return P
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global y
 global d
 N="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(y!=""):
  N=N+",\"AnaR\":\""+str(y.read())+"\""
 if(d!=""):
  N=N+",\"DigR\":\""+str(d.value())+"\""
 if error!="":
  N=N+",\"err\":\""+error+"\""
 return N+"}"
try:
 P=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  P.check_msg()
  if(time.time()-e)>s:
   P.publish(E,create_sensor_message())
   e=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

