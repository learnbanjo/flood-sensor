from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
R="1.0"
z=5
g="GenericSensor/SensorData"
H="OTA/OTARequest"
X="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 t=ADC(ANALOG_SENSOR_PIN)
else:
 t=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 C=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 C=""
b=mqtt_broker_address
s=ubinascii.hexlify(DEVICE_NAME)
K=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
O=0
W=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  x="\"deviceType\":\""+DEVICE_TYPE+"\""
  Q="\"deviceName\":\""+DEVICE_NAME+"\""
  e="\"deviceName\":\"*\"" 
  u=msg.decode()
  print('ESP received OTA message ',u)
  if x in u and(Q in u or e in u):
   k=json.loads(u)
   from ota import OTAUpdater
   q="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   U=k.get("otafiles")
   j=True
   u=DEVICE_NAME+" OTA: "+U
   try:
    F=OTAUpdater(q,U)
    if F.check_for_updates():
     if F.download_and_install_update():
      u+=" updated"
     else:
      u+=" update failed"
    else:
     u+=" up-to-date" 
     j=False
   except Exception as L:
    u+=" err:"+str(L)+" type:"+str(type(L))
   finally:
    print(u)
    D.publish(X,u)
    time.sleep(5)
    if j:
     machine.reset() 
def connect_and_subscribe():
 global s,b,K
 D=MQTTClient(s,b)
 D.set_callback(sub_cb)
 D.connect()
 D.subscribe(K)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(b,K))
 return D
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global t
 global C
 u="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(t!=""):
  u=u+",\"AnaR\":\""+str(t.read())+"\""
 if(C!=""):
  u=u+",\"DigR\":\""+str(C.value())+"\""
 if error!="":
  u=u+",\"err\":\""+error+"\""
 return u+"}"
try:
 D=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  D.check_msg()
  if(time.time()-O)>W:
   D.publish(E,create_sensor_message())
   O=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

