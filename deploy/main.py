from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
u="1.0"
e=5
i="GenericSensor/SensorData"
z="OTA/OTARequest"
o="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 x=ADC(ANALOG_SENSOR_PIN)
else:
 x=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 A=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 A=""
L=mqtt_broker_address
B=ubinascii.hexlify(DEVICE_NAME)
t=b'OTA/OTARequest'
Q=b'GenericSensor/SensorData'
H=0
E=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  k="\"deviceType\":\""+DEVICE_TYPE+"\""
  v="\"deviceName\":\""+DEVICE_NAME+"\""
  n="\"deviceName\":\"*\"" 
  g=msg.decode()
  print('ESP received OTA message ',g)
  if k in g and(v in g or n in g):
   a=json.loads(g)
   from ota import OTAUpdater
   q="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   y=a.get("otafiles")
   M=True
   g=DEVICE_NAME+" OTA: "+y
   try:
    F=OTAUpdater(q,y)
    if F.check_for_updates():
     if F.download_and_install_update():
      g+=" updated"
     else:
      g+=" update failed"
    else:
     g+=" up-to-date" 
     M=False
   except Exception as R:
    g+=" err:"+str(R)+" type:"+str(type(R))
   finally:
    print(g)
    G.publish(o,g)
    time.sleep(5)
    if M:
     machine.reset() 
def connect_and_subscribe():
 global B,L,t
 G=MQTTClient(B,L)
 G.set_callback(sub_cb)
 G.connect()
 G.subscribe(t)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(L,t))
 return G
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global x
 global A
 g="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(x!=""):
  g=g+",\"AnaR\":\""+str(x.read())+"\""
 if(A!=""):
  g=g+",\"DigR\":\""+str(A.value())+"\""
 if error!="":
  g=g+",\"err\":\""+error+"\""
 return g+"}"
try:
 G=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  G.check_msg()
  if(time.time()-H)>E:
   G.publish(Q,create_sensor_message())
   H=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

