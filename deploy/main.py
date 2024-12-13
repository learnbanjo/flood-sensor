from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
L="1.0"
F=5
k="GenericSensor/SensorData"
T="OTA/OTARequest"
e="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 N=ADC(ANALOG_SENSOR_PIN)
else:
 N=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 z=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 z=""
c=mqtt_broker_address
n=ubinascii.hexlify(DEVICE_NAME)
V=b'OTA/OTARequest'
H=b'GenericSensor/SensorData'
g=0
b=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  U="\"deviceType\":\""+DEVICE_TYPE+"\""
  E="\"deviceName\":\""+DEVICE_NAME+"\""
  l="\"deviceName\":\"*\"" 
  R=msg.decode()
  print('ESP received OTA message ',R)
  if U in R and(E in R or l in R):
   o=json.loads(R)
   from ota import OTAUpdater
   w="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   I=o.get("otafiles")
   d=True
   R=DEVICE_NAME+" OTA: "+I
   try:
    P=OTAUpdater(w,I)
    if P.check_for_updates():
     if P.download_and_install_update():
      R+=" updated"
     else:
      R+=" update failed"
    else:
     R+=" up-to-date" 
     d=False
   except Exception as y:
    R+=" err:"+str(y)+" type:"+str(type(y))
   finally:
    print(R)
    h.publish(e,R)
    time.sleep(5)
    if d:
     machine.reset() 
def connect_and_subscribe():
 global n,c,V
 h=MQTTClient(n,c)
 h.set_callback(sub_cb)
 h.connect()
 h.subscribe(V)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(c,V))
 return h
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global N
 global z
 R="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(N!=""):
  R=R+",\"AnaR\":\""+str(N.read())+"\""
 if(z!=""):
  R=R+",\"DigR\":\""+str(z.value())+"\""
 if error!="":
  R=R+",\"err\":\""+error+"\""
 return R+"}"
try:
 h=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  h.check_msg()
  if(time.time()-g)>b:
   h.publish(H,create_sensor_message())
   g=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

