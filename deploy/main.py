from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
s="1.0"
B=5
l="GenericSensor/SensorData"
U="OTA/OTARequest"
T="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 F=ADC(ANALOG_SENSOR_PIN)
else:
 F=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 E=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 E=""
O=mqtt_broker_address
o=ubinascii.hexlify(DEVICE_NAME)
S=b'OTA/OTARequest'
x=b'GenericSensor/SensorData'
g=0
D=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  e="\"deviceType\":\""+DEVICE_TYPE+"\""
  K="\"deviceName\":\""+DEVICE_NAME+"\""
  G="\"deviceName\":\"*\"" 
  L=msg.decode()
  print('ESP received OTA message ',L)
  if e in L and(K in L or G in L):
   v=json.loads(L)
   from ota import OTAUpdater
   H="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   i=v.get("otafiles")
   f=True
   L=DEVICE_NAME+" OTA: "+i
   try:
    j=OTAUpdater(H,i)
    if j.check_for_updates():
     if j.download_and_install_update():
      L+=" updated"
     else:
      L+=" update failed"
    else:
     L+=" up-to-date" 
     f=False
   except Exception as C:
    L+=" err:"+str(C)+" type:"+str(type(C))
   finally:
    print(L)
    Q.publish(T,L)
    time.sleep(5)
    if f:
     machine.reset() 
def connect_and_subscribe():
 global o,O,S
 Q=MQTTClient(o,O)
 Q.set_callback(sub_cb)
 Q.connect()
 Q.subscribe(S)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(O,S))
 return Q
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global F
 global E
 L="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(F!=""):
  L=L+",\"AnaR\":\""+str(F.read())+"\""
 if(E!=""):
  L=L+",\"DigR\":\""+str(E.value())+"\""
 if error!="":
  L=L+",\"err\":\""+error+"\""
 return L+"}"
try:
 Q=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  Q.check_msg()
  if(time.time()-g)>D:
   Q.publish(x,create_sensor_message())
   g=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

