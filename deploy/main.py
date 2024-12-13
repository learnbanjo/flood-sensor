from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
K="1.0"
E=5
z="GenericSensor/SensorData"
S="OTA/OTARequest"
Y="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 B=ADC(ANALOG_SENSOR_PIN)
else:
 B=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 X=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 X=""
O=mqtt_broker_address
v=ubinascii.hexlify(DEVICE_NAME)
H=b'OTA/OTARequest'
j=b'GenericSensor/SensorData'
N=0
q=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  c="\"deviceType\":\""+DEVICE_TYPE+"\""
  x="\"deviceName\":\""+DEVICE_NAME+"\""
  g="\"deviceName\":\"*\"" 
  I=msg.decode()
  print('ESP received OTA message ',I)
  if c in I and(x in I or g in I):
   Q=json.loads(I)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   y=Q.get("otafiles")
   t=True
   I=DEVICE_NAME+" OTA: "+y
   try:
    d=OTAUpdater(e,y)
    if d.check_for_updates():
     if d.download_and_install_update():
      I+=" updated"
     else:
      I+=" update failed"
    else:
     I+=" up-to-date" 
     t=False
   except Exception as A:
    I+=" err:"+str(A)+" type:"+str(type(A))
   finally:
    print(I)
    w.publish(Y,I)
    time.sleep(5)
    if t:
     machine.reset() 
def connect_and_subscribe():
 global v,O,H
 w=MQTTClient(v,O)
 w.set_callback(sub_cb)
 w.connect()
 w.subscribe(H)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(O,H))
 return w
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global B
 global X
 I="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(B!=""):
  I=I+",\"AnaR\":\""+str(B.read())+"\""
 if(X!=""):
  I=I+",\"DigR\":\""+str(X.value())+"\""
 if error!="":
  I=I+",\"err\":\""+error+"\""
 return I+"}"
try:
 w=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  w.check_msg()
  if(time.time()-N)>q:
   w.publish(j,create_sensor_message())
   N=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

