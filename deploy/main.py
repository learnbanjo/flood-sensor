from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
l="1.0"
S=5
C="GenericSensor/SensorData"
O="OTA/OTARequest"
w="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 E=ADC(ANALOG_SENSOR_PIN)
else:
 E=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 I=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 I=""
X=mqtt_broker_address
f=ubinascii.hexlify(DEVICE_NAME)
U=b'OTA/OTARequest'
P=b'GenericSensor/SensorData'
B=0
s=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  Y="\"deviceType\":\""+DEVICE_TYPE+"\""
  k="\"deviceName\":\""+DEVICE_NAME+"\""
  y="\"deviceName\":\"*\"" 
  J=msg.decode()
  print('ESP received OTA message ',J)
  if Y in J and(k in J or y in J):
   h=json.loads(J)
   from ota import OTAUpdater
   r="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   M=h.get("otafiles")
   q=True
   J=DEVICE_NAME+" OTA: "+M
   try:
    G=OTAUpdater(r,M)
    if G.check_for_updates():
     if G.download_and_install_update():
      J+=" updated"
     else:
      J+=" update failed"
    else:
     J+=" up-to-date" 
     q=False
   except Exception as c:
    J+=" err:"+str(c)+" type:"+str(type(c))
   finally:
    print(J)
    p.publish(w,J)
    time.sleep(5)
    if q:
     machine.reset() 
def connect_and_subscribe():
 global f,X,U
 p=MQTTClient(f,X)
 p.set_callback(sub_cb)
 p.connect()
 p.subscribe(U)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(X,U))
 return p
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global E
 global I
 J="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(E!=""):
  J=J+",\"AnaR\":\""+str(E.read())+"\""
 if(I!=""):
  J=J+",\"DigR\":\""+str(I.value())+"\""
 if error!="":
  J=J+",\"err\":\""+error+"\""
 return J+"}"
try:
 p=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  p.check_msg()
  if(time.time()-B)>s:
   p.publish(P,create_sensor_message())
   B=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

