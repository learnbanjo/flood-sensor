from DEVICE_CONFIG import DEVICE_NAME,DEVICE_TYPE,SSID
from DEVICE_CONFIG import ANALOG_SENSOR_PIN,DIGITAL_SENSOR_PIN
from DEVICE_CONFIG import mqtt_broker_address,mqtt_broker_port,mqtt_keep_alive_time,MQTT_PUBLISH_INTERVAL
import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
X="1.0"
L=5
u="GenericSensor/SensorData"
x="OTA/OTARequest"
N="OTA/OTAResponse"
if ANALOG_SENSOR_PIN!="":
 from machine import ADC
 V=ADC(ANALOG_SENSOR_PIN)
else:
 V=""
if DIGITAL_SENSOR_PIN!="":
 from machine import Pin
 y=Pin(DIGITAL_SENSOR_PIN,Pin.IN,Pin.PULL_UP)
else:
 y=""
c=mqtt_broker_address
z=ubinascii.hexlify(DEVICE_NAME)
D=b'OTA/OTARequest'
W=b'GenericSensor/SensorData'
r=0
d=MQTT_PUBLISH_INTERVAL
def sub_cb(topic,msg):
 print((topic,msg))
 if topic==b'OTA/OTARequest':
  print('ESP received OTA message')
  k="\"deviceType\":\""+DEVICE_TYPE+"\""
  B="\"deviceName\":\""+DEVICE_NAME+"\""
  Q="\"deviceName\":\"*\"" 
  O=msg.decode()
  print('ESP received OTA message ',O)
  if k in O and(B in O or Q in O):
   e=json.loads(O)
   from ota import OTAUpdater
   H="https://raw.githubusercontent.com/learnbanjo/flood-sensor/refs/heads/deploy-test/deploy/"
   J=e.get("otafiles")
   M=True
   O=DEVICE_NAME+" OTA: "+J
   try:
    b=OTAUpdater(H,J)
    if b.check_for_updates():
     if b.download_and_install_update():
      O+=" updated"
     else:
      O+=" update failed"
    else:
     O+=" up-to-date" 
     M=False
   except Exception as w:
    O+=" err:"+str(w)+" type:"+str(type(w))
   finally:
    print(O)
    n.publish(N,O)
    time.sleep(5)
    if M:
     machine.reset() 
def connect_and_subscribe():
 global z,c,D
 n=MQTTClient(z,c)
 n.set_callback(sub_cb)
 n.connect()
 n.subscribe(D)
 print('Connected to %s MQTT broker, subscribed to %s topic'%(c,D))
 return n
def restart_and_reconnect():
 print('Failed to connect to MQTT broker. Reconnecting...')
 time.sleep(10)
 machine.reset()
def create_sensor_message(error=""):
 global V
 global y
 O="{\"devNm\":\""+DEVICE_NAME+"\",\"devTy\":\""+DEVICE_TYPE+"\",\"AP\":\""+SSID+"\""
 if(V!=""):
  O=O+",\"AnaR\":\""+str(V.read())+"\""
 if(y!=""):
  O=O+",\"DigR\":\""+str(y.value())+"\""
 if error!="":
  O=O+",\"err\":\""+error+"\""
 return O+"}"
try:
 n=connect_and_subscribe()
except OSError as e:
 restart_and_reconnect()
while True:
 try:
  n.check_msg()
  if(time.time()-r)>d:
   n.publish(W,create_sensor_message())
   r=time.time()
 except OSError as e:
  restart_and_reconnect()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

