from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
b="1.0"
N=5
U="GenericSensor/SensorData"
p="OTA/OTARequest"
n="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 s=ADC(ANALOG_SENSOR_PIN)
else:
 s=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 R=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 R=""
O=mqtt_broker_address
i=ubinascii.hexlify(DEVICE_NAME)
M=b'OTA/OTARequest'
k=b'GenericSensor/SensorData'
H=0
Y=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  r="\"deviceType\":\""+DEVICE_TYPE+"\""
  q="\"deviceName\":\""+DEVICE_NAME+"\""
  x="\"deviceName\":\"*\"" 
  m=msg.decode()
  print('ESP received OTA message ',m)
  if r in m and(q in m or x in m):
   I=json.loads(m)
   from ota import OTAUpdater
   F="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   W=I.get("otafiles")
   v=True
   m=DEVICE_NAME+" OTA: "+W
   try:
    h=OTAUpdater(F,W)
    if h.check_for_updates():
     if h.download_and_install_update():
      m+=" updated"
     else:
      m+=" update failed"
    else:
     m+=" up-to-date" 
     v=False
   except Exception as u:
    m+=" err:"+str(u)+" type:"+str(type(u))
   finally:
    print(m)
    P.publish(n,m)
    time.sleep(5)
    if v:
     machine.reset() 
def connect_and_subscribe():
 global i,O,M
 P=MQTTClient(i,O)
 P.set_callback(sub_cb)
 P.connect()
 P.subscribe(M)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(O,M))
 return P
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global s
 global R
 m="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(s!=""):
  m=m+",\"AnaR\":\""+str(s.read())+"\""
 if(R!=""):
  m=m+",\"DigR\":\""+str(R.value())+"\""
 if error!="":
  m=m+",\"err\":\""+error+"\""
 return m+"}"
try:
 P=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  P.check_msg()
  if(time.time()-H)>Y:
   P.publish(k,create_sensor_message())
   H=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

