from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
M="1.0"
q=5
E="GenericSensor/SensorData"
U="OTA/OTARequest"
G="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 C=ADC(ANALOG_SENSOR_PIN)
else:
 C=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 b=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 b=""
B=mqtt_broker_address
e=ubinascii.hexlify(DEVICE_NAME)
W=b'OTA/OTARequest'
c=b'GenericSensor/SensorData'
H=0
S=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  w="\"deviceType\":\""+DEVICE_TYPE+"\""
  J="\"deviceName\":\""+DEVICE_NAME+"\""
  r="\"deviceName\":\"*\"" 
  y=msg.decode()
  print('ESP received OTA message ',y)
  if w in y and(J in y or r in y):
   p=json.loads(y)
   from ota import OTAUpdater
   L="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   u=p.get("otafiles")
   Y=True
   y=DEVICE_NAME+" OTA: "+u
   try:
    R=OTAUpdater(L,u)
    if R.check_for_updates():
     if R.download_and_install_update():
      y+=" updated"
     else:
      y+=" update failed"
    else:
     y+=" up-to-date" 
     Y=False
   except Exception as o:
    y+=" err:"+str(o)+" type:"+str(type(o))
   finally:
    print(y)
    D.publish(G,y)
    time.sleep(5)
    if Y:
     machine.reset() 
def connect_and_subscribe():
 global e,B,W
 D=MQTTClient(e,B)
 D.set_callback(sub_cb)
 D.connect()
 D.subscribe(W)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(B,W))
 return D
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global C
 global b
 y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(C!=""):
  y=y+",\"AnaR\":\""+str(C.read())+"\""
 if(b!=""):
  y=y+",\"DigR\":\""+str(b.value())+"\""
 if error!="":
  y=y+",\"err\":\""+error+"\""
 return y+"}"
try:
 D=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  D.check_msg()
  if(time.time()-H)>S:
   D.publish(c,create_sensor_message())
   H=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

