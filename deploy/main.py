from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
T="1.0"
G=5
D="GenericSensor/SensorData"
k="OTA/OTARequest"
R="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 Q=ADC(ANALOG_SENSOR_PIN)
else:
 Q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 M=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 M=""
F=mqtt_broker_address
A=ubinascii.hexlify(DEVICE_NAME)
b=b'OTA/OTARequest'
d=b'GenericSensor/SensorData'
H=0
N=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  P="\"deviceType\":\""+DEVICE_TYPE+"\""
  h="\"deviceName\":\""+DEVICE_NAME+"\""
  y="\"deviceName\":\"*\"" 
  l=msg.decode()
  print('ESP received OTA message ',l)
  if P in l and(h in l or y in l):
   i=json.loads(l)
   from ota import OTAUpdater
   Y="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   B=i.get("otafiles")
   j=True
   l=DEVICE_NAME+" OTA: "+B
   try:
    K=OTAUpdater(Y,B)
    if K.check_for_updates():
     if K.download_and_install_update():
      l+=" updated"
     else:
      l+=" update failed"
    else:
     l+=" up-to-date" 
     j=False
   except Exception as C:
    l+=" err:"+str(C)+" type:"+str(type(C))
   finally:
    print(l)
    J.publish(R,l)
    time.sleep(5)
    if j:
     machine.reset() 
def connect_and_subscribe():
 global A,F,b
 J=MQTTClient(A,F)
 J.set_callback(sub_cb)
 J.connect()
 J.subscribe(b)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(F,b))
 return J
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global Q
 global M
 l="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(Q!=""):
  l=l+",\"AnaR\":\""+str(Q.read())+"\""
 if(M!=""):
  l=l+",\"DigR\":\""+str(M.value())+"\""
 if error!="":
  l=l+",\"err\":\""+error+"\""
 return l+"}"
try:
 J=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  J.check_msg()
  if(time.time()-H)>N:
   J.publish(d,create_sensor_message())
   H=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

