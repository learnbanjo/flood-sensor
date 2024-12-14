from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
z="1.0"
D=5
X="GenericSensor/SensorData"
L="OTA/OTARequest"
P="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 e=ADC(ANALOG_SENSOR_PIN)
else:
 e=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 C=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 C=""
H=mqtt_broker_address
h=ubinascii.hexlify(DEVICE_NAME)
V=b'OTA/OTARequest'
o=b'GenericSensor/SensorData'
M=0
j=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  S="\"deviceType\":\""+DEVICE_TYPE+"\""
  d="\"deviceName\":\""+DEVICE_NAME+"\""
  g="\"deviceName\":\"*\"" 
  W=msg.decode()
  print('ESP received OTA message ',W)
  if S in W and(d in W or g in W):
   r=json.loads(W)
   from ota import OTAUpdater
   u="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   K=r.get("otafiles")
   I=True
   W=DEVICE_NAME+" OTA: "+K
   try:
    c=OTAUpdater(u,K)
    if c.check_for_updates():
     if c.download_and_install_update():
      W+=" updated"
     else:
      W+=" update failed"
    else:
     W+=" up-to-date" 
     I=False
   except Exception as R:
    W+=" err:"+str(R)+" type:"+str(type(R))
   finally:
    print(W)
    b.publish(P,W)
    time.sleep(5)
    if I:
     machine.reset() 
def connect_and_subscribe():
 global h,H,V
 b=MQTTClient(h,H)
 b.set_callback(sub_cb)
 b.connect()
 b.subscribe(V)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(H,V))
 return b
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global e
 global C
 W="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(e!=""):
  W=W+",\"AnaR\":\""+str(e.read())+"\""
 if(C!=""):
  W=W+",\"DigR\":\""+str(C.value())+"\""
 if error!="":
  W=W+",\"err\":\""+error+"\""
 return W+"}"
try:
 b=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  b.check_msg()
  if(time.time()-M)>j:
   b.publish(o,create_sensor_message())
   M=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

