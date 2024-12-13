from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
Q="1.0"
m=5
o="GenericSensor/SensorData"
c="OTA/OTARequest"
C="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 q=ADC(ANALOG_SENSOR_PIN)
else:
 q=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 r=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 r=""
i=mqtt_broker_address
O=ubinascii.hexlify(DEVICE_NAME)
d=b'OTA/OTARequest'
t=b'GenericSensor/SensorData'
K=0
x=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  I="\"deviceType\":\""+DEVICE_TYPE+"\""
  F="\"deviceName\":\""+DEVICE_NAME+"\""
  L="\"deviceName\":\"*\"" 
  y=msg.decode()
  print('ESP received OTA message ',y)
  if I in y and(F in y or L in y):
   z=json.loads(y)
   from ota import OTAUpdater
   B="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   w=z.get("otafiles")
   G=True
   y=DEVICE_NAME+" OTA: "+w
   try:
    s=OTAUpdater(B,w)
    if s.check_for_updates():
     if s.download_and_install_update():
      y+=" updated"
     else:
      y+=" update failed"
    else:
     y+=" up-to-date" 
     G=False
   except Exception as J:
    y+=" err:"+str(J)+" type:"+str(type(J))
   finally:
    print(y)
    R.publish(C,y)
    time.sleep(5)
    if G:
     machine.reset() 
def connect_and_subscribe():
 global O,i,d
 R=MQTTClient(O,i)
 R.set_callback(sub_cb)
 R.connect()
 R.subscribe(d)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(i,d))
 return R
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global q
 global r
 y="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(q!=""):
  y=y+",\"AnaR\":\""+str(q.read())+"\""
 if(r!=""):
  y=y+",\"DigR\":\""+str(r.value())+"\""
 if error!="":
  y=y+",\"err\":\""+error+"\""
 return y+"}"
try:
 R=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  R.check_msg()
  if(time.time()-K)>x:
   R.publish(t,create_sensor_message())
   K=time.time()
 except OSError as e:
  restart_and_reconnect()

