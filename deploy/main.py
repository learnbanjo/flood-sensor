from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
H="1.0"
V=5
u="GenericSensor/SensorData"
x="OTA/OTARequest"
N="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 B=ADC(ANALOG_SENSOR_PIN)
else:
 B=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 m=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 m=""
G=mqtt_broker_address
q=ubinascii.hexlify(DEVICE_NAME)
l=b'OTA/OTARequest'
K=b'GenericSensor/SensorData'
d=0
X=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  v="\"deviceType\":\""+DEVICE_TYPE+"\""
  o="\"deviceName\":\""+DEVICE_NAME+"\""
  t="\"deviceName\":\"*\"" 
  Y=msg.decode()
  print('ESP received OTA message ',Y)
  if v in Y and(o in Y or t in Y):
   P=json.loads(Y)
   from ota import OTAUpdater
   M="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   R=P.get("otafiles")
   j=True
   Y=DEVICE_NAME+" OTA: "+R
   try:
    U=OTAUpdater(M,R)
    if U.check_for_updates():
     if U.download_and_install_update():
      Y+=" updated"
     else:
      Y+=" update failed"
    else:
     Y+=" up-to-date" 
     j=False
   except Exception as e:
    Y+=" err:"+str(e)+" type:"+str(type(e))
   finally:
    print(Y)
    Q.publish(N,Y)
    time.sleep(5)
    if j:
     machine.reset() 
def connect_and_subscribe():
 global q,G,l
 Q=MQTTClient(q,G)
 Q.set_callback(sub_cb)
 Q.connect()
 Q.subscribe(l)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(G,l))
 return Q
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global B
 global m
 Y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(B!=""):
  Y=Y+",\"AnaR\":\""+str(B.read())+"\""
 if(m!=""):
  Y=Y+",\"DigR\":\""+str(m.value())+"\""
 if error!="":
  Y=Y+",\"err\":\""+error+"\""
 return Y+"}"
try:
 Q=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  Q.check_msg()
  if(time.time()-d)>X:
   Q.publish(K,create_sensor_message())
   d=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

