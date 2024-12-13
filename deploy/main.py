from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
W="1.0"
b=5
x="GenericSensor/SensorData"
B="OTA/OTARequest"
k="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 n=ADC(ANALOG_SENSOR_PIN)
else:
 n=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 p=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 p=""
X=mqtt_broker_address
P=ubinascii.hexlify(DEVICE_NAME)
d=b'OTA/OTARequest'
a=b'GenericSensor/SensorData'
A=0
t=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  r="\"deviceType\":\""+DEVICE_TYPE+"\""
  K="\"deviceName\":\""+DEVICE_NAME+"\""
  H="\"deviceName\":\"*\"" 
  w=msg.decode()
  print('ESP received OTA message ',w)
  if r in w and(K in w or H in w):
   i=json.loads(w)
   from ota import OTAUpdater
   e="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   N=i.get("otafiles")
   I=True
   w=DEVICE_NAME+" OTA: "+N
   try:
    z=OTAUpdater(e,N)
    if z.check_for_updates():
     if z.download_and_install_update():
      w+=" updated"
     else:
      w+=" update failed"
    else:
     w+=" up-to-date" 
     I=False
   except Exception as j:
    w+=" err:"+str(j)+" type:"+str(type(j))
   finally:
    print(w)
    M.publish(k,w)
    time.sleep(5)
    if I:
     machine.reset() 
def connect_and_subscribe():
 global P,X,d
 M=MQTTClient(P,X)
 M.set_callback(sub_cb)
 M.connect()
 M.subscribe(d)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(X,d))
 return M
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global n
 global p
 w="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(n!=""):
  w=w+",\"AnaR\":\""+str(n.read())+"\""
 if(p!=""):
  w=w+",\"DigR\":\""+str(p.value())+"\""
 if error!="":
  w=w+",\"err\":\""+error+"\""
 return w+"}"
try:
 M=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  M.check_msg()
  if(time.time()-A)>t:
   M.publish(a,create_sensor_message())
   A=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

