from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
A="1.0"
s=5
R="GenericSensor/SensorData"
E="OTA/OTARequest"
r="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 J=ADC(ANALOG_SENSOR_PIN)
else:
 J=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 l=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 l=""
h=mqtt_broker_address
w=ubinascii.hexlify(DEVICE_NAME)
e=b'OTA/OTARequest'
u=b'GenericSensor/SensorData'
G=0
K=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  f="\"deviceType\":\""+DEVICE_TYPE+"\""
  L="\"deviceName\":\""+DEVICE_NAME+"\""
  z="\"deviceName\":\"*\"" 
  Y=msg.decode()
  print('ESP received OTA message ',Y)
  if f in Y and(L in Y or z in Y):
   W=json.loads(Y)
   from ota import OTAUpdater
   x="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   Q=W.get("otafiles")
   M=True
   Y=DEVICE_NAME+" OTA: "+Q
   try:
    m=OTAUpdater(x,Q)
    if m.check_for_updates():
     if m.download_and_install_update():
      Y+=" updated"
     else:
      Y+=" update failed"
    else:
     Y+=" up-to-date" 
     M=False
   except Exception as c:
    Y+=" err:"+str(c)+" type:"+str(type(c))
   finally:
    print(Y)
    i.publish(r,Y)
    time.sleep(5)
    if M:
     machine.reset() 
def connect_and_subscribe():
 global w,h,e
 i=MQTTClient(w,h)
 i.set_callback(sub_cb)
 i.connect()
 i.subscribe(e)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(h,e))
 return i
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global J
 global l
 Y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(J!=""):
  Y=Y+",\"AnaR\":\""+str(J.read())+"\""
 if(l!=""):
  Y=Y+",\"DigR\":\""+str(l.value())+"\""
 if error!="":
  Y=Y+",\"err\":\""+error+"\""
 return Y+"}"
try:
 i=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  i.check_msg()
  if(time.time()-G)>K:
   i.publish(u,create_sensor_message())
   G=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

