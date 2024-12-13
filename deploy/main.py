from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
g="1.0"
E=5
V="GenericSensor/SensorData"
B="OTA/OTARequest"
N="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 o=ADC(ANALOG_SENSOR_PIN)
else:
 o=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 n=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 n=""
Q=mqtt_broker_address
I=ubinascii.hexlify(DEVICE_NAME)
p=b'OTA/OTARequest'
Y=b'GenericSensor/SensorData'
b=0
h=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  t="\"deviceType\":\""+DEVICE_TYPE+"\""
  k="\"deviceName\":\""+DEVICE_NAME+"\""
  y="\"deviceName\":\"*\"" 
  j=msg.decode()
  print('ESP received OTA message ',j)
  if t in j and(k in j or y in j):
   r=json.loads(j)
   from ota import OTAUpdater
   x="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   D=r.get("otafiles")
   C=True
   j=DEVICE_NAME+" OTA: "+D
   try:
    H=OTAUpdater(x,D)
    if H.check_for_updates():
     if H.download_and_install_update():
      j+=" updated"
     else:
      j+=" update failed"
    else:
     j+=" up-to-date" 
     C=False
   except Exception as e:
    j+=" err:"+str(e)+" type:"+str(type(e))
   finally:
    print(j)
    J.publish(N,j)
    time.sleep(5)
    if C:
     machine.reset() 
def connect_and_subscribe():
 global I,Q,p
 J=MQTTClient(I,Q)
 J.set_callback(sub_cb)
 J.connect()
 J.subscribe(p)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(Q,p))
 return J
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global o
 global n
 j="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(o!=""):
  j=j+",\"AnaR\":\""+str(o.read())+"\""
 if(n!=""):
  j=j+",\"DigR\":\""+str(n.value())+"\""
 if error!="":
  j=j+",\"err\":\""+error+"\""
 return j+"}"
try:
 J=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  J.check_msg()
  if(time.time()-b)>h:
   J.publish(Y,create_sensor_message())
   b=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

