from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
U="1.0"
X=5
h="GenericSensor/SensorData"
x="OTA/OTARequest"
i="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 q=ADC(ANALOG_SENSOR_PIN)
else:
 q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 S=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 S=""
R=mqtt_broker_address
C=ubinascii.hexlify(DEVICE_NAME)
P=b'OTA/OTARequest'
E=b'GenericSensor/SensorData'
g=0
W=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  a="\"deviceType\":\""+DEVICE_TYPE+"\""
  H="\"deviceName\":\""+DEVICE_NAME+"\""
  d="\"deviceName\":\"*\"" 
  l=msg.decode()
  print('ESP received OTA message ',l)
  if a in l and(H in l or d in l):
   k=json.loads(l)
   from ota import OTAUpdater
   F="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   y=k.get("otafiles")
   O=True
   l=DEVICE_NAME+" OTA: "+y
   try:
    N=OTAUpdater(F,y)
    if N.check_for_updates():
     if N.download_and_install_update():
      l+=" updated"
     else:
      l+=" update failed"
    else:
     l+=" up-to-date" 
     O=False
   except Exception as e:
    l+=" err:"+str(e)+" type:"+str(type(e))
   finally:
    print(l)
    B.publish(i,l)
    time.sleep(5)
    if O:
     machine.reset() 
def connect_and_subscribe():
 global C,R,P
 B=MQTTClient(C,R)
 B.set_callback(sub_cb)
 B.connect()
 B.subscribe(P)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(R,P))
 return B
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global q
 global S
 l="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(q!=""):
  l=l+",\"AnaR\":\""+str(q.read())+"\""
 if(S!=""):
  l=l+",\"DigR\":\""+str(S.value())+"\""
 if error!="":
  l=l+",\"err\":\""+error+"\""
 return l+"}"
try:
 B=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  B.check_msg()
  if(time.time()-g)>W:
   B.publish(E,create_sensor_message())
   g=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

