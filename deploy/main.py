from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
H="1.0"
X=5
x="GenericSensor/SensorData"
l="OTA/OTARequest"
U="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 u=ADC(ANALOG_SENSOR_PIN)
else:
 u=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 n=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 n=""
S=mqtt_broker_address
w=ubinascii.hexlify(DEVICE_NAME)
V=b'OTA/OTARequest'
y=b'GenericSensor/SensorData'
g=0
c=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  m="\"deviceType\":\""+DEVICE_TYPE+"\""
  v="\"deviceName\":\""+DEVICE_NAME+"\""
  W="\"deviceName\":\"*\"" 
  T=msg.decode()
  print('ESP received OTA message ',T)
  if m in T and(v in T or W in T):
   p=json.loads(T)
   from ota import OTAUpdater
   o="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   A=p.get("otafiles")
   i=True
   T=DEVICE_NAME+" OTA: "+A
   try:
    D=OTAUpdater(o,A)
    if D.check_for_updates():
     if D.download_and_install_update():
      T+=" updated"
     else:
      T+=" update failed"
    else:
     T+=" up-to-date" 
     i=False
   except Exception as d:
    T+=" err:"+str(d)+" type:"+str(type(d))
   finally:
    print(T)
    M.publish(U,T)
    time.sleep(5)
    if i:
     machine.reset() 
def connect_and_subscribe():
 global w,S,V
 M=MQTTClient(w,S)
 M.set_callback(sub_cb)
 M.connect()
 M.subscribe(V)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(S,V))
 return M
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global u
 global n
 T="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(u!=""):
  T=T+",\"AnaR\":\""+str(u.read())+"\""
 if(n!=""):
  T=T+",\"DigR\":\""+str(n.value())+"\""
 if error!="":
  T=T+",\"err\":\""+error+"\""
 return T+"}"
try:
 M=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  M.check_msg()
  if(time.time()-g)>c:
   M.publish(y,create_sensor_message())
   g=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

