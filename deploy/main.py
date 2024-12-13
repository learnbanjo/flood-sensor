from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
e="1.0"
t=5
F="GenericSensor/SensorData"
g="OTA/OTARequest"
E="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 a=ADC(ANALOG_SENSOR_PIN)
else:
 a=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 V=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 V=""
L=mqtt_broker_address
k=ubinascii.hexlify(DEVICE_NAME)
h=b'OTA/OTARequest'
i=b'GenericSensor/SensorData'
G=0
X=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  P="\"deviceType\":\""+DEVICE_TYPE+"\""
  R="\"deviceName\":\""+DEVICE_NAME+"\""
  c="\"deviceName\":\"*\"" 
  N=msg.decode()
  print('ESP received OTA message ',N)
  if P in N and(R in N or c in N):
   H=json.loads(N)
   from ota import OTAUpdater
   z="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   D=H.get("otafiles")
   S=True
   N=DEVICE_NAME+" OTA: "+D
   try:
    u=OTAUpdater(z,D)
    if u.check_for_updates():
     if u.download_and_install_update():
      N+=" updated"
     else:
      N+=" update failed"
    else:
     N+=" up-to-date" 
     S=False
   except Exception as o:
    N+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(N)
    j.publish(E,N)
    time.sleep(5)
    if S:
     machine.reset() 
def connect_and_subscribe():
 global k,L,h
 j=MQTTClient(k,L)
 j.set_callback(sub_cb)
 j.connect()
 j.subscribe(h)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(L,h))
 return j
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global a
 global V
 N="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(a!=""):
  N=N+",\"AnaR\":\""+str(a.read())+"\""
 if(V!=""):
  N=N+",\"DigR\":\""+str(V.value())+"\""
 if error!="":
  N=N+",\"err\":\""+error+"\""
 return N+"}"
try:
 j=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  j.check_msg()
  if(time.time()-G)>X:
   j.publish(i,create_sensor_message())
   G=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

