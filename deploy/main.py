from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
o="1.0"
q=5
W="GenericSensor/SensorData"
T="OTA/OTARequest"
M="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 A=ADC(ANALOG_SENSOR_PIN)
else:
 A=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 t=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 t=""
b=mqtt_broker_address
D=ubinascii.hexlify(DEVICE_NAME)
y=b'OTA/OTARequest'
k=b'GenericSensor/SensorData'
E=0
f=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  R="\"deviceType\":\""+DEVICE_TYPE+"\""
  m="\"deviceName\":\""+DEVICE_NAME+"\""
  S="\"deviceName\":\"*\"" 
  n=msg.decode()
  print('ESP received OTA message ',n)
  if R in n and(m in n or S in n):
   x=json.loads(n)
   from ota import OTAUpdater
   p="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   w=x.get("otafiles")
   i=True
   n=DEVICE_NAME+" OTA: "+w
   try:
    P=OTAUpdater(p,w)
    if P.check_for_updates():
     if P.download_and_install_update():
      n+=" updated"
     else:
      n+=" update failed"
    else:
     n+=" up-to-date" 
     i=False
   except Exception as O:
    n+=" err:"+str(O)+" type:"+str(type(O))
   finally:
    print(n)
    v.publish(M,n)
    time.sleep(5)
    if i:
     machine.reset() 
def connect_and_subscribe():
 global D,b,y
 v=MQTTClient(D,b)
 v.set_callback(sub_cb)
 v.connect()
 v.subscribe(y)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(b,y))
 return v
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global A
 global t
 n="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(A!=""):
  n=n+",\"AnaR\":\""+str(A.read())+"\""
 if(t!=""):
  n=n+",\"DigR\":\""+str(t.value())+"\""
 if error!="":
  n=n+",\"err\":\""+error+"\""
 return n+"}"
try:
 v=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  v.check_msg()
  if(time.time()-E)>f:
   v.publish(k,create_sensor_message())
   E=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

