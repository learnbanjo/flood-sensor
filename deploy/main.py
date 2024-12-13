from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
H="1.0"
c=5
O="GenericSensor/SensorData"
y="OTA/OTARequest"
Q="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 n=ADC(ANALOG_SENSOR_PIN)
else:
 n=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 M=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 M=""
N=mqtt_broker_address
I=ubinascii.hexlify(DEVICE_NAME)
V=b'OTA/OTARequest'
j=b'GenericSensor/SensorData'
A=0
U=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  p="\"deviceType\":\""+DEVICE_TYPE+"\""
  t="\"deviceName\":\""+DEVICE_NAME+"\""
  o="\"deviceName\":\"*\"" 
  a=msg.decode()
  print('ESP received OTA message ',a)
  if p in a and(t in a or o in a):
   l=json.loads(a)
   from ota import OTAUpdater
   g="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   G=l.get("otafiles")
   K=True
   a=DEVICE_NAME+" OTA: "+G
   try:
    b=OTAUpdater(g,G)
    if b.check_for_updates():
     if b.download_and_install_update():
      a+=" updated"
     else:
      a+=" update failed"
    else:
     a+=" up-to-date" 
     K=False
   except Exception as T:
    a+=" err:"+str(T)+" type:"+str(type(T))
   finally:
    print(a)
    S.publish(Q,a)
    time.sleep(5)
    if K:
     machine.reset() 
def connect_and_subscribe():
 global I,N,V
 S=MQTTClient(I,N)
 S.set_callback(sub_cb)
 S.connect()
 S.subscribe(V)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(N,V))
 return S
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global n
 global M
 a="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(n!=""):
  a=a+",\"AnaR\":\""+str(n.read())+"\""
 if(M!=""):
  a=a+",\"DigR\":\""+str(M.value())+"\""
 if error!="":
  a=a+",\"err\":\""+error+"\""
 return a+"}"
try:
 S=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  S.check_msg()
  if(time.time()-A)>U:
   S.publish(j,create_sensor_message())
   A=time.time()
 except OSError as e:
  restart_and_reconnect()

