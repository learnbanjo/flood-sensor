from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
i="1.0"
n=5
c="GenericSensor/SensorData"
P="OTA/OTARequest"
D="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 M=ADC(ANALOG_SENSOR_PIN)
else:
 M=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 k=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 k=""
R=mqtt_broker_address
O=ubinascii.hexlify(DEVICE_NAME)
U=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
Y=0
K=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  V="\"deviceType\":\""+DEVICE_TYPE+"\""
  x="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  S=msg.decode()
  print('ESP received OTA message ',S)
  if V in S and(x in S or Q in S):
   v=json.loads(S)
   from ota import OTAUpdater
   p="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   f=v.get("otafiles")
   l=True
   S=DEVICE_NAME+" OTA: "+f
   try:
    r=OTAUpdater(p,f)
    if r.check_for_updates():
     if r.download_and_install_update():
      S+=" updated"
     else:
      S+=" update failed"
    else:
     S+=" up-to-date" 
     l=False
   except Exception as A:
    S+=" err:"+str(A)+" type:"+str(type(A))
   finally:
    print(S)
    C.publish(D,S)
    time.sleep(5)
    if l:
     machine.reset() 
def connect_and_subscribe():
 global O,R,U
 C=MQTTClient(O,R)
 C.set_callback(sub_cb)
 C.connect()
 C.subscribe(U)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(R,U))
 return C
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global M
 global k
 S="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(M!=""):
  S=S+",\"AnaR\":\""+str(M.read())+"\""
 if(k!=""):
  S=S+",\"DigR\":\""+str(k.value())+"\""
 if error!="":
  S=S+",\"err\":\""+error+"\""
 return S+"}"
try:
 C=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  C.check_msg()
  if(time.time()-Y)>K:
   C.publish(E,create_sensor_message())
   Y=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

