from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
c="1.0"
h=5
l="GenericSensor/SensorData"
X="OTA/OTARequest"
d="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 y=ADC(ANALOG_SENSOR_PIN)
else:
 y=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 A=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 A=""
K=mqtt_broker_address
S=ubinascii.hexlify(DEVICE_NAME)
b=b'OTA/OTARequest'
T=b'GenericSensor/SensorData'
C=0
s=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  q="\"deviceType\":\""+DEVICE_TYPE+"\""
  a="\"deviceName\":\""+DEVICE_NAME+"\""
  H="\"deviceName\":\"*\"" 
  p=msg.decode()
  print('ESP received OTA message ',p)
  if q in p and(a in p or H in p):
   Y=json.loads(p)
   from ota import OTAUpdater
   P="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   D=Y.get("otafiles")
   o=True
   p=DEVICE_NAME+" OTA: "+D
   try:
    W=OTAUpdater(P,D)
    if W.check_for_updates():
     if W.download_and_install_update():
      p+=" updated"
     else:
      p+=" update failed"
    else:
     p+=" up-to-date" 
     o=False
   except Exception as w:
    p+=" err:"+str(w)+" type:"+str(type(w))
   finally:
    print(p)
    t.publish(d,p)
    time.sleep(5)
    if o:
     machine.reset() 
def connect_and_subscribe():
 global S,K,b
 t=MQTTClient(S,K)
 t.set_callback(sub_cb)
 t.connect()
 t.subscribe(b)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(K,b))
 return t
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global y
 global A
 p="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(y!=""):
  p=p+",\"AnaR\":\""+str(y.read())+"\""
 if(A!=""):
  p=p+",\"DigR\":\""+str(A.value())+"\""
 if error!="":
  p=p+",\"err\":\""+error+"\""
 return p+"}"
try:
 t=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  t.check_msg()
  if(time.time()-C)>s:
   t.publish(T,create_sensor_message())
   C=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

